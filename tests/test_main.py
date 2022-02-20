import os
import unittest

from src import main


TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), "test.md")


class TestMain(unittest.TestCase):
    def test_run_without_exceptions(self):
        result = main.run(TEST_FILE_PATH)
        self.assertEqual(
            [
                "## Contenidos",
                "- [Section 1](#section-1)",
                "- [Section  Finalización](#section--finalización)",
                "  - [Subsection](#subsection)",
            ],
            result,
        )


if __name__ == "__main__":
    unittest.main()
