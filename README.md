# FastFileServer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-brightgreen)](https://www.python.org/downloads/)

FastFileServer 是一个基于 Python 的轻量级高速文件传输服务器，提供直观的 Web 界面，支持所有 Linux 发行版（包括 ARM 架构），使文件共享变得简单高效。

![FastFileServer 预览](https://github.com/yourusername/fastfileserver/raw/main/preview.png)

## ✨ 功能特点

- **跨平台兼容性**：适用于所有主流 Linux 发行版，包括 ARM 架构
- **高速文件传输**：采用分块传输和多线程处理，显著提升传输效率
- **优雅的 Web 界面**：现代化设计的 UI，支持文件上传和下载
- **零依赖**：仅使用 Python 标准库，无需安装外部依赖
- **即开即用**：最小化配置，快速启动服务
- **自适应设计**：在桌面和移动设备上均可正常运行

## 📋 系统要求

- Python 3.6 或更高版本
- 支持的操作系统：
  - Linux（所有主要发行版）
  - macOS
  - Windows（虽然主要针对 Linux，但也兼容 Windows）

## 🚀 快速开始

### 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/fastfileserver.git
cd fastfileserver
```
2. 确保拥有执行权限：

```bash
chmod +x file_server.py
```
### 运行服务器

```bash
python3 file_server.py
```
服务器将在默认端口 55673 启动。你可以通过以下地址访问：
```bash
http://localhost:55673/
```
或者使用服务器的 IP 地址从网络中的其他设备访问。

## ⚙️ 配置选项
服务器的主要配置参数位于脚本顶部：
```bash
# 配置参数
PORT = 55673          # Web 服务器监听端口
UPLOAD_DIR = "uploads"  # 上传目录的名称
CHUNK_SIZE = 1024 * 1024  # 文件传输块大小 (1MB)
```

要自定义这些设置，只需编辑脚本中的相应值。

## 🖥️ 界面预览
FastFileServer 提供了一个现代化、直观的用户界面，具有以下特点：

清晰的文件列表视图
直观的上传按钮
每个文件的大小信息
响应式设计，适应不同屏幕尺寸
平滑过渡动画
视觉反馈的交互元素

## 🔧 进阶使用
更改端口
如果你想使用不同的端口，修改脚本中的 PORT 变量：
```bash
PORT = 8080  # 修改为你想要的端口

```
### 自定义上传目录
默认情况下，文件将上传到与脚本相同目录下的 uploads 文件夹中。要更改此设置：
```bash
UPLOAD_DIR = "/path/to/your/directory"  # 更改为你想要的目录路径

```
### 作为系统服务运行
要将 FastFileServer 设置为系统服务，创建以下 systemd 服务文件：
```bash
[Unit]
Description=FastFileServer
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/file_server.py
WorkingDirectory=/path/to/directory
Restart=always
User=yourusername

[Install]
WantedBy=multi-user.target
```
保存为 /etc/systemd/system/fastfileserver.service，然后运行：
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastfileserver
sudo systemctl start fastfileserver
```
## 🔒 安全注意事项

FastFileServer 旨在用于本地网络或受信任的环境。如果你需要通过互联网提供服务，请考虑以下安全措施：

- 在 Nginx 或 Apache 后面设置反向代理
- 实施 HTTPS
- 添加基本的身份验证
- 配置适当的防火墙规则

## ❓ 常见问题

**Q: 如何增加上传文件的大小限制？**

A: FastFileServer 使用 Python 的标准库处理上传，没有明确的大小限制。然而，非常大的文件可能会受到系统内存的限制。

**Q: 是否支持文件夹上传？**

A: 目前版本仅支持文件上传。文件夹上传功能可能会在未来版本中添加。

**Q: 如何删除文件？**

A: 当前版本不支持通过 Web 界面删除文件。你可以通过直接删除 `uploads` 目录中的文件来移除它们。

## 🤝 贡献

欢迎贡献！如果你有改进建议或问题报告：

1. Fork 该项目
2. 创建你的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目基于 MIT 许可证发布 - 详细信息请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢所有开源社区的贡献者
- 受到 SimpleHTTPServer 和现代 Web 文件共享工具的启发


开发者 © 2025
