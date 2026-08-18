#!/bin/bash

. script/lib/log.sh

log_info "installing neovim..."

sudo -v
git clone -b v0.11.3 --depth 1 https://github.com/neovim/neovim.git /tmp/neovim
pushd /tmp/neovim && make CMAKE_BUILD_TYPE=Release && sudo make install

# lazy vim
git clone https://github.com/LazyVim/starter ~/.config/nvim

popd
log_info "neovim compile!"
