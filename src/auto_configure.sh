#!/bin/bash
# @brief: 自动配置Ubuntu环境

. install/installer_init.sh
. install/time_synchronization.sh
. install/installer_python.sh
. install/install_google_chrome.sh
. install/installer_qt_opencv_depend.sh
. install/install_clion_pycharm.sh

chmod +x install/compile_install*.sh

echo "finished!"
echo "reboot ing..."

sleep 2

reboot
