#!/bin/bash

# Update package list
sudo apt-get update

# Install Python, pip, and git if they're not already installed
sudo apt-get install -y python3 python3-pip git

# Clone the repository
git clone https://github.com/defibabylon/setup_comfyui.git
cd setup_comfyui

# Install requirements
pip3 install -r requirements.txt

# Run the setup script
python3 setup_comfyui.py
