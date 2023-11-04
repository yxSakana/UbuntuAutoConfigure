#!/bin/bash
# @brief: install necessary depend
# @time: 2023-6-7 13:00

. script/color_config.sh

green "necessary depend installing..."
green "(正在下载必要依赖...)"

echo %{PWD} | sudo -S apt update
echo %{PWD} | sudo -S apt install -y \
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
                    wget \
                    ninja-build \
                    libssl-dev

green "necessary depend finished!"
