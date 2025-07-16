#!/bin/bash

LSD_SRC="https://github.com/lsd-rs/lsd/releases/download/v1.1.5/lsd_1.1.5_amd64.deb"
wget -O /tmp/lsd.deb ${LSD_SRC}
echo %{PWD} | sudo -S dpkg -i /tmp/lsd.deb
