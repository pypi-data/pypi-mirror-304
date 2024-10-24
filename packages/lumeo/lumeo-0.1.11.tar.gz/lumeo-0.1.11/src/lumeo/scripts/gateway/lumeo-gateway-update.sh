#!/bin/bash

set -eo pipefail

# Check if pipx is installed
if ! command -v pipx &> /dev/null
then
    echo "pipx not found. Installing pipx..."
    sudo apt-get update
    sudo apt-get install -y pipx python3
    sudo pipx ensurepath
fi

# Install lumeo using pipx
if pipx list | grep -q "lumeo"; then
    echo "Updating lumeo CLI to the latest version..."
    sudo pipx upgrade lumeo
else
    echo "Installing lumeo CLI..."
    sudo pipx install lumeo
fi

# Update lumeo gateway containers
sudo lumeo-gateway-manager update --no-prompt

# Update lumeo gateway manager web interface
sudo lumeo-gateway-manager update-wgm --no-prompt
