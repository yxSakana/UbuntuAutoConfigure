#!/bin/bash
# @brief:

. script/color_config.sh
. script/cmake_install_package.sh

installLibraryFromGithub() {
  proxy_url="https://ghproxy.com/"
  current_dir=$PWD
  pattern='s/.*\/\([^/]*\)\.git/\1/'
  name=$(echo "$1" | sed -n 's/.*\/\([^/]*\)\.git/\1/p')

  cd /tmp && \
  git clone ${proxy_url}"$1" --depth=1 && cd ${name} && cmakeInstallPackage "Ninja" && \
  cd ${current_dir} && \
  green "${name}Finished!"
}
