#!/bin/bash
# @brief: realsense && spdlog && Kdrobotlibs

compileRealsense() {
  echo "realsense compiling..."
  # depend
  sudo apt update && sudo apt upgrade
  sudo apt install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

  # compile
  git clone https://github.com/IntelRealSense/librealsense.git
  cd librealsense || (echo "librealsense not fond" && exit)
  mkdir build && cd build || (echo "build not fond" && exit)
  cmake .. -DBUILD_EXAMPLES=true
  make -j8
  sudo make install

  # install udev rule
  sudo cp ../config/99-realsense-libusb.rules /etc/udev/rules.d/
  sudo udevadm control --reload-rules && udevadm trigger

  cd ../..
  echo "realsense compiled!"
}

compileSpdlog() {
  echo "spdlog compiling..."

  git clone https://github.com/gabime/spdlog.git
  cd spdlog || (echo "spdlog not fond" && exit)
  mkdir build && cd build || (echo "build not fond" && exit)
  cmake ..
  sudo make install

  cd ../..
  echo "spdlog compiled!"
}

echo "realsense && spdlog compile installing"

compileRealsense
compileSpdlog

echo "compile finished!"
