#!/bin/bash

BAT_SRC="https://github.com/sharkdp/bat/releases/download/v0.25.0/bat_0.25.0_amd64.deb"
wget -O /tmp/bat.deb ${BAT_SRC}
echo %{PWD} | sudo -S dpkg -i /tmp/bat.deb
