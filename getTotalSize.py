import os
import sys

def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
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