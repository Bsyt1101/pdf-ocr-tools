#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试系统名称读取功能
"""

from pathlib import Path
from doc_classifier import DocumentClassifier

def test_file_code_extraction():
    """测试文件编号提取"""
    print("=" * 60)
    print("测试1：文件编号提取")
    print("=" * 60)

    classifier = DocumentClassifier()

    test_texts = [
        "文件编号：JDB25300-CPJG-01\n测评结果记录签字页",
        "文件编号：JDB25300-DCB-02\n情况调查表确认签字",
        "文件编号：JDB25300-CPWT-03\n测评问题列表签字页",
        "没有文件编号的文本",
    ]

    for text in test_texts:
        print(f"\n文本: {text[:50]}...")
        file_code = classifier.extract_file_code(text)
        if file_code:
            print(f"  ✓ 提取成功:")
            print(f"    项目编号: {file_code['project_code']}")
            print(f"    类型码: {file_code['doc_type_code']}")
            print(f"    系统编号: {file_code['system_code']} (类型: {type(file_code['system_code'])})")
            print(f"    文档类型: {file_code.get('doc_type_name', 'N/A')}")
        else:
            print(f"  ✗ 未能提取文件编号")


def test_system_seq_conversion():
    """测试系统序号转换"""
    print("\n" + "=" * 60)
    print("测试2：系统序号转换")
    print("=" * 60)

    system_codes = ["01", "02", "03", "1", "2", "3"]

    for code in system_codes:
        try:
            seq = int(code)
            print(f"  '{code}' → {seq} (类型: {type(seq).__name__})")
        except ValueError as e:
            print(f"  '{code}' → 转换失败: {e}")


def test_system_names_mapping():
    """测试系统名称映射"""
    print("\n" + "=" * 60)
    print("测试3：系统名称映射")
    print("=" * 60)

    # 模拟从Word文件读取的映射
    system_names_map = {
        1: "门户网站系统",
        2: "内部办公系统",
        3: "数据管理系统"
    }

    print(f"系统名称映射: {system_names_map}")

    # 测试查找
    test_seqs = [1, 2, 3, 4, "01", "02"]

    for seq in test_seqs:
        if isinstance(seq, str):
            try:
                seq = int(seq)
            except ValueError:
                print(f"  序号 '{seq}' → 转换失败")
                continue

        if seq in system_names_map:
            print(f"  序号 {seq} → {system_names_map[seq]}")
        else:
            print(f"  序号 {seq} → 未找到")


def test_filename_generation():
    """测试文件名生成"""
    print("\n" + "=" * 60)
    print("测试4：文件名生成")
    print("=" * 60)

    classifier = DocumentClassifier()

    test_cases = [
        ("xxx系统-测评结果记录签字页", "", "", "", True, 1),
        ("xxx系统-测评结果记录签字页", "", "", "门户网站系统", True, 1),
        ("xxx系统-情况调查表确认签字", "", "", "内部办公系统", True, 1),
        ("现场测评授权书", "", "JDB项目编号-xxx单位", "", False, 1),
    ]

    for doc_type, text, project_name, system_name, is_system_level, page_num in test_cases:
        print(f"\n输入:")
        print(f"  文档类型: {doc_type}")
        print(f"  系统名称: {system_name if system_name else '(无)'}")
        print(f"  是否系统级: {is_system_level}")

        filename = classifier.generate_filename(
            doc_type, text, project_name, system_name, is_system_level, page_num
        )
        print(f"输出: {filename}.pdf")


def test_complete_workflow():
    """测试完整工作流程"""
    print("\n" + "=" * 60)
    print("测试5：完整工作流程模拟")
    print("=" * 60)

    classifier = DocumentClassifier()

    # 模拟从Word文件读取的系统名称
    system_names_map = {
        1: "门户网站系统",
        2: "内部办公系统"
    }

    print(f"系统名称映射: {system_names_map}\n")

    # 模拟PDF文档内容
    test_docs = [
        "文件编号：JDB25300-CPJG-01\n测评结果记录签字页",
        "文件编号：JDB25300-CPJG-02\n测评结果记录签字页",
        "文件编号：JDB25300-DCB-01\n情况调查表确认签字",
    ]

    for idx, text in enumerate(test_docs, 1):
        print(f"文档 {idx}:")
        print(f"  文本: {text[:50]}...")

        # 1. 分类文档
        doc_type, is_system_level = classifier.classify(text)
        print(f"  识别类型: {doc_type} ({'系统级' if is_system_level else '项目级'})")

        # 2. 提取文件编号
        file_code = classifier.extract_file_code(text)
        if file_code:
            print(f"  文件编号: {file_code['project_code']}-{file_code['doc_type_code']}-{file_code['system_code']}")

        # 3. 确定系统名称
        current_system_name = ""
        if is_system_level and file_code:
            try:
                system_seq = int(file_code['system_code'])
                if system_seq in system_names_map:
                    current_system_name = system_names_map[system_seq]
                    print(f"  系统序号: {system_seq} → {current_system_name}")
            except (ValueError, KeyError) as e:
                print(f"  转换失败: {e}")

        # 4. 生成文件名
        filename = classifier.generate_filename(
            doc_type, text, "", current_system_name, is_system_level, 1
        )
        print(f"  最终文件名: {filename}.pdf")
        print()


if __name__ == "__main__":
    test_file_code_extraction()
    test_system_seq_conversion()
    test_system_names_mapping()
    test_filename_generation()
    test_complete_workflow()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
