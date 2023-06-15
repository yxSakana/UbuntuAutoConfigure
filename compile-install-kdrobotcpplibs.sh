compileKdrobotcpplibs() {
  echo "kdrobotcpplibs compiling..."

  cd "$1" || (echo "kdrobotcpplibs not fond" && exit)
  mkdir build && cd build || (echo "build not fond" && exit)
  cmake ..
  sudo make install -j8

  cd ../../
  rm -rf $1
  echo "kdrobotcpplibs compiled!"
}

if (($# == 1))
then
  echo "Kdrobotlibs compile installing"
  compileKdrobotcpplibs "$1"
else
  echo "argv len == $#"
  echo "argv[0] == $0"
  echo "argv[1] == $1"
  echo "input kdrobotlibs path"
fi
