#!/bin/bash
# @brief:

. script/color_config.sh
. script/cmake_install_package.sh

installLibraryFromGithub() {
  proxy_url="https://ghproxy.com/"
  current_dir=$PWD
  pattern='s/.*\/\([^/]*\)\.git/\1/'
  name=$1 | sed 's/.*\/\([^/]*\)\.git/\1/'

  cd /tmp && \
  git clone ${proxy_url}"$1" --depth && cd ${name} && cmake_install_package && \
  cd ${current_dir} && \
  green "${name}Finished!"
}
