#!/bin/bash

curl -sS https://starship.rs/install.sh | sh

echo eval "$(starship init zsh)" >> ~/.zshrc
echo eval "$(starship init bash)" >> ~/.bashrc

cp ./profile/starship.toml ~/.config/starship.toml

log_info "starship compile!"
