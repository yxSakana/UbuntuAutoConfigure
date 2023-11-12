#!/bin/bash

. script/lib/log.sh
. script/cmake_install_package.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD

cd /tmp
git clone https://github.com/openvinotoolkit/openvino.git --depth=1 && \
cd openvino && \
git submodule update --init --recursive && \
chmod +x scripts/submodule_update_with_gitee.sh && \
./scripts/submodule_update_with_gitee.sh && \
cmakeInstallPackage "Ninja" && \
cd ${current_dir} && \
log_info "openvino Finished!"
