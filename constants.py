from pathlib import Path


DEFAULT_FOLDER_A = Path.home() / "Desktop" / "FolderA"
DEFAULT_FOLDER_B = Path.home() / "Desktop" / "FolderB"
HOST = "127.0.0.1"
PORT = 8765

FILE_TYPE_EXTENSIONS = {
    "images": {
        ".avif", ".bmp", ".gif", ".heic", ".heif", ".jpeg", ".jpg",
        ".png", ".tif", ".tiff", ".webp",
    },
    "videos": {
        ".avi", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg",
        ".webm", ".wmv",
    },
    "word": {".doc", ".docm", ".docx", ".dot", ".dotm", ".dotx"},
    "excel": {
        ".csv", ".xls", ".xlsb", ".xlsm", ".xlsx", ".xlt", ".xltm",
        ".xltx",
    },
}
