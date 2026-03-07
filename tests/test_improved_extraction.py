#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的文件编号提取
"""

import sys
sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from doc_classifier import DocumentClassifier

def test_improved_extraction():
    """测试改进后的文件编号提取"""

    classifier = DocumentClassifier()

    test_cases = [
        # 标准格式
        ("标准格式", "文件编号：JDB25300-CTCS-01"),

        # 带空格
        ("带空格1", "文件编号：JDB25300 - CTCS - 01"),
        ("带空格2", "文件编号：JDB25300- CTCS -01"),
        ("带空格3", "文件编号： JDB25300 -CTCS- 01"),

        # 小写字母
        ("小写类型码", "文件编号：JDB25300-ctcs-01"),
        ("小写JDB", "文件编号：jdb25300-CTCS-01"),
        ("全小写", "文件编号：jdb25300-ctcs-01"),

        # 带换行
        ("换行1", "文件编号：\nJDB25300-CTCS-01"),
        ("换行2", "文件编号：JDB25300\n-CTCS-01"),

        # 其他前缀
        ("编号", "编号：JDB25300-CTCS-01"),
        ("档案编号", "档案编号：JDB25300-CTCS-01"),
        ("无前缀", "JDB25300-CTCS-01"),

        # 无文件编号
        ("无编号", "渗透测试记录签字确认表"),
    ]

    print("=" * 80)
    print("改进后的文件编号提取测试")
    print("=" * 80)

    success_count = 0
    total_count = len(test_cases) - 1  # 排除最后一个无编号的测试

    for name, text in test_cases:
        print(f"\n{name}: {text[:60]}...")
        file_code = classifier.extract_file_code(text)

        if file_code:
            print(f"  ✓ 提取成功:")
            print(f"    项目编号: {file_code['project_code']}")
            print(f"    类型码: {file_code['doc_type_code']}")
            print(f"    系统编号: {file_code['system_code']}")
            if name != "无编号":
                success_count += 1
        else:
            print(f"  ✗ 未能提取")

    print("\n" + "=" * 80)
    print(f"测试结果: {success_count}/{total_count} 成功")
    print("=" * 80)


if __name__ == "__main__":
    test_improved_extraction()
