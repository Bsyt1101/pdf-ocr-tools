"""
日志管理模块

支持两种输出模式：
1. 终端滚动显示：只显示最近 N 行，实时更新进度
2. 文件完整记录：所有日志写入文件，便于事后排查
"""

import sys
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    日志管理器

    终端显示滚动日志（最近 N 行），同时将完整日志写入文件。
    """

    def __init__(self, log_dir: Optional[str] = None, max_display_lines: int = 12):
        """
        Args:
            log_dir: 日志文件目录，默认为当前目录
            max_display_lines: 终端显示的最大行数
        """
        self.max_display_lines = max_display_lines
        self._lines = []  # 滚动缓冲区
        self._log_file = None
        self._displayed_lines = 0  # 上次在终端显示的行数
        self._progress_text = ""  # 当前进度文本
        self._enabled = True  # 是否启用滚动模式
        self._summary_lines = []  # 摘要信息（始终保留显示）

        # 检测终端是否支持 ANSI
        self._ansi = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

        # 创建日志文件
        if log_dir:
            log_path = Path(log_dir)
        else:
            log_path = Path(".")
        log_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._log_file_path = log_path / f"process_{timestamp}.log"
        self._log_file = open(self._log_file_path, 'w', encoding='utf-8')
        self._log_file.write(f"=== 日志开始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

    @property
    def log_file_path(self) -> Path:
        return self._log_file_path

    def info(self, msg: str):
        """普通信息日志"""
        self._write_log(msg)
        self._add_line(msg)
        self._refresh()

    def success(self, msg: str):
        """成功信息"""
        self._write_log(f"[OK] {msg}")
        self._add_line(f"  [OK] {msg}")
        self._refresh()

    def warn(self, msg: str):
        """警告信息"""
        self._write_log(f"[WARN] {msg}")
        self._add_line(f"  [WARN] {msg}")
        self._refresh()

    def error(self, msg: str):
        """错误信息"""
        self._write_log(f"[ERROR] {msg}")
        self._add_line(f"  [ERROR] {msg}")
        self._refresh()

    def detail(self, msg: str):
        """详细信息（只写日志文件，不显示在终端）"""
        self._write_log(f"  {msg}")

    def progress(self, current: int, total: int, desc: str = ""):
        """进度更新（覆盖当前行）"""
        pct = current / total * 100 if total > 0 else 0
        bar_width = 20
        filled = int(bar_width * current / total) if total > 0 else 0
        bar = "=" * filled + "-" * (bar_width - filled)
        self._progress_text = f"  [{bar}] {current}/{total} ({pct:.0f}%) {desc}"
        self._write_log(f"进度: {current}/{total} {desc}")
        self._refresh()

    def section(self, title: str):
        """分节标题"""
        separator = "=" * 50
        self._write_log(f"\n{separator}")
        self._write_log(title)
        self._write_log(separator)
        self._lines.clear()
        self._add_line("")
        self._add_line(f"{'=' * 50}")
        self._add_line(f"  {title}")
        self._add_line(f"{'=' * 50}")
        self._progress_text = ""
        self._refresh()

    def summary(self, lines: list):
        """设置摘要信息（始终显示在滚动区域上方）"""
        self._summary_lines = lines
        for line in lines:
            self._write_log(line)

    def print_static(self, msg: str):
        """静态输出（不参与滚动，直接打印，用于最终结果展示）"""
        self._clear_display()
        self._write_log(msg)
        print(msg)
        self._displayed_lines = 0
        self._lines.clear()

    def input(self, prompt: str) -> str:
        """获取用户输入（暂停滚动显示）"""
        self._clear_display()
        self._displayed_lines = 0
        result = input(prompt)
        self._write_log(f"{prompt}{result}")
        return result

    def close(self):
        """关闭日志文件"""
        if self._log_file:
            self._log_file.write(f"\n=== 日志结束 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            self._log_file.close()
            self._log_file = None

    def _add_line(self, line: str):
        """添加一行到滚动缓冲区"""
        self._lines.append(line)
        # 保留最近的行
        if len(self._lines) > self.max_display_lines * 2:
            self._lines = self._lines[-self.max_display_lines:]

    def _refresh(self):
        """刷新终端显示"""
        if not self._enabled:
            return

        if self._ansi:
            self._refresh_ansi()
        else:
            # 非 ANSI 终端，直接打印最后一行
            if self._lines:
                print(self._lines[-1])

    def _refresh_ansi(self):
        """ANSI 终端刷新"""
        # 清除之前显示的内容
        self._clear_display()

        # 构建显示内容
        display = []

        # 摘要区
        for line in self._summary_lines:
            display.append(line)

        # 滚动区：最近 N 行
        recent = self._lines[-self.max_display_lines:]
        for line in recent:
            display.append(line)

        # 进度条
        if self._progress_text:
            display.append(self._progress_text)

        # 输出
        output = "\n".join(display)
        sys.stdout.write(output)
        sys.stdout.flush()

        self._displayed_lines = len(display)

    def _clear_display(self):
        """清除之前显示的内容"""
        if self._ansi and self._displayed_lines > 0:
            # 移到第一行开头并清除
            sys.stdout.write(f"\033[{self._displayed_lines}A")
            for _ in range(self._displayed_lines):
                sys.stdout.write("\033[2K\n")
            sys.stdout.write(f"\033[{self._displayed_lines}A")
            sys.stdout.flush()

    def _write_log(self, msg: str):
        """写入日志文件"""
        if self._log_file:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self._log_file.write(f"[{timestamp}] {msg}\n")
            self._log_file.flush()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
