#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试页面合并功能
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import PDFProcessor


def test_merge_logic():
    """测试合并逻辑"""

    processor = PDFProcessor()

    # 模拟处理结果
    results = [
        # 第8页和第9页：相同文件编号，应该合并
        {
            'page': 8,
            'source': 'page_8.pdf',
            'doc_type': 'xxx系统-测评结果记录签字页',
            'is_system_level': True,
            'system_name': '门户网站系统',
            'file_code': {
                'project_code': 'JDB25300',
                'doc_type_code': 'CPJG',
                'system_code': '01'
            },
            'filename': '门户网站系统-测评结果记录签字页',
            'folder': '测评记录及问题汇总',
            'text_preview': '测评结果记录...'
        },
        {
            'page': 9,
            'source': 'page_9.pdf',
            'doc_type': 'xxx系统-测评结果记录签字页',
            'is_system_level': True,
            'system_name': '门户网站系统',
            'file_code': {
                'project_code': 'JDB25300',
                'doc_type_code': 'CPJG',
                'system_code': '01'
            },
            'filename': '门户网站系统-测评结果记录签字页',
            'folder': '测评记录及问题汇总',
            'text_preview': '测评结果记录...'
        },

        # 第10页：不同文件编号，不应该合并
        {
            'page': 10,
            'source': 'page_10.pdf',
            'doc_type': 'xxx系统-测评问题列表签字页',
            'is_system_level': True,
            'system_name': '门户网站系统',
            'file_code': {
                'project_code': 'JDB25300',
                'doc_type_code': 'CPWT',
                'system_code': '01'
            },
            'filename': '门户网站系统-测评问题列表签字页',
            'folder': '测评记录及问题汇总',
            'text_preview': '测评问题列表...'
        },

        # 第11页和第12页：相同文件编号，应该合并
        {
            'page': 11,
            'source': 'page_11.pdf',
            'doc_type': 'xxx系统-测评结果记录签字页',
            'is_system_level': True,
            'system_name': '内部办公系统',
            'file_code': {
                'project_code': 'JDB25300',
                'doc_type_code': 'CPJG',
                'system_code': '02'
            },
            'filename': '内部办公系统-测评结果记录签字页',
            'folder': '测评记录及问题汇总',
            'text_preview': '测评结果记录...'
        },
        {
            'page': 12,
            'source': 'page_12.pdf',
            'doc_type': 'xxx系统-测评结果记录签字页',
            'is_system_level': True,
            'system_name': '内部办公系统',
            'file_code': {
                'project_code': 'JDB25300',
                'doc_type_code': 'CPJG',
                'system_code': '02'
            },
            'filename': '内部办公系统-测评结果记录签字页',
            'folder': '测评记录及问题汇总',
            'text_preview': '测评结果记录...'
        },

        # 第13页：项目级文档，单页
        {
            'page': 13,
            'source': 'page_13.pdf',
            'doc_type': '现场测评授权书',
            'is_system_level': False,
            'system_name': '',
            'file_code': {
                'project_code': 'JDB25300',
                'doc_type_code': 'CPSQS',
                'system_code': '01'
            },
            'filename': '现场测评授权书',
            'folder': '测评授权书',
            'text_preview': '现场测评授权书...'
        },
    ]

    print("=" * 80)
    print("测试页面合并逻辑")
    print("=" * 80)

    # 测试合并键生成
    print("\n1. 测试合并键生成:")
    for result in results:
        merge_key = processor._get_merge_key(result)
        print(f"  第 {result['page']:2d} 页: {merge_key}")

    # 测试分组
    print("\n2. 测试页面分组:")
    groups = {}
    for result in results:
        merge_key = processor._get_merge_key(result)
        if merge_key not in groups:
            groups[merge_key] = []
        groups[merge_key].append(result)

    for merge_key, group in groups.items():
        print(f"\n  组: {merge_key}")
        print(f"    页面数: {len(group)}")
        print(f"    页码: {[r['page'] for r in group]}")
        print(f"    文档类型: {group[0]['doc_type']}")
        print(f"    是否需要合并: {'是' if len(group) > 1 else '否'}")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_merge_logic()
