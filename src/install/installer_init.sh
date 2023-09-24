#!/bin/bash
# @brief: install necessary depend
# @time: 2023-6-7 13:00

. ../utils/color_config.sh

green "necessary depend installing..."
green "(正在下载必要依赖...)"

sudo apt update
sudo apt install -y \
                    git \
                    vim \
                    cmake \
                    cmake-gui \
                    g++ \
                    gcc \
		    python3-pip \
                    zip \
                    unzip \
                    rar \
                    unrar \
                    tree \
                    wget

wget -O ~/Downloads/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
sudo dpkg -i ~/Downloads/google-chrome.deb
rm ~/Downloads/google-chrome.deb

green "necessary depend finished!"
