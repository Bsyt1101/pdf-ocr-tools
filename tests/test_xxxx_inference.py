#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 XXXX 占位符推断逻辑
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from doc_classifier import DocumentClassifier


def test_xxxx_inference():
    """测试 XXXX 占位符通过内容推断"""

    classifier = DocumentClassifier()

    # 模拟 OCR 识别错误的情况
    test_cases = [
        {
            "name": "XXXX 识别错误 - 情况调查表",
            "text": """文件编号：JDB25300-XXXX-01

日期：2025年10月20日

测评单位：广东中科实数科技有限公司

测评人员确认签字：______________________

系统情况调查表确认签字

惠州市惠城区政务服务和数据管理局
            """,
            "expected_code": "DCB",
            "expected_name": "xxx系统-情况调查表确认签字"
        },
        {
            "name": "XXXX 识别错误 - 测评方案初审",
            "text": """文件编号：JDB25136-XXXX-02

测评方案初审记录

项目名称：某某系统
            """,
            "expected_code": "FACS",
            "expected_name": "xxx系统-测评方案初审记录"
        },
        {
            "name": "XXXX 识别错误 - 渗透测试",
            "text": """文件编号：JDB25136-XXXX-03

渗透测试记录签字确认表

测评单位：广东中科实数科技有限公司
            """,
            "expected_code": "CTCS",
            "expected_name": "xxx系统-渗透测试记录签字确认表"
        }
    ]

    print("=" * 80)
    print("测试 XXXX 占位符推断逻辑")
    print("=" * 80)

    success_count = 0
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['name']}")
        print("-" * 80)

        file_code = classifier.extract_file_code(case['text'])

        if file_code:
            actual_code = file_code['doc_type_code']
            actual_name = file_code['doc_type_name']

            if actual_code == case['expected_code'] and actual_name == case['expected_name']:
                print(f"  ✓ 推断成功")
                print(f"    推断代码: {actual_code}")
                print(f"    文档类型: {actual_name}")
                print(f"    完整编号: {file_code['full_code']}")
                success_count += 1
            else:
                print(f"  ✗ 推断错误")
                print(f"    期望代码: {case['expected_code']}")
                print(f"    实际代码: {actual_code}")
        else:
            print(f"  ✗ 未能提取文件编号")

    print("\n" + "=" * 80)
    print(f"测试结果: {success_count}/{len(test_cases)} 成功")
    print("=" * 80)


if __name__ == "__main__":
    test_xxxx_inference()
