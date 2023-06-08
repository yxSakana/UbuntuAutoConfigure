#!/bin/bash
# @brief: install typora
# @time: 2023-6-7 13:00

echo "typora installing..."

typora_file_path=$1

# install rar unrar
sudo apt install rar unrar
# unrar
mkdir typora
unrar e "${typora_file_path}" -d typora
# install
sudo dpkg -i typora/typora_1.2.4_amd64.deb
# replace asar
sudo cp typora/app.asar /usr/share/typora/resources
# rm tmp
rm -rf typora

echo "typora install finished!"
