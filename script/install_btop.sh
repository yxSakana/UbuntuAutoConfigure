#!/bin/bash

. script/lib/log.sh

log_info "installing btop..."

git clone -b v1.4.4 --depth 1 https://github.com/aristocratos/btop.git /tmp/btop
cd /tmp/btop && make && echo %{PWD} | sudo -S make install

log_info "btop compile!"
