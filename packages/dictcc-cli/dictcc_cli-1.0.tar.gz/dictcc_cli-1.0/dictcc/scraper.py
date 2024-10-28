import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Iterable, Iterator
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag
from fake_useragent import UserAgent
from rich.table import Table
from rich.text import Text

from dictcc.utils import listify


@dataclass
class SearchResult:
    language1: str
    language2: str
    result_count: int
    results: list[tuple[Text, Text]]

    def build_table(self) -> Table:
        table = Table(expand=False)

        table.add_column(self.language1)
        table.add_column(self.language2)

        for entry in self.results:
            table.add_row(entry[0], entry[1])

        return table


class DictCCError(Exception):
    pass


@dataclass
class TextDecoration:
    style: str | None = None
    prefix: str = ""
    suffix: str = ""

    def decorate(self, text: Text) -> Text:
        text = Text.assemble(self.prefix, text, self.suffix)
        if self.style is not None:
            text.stylize(self.style)
        return text


@dataclass
class DictCCScrapeResult:
    soup: BeautifulSoup

    TEXT_DECORATIONS_BY_TAG: ClassVar[dict[str, TextDecoration]] = {
        "b": TextDecoration(style="bold"),
        "kbd": TextDecoration(style="blue"),
        "var": TextDecoration(style="green"),
        "sup": TextDecoration(style="italic yellow", prefix=" (", suffix=")"),
        "dfn": TextDecoration(style="magenta", prefix="[", suffix="]"),
        "span": TextDecoration(style="yellow", prefix="[", suffix="]"),
        "abbr": TextDecoration(style="orange"),
        "td": TextDecoration(),
        "a": TextDecoration(),
        "div": TextDecoration(),
    }
    IMG_TEXTS: ClassVar[dict[str, Text]] = {"warndreieck_30.png": Text("[WARNING]", style="red")}

    @listify(2)
    def parse_language_names(self) -> Iterator[str]:
        for lang_node in self.soup.select("td.td2[dir=ltr] b"):
            lang_text = lang_node.text.strip()
            if lang_text:
                yield lang_text

    def parse_element(self, element: PageElement) -> Text:
        if isinstance(element, NavigableString):
            element_str = str(element)
            return Text("[UNVERIFIED!]", "red") if element_str == "Unverified" else Text(element_str)

        elif isinstance(element, Tag):
            if element.name == "div" and element.string is not None and re.match("^[0-9]+$", element.string):
                return Text()

            if element.name == "img":
                img_name = Path(urlparse(element.get("src")).path).name
                if img_name in self.IMG_TEXTS:
                    return self.IMG_TEXTS[img_name]

            if element.name in self.TEXT_DECORATIONS_BY_TAG:
                return self.TEXT_DECORATIONS_BY_TAG[element.name].decorate(self.parse_elements(element.contents))

        raise DictCCError(f"Cannot parse {element}")

    def parse_elements(self, elements: Iterable[PageElement]) -> Text:
        return Text.assemble(*(self.parse_element(part) for part in elements))

    @listify(2)
    def parse_entry(self, entry: Tag) -> Text:
        for element in entry.find_all("td", {"class": re.compile(r"nl$")}):
            yield self.parse_elements(element)

    @listify()
    def parse_entries(self) -> Iterator[tuple[Text, Text]]:
        for entry in self.soup.find_all("tr", {"id": re.compile(r"^tr")}):
            yield self.parse_entry(entry)

    def parse_result_count(self) -> int:
        tags = self.soup.select("h1.searchh1 > b")

        if len(tags) < 3:
            return 0
        else:
            return int(tags[-1].contents[0].get_text())

    def parse_search_result(self) -> SearchResult:
        result_count = self.parse_result_count()

        if result_count == 0:
            raise DictCCError("No results found")

        language_name1, language_name2 = self.parse_language_names()

        return SearchResult(
            language_name1,
            language_name2,
            result_count,
            self.parse_entries(),
        )


@dataclass
class DictCCScraper:
    language1: str = "en"
    language2: str = "de"

    def get_url(self, term: str) -> str:
        return f"https://{self.language1}{self.language2}.dict.cc/?s={term}"

    def scrape(self, term: str) -> DictCCScrapeResult:
        response = requests.get(
            self.get_url(term),
            headers={"User-Agent": UserAgent().firefox},
            cookies={"use_desktop_version": "1"},
            timeout=30,
        )
        if not response.ok:
            raise DictCCError("Language combination is not supported.")

        soup = BeautifulSoup(response.text, "html.parser")
        return DictCCScrapeResult(soup)

    def lookup(self, term: str) -> SearchResult:
        return self.scrape(term).parse_search_result()
