#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试文件编号提取问题
"""

import re
from pathlib import Path

def test_file_code_extraction():
    """测试不同格式的文件编号提取"""

    # 标准正则表达式
    pattern = r'(JDB\d+)-([A-Z]+)-(\d+)'

    test_cases = [
        # 标准格式
        "文件编号：JDB25300-CTCS-01",
        "文件编号: JDB25300-CTCS-01",
        "JDB25300-CTCS-01",

        # 带空格
        "文件编号：JDB25300 - CTCS - 01",
        "文件编号：JDB25300- CTCS -01",

        # 带换行
        "文件编号：\nJDB25300-CTCS-01",
        "文件编号：JDB25300-\nCTCS-01",

        # 小写字母
        "文件编号：JDB25300-ctcs-01",
        "文件编号：jdb25300-CTCS-01",

        # 其他格式
        "编号：JDB25300-CTCS-01",
        "档案编号：JDB25300-CTCS-01",

        # 无文件编号
        "这是一个没有文件编号的文档",
        "渗透测试记录签字确认表",
    ]

    print("=" * 80)
    print("文件编号提取测试")
    print("=" * 80)
    print(f"\n正则表达式: {pattern}\n")

    for i, text in enumerate(test_cases, 1):
        print(f"测试 {i}: {text[:50]}...")
        match = re.search(pattern, text)
        if match:
            print(f"  ✓ 匹配成功:")
            print(f"    项目编号: {match.group(1)}")
            print(f"    类型码: {match.group(2)}")
            print(f"    系统编号: {match.group(3)}")
        else:
            print(f"  ✗ 未匹配")
        print()


def suggest_improved_pattern():
    """建议改进的正则表达式"""

    print("=" * 80)
    print("改进建议")
    print("=" * 80)

    # 更宽松的正则表达式
    patterns = {
        "标准格式": r'(JDB\d+)-([A-Z]+)-(\d+)',
        "允许空格": r'(JDB\d+)\s*-\s*([A-Z]+)\s*-\s*(\d+)',
        "大小写不敏感": r'(JDB\d+)-([A-Za-z]+)-(\d+)',
        "允许空格+大小写不敏感": r'(JDB\d+)\s*-\s*([A-Za-z]+)\s*-\s*(\d+)',
    }

    test_text = "文件编号：JDB25300 - CTCS - 01"

    print(f"\n测试文本: {test_text}\n")

    for name, pattern in patterns.items():
        match = re.search(pattern, test_text, re.IGNORECASE)
        if match:
            print(f"✓ {name}: 匹配成功")
            print(f"  {match.group(0)}")
        else:
            print(f"✗ {name}: 未匹配")
        print()


if __name__ == "__main__":
    test_file_code_extraction()
    suggest_improved_pattern()
