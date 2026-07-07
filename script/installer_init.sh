#!/bin/bash
# @brief: install necessary depend
# @time: 2023-6-7 13:00

. script/lib/log.sh

log_info "necessary depend installing..."
log_info "(正在下载必要依赖...)"

sudo -v
sudo apt update
sudo apt install -y \
                    git \
                    vim \
                    cmake \
                    cmake-gui \
                    g++ \
                    gcc \
                    zsh \
		            python3-pip \
                    zip \
                    unzip \
                    rar \
                    unrar \
                    tree \
                    wget \
                    curl \
                    neofetch \
                    ninja-build \
                    libssl-dev

log_info "necessary depend finished!"
