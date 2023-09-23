#!/bin/bash
# @brief: install python depend
# @time: 2023-6-7 13:00

. ../utils/color_config.sh

green "python depend installing..."

sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-dev python3-pip python3-venv

green "python depend finished!"
