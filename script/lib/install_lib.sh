#!/bin/bash

if [ ! -v __INSTALL_LIB_SH__ ]; then
  . script/lib/log.sh

  # @param: generator: 生成器名称(define: Unix Makefiles)
  # @param: sudo_password:
  cmakeInstallPackage() {
    if [[ $# == 0 ]]; then
      cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --build build --target install -j$(nproc)
    elif [[ $# == 1 ]]; then
      generator=$1
      cmake -B build -G ${generator} -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --build build --target install -j$(nproc)
    elif [[ $# == 2 ]]; then
      generator=$1
      sudo_password=$2
      cmake -B build -G ${generator} -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && echo ${sudo_password} | sudo -S cmake --build build --target install -j$(nproc)
    fi
  }

  # @param: name: install library name
  # @param: is_need_proxy:
  # @param: sudo password
  installLibraryFromGithub() {
    local proxy_url="https://ghproxy.com/"
    local current_dir=$PWD
    local git_repositories_url=$1
    local is_need_proxy=$2
    local sudo_password=$3
    local pattern='s/.*\/\([^/]*\)\.git/\1/'
    local name=$(echo "${git_repositories_url}" | sed -n 's/.*\/\([^/]*\)\.git/\1/p')

    cd /tmp
    if [ ! -e ${name} ]; then
      if [[ ${is_need_proxy} == "true" ]]; then
        git clone ${proxy_url}"${git_repositories_url}" --depth=1
      else
        git clone ${git_repositories_url} --depth=1
      fi
    fi
    cd ${name} && cmakeInstallPackage "Ninja" ${sudo_password} && \
    cd ${current_dir} && \
    log_info "${name} Finished!"
  }

  # @brief: 安装多个 Github 库
  # @param: List of library names
  # @param: need proxy
  # @param: sudo password
  installLibrariesFromGithub() {
    local library_names=($1)
    local is_need_proxy=$2
    local password=$3

    log_debug "library names: ${library_names[*]}"
    log_debug "is need proxy: ${is_need_proxy}"
#    log_debug "password: ${password}"

    for library_name in ${library_names[*]}; do
      log_debug "current library name: ${library_name}"
      installLibraryFromGithub ${library_name} ${is_need_proxy} ${password}
    done
  }
fi