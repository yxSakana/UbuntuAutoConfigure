#!/bin/bash

. script/lib/log.sh

pycharm_vision="2023.1.2"
pycharm_url="https://download.jetbrains.com/python/pycharm-professional-${pycharm_vision}.tar.gz"

download_dir="_tmp"
mkdir -p "${download_dir}"

if [ ! -e "${download_dir}/pycharm-${pycharm_vision}.tar.gz" ]
then
   wget -O "${download_dir}/pycharm-${pycharm_vision}.tar.gz" "${pycharm_url}"
fi

log_info "Download finished!"
log_info "tar -xzvf ..."

tar -xzvf "${download_dir}/pycharm-${pycharm_vision}.tar.gz"

echo %{PWD} | sudo -S mv "pycharm-${pycharm_vision}" /opt/

echo "export PATH=/opt/pycharm-${pycharm_vision}/bin\${PATH:+:\${PATH}}" >> ~/.bashrc

rm -rf ${download_dir}
