#!/bin/bash

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install a package
install_package() {
    local package=$1
    log "$package is not installed. Attempting to install..."
    if command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y "$package"
    elif command_exists yum; then
        sudo yum install -y "$package"
    else
        log "Error: Unable to install $package. Please install it manually."
        exit 1
    fi
}

# Check and install rsync and pv if not present
for package in rsync pv; do
    if ! command_exists "$package"; then
        install_package "$package"
    fi

    if ! command_exists "$package"; then
        log "Error: $package installation failed. Please install it manually."
        exit 1
    fi
done

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

# Calculate total size of source directory
total_size=$(du -sb "$SOURCE_DIR" | cut -f1)

# Perform the copy operation with progress
log "Starting copy operation from $SOURCE_DIR to $DEST_DIR"
rsync -ah --info=progress2 "$SOURCE_DIR/" "$DEST_DIR/" | pv -lep -s "$total_size" > /dev/null

# Check the exit status of rsync
if [ $? -eq 0 ]; then
    log "Copy operation completed successfully."
else
    log "Error: Copy operation failed. Please check the output above for details."
    exit 1
fi