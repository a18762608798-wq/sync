"""Local Times New Roman registration; run with the project Python.

python -m unittest discover -s test -p test_figure_fonts.py
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import figure_style

FONT_DIR = ROOT / "assets" / "fonts" / "times-new-roman"
FACES = (
    ("normal", "normal", "times.ttf"),
    ("normal", "bold", "timesbd.ttf"),
    ("italic", "normal", "timesi.ttf"),
    ("italic", "bold", "timesbi.ttf"),
)


class ProjectFontTests(unittest.TestCase):
    def test_all_faces_resolve_to_local_files(self):
        palette = figure_style.apply_figure_style()
        self.assertEqual(palette, figure_style.DEFAULT_PALETTE)
        for style, weight, filename in FACES:
            with self.subTest(face=filename):
                properties = font_manager.FontProperties(
                    family=["Times New Roman"], style=style, weight=weight,
                )
                resolved = font_manager.fontManager.findfont(
                    properties, fallback_to_default=False,
                )
                self.assertEqual(Path(resolved).resolve(), (FONT_DIR / filename).resolve())

    def test_repeated_registration_does_not_duplicate_faces(self):
        figure_style.register_project_fonts()
        figure_style.register_project_fonts()
        entries = [
            entry for entry in font_manager.fontManager.ttflist
            if entry.name == "Times New Roman"
        ]
        self.assertEqual(len(entries), 4)
        self.assertEqual(
            {Path(entry.fname).resolve() for entry in entries},
            {(FONT_DIR / filename).resolve() for _, _, filename in FACES},
        )

    def test_discovery_does_not_use_working_directory(self):
        with patch.object(Path, "cwd", side_effect=AssertionError("cwd used")):
            registered = figure_style.register_project_fonts()
        self.assertEqual(len(registered), 4)

    def test_explicit_missing_directory_fails(self):
        with self.assertRaisesRegex(FileNotFoundError, "times.ttf"):
            figure_style.register_project_fonts(FONT_DIR / "missing")

    def test_partial_bundle_fails_before_changing_font_manager(self):
        previous = list(font_manager.fontManager.ttflist)
        is_file = Path.is_file
        with patch.object(Path, "is_file", lambda path: path.name != "timesbi.ttf" and is_file(path)):
            with self.assertRaisesRegex(FileNotFoundError, "timesbi.ttf"):
                figure_style.register_project_fonts(FONT_DIR)
        self.assertEqual(font_manager.fontManager.ttflist, previous)

    def test_wrong_family_fails_before_changing_font_manager(self):
        previous = list(font_manager.fontManager.ttflist)
        with patch.object(font_manager, "FontProperties") as properties:
            properties.return_value.get_name.return_value = "Other Font"
            with self.assertRaisesRegex(ValueError, "Expected Times New Roman"):
                figure_style.register_project_fonts(FONT_DIR)
        self.assertEqual(font_manager.fontManager.ttflist, previous)

    def test_generic_project_without_local_directory_retains_fallback(self):
        previous = list(font_manager.fontManager.ttflist)
        with patch.object(Path, "is_dir", return_value=False):
            self.assertEqual(figure_style.register_project_fonts(), ())
        self.assertEqual(font_manager.fontManager.ttflist, previous)


if __name__ == "__main__":
    unittest.main()
