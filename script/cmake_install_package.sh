#!/bin/bash

# @param: generator: 生成器名称(define: Unix Makefiles)
cmakeInstallPackage() {
  if [[ $# == 0 ]]; then
    cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --build build --target install
  elif [[ $# == 1 ]]; then
    generator=$1
    cmake -B build -G ${generator} -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --build build --target install
  elif [[ $# == 2 ]]; then
    generator=$1
    sudo_password=$2
    cmake -B build -G ${generator} -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && echo ${sudo_password} | sudo -S cmake --build build --target install
  fi
}
