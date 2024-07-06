import os
import subprocess

def run_benchmark():
    result = subprocess.run(['fio', 'benchmark.fio'], capture_output=True, text=True)
    print(result.stdout)
    return result.stdout

def mount_with_settings(transfers, chunk_size, buffer_size):
    umount_command = ['fusermount', '-u', '/mnt/swarm/firstbucket']
    mount_command = [
        'rclone', 'mount', 'myswarm:firstbucket', '/mnt/swarm/firstbucket', '--daemon',
        '--vfs-cache-mode', 'full',
        '--transfers', str(transfers),
        '--s3-chunk-size', chunk_size,
        '--buffer-size', buffer_size
    ]
    subprocess.run(umount_command, check=True)
    subprocess.run(mount_command, check=True)

# Initial benchmark with default settings
print("Initial benchmark with default settings:")
run_benchmark()

# Test with different settings
settings = [
    (8, '32M', '16M'),
    (16, '64M', '32M'),
    (32, '128M', '64M')
]

for transfers, chunk_size, buffer_size in settings:
    print(f"\nTesting with transfers={transfers}, chunk_size={chunk_size}, buffer_size={buffer_size}:")
    mount_with_settings(transfers, chunk_size, buffer_size)
    run_benchmark()
