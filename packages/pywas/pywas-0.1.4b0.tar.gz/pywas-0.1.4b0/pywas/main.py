import os
from rich import print
import typer
from .wrapper.ngspice import ng_spice
from .wrapper.base_wrapper import write_conf
from .wrapper.template import template

help = """
*Py*thon *W*rapper for *A*nalog design *S*oftware

**Installation using [pipx](https://pypa.github.io/pipx/installation/)**:

```console
$ pipx install pywas
```
"""
cli = typer.Typer(help=help)
cli.add_typer(ng_spice, name="ngspice", help="ngspice utility")
cli.add_typer(template, name="template", help="templating part")


@cli.command("create")
def new_project(name: str, flow: str = typer.Argument("OpenLane")):
    """
    Create a new project with specified options.
    """
    os.mkdir(name)
    write_conf({"flow": flow}, os.path.join(name, "config.yaml"))
    print("New project created !")


if __name__ == "__main__":
    cli()
