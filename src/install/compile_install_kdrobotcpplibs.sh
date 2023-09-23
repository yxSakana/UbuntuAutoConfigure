#!/bin/bash

. ../utils/color_config.sh

compileKdrobotcpplibs() {
  green "kdrobotcpplibs compiling..."

  cd "$1" || (red "kdrobotcpplibs not fond" && exit)
  mkdir build && cd build || (red "build not fond" && exit)
  cmake ..
  sudo make install -j8

  cd ../../
  rm -rf $1
  green "kdrobotcpplibs compiled!"
}

if (($# == 1))
then
  green "Kdrobotlibs compile installing"
  compileKdrobotcpplibs "$1"
else
  red "argv len == $#"
  red "argv[0] == $0"
  red "argv[1] == $1"
  red "input kdrobotlibs path"
fi
