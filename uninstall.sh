#!/usr/bin/env bash
set -e

echo "==> 正在卸载 kde-auto-monitor-switch..."

systemctl --user disable --now auto-monitor-switch.service 2>/dev/null || true
rm -f "$HOME/.config/systemd/user/auto-monitor-switch.service"
rm -f "$HOME/.local/bin/auto-monitor-switch.py"

systemctl --user daemon-reload

echo "==> 卸载完成。服务与脚本已彻底移除。"
