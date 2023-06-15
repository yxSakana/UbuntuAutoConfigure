自动配置Ubuntu环境(简易)

运行auto_configure.sh即可

```shell
chmod +x auto_configure.sh
./auto_configure.sh
```

auto_configure.sh 脚本可以完成
1. 下载必要依赖(git cmake g++等)并且会自动安装google chrome
2. 下载python依赖
3. 双系统时间同步
4. Qt && opencv 依赖
5. 下载Clion && Pycharm
6. 在所有命令执行完成之后会进行重启`reboot`


其余脚本

`auto-copy.sh` 自动复制U盘中的文件，包括kdrobotcpplibs opencv typora 并解压, 会自动安装typora

`compile_install.sh` 编译安装 Realsense && Spdlog

`compile-install-kdrobotcpplibs.sh` 提供第二个参数-->队库路径 编译安装 KdrobotCppLibs
