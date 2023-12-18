# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file data.py
  @brief 
 
  @author yx 
  @date 2023-09-24 16:47
"""

from typing import Dict, List

InstallGithubRepositoriesLibraryScript: str = "install_github_repositories_library.sh"

NeedFilePath: List = []

MustNeedFilePath: List = []

GithubRepositories: Dict = {
    "fmt": "https://github.com/fmtlib/fmt.git",
    "glog": "https://github.com/google/glog.git",
    "gtest": "https://github.com/google/googletest.git",
    "yaml-cpp": "https://github.com/jbeder/yaml-cpp.git",
    "matplotlib-cpp": "https://github.com/lava/matplotlib-cpp.git",
    "ceres_solver": "https://github.com/ceres-solver/ceres-solver.git",
    "nlohmann-json": "https://github.com/nlohmann/json.git",
    "cpp-httplib": "https://github.com/yhirose/cpp-httplib.git",
    "kdrobotcpplibs": "https://github.com/LX050724/KdrobotCppLibs.git"
}
RunScript: Dict = {
    "x86_64": {
        "necessary depend": "installer_init.sh",
        "time synchronization": "time_synchronization.sh",
        "google chrome": "install_google_chrome.sh",
        "python depend": "installer_python.sh",
        "Qt&OpenCV depend": "installer_qt_opencv_depend.sh",
        "Clion": "install_clion.sh",
        "PyCharm": "install_pycharm.sh",
        "cmake-3.27.7": "install_cmake_3.27.sh",
        "spdlog": "install_spdlog.sh",
        "Realsense": "install_realsense.sh",
        "OpenCV": "install_opencv_package.sh",
        "kdrobotcpplibs": "install_kdrobotcpplibs.sh",
        "hikCamera": "install_hikcamera_x86.sh",
        "gflags": "install_gflags.sh",
        "OpenVINO": "install_openvino.sh",
    },
    "aarch64": {
        "necessary depend": "installer_init.sh",
        "python depend": "installer_python.sh",
        "Qt&OpenCV depend": "installer_qt_opencv_depend.sh",
        "Qt(aarch)": "install_aarch_qt.sh",
        "Clion": "install_clion.sh",
        "PyCharm": "install_pycharm.sh",
        "cmake-3.27.7": "install_cmake_3.27.sh",
        "spdlog": "install_spdlog.sh",
        "Realsense": "install_realsense.sh",
        "OpenCV": "install_opencv_package.sh",
        "kdrobotcpplibs": "install_kdrobotcpplibs.sh",
        "gflags": "install_gflags.sh",
        "OpenVINO": "install_openvino.sh",
    }
}

SupportOptions: Dict = {
    "x86_64":  list(RunScript["x86_64"].keys()) + list(GithubRepositories.keys()),
    "aarch64": list(RunScript["aarch64"].keys()) + list(GithubRepositories.keys()),
}
