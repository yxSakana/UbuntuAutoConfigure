#!/bin/bash
# @brief: spdlog

. script/color_config.sh

proxy_url="https://ghproxy.com/"

green "spdlog compiling..."

if (( $# == 1 ))
then
  dir_path=$1
else
  git clone ${proxy_url}https://github.com/gabime/spdlog.git
  dir_path="spdlog"
fi

cd dir_path || (echo "spdlog not fond" && exit)
mkdir build && cd build || (echo "build not fond" && exit)
cmake ..
echo %{PWD} | sudo -S make install

cd ../..
rm -rf spdlog

green "spdlog compiled!"
