#!/bin/bash
# @brief: spdlog

. script/color_config.sh

compileSpdlog() {
  green "spdlog compiling..."

  git clone https://github.com/gabime/spdlog.git
  cd spdlog || (echo "spdlog not fond" && exit)
  mkdir build && cd build || (echo "build not fond" && exit)
  cmake ..
  echo %{PWD} | sudo -S make install

  cd ../..
  rm -rf spdlog

  green "spdlog compiled!"
}

compileSpdlog
