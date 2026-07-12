import unittest
from pathlib import Path
from unittest.mock import patch

import main


class RevealPathTests(unittest.TestCase):
    @patch("main.subprocess.run")
    @patch("main.sys.platform", "win32")
    def test_windows_passes_select_switch_separately(self, run):
        target = Path("photo folder") / "image.jpg"

        with patch.object(Path, "exists", return_value=True):
            main.reveal_path(target)

        resolved_target = target.resolve()
        run.assert_called_once_with(
            ["explorer.exe", "/select,", main.os.path.normpath(resolved_target)],
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
