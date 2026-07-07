# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="re5et"

plugins=(
    git
    aliases
    systemd
    dnote

    # autojump # install: git clone https://github.com/wting/autojump.git && cd autojump && ./install.py

    zsh-syntax-highlighting
    zsh-autosuggestions
)

source $ZSH/oh-my-zsh.sh

source /home/skn/.config/.skn_profile
