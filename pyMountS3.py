import os
import subprocess
import click
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
IPADDR = os.getenv('IPADDR')
MOUNT_POINT = os.getenv('MOUNT_POINT')
RCLONE_REMOTE_NAME = 'myswarm'

@click.group()
def cli():
    """A CLI to configure and mount S3 storage using rclone."""
    pass

@click.command()
def install():
    """Install rclone on the system."""
    install_commands = [
        'sudo apt update',
        'sudo apt install -y rclone',
    ]

    for cmd in install_commands:
        subprocess.run(cmd.split(), check=True)
    
    click.echo('Rclone installation complete.')

@click.command()
def configure():
    """Configure rclone with the S3 settings."""
    config_commands = [
        f'rclone config create {RCLONE_REMOTE_NAME} s3 provider Other env_auth false access_key_id {S3_ACCESS_KEY} secret_access_key {S3_SECRET_KEY} endpoint {os.getenv("S3_ENDPOINT")}',
    ]

    for cmd in config_commands:
        subprocess.run(cmd.split(), check=True)
    
    click.echo('Rclone configuration complete.')


@click.command()
@click.argument('bucket_name')
def mount(bucket_name):
    """Mount the S3 bucket using rclone."""
    mount_path = os.path.join(MOUNT_POINT, bucket_name)
    if not os.path.exists(mount_path):
        os.makedirs(mount_path)
    
    mount_command = [
        'rclone', 'mount', f'{RCLONE_REMOTE_NAME}:{bucket_name}', mount_path, '--daemon',
        '--vfs-cache-mode', 'writes',
        '--transfers', '32',
        '--s3-chunk-size', '128M',
        '--buffer-size', '64M'
    ]
    
    subprocess.run(mount_command, check=True)
    click.echo(f'Mounted {RCLONE_REMOTE_NAME}:{bucket_name} to {mount_path}')

@click.command()
@click.argument('bucket_name')
def unmount(bucket_name):
    """Unmount the S3 bucket."""
    mount_path = os.path.join(MOUNT_POINT, bucket_name)
    unmount_command = ['fusermount', '-u', mount_path]
    
    subprocess.run(unmount_command, check=True)
    click.echo(f'Unmounted {mount_path}')

cli.add_command(install)
cli.add_command(configure)
cli.add_command(mount)
cli.add_command(unmount)

if __name__ == '__main__':
    cli()
