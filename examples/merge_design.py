#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF页面合并逻辑设计

需求：将同一文档的多页合并为一个PDF文件
"""

from typing import List, Dict, Tuple
from pathlib import Path


class PageInfo:
    """页面信息"""
    def __init__(self, page_num: int, file_path: str, doc_type: str,
                 is_system_level: bool, file_code: Dict = None, system_name: str = ""):
        self.page_num = page_num
        self.file_path = file_path
        self.doc_type = doc_type
        self.is_system_level = is_system_level
        self.file_code = file_code  # {'project_code': 'JDB25300', 'doc_type_code': 'CPJG', 'system_code': '01'}
        self.system_name = system_name


def get_merge_key(page: PageInfo) -> str:
    """
    生成合并键，用于判断哪些页面应该合并

    优先级：
    1. 如果有文件编号，使用文件编号作为键
    2. 如果没有文件编号，使用文档类型+系统名称作为键

    Args:
        page: 页面信息

    Returns:
        合并键字符串
    """
    if page.file_code:
        # 方案A：基于文件编号（最准确）
        project_code = page.file_code.get('project_code', '')
        doc_type_code = page.file_code.get('doc_type_code', '')
        system_code = page.file_code.get('system_code', '')
        return f"{project_code}-{doc_type_code}-{system_code}"
    else:
        # 方案B：基于文档类型+系统名称（备用）
        if page.is_system_level and page.system_name:
            # 系统级文档：使用系统名称+文档类型
            return f"{page.system_name}-{page.doc_type}"
        else:
            # 项目级文档：使用文档类型
            return page.doc_type


def group_pages_for_merge(pages: List[PageInfo]) -> Dict[str, List[PageInfo]]:
    """
    将页面分组，相同合并键的页面归为一组

    Args:
        pages: 页面信息列表

    Returns:
        分组结果：{合并键: [页面列表]}
    """
    groups = {}

    for page in pages:
        merge_key = get_merge_key(page)

        if merge_key not in groups:
            groups[merge_key] = []

        groups[merge_key].append(page)

    return groups


def should_merge_pages(pages: List[PageInfo]) -> bool:
    """
    判断是否应该合并页面

    规则：
    1. 至少有2页
    2. 所有页面的合并键相同
    3. 页面连续或接近（可选）

    Args:
        pages: 页面列表

    Returns:
        是否应该合并
    """
    if len(pages) < 2:
        return False

    # 检查所有页面的合并键是否相同
    merge_keys = [get_merge_key(page) for page in pages]
    if len(set(merge_keys)) > 1:
        return False

    # 可选：检查页面是否连续或接近
    page_nums = sorted([page.page_num for page in pages])
    max_gap = 2  # 允许的最大页面间隔

    for i in range(len(page_nums) - 1):
        if page_nums[i + 1] - page_nums[i] > max_gap:
            # 页面间隔太大，可能不是同一文档
            print(f"  警告：页面 {page_nums[i]} 和 {page_nums[i + 1]} 间隔较大")

    return True


def merge_pdf_pages(pages: List[PageInfo], output_path: str) -> bool:
    """
    合并PDF页面

    Args:
        pages: 要合并的页面列表（按页码排序）
        output_path: 输出文件路径

    Returns:
        是否成功
    """
    import fitz  # PyMuPDF

    try:
        # 按页码排序
        pages = sorted(pages, key=lambda p: p.page_num)

        # 创建新的PDF
        merged_pdf = fitz.open()

        # 逐页添加
        for page in pages:
            src_pdf = fitz.open(page.file_path)
            merged_pdf.insert_pdf(src_pdf)
            src_pdf.close()

        # 保存
        merged_pdf.save(output_path)
        merged_pdf.close()

        print(f"  ✓ 合并 {len(pages)} 页 → {output_path}")
        return True

    except Exception as e:
        print(f"  ✗ 合并失败: {e}")
        return False


def process_with_merge(pages: List[PageInfo], output_dir: Path) -> List[str]:
    """
    处理页面并合并

    Args:
        pages: 所有页面信息
        output_dir: 输出目录

    Returns:
        生成的文件列表
    """
    # 1. 分组
    groups = group_pages_for_merge(pages)

    print(f"\n发现 {len(groups)} 个文档组:")

    output_files = []

    # 2. 处理每个组
    for merge_key, group_pages in groups.items():
        print(f"\n组: {merge_key}")
        print(f"  页面: {[p.page_num for p in group_pages]}")

        if should_merge_pages(group_pages):
            # 需要合并
            print(f"  → 合并 {len(group_pages)} 页")

            # 生成文件名
            first_page = group_pages[0]
            if first_page.is_system_level and first_page.system_name:
                filename = f"{first_page.system_name}-{first_page.doc_type.replace('xxx系统-', '')}.pdf"
            else:
                filename = f"{first_page.doc_type}.pdf"

            output_path = output_dir / filename

            # 合并
            if merge_pdf_pages(group_pages, str(output_path)):
                output_files.append(str(output_path))
        else:
            # 单页，直接复制
            print(f"  → 单页文档")
            # ... 复制逻辑

    return output_files


# 示例使用
if __name__ == "__main__":
    # 模拟数据
    pages = [
        PageInfo(8, "page_8.pdf", "xxx系统-测评结果记录签字页", True,
                {'project_code': 'JDB25300', 'doc_type_code': 'CPJG', 'system_code': '01'},
                "门户网站系统"),
        PageInfo(9, "page_9.pdf", "xxx系统-测评结果记录签字页", True,
                {'project_code': 'JDB25300', 'doc_type_code': 'CPJG', 'system_code': '01'},
                "门户网站系统"),
        PageInfo(10, "page_10.pdf", "xxx系统-测评问题列表签字页", True,
                {'project_code': 'JDB25300', 'doc_type_code': 'CPWT', 'system_code': '01'},
                "门户网站系统"),
    ]

    # 分组
    groups = group_pages_for_merge(pages)

    print("=" * 80)
    print("页面分组结果")
    print("=" * 80)

    for merge_key, group_pages in groups.items():
        print(f"\n合并键: {merge_key}")
        print(f"页面数: {len(group_pages)}")
        print(f"页码: {[p.page_num for p in group_pages]}")
        print(f"文档类型: {group_pages[0].doc_type}")
        print(f"是否合并: {'是' if should_merge_pages(group_pages) else '否'}")
