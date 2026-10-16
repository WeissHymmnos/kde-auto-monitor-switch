#!/usr/bin/env python3
"""
kde-auto-monitor-switch
=======================
Automatically disables laptop internal display when an external monitor is connected,
and re-enables internal display when all external monitors are disconnected.
Designed for KDE Plasma 5 & 6 (Wayland & X11).
"""

import sys
import glob
import json
import time
import shutil
import argparse
import subprocess

def get_drm_state():
    """Read connector connection states directly from sysfs."""
    state = {}
    for path in glob.glob('/sys/class/drm/*/status'):
        try:
            with open(path, 'r') as f:
                state[path] = f.read().strip()
        except Exception:
            pass
    return state

def get_outputs():
    """Retrieve current display status via kscreen-doctor."""
    if not shutil.which('kscreen-doctor'):
        print("[Error] kscreen-doctor command not found. Is KDE Plasma installed?", file=sys.stderr, flush=True)
        return []
    try:
        res = subprocess.run(['kscreen-doctor', '-j'], capture_output=True, text=True, check=True)
        return json.loads(res.stdout).get('outputs', [])
    except Exception as e:
        print(f"[Error] Failed to execute kscreen-doctor: {e}", file=sys.stderr, flush=True)
        return []

def check_and_switch():
    """Evaluate connected monitors and apply the appropriate layout."""
    outputs = get_outputs()
    if not outputs:
        return

    builtin = None
    externals = []

    # Identify built-in laptop panel (eDP, LVDS, DSI)
    for out in outputs:
        name = out.get('name', '')
        conn = out.get('connected', False)
        if conn and name.lower().startswith(('edp', 'lvds', 'dsi')):
            builtin = out
            break

    # Fallback to output type 7 (Panel) if name differs
    if not builtin:
        for out in outputs:
            if out.get('connected', False) and out.get('type') == 7:
                builtin = out
                break

    # Collect connected external displays
    for out in outputs:
        if out.get('connected', False):
            if builtin and out.get('id') == builtin.get('id'):
                continue
            externals.append(out)

    if not builtin:
        print("[Info] No built-in display detected. Skipping switch.", flush=True)
        return

    builtin_name = builtin.get('name')
    builtin_enabled = builtin.get('enabled', False)

    if externals:
        # At least one external display is connected
        any_ext_disabled = any(not ext.get('enabled', False) for ext in externals)
        if builtin_enabled or any_ext_disabled:
            ext_names = [e['name'] for e in externals]
            print(f"[Action] External display connected: {ext_names}. Disabling internal screen {builtin_name}...", flush=True)
            cmd = ['kscreen-doctor', f'output.{builtin_name}.disable']
            for i, ext in enumerate(externals):
                ext_name = ext['name']
                cmd.append(f'output.{ext_name}.enable')
                if i == 0:
                    cmd.append(f'output.{ext_name}.position.0,0')
                    cmd.append(f'output.{ext_name}.primary')
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # No external displays connected
        if not builtin_enabled:
            print(f"[Action] No external display detected. Re-enabling internal screen {builtin_name}...", flush=True)
            cmd = [
                'kscreen-doctor',
                f'output.{builtin_name}.enable',
                f'output.{builtin_name}.position.0,0',
                f'output.{builtin_name}.primary'
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def print_status():
    """Print current monitor statuses."""
    outputs = get_outputs()
    print("=== Current Display Status ===")
    for out in outputs:
        conn = "Connected" if out.get('connected') else "Disconnected"
        enb = "Enabled" if out.get('enabled') else "Disabled"
        prio = out.get('priority', 0)
        print(f"- {out.get('name')}: {conn}, {enb}, Priority={prio}")

def main():
    parser = argparse.ArgumentParser(description="KDE Plasma Auto Monitor Switcher")
    parser.add_argument('--once', action='store_true', help="Check and apply monitor switch once and exit")
    parser.add_argument('--status', action='store_true', help="Show current monitor configuration")
    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.once:
        check_and_switch()
        return

    print("[Start] kde-auto-monitor-switch daemon started.", flush=True)
    check_and_switch()
    last_drm_state = get_drm_state()
    loop_count = 0

    while True:
        time.sleep(1.0)
        loop_count += 1
        current_drm_state = get_drm_state()

        if current_drm_state != last_drm_state:
            print("[Event] DRM connector state changed. Waiting 1s for handshake...", flush=True)
            time.sleep(1.0)
            check_and_switch()
            last_drm_state = get_drm_state()
        elif loop_count >= 15:
            # Periodic alignment check every 15s
            check_and_switch()
            loop_count = 0

if __name__ == '__main__':
    main()
