#!/bin/bash

. script/color_config.sh

compileKdrobotcpplibs() {
  green "kdrobotcpplibs compiling..."

  cd "$1" || (red "kdrobotcpplibs not fond" && exit)
  cmake -B build -G "Ninja" && cmake --build build -j$(nproc) && echo %{PWD} | sudo -S cmake --build build --target install -j$(nproc)

  green "kdrobotcpplibs compiled!"
}

if (($# == 1))
then
  current_path=${PWD}
  green "Kdrobotlibs compile installing"
  cd ${current_path} && compileKdrobotcpplibs "$1"
else
  red "argv len == $#"
  red "argv[0] == $0"
  red "argv[1] == $1"
  red "input kdrobotlibs path"
fi
