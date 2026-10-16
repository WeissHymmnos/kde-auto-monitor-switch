#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> 正在安装 kde-auto-monitor-switch..."

mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.config/systemd/user"

cp "$SCRIPT_DIR/auto-monitor-switch.py" "$HOME/.local/bin/auto-monitor-switch.py"
chmod +x "$HOME/.local/bin/auto-monitor-switch.py"

cp "$SCRIPT_DIR/auto-monitor-switch.service" "$HOME/.config/systemd/user/auto-monitor-switch.service"

systemctl --user daemon-reload
systemctl --user enable --now auto-monitor-switch.service

echo "==> 安装完成！服务已启用并正在运行。"
echo ""
echo "常用命令："
echo "  - 查看服务状态: systemctl --user status auto-monitor-switch.service"
echo "  - 查看实时日志: journalctl --user -u auto-monitor-switch.service -f"
echo "  - 临时停用服务: systemctl --user stop auto-monitor-switch.service"
echo "  - 卸载该服务:   bash $SCRIPT_DIR/uninstall.sh"
