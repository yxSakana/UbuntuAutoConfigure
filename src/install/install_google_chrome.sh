#!/bin/bash

. ../utils/color_config.sh

green "Downloading Goole-Chrome..."

wget -O ~/Downloads/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
sudo dpkg -i ~/Downloads/google-chrome.deb
rm ~/Downloads/google-chrome.deb

green "Goole-Chrome Finshed!"
