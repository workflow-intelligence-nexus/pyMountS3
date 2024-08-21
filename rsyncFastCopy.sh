#!/bin/bash

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install rsync
install_rsync() {
    log "rsync is not installed. Attempting to install..."
    if command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y rsync
    elif command_exists yum; then
        sudo yum install -y rsync
    else
        log "Error: Unable to install rsync. Please install it manually."
        exit 1
    fi
}

# Check if rsync is installed
if ! command_exists rsync; then
    install_rsync
fi

# Check if rsync is now available
if ! command_exists rsync; then
    log "Error: rsync installation failed. Please install it manually."
    exit 1
fi

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    log "Usage: $0 <source_directory> <destination_directory>"
    exit 1
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    log "Error: Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Perform the copy operation
log "Starting copy operation from $SOURCE_DIR to $DEST_DIR"
rsync -avh --progress --stats --numeric-ids --delete "$SOURCE_DIR/" "$DEST_DIR/"

# Check the exit status of rsync
if [ $? -eq 0 ]; then
    log "Copy operation completed successfully."
else
    log "Error: Copy operation failed. Please check the output above for details."
    exit 1
fi