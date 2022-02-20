import os.path
import re
import sys
from typing import Iterator, List


class Extractor:
    def get_lines_in_file(self, file: str) -> Iterator[str]:
        self._assert_is_file(file)
        with open(file, "r") as f:
            for line in f.read().splitlines():
                if len(line) != 0:
                    yield (line)

    def _assert_is_file(self, file: str):
        if not os.path.isfile(file):
            raise FileNotFoundError(file)


class Transformer:
    _REGEX_INIT_TOC_SECTION = r"^##+\s+"

    def __init__(self):
        self._is_code_block = False

    def get_toc(self, lines: Iterator[str]) -> List[str]:
        toc_lines = [
            self._get_section_as_toc(line)
            for line in lines
            if self._is_line_a_toc_section(line)
        ]
        return ["## Contenidos"] + toc_lines

    def _get_section_as_toc(self, section_line: str) -> str:
        return "{indentation}- [{section_value}](#{section_as_toc})".format(
            indentation=self._get_section_indentation(section_line),
            section_value=self._get_section_value(section_line),
            section_as_toc=self._get_section_value_as_toc(section_line),
        )

    def _get_section_indentation(self, section_line: str) -> str:
        indentations = self._get_section_level_number(section_line) - 1
        return "  " * indentations

    def _get_section_level_number(self, section_line: str) -> int:
        simbol_levels = re.search(r"^#(#+).*", section_line).group(1)
        return len(simbol_levels)

    def _get_section_value(self, section_line: str) -> str:
        result = re.search(rf"{self._REGEX_INIT_TOC_SECTION}(.*)", section_line).group(
            1
        )
        return result.strip()

    def _get_section_value_as_toc(self, section_line: str) -> str:
        result = re.sub(r"\s", "-", self._get_section_value(section_line))
        return result.lower()

    def _is_line_a_toc_section(self, line: str) -> bool:
        if self._is_line_a_code_block(line):
            return False
        return re.match(rf"{self._REGEX_INIT_TOC_SECTION}", line)

    def _is_line_a_code_block(self, line: str) -> bool:
        if line.startswith("```"):
            self._is_code_block = not self._is_code_block
        return self._is_code_block


class Loader:
    @staticmethod
    def print_toc(toc: List[str]):
        for line in toc:
            print(line)


class Manager:
    def __init__(self):
        self._extractor = Extractor()
        self._transformer = Transformer()
        self._loader = Loader()

    def get_and_print_toc(self, file: str) -> List[str]:
        lines = self._extractor.get_lines_in_file(file)
        toc = self._transformer.get_toc(lines)
        self._loader.print_toc(toc)
        return toc


def run(file: str):
    return Manager().get_and_print_toc(file)


if __name__ == "__main__":
    file = sys.argv[1]
    run(file)
