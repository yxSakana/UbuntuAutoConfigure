#!/bin/bash

GOLANG_SRC="https://dl.google.com/go/go1.24.5.linux-amd64.tar.gz"
wget -O /tmp/go.tar.gz ${GOLANG_SRC}
tar -xzvf /tmp/go.tar.gz -C /usr/local
echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
