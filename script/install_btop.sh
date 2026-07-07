#!/bin/bash

. script/lib/log.sh

log_info "installing btop..."

sudo -v
git clone -b v1.4.4 --depth 1 https://github.com/aristocratos/btop.git /tmp/btop
cd /tmp/btop && make && sudo make install

log_info "btop compile!"
