#!/bin/bash
# @brief: install typora
# @time: 2023-6-7 13:00

. script/color_config.sh

echo "typora installing..."

# install rar unrar
echo %{PWD} | sudo -S apt install -y rar unrar
# unrar
git clone https://github.com/yxVision/typora_1.2.4_Linux.git
mkdir typora
unrar e "typora_1.2.4_Linux" -d typora
# install
echo %{PWD} | sudo -S dpkg -i typora/typora_1.2.4_amd64.deb
# replace asar
echo %{PWD} | sudo -S cp typora/app.asar /usr/share/typora/resources
# rm tmp
rm -rf typora

echo "typora install finished!"
