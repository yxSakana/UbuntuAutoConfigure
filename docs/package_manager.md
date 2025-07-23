# Ubuntu Auto Configure - Package Manager

一个现代化的包管理器，支持多种安装方式，用于自动化安装最新版本的软件包。

## 特性

- **多种安装方式支持**：
  - GitHub deb包下载安装
  - GitHub源码编译安装
  - 安装脚本执行
  - 系统包管理器（apt、snap、flatpak）
  - 自定义脚本执行

- **自动化处理**：
  - 自动获取GitHub最新版本
  - 自动化处理交互式安装脚本
  - 依赖管理
  - 安装验证

- **用户友好**：
  - 图形界面（GUI）
  - 命令行界面（CLI）
  - 安装脚本生成
  - 详细的日志记录

## 安装

### 依赖要求

```bash
# 基本依赖
sudo apt install -y python3 python3-pip python3-tk

# 可选依赖（用于某些包的安装）
sudo apt install -y wget curl git build-essential
```

### 运行

```bash
# 克隆项目
git clone <repository-url>
cd UbuntuAutoConfigure

# 图形界面
python3 src/modern_app.py

# 命令行界面
python3 src/cli_app.py --help
```

## 使用方法

### 图形界面（GUI）

1. 运行 `python3 src/modern_app.py`
2. 在"Package Selection"标签页中选择要安装的软件包
3. 点击"Install Selected"开始安装
4. 输入sudo密码
5. 在"Installation Log"标签页查看安装进度和日志

### 命令行界面（CLI）

#### 列出所有可用包

```bash
python3 src/cli_app.py list
```

#### 查看包信息

```bash
python3 src/cli_app.py info bat
python3 src/cli_app.py info bat starship neovim
```

#### 安装包

```bash
# 交互式安装
python3 src/cli_app.py install bat starship

# 生成安装脚本
python3 src/cli_app.py install --script bat starship lsd
```

#### 查看系统信息

```bash
python3 src/cli_app.py system-info
```

## 支持的软件包

### 开发工具

- **bat**: cat命令的现代替代品，支持语法高亮
- **starship**: 跨shell的提示符
- **neovim**: 现代化的Vim编辑器
- **golang**: Go编程语言
- **rust**: Rust编程语言
- **nodejs**: Node.js JavaScript运行时

### 系统工具

- **btop**: 资源监控工具
- **lsd**: ls命令的现代替代品
- **htop**: 交互式进程查看器
- **tree**: 目录树显示工具

### 应用程序

- **docker**: 容器平台
- **code**: Visual Studio Code编辑器
- **firefox**: Firefox浏览器
- **chromium**: Chromium浏览器
- **vlc**: VLC媒体播放器
- **gimp**: GIMP图像编辑器

## 配置文件

### 包配置格式

包配置使用JSON格式，示例：

```json
{
  "name": "bat",
  "display_name": "bat (cat clone)",
  "description": "A cat clone with syntax highlighting and Git integration",
  "install_method": "github_deb",
  "github_repo": "sharkdp/bat",
  "github_asset_pattern": "*amd64.deb",
  "verify_command": "bat --version",
  "supported_architectures": ["x86_64", "aarch64"]
}
```

### 安装方法

#### 1. GitHub DEB包安装 (`github_deb`)

```json
{
  "install_method": "github_deb",
  "github_repo": "owner/repo",
  "github_asset_pattern": "*amd64.deb"
}
```

#### 2. GitHub源码编译 (`github_source`)

```json
{
  "install_method": "github_source",
  "github_repo": "owner/repo",
  "dependencies": ["build-essential", "cmake"],
  "build_commands": [
    "git clone https://github.com/owner/repo.git /tmp/repo",
    "cd /tmp/repo && make",
    "cd /tmp/repo && sudo make install"
  ]
}
```

#### 3. 安装脚本执行 (`script_url`)

```json
{
  "install_method": "script_url",
  "script_url": "https://example.com/install.sh",
  "script_inputs": ["y", "1", ""]
}
```

#### 4. 系统包管理器 (`apt`, `snap`, `flatpak`)

```json
{
  "install_method": "apt",
  "package_name": "package-name"
}
```

#### 5. 自定义脚本 (`custom_script`)

```json
{
  "install_method": "custom_script",
  "custom_script_path": "script/install_custom.sh"
}
```

### 添加新包

1. 在 `src/package_manager/configs/` 目录下创建JSON配置文件
2. 或者在代码中使用 `PackageConfigManager.add_package()` 方法

## 自动化输入处理

对于需要用户交互的安装脚本，包管理器提供自动化输入处理：

```json
{
  "script_inputs": [
    "y",           // 确认安装
    "1",           // 选择选项1
    "",            // 按回车继续
    "/opt/app"     // 输入安装路径
  ]
}
```

## 高级功能

### 自定义GitHub API Token

```python
from package_manager.github_api import GitHubAPI

api = GitHubAPI(token="your_github_token")
```

### 自定义配置目录

```python
from package_manager import PackageManager

manager = PackageManager(config_dir="/path/to/configs")
```

### 进度监控

```python
from package_manager.automation import ProgressMonitor

def progress_callback(message):
    print(f"Progress: {message}")

monitor = ProgressMonitor(callback=progress_callback)
```

## 故障排除

### 常见问题

1. **GitHub API限制**
   - 使用GitHub Token提高API限制
   - 检查网络连接

2. **权限问题**
   - 确保sudo密码正确
   - 检查文件权限

3. **依赖问题**
   - 更新包列表：`sudo apt update`
   - 安装缺失的依赖

4. **网络问题**
   - 检查防火墙设置
   - 使用代理（如需要）

### 日志文件

- 应用程序日志：`package_manager.log`
- 详细调试：使用 `--verbose` 参数

### 测试

运行测试套件：

```bash
python3 test/test_package_manager.py
```

## 扩展开发

### 添加新的安装方法

1. 在 `src/package_manager/installers/` 目录下创建新的安装器类
2. 继承 `BaseInstaller` 类
3. 实现 `install()` 方法
4. 在 `PackageManager` 中注册新的安装方法

### 示例：自定义安装器

```python
from .base import BaseInstaller, InstallResult, InstallStatus

class CustomInstaller(BaseInstaller):
    def install(self, config):
        # 实现自定义安装逻辑
        return InstallResult(
            status=InstallStatus.SUCCESS,
            message="Installation completed"
        )
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。
