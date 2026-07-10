from pathlib import Path


FOLDER_A = Path("/Users/jinyangchen/Desktop/Folder1")
FOLDER_B = Path("/Users/jinyangchen/Desktop/Folder2")


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
                    "keep": keep_paths,
                    "delete": delete_path,
                }
            )

    return duplicates


def main():
    if not FOLDER_A.exists():
        raise FileNotFoundError(f"Folder A does not exist: {FOLDER_A}")
    if not FOLDER_B.exists():
        raise FileNotFoundError(f"Folder B does not exist: {FOLDER_B}")

    folder_a_files = scan_files(FOLDER_A)
    folder_b_files = scan_files(FOLDER_B)
    duplicates = find_duplicates(folder_a_files, folder_b_files)

    if not duplicates:
        print("No duplicate filenames found.")
        return

    print(f"Found {len(duplicates)} duplicate file(s):")
    for duplicate in duplicates:
        print()
        print(f"Filename: {duplicate['filename']}")
        print("Keep:")
        for keep_path in duplicate["keep"]:
            print(f"  {keep_path}")
        print(f"Delete candidate: {duplicate['delete']}")


if __name__ == "__main__":
    main()
