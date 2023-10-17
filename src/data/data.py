# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file data.py
  @brief 
 
  @author yx 
  @date 2023-09-24 16:47
"""

NEED_FILE_PATH = ["Realsense", "spdlog", "kdrobotcpplibs"]

MUST_NEED_FILE_PATH = ["kdrobotcpplibs"]
OPTION_MAP_CMD = {
    "x86_64": {
        "necessary depend": "run/installer_init.sh",
        "time synchronization": "run/time_synchronization.sh",
        "google chrome": "run/install_google_chrome.sh",
        "python depend": "run/installer_python.sh",
        "Qt&OpenCV depend": "run/installer_qt_opencv_depend.sh",
        "Clion": "run/install_clion.sh",
        "PyCharm": "run/install_pycharm.sh",
        "spdlog": "run/install_spdlog.sh",
        "Realsense": "run/install_realsense.sh",
        "OpenCV": "run/install_opencv_package.sh",
        "kdrobotcpplibs": "run/install_kdrobotcpplibs.sh",
        "OpenVINO": "run/install_openvino.sh",
        "fmt": "run/install_fmt.sh",
        "glog": "run/install_glog.sh",
        "gtest": "run/install_gtest.sh",
        "matplotlib-cpp": "run/install_matplotlib.sh",
        "yaml-cpp": "run/install_yaml_cpp.sh",
        "ceres_solver": "run/install_ceres_solver.sh",
        "reboot": "reboot"
    },
    "aarch64": {
        "necessary depend": "run/installer_init.sh",
        "python depend": "run/installer_python.sh",
        "Qt&OpenCV depend": "run/installer_qt_opencv_depend.sh",
        "Qt(aarch)": "run/install_aarch_qt.sh",
        "Clion": "run/install_clion.sh",
        "PyCharm": "run/install_pycharm.sh",
        "spdlog": "run/install_spdlog.sh",
        "Realsense": "run/install_realsense.sh",
        "OpenCV": "run/install_opencv_package.sh",
        "kdrobotcpplibs": "run/install_kdrobotcpplibs.sh",
        "OpenVINO": "run/install_openvino.sh",
        "fmt": "run/install_fmt.sh",
        "glog": "run/install_glog.sh",
        "gtest": "run/install_gtest.sh",
        "matplotlib-cpp": "run/install_matplotlib.sh",
        "yaml-cpp": "run/install_yaml_cpp.sh",
        "ceres_solver": "run/install_ceres_solver.sh",
        "reboot": "reboot"
    }
}

