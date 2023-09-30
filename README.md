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
  - 安装 `KdrobotCppLibs`
  - 安装完成后是否重启
- aarch
    - 自动安装 git、gcc、g++、vim、cmake、cmake-gui等
    - 下载 `python`依赖
    - 下载 `Qt && OpenCV` 依赖
    - 安装 `Qt`
    - 安装 `Clion`
    - 安装 `PyCharm`
    - 安装 `Realsense`
    - 安装 `spdlog`
    - 安装 `KdrobotCppLibs`
    - 安装完成后是否重启

# Usage

```shell
python3 src/app.py
```

执行 python 脚本后

- 如果勾选 `在python脚本中执行` 那么在点击 `Run` 之后会在这个脚本中执行(不建议)

- 如果不勾选那么会生成一个 `auto_config.sh` 文件, 运行 `./auto_config.sh` 即可执行预期命令

# 关于可扩展性

只需要在 `src/data/data.py` 中的字典中添加对应 `key-value` 即可
