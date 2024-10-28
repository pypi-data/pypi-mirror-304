# hooks.py
from hatchling.plugin import hookimpl

from hatch_paulrein_template.__about__ import __version__

from .plugin import PaulReinTemplate


@hookimpl
def hatch_register_template() -> type[PaulReinTemplate]:
    print(f"Running version {__version__} of PaulReinTemplate!")
    return PaulReinTemplate
