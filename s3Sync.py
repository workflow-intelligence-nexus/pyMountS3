import os
import subprocess
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOCAL_DIR = "/mnt/myswarm/clientdemos"
REMOTE = "myswarm:clientdemos"
SYNC_INTERVAL = 60  # seconds

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_remote_files():
    cmd = f"rclone lsf {REMOTE}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return set(result.stdout.splitlines())

def sync_from_s3():
    remote_files = get_remote_files()
    local_files = set(os.listdir(LOCAL_DIR))

    # Download new or updated files from S3
    for file in remote_files:
        remote_path = f"{REMOTE}/{file}"
        local_path = os.path.join(LOCAL_DIR, file)
        if file not in local_files or md5(local_path) != get_remote_md5(remote_path):
            cmd = f"rclone copy '{remote_path}' '{LOCAL_DIR}' --progress"
            subprocess.run(cmd, shell=True, check=True)

    # Upload local files that don't exist in S3
    for file in local_files - remote_files:
        local_path = os.path.join(LOCAL_DIR, file)
        remote_path = f"{REMOTE}/{file}"
        cmd = f"rclone copy '{local_path}' '{REMOTE}' --progress"
        subprocess.run(cmd, shell=True, check=True)

def get_remote_md5(remote_path):
    cmd = f"rclone md5sum {remote_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.split()[0]
    return None

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
        
        remote_md5 = get_remote_md5(remote_path)
        local_md5 = md5(file_path)
        
        if remote_md5 != local_md5:
            print(f"Uploading {file_path} to {remote_path}")
            cmd = f"rclone copy '{file_path}' '{os.path.dirname(remote_path)}' --progress"
            subprocess.run(cmd, shell=True, check=True)
        else:
            print(f"File {file_path} unchanged. Skipping upload.")

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