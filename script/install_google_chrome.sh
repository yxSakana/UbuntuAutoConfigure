#!/bin/bash

. script/lib/log.sh

log_info "Downloading Goole-Chrome..."

wget -O ~/Downloads/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
echo %{PWD} | sudo -S dpkg -i ~/Downloads/google-chrome.deb
rm ~/Downloads/google-chrome.deb

log_info "Goole-Chrome Finshed!"
