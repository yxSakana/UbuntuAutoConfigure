#!/bin/bash

. script/lib/log.sh

log_info "installing bat..."

sudo -v
BAT_SRC="https://github.com/sharkdp/bat/releases/download/v0.25.0/bat_0.25.0_amd64.deb"
wget -O /tmp/bat.deb ${BAT_SRC}
sudo dpkg -i /tmp/bat.deb

log_info "bat compile!"
