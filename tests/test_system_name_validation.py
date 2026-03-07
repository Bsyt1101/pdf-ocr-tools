#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试系统名称一致性验证功能
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from doc_classifier import DocumentClassifier


def test_system_name_validation():
    """测试系统名称一致性验证逻辑"""

    print("=" * 60)
    print("测试系统名称一致性验证功能")
    print("=" * 60)

    classifier = DocumentClassifier()

    # 模拟实施单映射
    system_names_map = {
        1: "门户网站系统",
        2: "内部办公系统",
        3: "数据管理系统"
    }

    # 测试场景1：文件编号序号为2，但匹配到序号1的系统名称
    print("\n场景1：模糊匹配时的不一致")
    print("-" * 60)

    text1 = """
    文件编号：JDB25300-CPSQS-02

    门户网站系统情况调查表

    系统名称：门户网站系统
    """

    file_code = classifier.extract_file_code(text1)
    print(f"文件编号: {file_code}")

    if file_code:
        file_code_system_seq = int(file_code['system_code'])
        print(f"文件编号中的系统序号: {file_code_system_seq}")

        # 模拟模糊匹配
        matched_seq = None
        matched_name = None
        for seq, name in system_names_map.items():
            name_core = name.replace('系统', '').replace('平台', '').strip()
            if name in text1 or name_core in text1:
                matched_seq = seq
                matched_name = name
                print(f"匹配到的系统名称: {matched_name} (序号 {seq})")
                break

        # 验证
        if matched_seq and file_code_system_seq != matched_seq:
            print(f"\n⚠️  警告：系统名称不一致！")
            print(f"    - 文件编号中的系统序号: {file_code_system_seq}")
            print(f"    - 匹配到的系统名称: {matched_name} (序号 {matched_seq})")
            print(f"    - 建议检查文件编号或系统名称是否正确")
        else:
            print("\n✓ 系统名称一致")

    # 测试场景2：文件编号序号为1，但页面提取的系统名称不匹配
    print("\n\n场景2：内容提取时的不一致")
    print("-" * 60)

    text2 = """
    文件编号：JDB25300-CPSQS-01

    提供数据管理系统的系统情况调查表

    关于数据管理系统等级保护测评
    """

    file_code2 = classifier.extract_file_code(text2)
    print(f"文件编号: {file_code2}")

    if file_code2:
        file_code_system_seq2 = int(file_code2['system_code'])
        print(f"文件编号中的系统序号: {file_code_system_seq2}")

        # 模拟从内容提取系统名称
        extracted_name = classifier.extract_system_name_from_content(text2)
        print(f"页面提取的系统名称: {extracted_name}")

        # 验证
        if file_code_system_seq2 in system_names_map:
            expected_name = system_names_map[file_code_system_seq2]
            print(f"实施单中对应的系统名称: {expected_name}")

            if extracted_name and expected_name != extracted_name:
                # 检查是否是同一个系统（去掉"系统"/"平台"后缀比较）
                extracted_core = extracted_name.replace('系统', '').replace('平台', '').strip()
                expected_core = expected_name.replace('系统', '').replace('平台', '').strip()

                if extracted_core not in expected_core and expected_core not in extracted_core:
                    print(f"\n⚠️  警告：系统名称不一致！")
                    print(f"    - 文件编号中的系统序号: {file_code_system_seq2}")
                    print(f"    - 实施单中对应的系统名称: {expected_name}")
                    print(f"    - 页面提取的系统名称: {extracted_name}")
                    print(f"    - 建议检查文件编号或页面内容是否正确")
                else:
                    print("\n✓ 系统名称一致（核心名称匹配）")
            else:
                print("\n✓ 系统名称一致")

    # 测试场景3：智能比较（不会误报）
    print("\n\n场景3：智能比较（不会误报）")
    print("-" * 60)

    text3 = """
    文件编号：JDB25300-CPSQS-01

    提供门户网站平台的系统情况调查表

    关于门户网站平台等级保护测评
    """

    file_code3 = classifier.extract_file_code(text3)
    print(f"文件编号: {file_code3}")

    if file_code3:
        file_code_system_seq3 = int(file_code3['system_code'])
        print(f"文件编号中的系统序号: {file_code_system_seq3}")

        # 模拟从内容提取系统名称
        extracted_name3 = classifier.extract_system_name_from_content(text3)
        print(f"页面提取的系统名称: {extracted_name3}")

        # 验证
        if file_code_system_seq3 in system_names_map:
            expected_name3 = system_names_map[file_code_system_seq3]
            print(f"实施单中对应的系统名称: {expected_name3}")

            if extracted_name3 and expected_name3 != extracted_name3:
                # 检查是否是同一个系统（去掉"系统"/"平台"后缀比较）
                extracted_core3 = extracted_name3.replace('系统', '').replace('平台', '').strip()
                expected_core3 = expected_name3.replace('系统', '').replace('平台', '').strip()

                print(f"核心名称比较: '{extracted_core3}' vs '{expected_core3}'")

                if extracted_core3 not in expected_core3 and expected_core3 not in extracted_core3:
                    print(f"\n⚠️  警告：系统名称不一致！")
                    print(f"    - 文件编号中的系统序号: {file_code_system_seq3}")
                    print(f"    - 实施单中对应的系统名称: {expected_name3}")
                    print(f"    - 页面提取的系统名称: {extracted_name3}")
                    print(f"    - 建议检查文件编号或页面内容是否正确")
                else:
                    print("\n✓ 系统名称一致（核心名称匹配，不会误报）")
            else:
                print("\n✓ 系统名称一致")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_system_name_validation()
