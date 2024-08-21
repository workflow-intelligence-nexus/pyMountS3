#!/bin/bash

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check required tools
check_required_tools() {
    local missing_tools=()
    for tool in rsync pv; do
        if ! command_exists "$tool"; then
            missing_tools+=("$tool")
        fi
    done

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log "Error: The following required tools are missing: ${missing_tools[*]}"
        log "Please install them manually or use a system where they are available."
        exit 1
    fi
}

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    log "Usage: $0 <source_directory> <destination_directory>"
    exit 1
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

# Check for required tools
check_required_tools

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