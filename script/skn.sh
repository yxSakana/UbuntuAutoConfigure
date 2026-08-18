#!/bin/bash

set -e

. script/lib/log.sh

sudo -v

# nvim lsd starship bat btop docker tabby
. script/installer_init.sh

# zsh
log_info "installing zsh"
sudo apt install zsh -y
chsh -s /usr/bin/zsh
log_info "zsh compile!"

# omz
log_info "installing omz"
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
log_info "omz compile!"

# zsh plugin
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
log_info "zsh plugin: 'highlighting' 'autosuggestions' is compile!"

# path
cp ./profile/.alias_profile ${HOME}/.config/
echo 'export PATH=${HOME}/.local/bin${PATH:+:${PATH}}' >> ${HOME}/.config/.skn_profile
echo '# proxy' >> ${HOME}/.config/.skn_profile
echo 'export PROXY_ADDRESS="127.0.0.1:7897"' >> ${HOME}/.config/.skn_profile
echo 'export https_proxy=${PROXY_ADDRESS}' >> ${HOME}/.config/.skn_profile
echo 'export http_proxy=${PROXY_ADDRESS}' >> ${HOME}/.config/.skn_profile
echo 'export HTTP_PROXY=${PROXY_ADDRESS}' >> ${HOME}/.config/.skn_profile
echo 'export HTTPS_PROXY=${PROXY_ADDRESS}' >> ${HOME}/.config/.skn_profile
echo "source ${HOME}/.config/.skn_profile" >> ${HOME}/.zshrc
echo "source ${HOME}/.config/.alias_profile" >> ${HOME}/.zshrc

. script/install_nvim.sh
. script/install_lsd.sh
. script/install_starship.sh
. script/install_bat.sh
. script/install_btop.sh
. script/install_docker_engine.sh
. script/install_tabby.sh

# clangd
sudo apt-get install -y clangd-12
sudo update-alternatives --install /usr/bin/clangd clangd /usr/bin/clangd-12 100

# brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo >> ${HOME}/.zshrc
echo '# brew' >> ${HOME}/.zshrc
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv zsh)"' >> ${HOME}/.zshrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv zsh)"

# fzf
brew install -y fzf

# zoxide
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
echo 'eval "$(zoxide init zsh)"' >> ${HOME}/.zshrc
log_info "zoxide installed"
