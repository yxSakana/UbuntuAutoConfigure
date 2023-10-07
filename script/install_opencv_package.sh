#!/bin/bash

. script/color_config.sh

proxy_url="https://ghproxy.com/"
current_dir=$PWD
is_has_opencv="False"
is_has_opencv_contrib="False"

green "Download OpenCV"

cd package
if [ ! -e ${PWD}/opencv ]; then
  git clone ${proxy_url}https://github.com/opencv/opencv.git && is_has_opencv="True"
else
  is_has_opencv="True"
fi

if [ ! -e ${PWD}/opencv_contrib ]; then
  git clone ${proxy_url}https://github.com/opencv/opencv_contrib.git && is_has_opencv_contrib="True"
else
  is_has_opencv_contrib="True"
fi

if [ $is_has_opencv == "True" ] && [ $is_has_opencv_contrib == "True" ]; then
  chmod +x ../src/utils/OpencvProxyRex.py && \
  ../src/utils/OpencvProxyRex.py ${PWD}/opencv ${PWD}/opencv_contrib && \
  green "Download OpenCV Finished!" && cd .. || red "OpenCV Download Failed!"
else
  red "OpenCV Download Failed!(文件异常)"
fi

cd ${current_dir}
