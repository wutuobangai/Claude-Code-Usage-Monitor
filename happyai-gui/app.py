# Claude 额度小助手 · Happy AI
# 我们自己的外壳（不开源许可）；额度数据来自开源项目 Claude-Code-Usage-Monitor（MIT，© 2025 Maciej），
# 通过它官方提供的「--once --output json」只读接口获取，原项目代码未修改。
# 用法：直接双击运行。内部用 `本程序 --engine ...` 调用打包进来的引擎。
import json
import os
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

SITE = 'https://wutuobangai.top/'
UTM = '?utm_source=claude-quota-app&utm_medium=app&utm_campaign=claude-quota-20260923'
LINKS = {
    'site': SITE + UTM + '&utm_content=app-site',
    'claude': SITE + 'tool.html?id=claude-pro-sub&' + UTM[1:] + '&utm_content=app-claude',
    'knowledge': SITE + 'knowledge.html' + UTM + '&utm_content=app-knowledge',
    'source': 'https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor',
}


def run_engine(argv):
    """在打包后的程序里充当 claude-monitor 命令本身。"""
    from claude_monitor.cli.main import main as monitor_main
    sys.argv = ['claude-monitor'] + argv
    code = monitor_main()
    sys.exit(code if isinstance(code, int) else 0)


def engine_cmd():
    if getattr(sys, 'frozen', False):
        return [sys.executable, '--engine']
    return [sys.executable, os.path.abspath(__file__), '--engine']


_ENGINE_LOCK = threading.Lock()


def fetch_snapshot_inprocess():
    """在本进程内调用引擎（Windows 无控制台程序也能拿到输出，不弹黑框）。"""
    import contextlib
    import io
    from claude_monitor.cli.main import main as monitor_main
    buf, err = io.StringIO(), io.StringIO()
    with _ENGINE_LOCK, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        try:
            monitor_main(['--once', '--output', 'json'])
        except SystemExit:
            pass
    text = buf.getvalue().strip()
    start = text.find('{')
    if start < 0:
        return {'error': 'no_data', 'detail': (err.getvalue() or text)[-300:]}
    return json.loads(text[start:])


def fetch_snapshot():
    try:
        return fetch_snapshot_inprocess()
    except Exception:
        pass  # 进程内失败再退回子进程方式
    try:
        out = subprocess.run(engine_cmd() + ['--once', '--output', 'json'],
                             capture_output=True, text=True, timeout=90,
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        text = out.stdout.strip()
        start = text.find('{')
        if start < 0:
            return {'error': 'no_data', 'detail': (out.stderr or text)[-300:]}
        return json.loads(text[start:])
    except Exception as e:  # 引擎异常时给界面一个可读状态，不崩溃
        return {'error': 'engine_failed', 'detail': str(e)[:300]}


def local_time(iso):
    if not iso:
        return None
    try:
        return datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone().strftime('%m-%d %H:%M')
    except Exception:
        return None


def simplify(snap):
    if 'error' in snap:
        return snap
    five = (snap.get('limits') or {}).get('five_hour') or {}
    week = (snap.get('limits') or {}).get('seven_day') or {}
    fc = snap.get('forecast') or {}
    return {
        'five_pct': five.get('used_percentage'),
        'five_used': five.get('tokens_used'),
        'five_limit': five.get('token_limit'),
        'five_reset': local_time(five.get('resets_at')),
        'week_pct': week.get('used_percentage'),
        'week_reset': local_time(week.get('resets_at')),
        'eta': local_time(fc.get('predicted_tokens_exhausted_at')),
        'minutes_left': fc.get('minutes_remaining'),
        'confidence': snap.get('confidence'),
        'status': (snap.get('status') or {}).get('label'),
        'updated': datetime.now().strftime('%H:%M:%S'),
    }


class Api:
    def refresh(self):
        return simplify(fetch_snapshot())

    def open(self, key):
        url = LINKS.get(key)
        if url:
            webbrowser.open(url)
        return True


def resource(name):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def main():
    import webview
    html = Path(resource('ui.html')).read_text(encoding='utf-8')
    webview.create_window('Claude 额度小助手 · Happy AI', html=html, js_api=Api(),
                          width=940, height=740, min_size=(780, 600))
    webview.start()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--engine':
        run_engine(sys.argv[2:])
    else:
        main()
