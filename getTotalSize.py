import os
import sys
import concurrent.futures
import multiprocessing

def get_size(file_path):
    try:
        return os.path.getsize(file_path)
    except (OSError, FileNotFoundError):
        return 0

def process_directory(directory):
    total_size = 0
    for entry in os.scandir(directory):
        if entry.is_file(follow_symlinks=False):
            total_size += entry.stat().st_size
        elif entry.is_dir(follow_symlinks=False):
            total_size += process_directory(entry.path)
    return total_size

def get_directory_size(path):
    cpu_count = multiprocessing.cpu_count()
    total_size = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                futures.append(executor.submit(process_directory, entry.path))
            elif entry.is_file(follow_symlinks=False):
                total_size += entry.stat().st_size

        for future in concurrent.futures.as_completed(futures):
            total_size += future.result()

    return total_size

def bytes_to_gb(bytes_value):
    return bytes_value / (1024 * 1024 * 1024)

def main():
    if len(sys.argv) != 2:
        print("Usage: python getTotalSize.py /path/to/directory")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        sys.exit(1)

    total_size_bytes = get_directory_size(directory_path)
    total_size_gb = bytes_to_gb(total_size_bytes)

    print(f"{directory_path} total size: {total_size_gb:.2f}GB")

if __name__ == "__main__":
    main()