#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件夹搜索功能
"""

from pathlib import Path

def find_matching_folder(base_dir: Path, folder_keyword: str):
    """
    在基础目录下搜索包含关键词的文件夹
    """
    if not base_dir.exists():
        print(f"目录不存在: {base_dir}")
        return None

    print(f"\n搜索目录: {base_dir}")
    print(f"关键词: {folder_keyword}")
    print("-" * 60)

    # 遍历基础目录下的所有文件夹
    for item in base_dir.iterdir():
        if item.is_dir():
            print(f"  检查文件夹: {item.name}")
            # 检查文件夹名称是否包含关键词
            if folder_keyword in item.name:
                print(f"  ✓ 匹配成功!")
                return item

    print(f"  ✗ 未找到匹配的文件夹")
    return None


# 测试用例
if __name__ == "__main__":
    # 假设PDF文件在某个目录下
    test_dir = Path(".")

    # 测试文件夹关键词
    test_keywords = [
        "现场接收归还文档清单",
        "测评授权书",
        "风险告知书",
        "测评调研表",
    ]

    print("=" * 60)
    print("文件夹搜索测试")
    print("=" * 60)

    for keyword in test_keywords:
        result = find_matching_folder(test_dir, keyword)
        if result:
            print(f"结果: {result.name}\n")
        else:
            print(f"结果: 未找到\n")
