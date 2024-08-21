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

def sync_from_s3():
    cmd = f"rclone sync {REMOTE} {LOCAL_DIR} --progress"
    subprocess.run(cmd, shell=True, check=True)

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
        
        # Check if file exists remotely and compare MD5 hashes
        check_cmd = f"rclone md5sum {remote_path}"
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            remote_md5 = result.stdout.split()[0]
            local_md5 = md5(file_path)
            
            if remote_md5 == local_md5:
                print(f"File {file_path} unchanged. Skipping upload.")
                return

        print(f"Uploading {file_path} to {remote_path}")
        cmd = f"rclone copy '{file_path}' '{os.path.dirname(remote_path)}' --progress"
        subprocess.run(cmd, shell=True, check=True)

def main():
    # Initial sync from S3
    print("Performing initial sync from S3...")
    sync_from_s3()

    # Set up file watcher for uploads
    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, LOCAL_DIR, recursive=True)
    observer.start()

    try:
        while True:
            print(f"Syncing from S3...")
            sync_from_s3()
            print(f"Sleeping for {SYNC_INTERVAL} seconds...")
            time.sleep(SYNC_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()