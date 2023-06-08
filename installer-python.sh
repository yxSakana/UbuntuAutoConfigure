#!/bin/bash
# @brief: install python depend
# @time: 2023-6-7 13:00

echo "python depend installing..."

sudo apt update
sudo apt install python3-pip
sudo apt install python3-dev python3-pip python3-venv

echo "python depend finished!"
