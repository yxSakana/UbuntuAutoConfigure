#!/bin/bash
# @brief: realsense

. script/color_config.sh

if (( $# == 1 ))
then
  dir_path=$1
else
  dir_path="librealsense"
fi

green "realsense compiling..."
# depend
echo %{PWD} | sudo -S apt update
echo %{PWD} | sudo -S apt install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

# compile
if (( $dir_path == "librealsense" ))
then
  git clone https://github.com/IntelRealSense/librealsense.git
fi
cd dir_path || (red "librealsense not fond" && exit)
mkdir build && cd build || (red "build not fond" && exit)

cmake .. -DBUILD_EXAMPLES=true && make -j$(nproc) && echo %{PWD} | sudo -S make install -j$(nproc) && \
echo %{PWD} | sudo -S cp ../config/99-realsense-libusb.rules /etc/udev/rules.d/ && \
echo %{PWD} | sudo -S udevadm control --reload-rules && udevadm trigger && \
cd ../.. && rm -rf librealsense && \
green "realsense compiled!"
