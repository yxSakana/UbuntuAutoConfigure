#!/bin/bash
# @brief: realsense

. script/lib/log.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD

log_info "realsense compiling..."
# depend
echo %{PWD} | sudo -S apt update
echo %{PWD} | sudo -S apt install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

# compile
if (( $# == 1 ))
then
  dir_path=$1
else
  cd package
    if [ ! -e librealsense ]; then
      git clone ${proxy_url}https://github.com/IntelRealSense/librealsense.git
    fi
  dir_path="librealsense"
fi

cd $dir_path || (log_error "librealsense not fond" && exit)

cmake -B build -DBUILD_EXAMPLES=true && cmake --build build -j$(nproc) && echo %{PWD} | sudo -S cmake --build build --target install -j$(nproc) && \
echo %{PWD} | sudo -S cp config/99-realsense-libusb.rules /etc/udev/rules.d/ && \
echo %{PWD} | sudo -S udevadm control --reload-rules && udevadm trigger && \
cd ../ && rm -rf librealsense && \
log_info "realsense compiled!" || log_error "Failed: realsense compile"

cd ${current_dir}
