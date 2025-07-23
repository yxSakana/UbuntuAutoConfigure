#!/bin/bash

set -e

. script/lib/log.sh

. script/installer_init.sh
. script/install_nvim.sh
. script/install_lsd.sh
. script/install_starship.sh
. script/install_bat.sh
. script/btop.sh

log_info "installing zsh"
sudo apt install zsh -y
chsh -s /usr/bin/zsh
log_info "zsh compile!"

log_info "installing omz"
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
log_info "omz compile!"

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
