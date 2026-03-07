#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试系统名称提取集成
"""

import sys
import os

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

# 设置 API Key
os.environ['SILICONFLOW_API_KEY'] = 'your_siliconflow_api_key_here'

from pdf_processor import PDFProcessor
from doc_classifier import DocumentClassifier

def test_system_name_extraction():
    """测试系统名称提取集成"""

    # 模拟无法识别文件编号的情况
    classifier = DocumentClassifier()

    test_cases = [
        {
            "name": "情况调查表 - 人民政府门户网站",
            "text": """系统情况调查表确认签字

惠州市惠城区政务服务和数据管理局提供惠城区人民政府门户网站的系统情况调查所需资料真实准确，无遗漏。

测评单位：广东中科实数科技有限公司
委托单位：惠州市惠城区政务服务和数据管理局""",
            "expected_system": "惠城区人民政府门户网站"
        },
        {
            "name": "情况调查表 - 政务服务好评系统",
            "text": """系统情况调查表确认签字

惠州市惠城区政务服务和数据管理局提供惠城区政务服务好评系统的系统情况调查所需资料真实准确，无遗漏。

测评单位：广东中科实数科技有限公司""",
            "expected_system": "惠城区政务服务好评系统"
        },
        {
            "name": "情况调查表 - 行政服务中心预约系统",
            "text": """系统情况调查表确认签字

惠州市惠城区政务服务和数据管理局提供惠城区行政服务中心预约系统的系统情况调查所需资料真实准确，无遗漏。

测评单位：广东中科实数科技有限公司""",
            "expected_system": "惠城区行政服务中心预约系统"
        }
    ]

    print("=" * 80)
    print("测试系统名称提取集成")
    print("=" * 80)

    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['name']}")
        print("-" * 80)

        # 1. 尝试提取文件编号（应该失败）
        file_code = classifier.extract_file_code(case['text'])
        if file_code:
            print(f"  文件编号: {file_code['full_code']}")
        else:
            print(f"  ✗ 无法提取文件编号")

        # 2. 识别文档类型
        doc_type, is_system_level = classifier.classify(case['text'])
        print(f"  文档类型: {doc_type}")
        print(f"  系统级文档: {is_system_level}")

        # 3. 从内容提取系统名称
        if is_system_level:
            system_name = classifier.extract_system_name_from_content(case['text'])
            if system_name:
                print(f"  ✓ 提取系统名称: {system_name}")
                if system_name == case['expected_system']:
                    print(f"  ✓ 匹配预期结果")
                else:
                    print(f"  ✗ 不匹配预期: {case['expected_system']}")
            else:
                print(f"  ✗ 无法提取系统名称")

        # 4. 生成文件名
        filename = classifier.generate_filename(
            doc_type, case['text'], "", system_name if system_name else "", is_system_level
        )
        print(f"  生成文件名: {filename}.pdf")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_system_name_extraction()
