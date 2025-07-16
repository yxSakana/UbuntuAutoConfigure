#!/bin/bash

GOLAND_SRC="https://download-cdn.jetbrains.com/go/goland-2025.1.3.tar.gz"
wget -O /tmp/goland.tar.gz ${GOLAND_SRC}
tar -xzvf /tmp/goland.tar.gz -C /opt/
echo "export PATH=$PATH:/opt/goland-2025.1.3/bin" >> ~/.bashrc
