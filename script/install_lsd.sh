#!/bin/bash

. script/lib/log.sh

log_info "installing lsd..."

sudo -v
LSD_SRC="https://github.com/lsd-rs/lsd/releases/download/v1.1.5/lsd_1.1.5_amd64.deb"
wget -O /tmp/lsd.deb ${LSD_SRC}
sudo dpkg -i /tmp/lsd.deb

log_info "lsd compile!"
