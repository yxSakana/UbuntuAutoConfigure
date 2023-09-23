#!/bin/bash
# @brief: install typora
# @time: 2023-6-7 13:00

. ../utils/color_config.sh

echo "typora installing..."

# install rar unrar
sudo apt install -y rar unrar
# unrar
git clone https://github.com/yxVision/typora_1.2.4_Linux.git
mkdir typora
unrar e "typora_1.2.4_Linux" -d typora
# install
sudo dpkg -i typora/typora_1.2.4_amd64.deb
# replace asar
sudo cp typora/app.asar /usr/share/typora/resources
# rm tmp
rm -rf typora

echo "typora install finished!"
