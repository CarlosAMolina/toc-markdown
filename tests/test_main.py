import os
import random
import string
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
                "- [Section Gnu/Linux](#section-gnulinux)",
                "- [Section  Finalización](#section--finalización)",
                "  - [Subsection](#subsection)",
            ],
            result,
        )


class TestFileModifier(unittest.TestCase):
    def test_save_at_the_beginning_of_the_file(self):
        file_path = "/tmp/test-toc-{random_string}.md".format(
            random_string="".join(
                [random.choice(string.ascii_lowercase) for x in range(6)]
            )
        )
        file_initial_content = "Line 1\nLine 2"
        string_to_add = "foo"
        with open(file_path, "w") as f:
            f.write(file_initial_content)
        main.FileModifier().save_at_the_beginning_of_the_file(file_path, string_to_add)
        with open(file_path, "r") as f:
            file_final_content = f.read()
        os.remove(file_path)
        self.assertEqual(f"{string_to_add}\n{file_initial_content}", file_final_content)


if __name__ == "__main__":
    unittest.main()
