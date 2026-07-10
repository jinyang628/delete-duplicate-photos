import json
import os
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from html import INDEX_HTML
from constants import DEFAULT_FOLDER_A, DEFAULT_FOLDER_B, HOST, PORT

def scan_files(folder):
    files_by_name = {}

    for path in folder.rglob("*"):
        if path.is_file():
            files_by_name.setdefault(path.name, []).append(path)

    return files_by_name


def find_duplicates(folder_a_files, folder_b_files):
    duplicates = []

    for filename, delete_paths in folder_b_files.items():
        keep_paths = folder_a_files.get(filename)
        if keep_paths is None:
            continue

        for delete_path in delete_paths:
            duplicates.append(
                {
                    "filename": filename,
                    "keep": [str(path) for path in keep_paths],
                    "delete": str(delete_path),
                }
            )

    return duplicates


def open_path(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def reveal_path(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if sys.platform.startswith("win"):
        subprocess.run(["explorer", f"/select,{path}"], check=False)
    elif sys.platform == "darwin":
        subprocess.run(["open", "-R", str(path)], check=False)
    else:
        open_path(path.parent)


class DuplicatePhotoServer(BaseHTTPRequestHandler):
    duplicates = []

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self._send_html(INDEX_HTML)
            return

        if parsed.path == "/api/defaults":
            self._send_json(
                {
                    "folderA": str(DEFAULT_FOLDER_A),
                    "folderB": str(DEFAULT_FOLDER_B),
                }
            )
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/scan":
            self._scan()
            return

        if parsed.path == "/api/open":
            self._open_selected(reveal=False)
            return

        if parsed.path == "/api/reveal":
            self._open_selected(reveal=True)
            return

        self._send_json({"error": "Not found"}, status=404)

    def _scan(self):
        data = self._read_json()
        folder_a = Path(data.get("folderA", "")).expanduser()
        folder_b = Path(data.get("folderB", "")).expanduser()

        if not folder_a.is_dir():
            self._send_json({"error": f"Folder A does not exist: {folder_a}"}, status=400)
            return
        if not folder_b.is_dir():
            self._send_json({"error": f"Folder B does not exist: {folder_b}"}, status=400)
            return

        folder_a_files = scan_files(folder_a)
        folder_b_files = scan_files(folder_b)
        type(self).duplicates = find_duplicates(folder_a_files, folder_b_files)

        self._send_json({"duplicates": type(self).duplicates})

    def _open_selected(self, reveal):
        data = self._read_json()
        index = data.get("index")
        target = data.get("target")

        if not isinstance(index, int) or index < 0 or index >= len(type(self).duplicates):
            self._send_json({"error": "Invalid duplicate selection."}, status=400)
            return

        duplicate = type(self).duplicates[index]
        try:
            if reveal:
                reveal_path(duplicate["delete"])
            elif target == "keep":
                for path in duplicate["keep"]:
                    open_path(path)
            elif target == "delete":
                open_path(duplicate["delete"])
            elif target == "both":
                for path in duplicate["keep"]:
                    open_path(path)
                open_path(duplicate["delete"])
            else:
                self._send_json({"error": "Invalid open target."}, status=400)
                return
        except OSError as error:
            self._send_json({"error": str(error)}, status=500)
            return

        self._send_json({"ok": True})

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), DuplicatePhotoServer)
    url = f"http://{HOST}:{PORT}"
    print(f"Duplicate Photo Finder is running at {url}")
    print("Press Ctrl+C to stop the app.")
    threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Duplicate Photo Finder.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
