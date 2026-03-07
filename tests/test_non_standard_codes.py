#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试非标准文件编号识别
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from doc_classifier import DocumentClassifier


def test_non_standard_codes():
    """测试非标准文件编号识别"""

    classifier = DocumentClassifier()

    test_cases = [
        {
            "name": "STCS (应为 CTCS)",
            "text": """文件编号：JDB25136-STCS-04

渗透测试记录签字确认表

序号 | 备案系统名称 | 资产对象 | 渗透工程师
            """,
            "expected_code": "STCS",
            "expected_type": "xxx系统-渗透测试记录签字确认表"
        },
        {
            "name": "WDJ (应为 WDJJ)",
            "text": """文件编号：JDB25136-WDJ-01

网络安全等级保护测评现场
接收/归还文档清单

甲方：惠州市惠城区政务服务和数据管理局
            """,
            "expected_code": "WDJ",
            "expected_type": "现场接收归还文档清单"
        },
        {
            "name": "XXXX 占位符（情况调查表）",
            "text": """文件编号：JDB25300-XXXX-01

日期：2023年10月20日

测评单位：广东中科实数科技有限公司

情况调查表确认签字
            """,
            "expected_code": "DCB",  # 应推断为 DCB
            "expected_type": "xxx系统-情况调查表确认签字"
        },
        {
            "name": "标准编号 CTCS",
            "text": """文件编号：JDB25136-CTCS-01

渗透测试记录签字确认表
            """,
            "expected_code": "CTCS",
            "expected_type": "xxx系统-渗透测试记录签字确认表"
        }
    ]

    print("=" * 80)
    print("测试非标准文件编号识别")
    print("=" * 80)

    success_count = 0
    total_count = len(test_cases)

    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['name']}")
        print("-" * 80)

        file_code = classifier.extract_file_code(case['text'])

        if file_code:
            print(f"  ✓ 成功提取文件编号")
            print(f"    项目编号: {file_code['project_code']}")
            print(f"    类型码: {file_code['doc_type_code']}")
            print(f"    文档类型: {file_code['doc_type_name']}")
            print(f"    系统编号: {file_code['system_code']}")

            # 验证结果
            if file_code['doc_type_name'] == case['expected_type']:
                print(f"  ✓ 类型识别正确")
                success_count += 1
            else:
                print(f"  ✗ 类型识别错误")
                print(f"    期望: {case['expected_type']}")
                print(f"    实际: {file_code['doc_type_name']}")
        else:
            print(f"  ✗ 未能提取文件编号")

    print("\n" + "=" * 80)
    print(f"测试结果: {success_count}/{total_count} 成功")
    print("=" * 80)

    print("\n支持的非标准编号:")
    print("  - STCS → 渗透测试记录（常见错误）")
    print("  - WDJ → 文档接交清单（简写）")
    print("  - XXXX → 通过内容推断类型（占位符）")


if __name__ == "__main__":
    test_non_standard_codes()
