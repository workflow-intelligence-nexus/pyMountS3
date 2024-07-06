import os
import subprocess
import click
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
IPADDR = os.getenv('IPADDR')
BUCKET_NAME = os.getenv('BUCKET_NAME')
RCLONE_REMOTE_NAME = 'myswarm'
MOUNT_POINT = '/mnt/myswarm'

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
        f'rclone config create {RCLONE_REMOTE_NAME} s3 provider Other',
        f'rclone config {RCLONE_REMOTE_NAME} env_auth false',
        f'rclone config {RCLONE_REMOTE_NAME} access_key_id {S3_ACCESS_KEY}',
        f'rclone config {RCLONE_REMOTE_NAME} secret_access_key {S3_SECRET_KEY}',
        f'rclone config {RCLONE_REMOTE_NAME} endpoint http://{IPADDR}:9010'
    ]

    for cmd in config_commands:
        subprocess.run(cmd.split(), check=True)
    
    click.echo('Rclone configuration complete.')

@click.command()
def mount():
    """Mount the S3 bucket using rclone."""
    if not os.path.exists(MOUNT_POINT):
        os.makedirs(MOUNT_POINT)
    
    mount_command = [
        'rclone', 'mount', f'{RCLONE_REMOTE_NAME}:{BUCKET_NAME}', MOUNT_POINT, '--daemon'
    ]
    
    subprocess.run(mount_command, check=True)
    click.echo(f'Mounted {RCLONE_REMOTE_NAME}:{BUCKET_NAME} to {MOUNT_POINT}')

@click.command()
def unmount():
    """Unmount the S3 bucket."""
    unmount_command = ['fusermount', '-u', MOUNT_POINT]
    
    subprocess.run(unmount_command, check=True)
    click.echo(f'Unmounted {MOUNT_POINT}')

cli.add_command(install)
cli.add_command(configure)
cli.add_command(mount)
cli.add_command(unmount)

if __name__ == '__main__':
    cli()
