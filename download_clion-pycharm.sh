#!/bin/bash

clion_vision="2023.1.3"
pycharm_vision="2023.1.2"
clion_url="https://download.jetbrains.com/cpp/CLion-${clion_vision}.tar.gz"
pycharm_url="https://download.jetbrains.com/python/pycharm-professional-${pycharm_vision}.tar.gz"

download_dir="_tmp"
mkdir -p "${download_dir}"

echo "clion downloading..."

if [ ! -e "${download_dir}/clion-${clion_vision}.tar.gz" ]
then
    wget -O "${download_dir}/clion-${clion_vision}.tar.gz" "${clion_url}"
fi
if [ ! -e "${download_dir}/pycharm-${pycharm_vision}.tar.gz" ]
then
   wget -O "${download_dir}/pycharm-${pycharm_vision}.tar.gz" "${pycharm_url}"
fi

echo "Download finished!"

tar -xzvf "${download_dir}/clion-${clion_vision}.tar.gz"
tar -xzvf "${download_dir}/pycharm-${pycharm_vision}.tar.gz"

sudo mv "clion-${clion_vision}" /opt/
sudo mv "pycharm-${pycharm_vision}" /opt/

echo "export PATH=/opt/clion-${clion_vision}/bin\${PATH:+:\${PATH}}" >> ~/.bashrc
echo "export PATH=/opt/pycharm-${pycharm_vision}/bin\${PATH:+:\${PATH}}" >> ~/.bashrc

rm -rf ${download_dir}
