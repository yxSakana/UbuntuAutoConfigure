#!/bin/bash
# @brief: install qt && opencv depend
# @time: 2023-6-7 13:00

. ../utils/color_config.sh

green "qt && opencv depend installing..."

sudo apt update
sudo apt install -y \
                    git \
                    vim \
                    htop \
                    cmake \
                    cmake-gui \
                    screen \
                    libavcodec-dev \
                    libavformat-dev \
                    libavutil-dev \
                    libeigen3-dev \
                    libglew-dev \
                    libgtk2.0-dev \
                    libgtk-3-dev \
                    libjpeg-dev \
                    libpostproc-dev \
                    libswscale-dev \
                    libtbb-dev \
                    libtiff5-dev \
                    libv4l-dev \
                    libxvidcore-dev \
                    libx264-dev \
                    zlib1g-dev \
                    pkg-config \
                    libxcb*
sudo apt install -y python3-pip
sudo -H pip3 install Cython -i https://pypi.tuna.tsinghua.edu.cn/simple
sudo -H pip3 install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

green "qt && opencv depend finished!"
