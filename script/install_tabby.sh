#!/bin/bash

TABBY_SRC="https://github.com/Eugeny/tabby/releases/download/v1.0.223/tabby-1.0.223-linux-x64.deb"
wget -O /tmp/tabby.deb ${TABBY_SRC}
echo %{PWD} | sudo -S dpkg -i /tmp/tabby.deb
