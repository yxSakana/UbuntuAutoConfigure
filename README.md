# illustrate

Ubuntu 自动化环境配置

目前支持自动配置
- x86
  - 自动安装 git、gcc、g++、vim、cmake、cmake-gui等
  - 双系统时间同步
  - 安装 `Google Chrome`
  - 下载 `python`依赖
  - 下载 `Qt && OpenCV` 依赖
  - 下载 `Clion`
  - 下载 `PyCharm`
  - 安装 `Realsense`
  - 安装 `spdlog`
  - 下载 `OpenCV` 包 (自动调换代理)
  - 安装 `KdrobotCppLibs`
  - `hikCamera`
  - `OpenVINO`
  - `fmt`
  - `gflags`
  - `glog`
  - `gtest`
  - `matplotlib-cpp`
  - `yaml-cpp`
  - `ceres_solver`
  - `nlohmann-json`
  - `cpp-httplib`
- aarch
  - 自动安装 git、gcc、g++、vim、cmake、cmake-gui等
  - 下载 `python`依赖
  - 下载 `Qt && OpenCV` 依赖
  - 安装 `Qt`
  - 安装 `Clion`
  - 安装 `PyCharm`
  - 安装 `Realsense`
  - 安装 `spdlog`
  - 下载 `OpenCV` 包 (自动调换代理)
  - 安装 `KdrobotCppLibs`
  - `hikCamera`
  - `OpenVINO`
  - `fmt`
  - `gflags`
  - `glog`
  - `gtest`
  - `matplotlib-cpp`
  - `yaml-cpp`
  - `ceres_solver`
  - `nlohmann-json`
  - `cpp-httplib`

对于后方有`select`选项的，可以提供库的源代码所在的目录(可选)

# Usage

如果没有 `python3-tk` 需要下载
```shell
sudo apt install -y python3-tk
```

```shell
src/app.py  # 运行程序
```

执行 python 脚本后

- 如果勾选 `在python脚本中执行` 那么在点击 `Run` 之后会在这个脚本中执行(不建议)

- 如果不勾选那么会生成一个 `auto_config.sh` 文件, 运行 `./auto_config.sh` 即可执行预期命令

# 关于可扩展性

只需要在 `src/data/data.py` 中的字典中添加对应 `key-value` 即可(`key`为图形界面显示的名称, `value`是具体执行的脚本, 脚本添加在`script/<name>.sh`, 具体的`value`为`run/<name>.sh`)

# 安装完成后的测试

测试代码全部在`test`文件夹内, 涵盖了`Qt`、`OpenCV`、`spdlog`、`Realsense2`、`kdlib`, 如果初次接触某库可起到一定参考作用

```shell
chmod +x script/compile/*.sh

script/compile/test.sh  # test for all
script/compile/test_spdlog.sh  # test for spdlog
script/compile/test_realsense2.sh  # test for realsense2
script/compile/test_qt.sh  # test for qt
script/compile/test_opencv.sh  # test for opencv
script/compile/test_kdlib.sh  # test for KdRobotCppLibs
```
