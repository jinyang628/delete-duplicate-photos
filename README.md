# Delete Duplicate Photos

A small cross-platform Python app for finding duplicate photo filenames across two folders or within one parent folder.

## What it does

- Scans Folder A and Folder B recursively, including subfolders.
- Treats files as duplicates when their filenames are identical.
- Shows matching Folder A and Folder B files.
- Can instead scan one parent folder recursively and review repeated filenames within it.
- Groups every copy of a repeated filename into one scrollable list with a Reveal button for each file.
- Opens selected files with the default macOS or Windows app.
- Reveals either selected file in Finder or Explorer.
- Removes reviewed matches from the table after they are confirmed as resolved.

The app does not delete files yet. It is currently a safe review tool.

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

Closing the app's browser tab or window also stops the local server. Refreshing the
page leaves the app running. If the browser is forcibly terminated and cannot send
its close notification, press Ctrl+C in the console to stop the server.

## Windows executable

GitHub Actions can build a standalone Windows executable, so end users do not need to install Python.

To make a test build, open the repository's **Actions** tab, select **Build Windows executable**, and choose **Run workflow**. Download `DuplicatePhotoFinder-Windows` from the completed run's **Artifacts** section.

To publish a version, push a tag whose name starts with `v`:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow creates a GitHub Release containing `DuplicatePhotoFinder.exe` and its SHA-256 checksum.
