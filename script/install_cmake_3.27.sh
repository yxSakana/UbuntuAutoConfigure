#!/bin/bash

wget -O cmake-3.27.tar.gz https://github.com/Kitware/CMake/releases/download/v3.27.7/cmake-3.27.7.tar.gz
tar -xzvf cmake-3.27.tar.gz
cd cmake-3.27.7 && ./configure && make -j$(nproc) && echo %{PWD} | sudo -S make install -j$(nproc) && cd ../
