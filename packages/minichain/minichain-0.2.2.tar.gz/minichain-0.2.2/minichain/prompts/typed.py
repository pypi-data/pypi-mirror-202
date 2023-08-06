from typing import Any, Dict, List, Mapping, Type, get_args, get_origin
from dataclasses import asdict, fields, is_dataclass
from enum import Enum
from dataclasses import dataclass
import json
from jinja2 import (
    Environment,
    FileSystemLoader,
    PackageLoader,
    Template,
    select_autoescape,
)
from .template import Template
from minichain import Prompt, Output, Input, Request

env = Environment(
    loader=PackageLoader("minichain"),
    autoescape=select_autoescape(),
    extensions=["jinja2_highlight.HighlightExtension"],
)


def enum(x: Type[Enum]) -> Dict[str, int]:
    d = {e.name: e.value for e in x}
    return d


def walk(x: Any) -> Any:
    if issubclass(x if get_origin(x) is None else get_origin(x), List):
        return {"_t_": "list", "t": walk(get_args(x)[0])}
    if issubclass(x, Enum):
        return enum(x)

    if is_dataclass(x):
        return {y.name: walk(y.type) for y in fields(x)}
    return x.__name__

@dataclass
class TypedTemplate(Template[Output]):
    """
    Prompt that is automatically generated to produce a
    list of objects of of the dataclass `Out`.
    """

    def prompt(self, inp) -> Request:
        inp = dict(inp)
        tmp = env.get_template("type_prompt.pmpt.tpl")
        d = walk(self.Out)
        inp["typ"] = tmp.render({"typ": d})

        return super().prompt(inp)

    def parse(self, out: str, inp) -> Output:
        return [self.Out(**j) for j in json.loads(out)]  # type: ignore
