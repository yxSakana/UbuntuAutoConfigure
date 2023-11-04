#!/bin/bash

current_path=${PWD}
cd /tmp && \
git clone https://github.com/gflags/gflags.git --depth=1 && \
cd gflags && \
cmake -B build -G "Ninja" -DBUILD_SHARED_LIBS=ON && cmake --build build && sudo cmake --build build --target install
cd {current_path}
