#!/bin/bash
# @brief: 自动配置Ubuntu环境

. installer-init.sh
. installer-python.sh
. time-synchronization.sh
. installer-typora.sh
. installer-qt_opencv-depend.sh

chmod +x compile_install.sh

echo "finished!"
echo "reboot ing..."

sleep 2

reboot
