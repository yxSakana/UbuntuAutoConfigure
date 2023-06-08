#!/bin/bash

clion_vision="2023.1.3"
pycharm_vision="2023.1.2"
clion_url="https://download.jetbrains.com/cpp/CLion-${clion_vision}.tar.gz"
pycharm_url="https://download.jetbrains.com/python/pycharm-professional-${pycharm_vision}.tar.gz"

download_dir="_tmp"
mkdir -p "${download_dir}"

echo "clion downloading..."

wget -O "${download_dir}/clion-${clion_vision}.tar.gz" "${clion_url}"
wget -O "${download_dir}/pycharm-${pycharm_vision}.tar.gz" "${pycharm_url}"

echo "Download finished!"

tar -xzvf "${download_dir}/clion-${clion_vision}.tar.gz"
tar -xzvf "${download_dir}/pycharm-${pycharm_vision}.tar.gz"

sudo mv "${download_dir}/clion-${clion_vision}" /opt/
sudo mv "${download_dir}/pycharm-2023.1.3" /opt/

echo "export PATH=/opt/clion-${clion_vision}/bin\${PATH:+:\${PATH}}" > ~/.bashrc
echo "export PATH=/opt/pycharm-${pycharm_vision}/bin\${PATH:+:\${PATH}}" > ~/.bashrc

rm -rf ${download_dir}
