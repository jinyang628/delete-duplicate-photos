import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class RevealPathTests(unittest.TestCase):
    @patch("main.subprocess.run")
    @patch("main.sys.platform", "win32")
    def test_windows_opens_new_window_with_file_selected(self, run):
        target = Path("photo folder") / "image.jpg"

        with patch.object(Path, "exists", return_value=True):
            main.reveal_path(target)

        resolved_target = target.resolve()
        run.assert_called_once_with(
            [
                "explorer.exe",
                "/n,",
                f"/select,{main.os.path.normpath(resolved_target)}",
            ],
            check=False,
        )


class ScanFilesTests(unittest.TestCase):
    def test_only_indexes_selected_file_types_case_insensitively(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "photo.JPG").touch()
            (folder / "other.png").touch()
            (folder / "movie.mp4").touch()
            (folder / "notes.txt").touch()

            files = main.scan_files(folder, ["images"])

        self.assertEqual(set(files), {"photo.jpg", "other.png"})

    def test_filename_matching_ignores_capitalization(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            first = folder / "first"
            second = folder / "second"
            first.mkdir()
            second.mkdir()
            (first / "Photo.JPG").touch()
            (second / "photo.jpg").touch()

            duplicates = main.find_duplicates_within_folder(
                main.scan_files(folder, ["images"])
            )

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(duplicates[0]["files"]), 2)

    def test_ignores_files_inside_recycle_bin_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            recycle_bin = folder / "$RECYCLE.BIN" / "user-id"
            recycle_bin.mkdir(parents=True)
            (recycle_bin / "deleted.jpg").touch()
            (folder / "kept.jpg").touch()

            files = main.scan_files(folder, ["images"])

        self.assertEqual(set(files), {"kept.jpg"})

    def test_ignores_trash_directory_names_case_insensitively(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            trash = folder / ".TRASHES" / "501"
            trash.mkdir(parents=True)
            (trash / "deleted.png").touch()

            files = main.scan_files(folder, ["images"])

        self.assertEqual(files, {})


if __name__ == "__main__":
    unittest.main()
