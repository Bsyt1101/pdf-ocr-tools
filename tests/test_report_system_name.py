#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试从测评报告读取系统名称功能
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pdf_processor import PDFProcessor


def test_extract_system_name_from_report():
    """测试从测评报告提取系统名称"""

    # 测试目录（根据实际情况修改）
    test_dirs = [
        Path("/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/JDB25210-xxx单位-初审阶段归档-26-0127"),
        Path("/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/JDB25253-xxx单位-初审阶段归档-26-0127"),
    ]

    processor = PDFProcessor()

    for test_dir in test_dirs:
        if not test_dir.exists():
            print(f"跳过不存在的目录: {test_dir}")
            continue

        print(f"\n{'='*60}")
        print(f"测试目录: {test_dir.name}")
        print(f"{'='*60}")

        # 测试从测评报告提取系统名称
        system_name = processor.extract_system_name_from_report(test_dir)
        if system_name:
            print(f"✓ 成功提取系统名称: {system_name}")
        else:
            print(f"✗ 未能提取系统名称")

        # 测试读取系统名称（包含从测评报告提取和更新实施单）
        print(f"\n--- 测试读取系统名称映射 ---")
        system_names_map = processor.read_system_names_from_word(test_dir)
        if system_names_map:
            print(f"✓ 成功读取系统名称映射:")
            for seq, name in system_names_map.items():
                print(f"  序号 {seq}: {name}")
        else:
            print(f"✗ 未能读取系统名称映射")


if __name__ == "__main__":
    test_extract_system_name_from_report()
