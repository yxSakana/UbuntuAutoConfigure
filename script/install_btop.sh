#!/bin/bash

git clone -b v1.4.4 --depth 1 https://github.com/aristocratos/btop.git /tmp/btop
cd /tmp/btop && make && echo %{PWD} | sudo -S make install
