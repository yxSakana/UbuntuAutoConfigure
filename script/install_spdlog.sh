#!/bin/bash
# @brief: spdlog

. script/lib/log.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD

log_info "spdlog compiling..."

if (( $# == 1 ))
then
  dir_path=$1
else
  cd package && \
  if [ ! -e spdlog ]; then
    git clone ${proxy_url}https://github.com/gabime/spdlog.git
  fi
  dir_path="spdlog"
fi

cd $dir_path || (echo "spdlog not fond" && exit)

cmake -B build && cmake --build build -j$(nproc) && echo %{PWD} | sudo -S cmake --build build --target install -j$(nproc) && \
cd ../ && rm -rf spdlog && \
log_info "spdlog compiled!" || log_error "Failed: spdlog compie"

cd ${current_dir}
