import os
import subprocess
import time
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOCAL_DIR = "/mnt/myswarm/clientdemos"
REMOTE = "myswarm:clientdemos"
SYNC_INTERVAL = 300  # increased to 5 minutes
CACHE_FILE = "/tmp/s3_sync_cache.json"
MAX_WORKERS = 4  # for parallel transfers

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_remote_files():
    cmd = f"rclone lsf --format ip {REMOTE}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    files = {}
    for line in result.stdout.splitlines():
        parts = line.split(';')
        if len(parts) == 2:
            files[parts[1]] = parts[0]
    return files

def sync_file(file, local_path, remote_path, is_upload):
    if is_upload:
        cmd = f"rclone copy '{local_path}' '{os.path.dirname(remote_path)}' --progress --transfers 1 --s3-chunk-size 10M"
    else:
        cmd = f"rclone copy '{remote_path}' '{os.path.dirname(local_path)}' --progress --transfers 1 --s3-chunk-size 10M"
    subprocess.run(cmd, shell=True, check=True)

def sync_from_s3():
    cache = load_cache()
    remote_files = get_remote_files()
    local_files = {f: md5(os.path.join(LOCAL_DIR, f)) for f in os.listdir(LOCAL_DIR) if os.path.isfile(os.path.join(LOCAL_DIR, f))}

    tasks = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Download new or updated files from S3
        for file, remote_hash in remote_files.items():
            local_path = os.path.join(LOCAL_DIR, file)
            remote_path = f"{REMOTE}/{file}"
            if file not in local_files or local_files[file] != remote_hash:
                tasks.append(executor.submit(sync_file, file, local_path, remote_path, False))

        # Upload local files that don't exist in S3 or have changed
        for file, local_hash in local_files.items():
            local_path = os.path.join(LOCAL_DIR, file)
            remote_path = f"{REMOTE}/{file}"
            if file not in remote_files or remote_files[file] != local_hash:
                tasks.append(executor.submit(sync_file, file, local_path, remote_path, True))

    # Wait for all tasks to complete
    for task in tasks:
        task.result()

    # Update cache
    cache.update(local_files)
    save_cache(cache)

class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.upload_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.upload_file(event.src_path)

    def upload_file(self, file_path):
        relative_path = os.path.relpath(file_path, LOCAL_DIR)
        remote_path = f"{REMOTE}/{relative_path}"
        sync_file(relative_path, file_path, remote_path, True)

def main():
    print("Performing initial sync...")
    sync_from_s3()

    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, LOCAL_DIR, recursive=True)
    observer.start()

    try:
        while True:
            print(f"Syncing...")
            sync_from_s3()
            print(f"Sleeping for {SYNC_INTERVAL} seconds...")
            time.sleep(SYNC_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()