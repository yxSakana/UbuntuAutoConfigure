#!/bin/bash

. script/lib/log.sh

compileKdrobotcpplibs() {
  log_info "kdrobotcpplibs compiling..."

  cd "$1" || (red "kdrobotcpplibs not fond" && exit)
  cmake -B build -G "Ninja" && cmake --build build -j$(nproc) && echo %{PWD} | sudo -S cmake --build build --target install -j$(nproc)

  log_info "kdrobotcpplibs compiled!"
}

if (($# == 1))
then
  current_path=${PWD}
  log_info "Kdrobotlibs compile installing"
  cd ${current_path} && compileKdrobotcpplibs "$1"
else
  log_error "argv len == $#"
  log_error "argv[0] == $0"
  log_error "argv[1] == $1"
  log_error "input kdrobotlibs path"
fi
