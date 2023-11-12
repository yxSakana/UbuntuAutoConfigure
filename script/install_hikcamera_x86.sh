#!/bin/bash

. script/color_config.sh

current_path=${PWD}
cd "/tmp" && mkdir "hik_camera" && cd "hik_camera"
wget -O "hik_camera.zip" "https://www.hikrobotics.com/cn2/source/support/software/MvCamCtrlSDK_STD_V4.1.2_231011.zip"
unzip hik_camera.zip
tar -xzvf MvCamCtrlSDK_Runtime-4.1.2_x86_64_20231011.tar.gz
cd "MvCamCtrlSDK_Runtime-4.1.2_x86_64_20231011"
echo %{PWD} | sudo -S ./setup.sh
cd ${current_path} && blue "hik camera is Ok"
