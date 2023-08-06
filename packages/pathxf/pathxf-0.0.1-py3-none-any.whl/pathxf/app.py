from __future__ import annotations

import copy
import itertools as it
import json
import os
from pathlib import Path
from typing import Optional

import more_itertools as itx
import typer
import yaml
from appdirs import user_cache_dir
from typer import Option, Typer

from pathxf.bids import bids
from pathxf.spec import CompSpec, Spec
from pathxf.utils import dict_merge, hash_container, listfiles, oswalk

app = Typer()

cache = Path(".cache")
if cache.exists():
    with cache.open() as f:
        maps = json.load(f)


def _merge_conditionals(compspec: CompSpec | list[CompSpec]) -> list[CompSpec]:
    if isinstance(compspec, list):
        return _merge_conditionals(CompSpec(conditions=compspec))
    if not "conditions" in compspec:
        return [compspec]
    mergables = copy.copy(compspec)
    conditions = mergables.pop("conditions")
    return [
        CompSpec(**dict_merge(mergables, s))
        for spec in conditions
        for s in _merge_conditionals(spec)
    ] + [mergables]


class IndexCache(dict[Spec, dict[str, str]]):
    dir: Path = Path(user_cache_dir("file_renamer", "pvandyken"))

    def __init__(self):
        if not self.dir.exists():
            self.dir.mkdir(parents=True)
        if not self.dir.joinpath("index").exists():
            self.dir.joinpath("index").mkdir()

    def contains(self, hash: str):
        if self.dir.joinpath(hash).exists():
            return True
        return False

    def index(self, hash: str):
        return self.dir / "index" / hash

    def purge(self):
        for file in self.dir.joinpath("index").iterdir():
            os.remove(file)

    def __getitem__(self, spec: Spec):
        name = hash_container(spec)
        if self.contains(name):
            with open(self.index(name), "r") as f:
                return json.load(f)["maps"]
        raise KeyError(name)

    def __setitem__(self, __key: Spec, __value: dict[str, str]) -> None:
        name = hash_container(__key)
        with open(self.index(name), "w") as f:
            json.dump({"version": "0.0.0", "maps": __value}, f)

    def __contains__(self, __key: object) -> bool:
        if not isinstance(__key, dict):
            return False
        name = hash_container(__key)
        return self.contains(name)


def index(config: Spec):
    maps: dict[str, str] = {}
    for group in config["maps"]:
        if not "comps" in group:
            for inp, wcards in listfiles(Path(config["input"], group["root"])):
                wcards = dict(wcards.items())
                try:
                    maps[group["out"].format(**wcards)] = inp
                except KeyError:
                    raise Exception(
                        f"Not all wildcards found in input '{inp}'\n"
                        f"Found: {wcards}\n"
                    )
            continue
        for root, (path, _entityspecs) in it.product(
            itx.always_iterable(group["root"]), list(group["comps"].items())
        ):
            entityspecs = _merge_conditionals(_entityspecs)
            for inp, wcards in listfiles(Path(config["input"], root + path)):
                wcards = dict(wcards.items())
                spec = None
                for _spec in entityspecs:
                    good = True
                    if not "when" in _spec:
                        spec = _spec
                        break
                    for ent, values in _spec["when"].items():
                        if wcards[ent] not in itx.always_iterable(values):
                            good = False
                            break
                    if good:
                        spec = _spec
                        break
                if spec is None:
                    raise Exception(f"No valid entityspec found for {inp}")
                for ent, _m in spec.get("map", {}).items():
                    wcards[ent] = _m.get(wcards[ent], wcards[ent])

                outroot = os.path.join(config.get("output", ""), group.get("out", ""))
                assert "bids" in spec
                outtemplate = bids(
                    root=outroot,
                    **{
                        **group.get("all", {}),
                        **spec["bids"],
                    },
                )
                try:
                    maps[inp] = outtemplate.format(**wcards)
                except KeyError:
                    raise Exception(
                        f"Not all wildcards found in input '{inp}'\n"
                        f"Found: {wcards}\n"
                        f"Expected: {spec['bids']}"
                    )
    return maps


def main(
    config: Path,
    input: Optional[Path] = Option(None, "-i", help="Override the input field in the config"),
    output: Optional[Path] = Option(None, "-o", help="Override the ouptut field in the config"),
    do_index: bool = Option(False, "--index", help="Force reindexing of the filesystem"),
    purge: bool = Option(False, help="Remove all cached indexes"),
    _print: bool = Option(False, "--print", "-p", help="Print the file mapping as json, without doing any renaming"),
    inverse: bool = Option(False, "-v", help="Print list of files in the input directory not indexed, formatted as json"),
):
    cache = IndexCache()
    if purge:
        cache.purge()
        return
    with config.open() as f:
        config_obj: Spec = yaml.safe_load(f)
    if input is not None:
        config_obj["input"] = str(input)
    if output is not None:
        config_obj["output"] = str(output)
    if do_index or config_obj not in cache:
        maps = index(config_obj)
        cache[config_obj] = maps
    else:
        maps = cache[config_obj]
    if _print:
        print(json.dumps(maps))
        return
    if inverse:
        unused: list[str] = []
        for f in oswalk(config_obj["input"]):
            if Path(f).is_dir():
                continue
            if f in maps:
                continue
            unused.append(f)
        print(json.dumps(unused))
        return

    for src, dest in maps.items():
        if Path(src).exists() and not Path(dest).exists():
            Path(dest).parent.mkdir(parents=True, exist_ok=True)
            os.symlink(
                os.path.relpath(Path(src).resolve(), Path(dest).resolve().parent), dest
            )


def run():
    typer.run(main)
