from dataclasses import dataclass
from jinja2 import (
    Environment,
    FileSystemLoader,
    PackageLoader,
    Template,
    select_autoescape,
)
from typing import Mapping, Any, Optional
from minichain import Prompt, Output, Input, Request

@dataclass
class Template(Prompt[Mapping[str, Any], Output]):
    """
    A prompt that uses Jinja to define a prompt based on a static template.
    Set `template_file` to the Jinja template file.
    """
    template_file: Optional[str] = None
    template: Optional[str] = None
    stop_template: Optional[str] = None
        
    def parse(self, result: str, inp: Mapping[str, Any]) -> Output:
        return str(result)  # type: ignore

    def prompt(self, inp: Input) -> Request:
        kwargs = self.to_dict(inp)
        if self.template_file:
            tmp = Environment(loader=FileSystemLoader(".")).get_template(
                name=self.template_file
            )
        elif self.template:
            tmp = self.template  # type: ignore
        else:
            tmp = Template(self.prompt_template)
        if isinstance(kwargs, dict):
            x = tmp.render(**kwargs)
        else:
            x = tmp.render(**asdict(kwargs))

        if self.stop_template:
            stop = [Template(self.stop_template).render(**kwargs)]
        else:
            stop = None
        return Request(x, stop)
