# Delete Duplicate Photos

A small cross-platform Python app for finding duplicate photo filenames across two folders.

## What it does

- Scans Folder A and Folder B recursively, including subfolders.
- Treats files as duplicates when their filenames are identical.
- Shows matching Folder A and Folder B files.
- Opens selected files with the default macOS or Windows app.
- Reveals either selected file in Finder or Explorer.
- Removes reviewed matches from the table after they are confirmed as resolved.

The app does not delete files yet. It is currently a safe review tool.

## Dependencies

No pip dependencies are required. The app uses Python's standard library and opens a local browser UI, so it does not require Tkinter or `_tkinter`.

## Run

macOS/Linux:

```bash
python3 main.py
```

Windows:

```powershell
py main.py
```

Then use the browser window that opens. If a browser does not open automatically, visit `http://127.0.0.1:8765`.
