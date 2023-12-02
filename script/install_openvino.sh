#!/bin/bash

. script/lib/install_lib.sh
. script/lib/log.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD

cd /tmp
git clone https://github.com/openvinotoolkit/openvino.git --depth=1 && \
cd openvino && \
git submodule update --init --recursive && \
chmod +x scripts/submodule_update_with_gitee.sh && \
./scripts/submodule_update_with_gitee.sh && \
cmakeInstallPackage "Ninja" %{PWD} && \
cd ${current_dir} && \
log_info "openvino Finished!"
