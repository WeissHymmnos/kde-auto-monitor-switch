# kde-auto-monitor-switch

🚀 **适用于 KDE Plasma（X11 & Wayland）的外接显示器即插即用自动切换工具**

当连接外接显示器时，自动关闭笔记本内建屏幕（`eDP`），并将外接屏幕设为主屏幕；当断开外接显示器时，自动重新唤醒并点亮笔记本内建屏幕。

---

## ✨ 特性 (Features)

- **完全自动化**：无需每次手动切换显示模式或按快捷键。
- **即插即用**：内核 DRM 级别监听，插拔外接屏幕后 1 秒内自动完成切换。
- **无需 Root / Sudo 权限**：基于 `systemd --user` 用户级服务和 KDE 原生 `kscreen-doctor`，不修改任何系统根目录。
- **双协议兼容**：支持 KDE Plasma 5 与 Plasma 6，同时兼容 X11 和 Wayland 会话。
- **开箱即用一键安装**：提供一键安装与彻底卸载脚本。

---

## 📦 依赖 (Dependencies)

- **桌面环境**：KDE Plasma 5 / 6 (`kscreen-doctor`)
- **Python**：Python 3.6+（无需安装任何外部 pip 依赖，纯标准库）
- **初始化系统**：systemd (`systemctl --user`)

在 openSUSE、Arch Linux、Fedora、Debian/Ubuntu 等 Linux 发行版的 KDE 环境下默认均已满足。

---

## 🛠️ 安装与使用 (Installation)

### 1. 一键安装

克隆仓库并运行安装脚本：

```bash
git clone https://github.com/WeissHymmnos/kde-auto-monitor-switch.git
cd kde-auto-monitor-switch
chmod +x install.sh
./install.sh
```

脚本将自动执行以下操作：
1. 安装脚本至 `~/.local/bin/auto-monitor-switch.py`
2. 配置 systemd 用户服务至 `~/.config/systemd/user/auto-monitor-switch.service`
3. 立即启动服务并加入桌面登录自启

---

## 🔍 管理与调试 (Management)

- **查看当前后台服务运行状态**：
  ```bash
  systemctl --user status auto-monitor-switch.service
  ```

- **查看实时热插拔事件切换日志**：
  ```bash
  journalctl --user -u auto-monitor-switch.service -f
  ```

- **单次手动触发检测**：
  ```bash
  ~/.local/bin/auto-monitor-switch.py --once
  ```

- **查看当前屏幕识别状态**：
  ```bash
  ~/.local/bin/auto-monitor-switch.py --status
  ```

---

## 🗑️ 卸载 (Uninstallation)

如需彻底移除该服务及相关脚本，运行：

```bash
cd kde-auto-monitor-switch
./uninstall.sh
```

---

## 📄 开源许可 (License)

[MIT License](LICENSE)
