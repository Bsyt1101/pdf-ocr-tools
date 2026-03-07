#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试横向页面文件编号识别优化
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from doc_classifier import DocumentClassifier


def test_header_priority():
    """测试页眉优先识别"""

    classifier = DocumentClassifier()

    # 模拟横向页面的文本（签字日期在前，文件编号在后）
    test_cases = [
        {
            "name": "签字日期在前（旧逻辑会误识别）",
            "text": """
日期：2025年10月20日
签字：张三

文件编号：JDB25136-FACS-01

等级保护测评方案评审记录表
项目名称：惠州市惠城区政务服务和数据管理局
            """
        },
        {
            "name": "文件编号在页眉（正常情况）",
            "text": """
文件编号：JDB25136-FACS-01

等级保护测评方案评审记录表
项目名称：惠州市惠城区政务服务和数据管理局

日期：2025年10月20日
签字：张三
            """
        },
        {
            "name": "文件编号在中间位置",
            "text": """
等级保护测评方案评审记录表
项目名称：惠州市惠城区政务服务和数据管理局

文件编号：JDB25136-FACS-01

评审内容：
1. 测评方案完整性
2. 测评方法合理性

日期：2025年10月20日
            """
        }
    ]

    print("=" * 80)
    print("测试页眉优先识别策略")
    print("=" * 80)

    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['name']}")
        print("-" * 80)

        file_code = classifier.extract_file_code(case['text'])

        if file_code:
            print(f"  ✓ 成功提取文件编号")
            print(f"    项目编号: {file_code['project_code']}")
            print(f"    类型码: {file_code['doc_type_code']}")
            print(f"    系统编号: {file_code['system_code']}")
            print(f"    完整编号: {file_code['full_code']}")
        else:
            print(f"  ✗ 未能提取文件编号")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n优化说明:")
    print("  1. 优先在前20%文本（页眉区域）查找文件编号")
    print("  2. 如果页眉没找到，再搜索全文")
    print("  3. 避免误识别签字日期等其他编号格式")


if __name__ == "__main__":
    test_header_priority()
