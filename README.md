# Ubuntu Auto Configure

Ubuntu 自动化环境配置工具，现在包含现代化的包管理器！

## 🚀 新功能：现代化包管理器

我们全新开发了一个现代化的包管理器，支持多种安装方式，能够自动获取最新版本的软件包。

### ✨ 主要特性

- **多种安装方式**：
  - 🐙 GitHub deb包自动下载安装
  - 🔨 GitHub源码自动编译安装
  - 📜 安装脚本自动执行
  - 📦 系统包管理器（apt、snap、flatpak）
  - 🛠️ 自定义脚本执行

- **智能自动化**：
  - 🔄 自动获取GitHub最新版本
  - 🤖 自动化处理交互式安装
  - 📋 依赖管理和验证
  - ✅ 安装状态检查

- **用户友好界面**：
  - 🖥️ 现代化图形界面（GUI）
  - ⌨️ 强大的命令行界面（CLI）
  - 📄 安装脚本生成
  - 📊 详细的安装日志

### 🎯 支持的软件包

#### 开发工具
- **bat**: cat命令的现代替代品，支持语法高亮
- **starship**: 跨shell的美观提示符
- **neovim**: 现代化的Vim编辑器
- **golang**: Go编程语言
- **rust**: Rust编程语言
- **nodejs**: Node.js JavaScript运行时

#### 系统工具
- **btop**: 现代化资源监控工具
- **lsd**: ls命令的现代替代品
- **htop**: 交互式进程查看器
- **tree**: 目录树显示工具

#### 应用程序
- **docker**: 容器平台
- **code**: Visual Studio Code编辑器
- **firefox**: Firefox浏览器
- **vlc**: VLC媒体播放器
- **gimp**: GIMP图像编辑器

## 🚀 快速开始

### 安装依赖

```bash
sudo apt install -y python3 python3-pip python3-tk wget curl git
```

### 使用方法

#### 图形界面（推荐）
```bash
python3 src/modern_app.py
```

#### 命令行界面
```bash
# 列出所有可用包
python3 src/cli_app.py list

# 查看包信息
python3 src/cli_app.py info bat starship

# 安装包
python3 src/cli_app.py install bat starship neovim

# 生成安装脚本
python3 src/cli_app.py install --script bat lsd btop
```

## 📚 传统功能

原有的Ubuntu自动化配置功能依然可用：

### 支持的传统安装项目

#### x86_64 架构
- 自动安装 git、gcc、g++、vim、cmake、cmake-gui等
- 双系统时间同步
- 安装 `Google Chrome`
- 下载 `python`依赖
- 下载 `Qt && OpenCV` 依赖
- 下载 `Clion`、`PyCharm`
- 安装 `Realsense`、`spdlog`
- 下载 `OpenCV` 包 (自动调换代理)
- 安装 `KdrobotCppLibs`
- `hikCamera`、`OpenVINO`
- C++库：`fmt`、`gflags`、`glog`、`gtest`、`matplotlib-cpp`、`yaml-cpp`、`ceres_solver`、`nlohmann-json`、`cpp-httplib`

#### aarch64 架构
- 基本开发环境配置
- Qt和OpenCV环境
- 各种C++开发库

### 传统界面使用方法

```bash
# 安装GUI依赖
sudo apt install -y python3-tk

# 运行传统界面
python3 src/app.py
```

执行后可以选择：
- 勾选 `在python脚本中执行`：直接在脚本中执行（不推荐）
- 不勾选：生成 `auto_config.sh` 文件，然后运行 `./auto_config.sh`

## 🔧 扩展开发

### 添加新的软件包

1. **使用配置文件**（推荐）：
   在 `src/package_manager/configs/` 目录下创建JSON配置文件

2. **编程方式**：
   ```python
   from package_manager import PackageManager, PackageConfig, InstallMethod

   config = PackageConfig(
       name="my_tool",
       display_name="My Tool",
       install_method=InstallMethod.GITHUB_DEB,
       github_repo="owner/repo",
       github_asset_pattern="*.deb"
   )

   manager = PackageManager()
   manager.add_package_config(config)
   ```

3. **传统方式**：
   在 `src/data/data.py` 中添加配置

### 自定义安装器

可以创建自定义安装器来支持特殊的安装需求：

```python
from package_manager.installers.base import BaseInstaller, InstallResult

class MyCustomInstaller(BaseInstaller):
    def install(self, config):
        # 实现自定义安装逻辑
        return InstallResult(...)
```

## 🧪 测试

### 包管理器测试
```bash
python3 test/test_package_manager.py
```

### 传统功能测试
测试代码在`test`文件夹内，涵盖了`Qt`、`OpenCV`、`spdlog`、`Realsense2`、`kdlib`：

```bash
chmod +x script/compile/*.sh

script/compile/test.sh  # 测试所有
script/compile/test_spdlog.sh  # 测试spdlog
script/compile/test_realsense2.sh  # 测试realsense2
script/compile/test_qt.sh  # 测试qt
script/compile/test_opencv.sh  # 测试opencv
script/compile/test_kdlib.sh  # 测试KdRobotCppLibs
```

## 📖 文档

- [包管理器详细文档](docs/package_manager.md)
- [使用示例](examples/example_usage.py)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License
