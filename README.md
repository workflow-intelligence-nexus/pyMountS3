# pyMountS3

A CLI application to configure and mount S3 storage using Rclone. This application reads settings from a `.env` file, allows you to install `rclone`, configure it, and provides commands to mount and unmount your S3 storage. Additionally, it includes a utility to benchmark and optimize the performance of your mounted S3 bucket.

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
2. Set Up Conda Environment and Install Dependencies
```bash
conda create --name pyMountS3 python=3.10
conda activate pyMountS3
pip install -r requirements.txt
```
3. Create and Configure .env File
Create a .env file in the root directory of the project and populate it with your settings. You can use the provided .env.example as a template.

env
```bash
# S3 Storage Settings
IPADDR=your_ip
WEB_USER=your_user
PASSWORD=your_password
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
MOUNT_POINT=/mnt/myswarm
```

4. Install Rclone
The CLI includes a command to install rclone:

```bash
python pyMountS3.py install
```

Usage
Configure Rclone
Configure rclone with the S3 settings from your .env file:

```bash
python pyMountS3.py configure
```

Mount the S3 Bucket
Mount your S3 bucket to the specified mount point:

```bash
python pyMountS3.py mount <bucket_name>
```

Replace <bucket_name> with the name of your S3 bucket.

Unmount the S3 Bucket
Unmount the S3 bucket:

```bash
python pyMountS3.py unmount <bucket_name>
```

Replace <bucket_name> with the name of your S3 bucket.

Benchmarking and Optimization
The project includes a utility to benchmark and optimize the performance of your mounted S3 bucket.

1. Install Benchmarking Tools
Install fio for benchmarking:

```bash
sudo apt-get install -y fio
```

2. Create Benchmark Script
Create a benchmark.fio file with the following content:

ini
```bash
[global]
directory=/mnt/swarm/firstbucket
ioengine=libaio
direct=1
size=1G
bs=4k

[write_test]
rw=write
name=write_test
numjobs=4
group_reporting

[read_test]
rw=read
name=read_test
numjobs=4
```

group_reporting
3. Run the Benchmark Utility
Run the autoBenchmark.py script to benchmark and optimize the performance:

```bash
python autoBenchmark.py
```

This script will test various configurations and output the performance metrics.

Files and Directories
pyMountS3.py: The main CLI application script.
autoBenchmark.py: The benchmarking and optimization utility.
requirements.txt: Python dependencies for the project.
.env.example: Example environment configuration file.
.gitignore: Git ignore file to exclude .env and pyMountS3 conda environment directories.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Fork the repository.
Create a new branch: git checkout -b feature-name.
Make your changes and commit them: git commit -m 'Add feature'.
Push to the branch: git push origin feature-name.
Submit a pull request.
Acknowledgements
Rclone - Rclone documentation and tool.
Click - Python package for creating command-line interfaces.
Python-dotenv - Python package to read key-value pairs from a .env file and set them as environment variables.
Fio - Flexible I/O tester for benchmarking and testing.
Contact
For issues or questions, please open an issue on GitHub.

javascript
Copy code
