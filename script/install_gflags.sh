#!/bin/bash

. script/lib/install_lib.sh
. script/lib/log.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD
git_repositories_url="https://github.com/gflags/gflags.git"
pattern='s/.*\/\([^/]*\)\.git/\1/'
name=$(echo "${git_repositories_url}" | sed -n 's/.*\/\([^/]*\)\.git/\1/p')

cd /tmp
if [ ! -e ${name} ]; then
  if [[ ${is_need_proxy} == "true" ]]; then
    git clone ${proxy_url}"${git_repositories_url}" --depth=1
  else
    git clone ${git_repositories_url} --depth=1
  fi
fi

cd gflags && cmake -B build -G "Ninja" -DBUILD_SHARED_LIBS=ON && cmake --build build && echo %{PWD} | sudo -S cmake --build build --target install
cd ${current_dir}
log_info "gflags Finished!"
