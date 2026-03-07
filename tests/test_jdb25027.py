#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 JDB25027 项目的系统名称读取功能
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pdf_processor import PDFProcessor


def test_jdb25027():
    """测试 JDB25027 项目"""

    # 测试目录
    test_dir = Path("/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/JDB25027-广州数语科技有限公司-验收阶段归档")

    if not test_dir.exists():
        print(f"错误：测试目录不存在: {test_dir}")
        return

    print(f"{'='*80}")
    print(f"测试项目: JDB25027")
    print(f"测试目录: {test_dir.name}")
    print(f"{'='*80}\n")

    processor = PDFProcessor()

    # 1. 测试从测评报告提取系统名称
    print("【步骤1】从测评报告提取系统名称")
    print("-" * 80)
    system_name = processor.extract_system_name_from_report(test_dir)
    if system_name:
        print(f"✓ 成功提取系统名称: {system_name}\n")
    else:
        print(f"✗ 未能提取系统名称\n")

    # 2. 测试读取系统名称映射（包含从测评报告提取和更新实施单）
    print("【步骤2】读取项目实施单并更新系统名称")
    print("-" * 80)
    system_names_map = processor.read_system_names_from_word(test_dir)
    if system_names_map:
        print(f"✓ 成功读取系统名称映射:")
        for seq, name in system_names_map.items():
            print(f"  序号 {seq}: {name}")
    else:
        print(f"✗ 未能读取系统名称映射")

    print(f"\n{'='*80}")
    print("测试完成")
    print(f"{'='*80}")


if __name__ == "__main__":
    test_jdb25027()
