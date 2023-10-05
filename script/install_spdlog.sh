#!/bin/bash
# @brief: spdlog

. script/color_config.sh

green "spdlog compiling..."

if (( $# == 1 ))
then
  dir_path=$1
else
  dir_path="spdlog"
  git clone https://github.com/gabime/spdlog.git
fi
cd dir_path || (echo "spdlog not fond" && exit)
mkdir build && cd build || (echo "build not fond" && exit)
cmake ..
echo %{PWD} | sudo -S make install

cd ../..
rm -rf spdlog

green "spdlog compiled!"
