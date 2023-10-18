#!/bin/bash
# @brief: 安装fmt

. script/color_config.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD

green "fmt compiling..."

cd /tmp
git clone ${proxy_url}https://github.com/fmtlib/fmt.git --depth=1 && cd fmt
cmake -B build -G "Ninja" && cmake --build build -j$(nproc) && echo %{PWD} | sudo -S cmake --build build --target install -j$(nproc) && \
cd ${current_dir} && green "fmt Finished!"
