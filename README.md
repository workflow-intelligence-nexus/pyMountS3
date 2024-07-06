# pyMountS3

A CLI application to configure and mount S3 storage using Rclone. This application reads settings from a `.env` file, allows you to install `rclone`, configure it, and provides commands to mount and unmount your S3 storage.

## Prerequisites

- Python 3.10
- Ubuntu 22.04
- Conda (Anaconda or Miniconda)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pyMountS3.git
cd pyMountS3
```

### 2. Set Up Virtual Environment and Install Dependencies

```bash
conda create --name pyMountS3 python=3.10
conda activate pyMountS3
pip install -r requirements.txt
```

### 3. Create and Configure `.env` File

Create a `.env` file in the root directory of the project and populate it with your settings. You can use the provided `.env.example` as a template.

```env
# S3 Storage Settings
IPADDR=your_ip
WEB_USER=your_user
PASSWORD=your_password
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
BUCKET_NAME=your_bucket_name
```

### 4. Install Rclone

The CLI includes a command to install `rclone`:

```bash
python mountSWARM.py install
```

## Usage

### Configure Rclone

Configure `rclone` with the S3 settings from your `.env` file:

```bash
python mountSWARM.py configure
```

### Mount the S3 Bucket

Mount your S3 bucket to the specified mount point:

```bash
python mountSWARM.py mount
```

### Unmount the S3 Bucket

Unmount the S3 bucket:

```bash
python mountSWARM.py unmount
```

## Files and Directories

- `mountSWARM.py`: The main CLI application script.
- `requirements.txt`: Python dependencies for the project.
- `.env.example`: Example environment configuration file.
- `.gitignore`: Git ignore file to exclude `.env` and `venv` directories.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## Acknowledgements

- [Rclone](https://rclone.org/) - Rclone documentation and tool.
- [Click](https://click.palletsprojects.com/) - Python package for creating command-line interfaces.
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Python package to read key-value pairs from a `.env` file and set them as environment variables.

## Contact

For issues or questions, please open an issue on GitHub.
