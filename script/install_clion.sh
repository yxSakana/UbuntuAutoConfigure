#!/bin/bash

. script/color_config.sh

clion_vision="2023.1.3"
clion_url="https://download.jetbrains.com/cpp/CLion-${clion_vision}.tar.gz"

download_dir="_tmp"
mkdir -p "${download_dir}"

green "clion downloading..."

if [ ! -e "${download_dir}/clion-${clion_vision}.tar.gz" ]
then
    wget -O "${download_dir}/clion-${clion_vision}.tar.gz" "${clion_url}"
fi

green "Download finished!"
green "tar -xzvf ..."

tar -xzvf "${download_dir}/clion-${clion_vision}.tar.gz"

echo %{PWD} | sudo -S mv "clion-${clion_vision}" /opt/

echo "export PATH=/opt/clion-${clion_vision}/bin\${PATH:+:\${PATH}}" >> ~/.bashrc

rm -rf ${download_dir}
