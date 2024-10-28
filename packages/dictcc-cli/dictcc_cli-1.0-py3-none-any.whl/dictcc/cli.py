from enum import Enum
from typing import Annotated, List, Optional

import typer
from click import ClickException
from rich.console import Console

from dictcc.scraper import DictCCError, DictCCScraper

app = typer.Typer(add_completion=False)

DEFAULT_LANGUAGE1 = "de"
DEFAULT_LANGUAGE2 = "en"


class ColorMode(str, Enum):
    ALWAYS = "always"
    AUTO = "auto"
    NEVER = "never"


@app.command(
    name="lookup-term",
    help="Look up a term on dict.cc.",
    no_args_is_help=True,
)
def lookup_term(
    *,
    terms: Annotated[List[str], typer.Argument(help="the words or phrase to search for in the dictionary")],
    languages: Annotated[
        Optional[List[str]],
        typer.Option(
            "--languages",
            "-l",
            metavar="LANGUAGE_CODE",
            help="ISO 639-1 codes of the languages to translate between (up to 2).\n\n"
            f"If no languages are specified, defaults to '{DEFAULT_LANGUAGE1}' and '{DEFAULT_LANGUAGE2}'.\n\n"
            f"If only one language is provided, the other will default to '{DEFAULT_LANGUAGE1}'.",
        ),
    ] = None,
    color: Annotated[
        ColorMode,
        typer.Option(
            help=(
                "controls when to use colored output: 'always' to force color, 'never' to disable, "
                "or 'auto' to use color only when output is connected to a terminal"
            ),
            show_choices=True,
        ),
    ] = ColorMode.AUTO,
) -> None:
    term = " ".join(terms)

    # Determine languages
    if languages:
        if len(languages) > 2:
            raise ClickException("More than two languages given.")
        elif len(languages) == 2:
            language1, language2 = languages
        else:
            language1 = DEFAULT_LANGUAGE1
            language2 = languages[0]
    else:
        language1 = DEFAULT_LANGUAGE1
        language2 = DEFAULT_LANGUAGE2

    dictcc = DictCCScraper(language1, language2)
    try:
        result = dictcc.lookup(term)

        console = Console(
            force_terminal=(None if color == ColorMode.AUTO else (color == ColorMode.ALWAYS)),
        )
        console.print(result.build_table())
    except DictCCError as e:
        raise ClickException(str(e)) from e
