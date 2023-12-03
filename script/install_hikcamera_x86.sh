#!/bin/bash

. lib/log.sh

current_path=${PWD}
cd "/tmp" && mkdir "hik_camera" && cd "hik_camera"
wget -O "hik_camera.zip" "https://www.hikrobotics.com/cn2/source/support/software/MVS_STD_GML_V2.1.2_231011.zip"
unzip hik_camera.zip
tar -xzvf MVS-2.1.2_x86_64_20231011.tar.gz
cd "MVS-2.1.2_x86_64_20231011"
echo %{PWD} | sudo -S ./setup.sh
cd ${current_path} && log_info "hik camera is Ok"
