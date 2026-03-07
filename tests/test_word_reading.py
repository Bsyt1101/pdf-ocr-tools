#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试读取指定Word文件中的系统名称
"""

from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import PDFProcessor

def test_read_word_file():
    """测试读取指定的Word文件"""

    # Word文件路径
    word_file_dir = Path("/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/2025年项目归档/JDB25136-惠州市惠城区政务服务和数据管理局-验收阶段归档")

    print("=" * 80)
    print("测试读取Word文件中的系统名称")
    print("=" * 80)
    print(f"\n搜索目录: {word_file_dir}")

    # 创建处理器
    processor = PDFProcessor()

    # 尝试读取系统名称
    system_names_map = processor.read_system_names_from_word(word_file_dir)

    print("\n" + "=" * 80)
    print("读取结果")
    print("=" * 80)

    if system_names_map:
        print(f"\n✓ 成功读取 {len(system_names_map)} 个系统名称:")
        for seq, name in sorted(system_names_map.items()):
            print(f"  序号 {seq} → {name}")
    else:
        print("\n✗ 未能读取到系统名称")
        print("\n可能的原因:")
        print("  1. 未找到'项目实施单'文件夹")
        print("  2. 未找到'项目实施申请单'Word文件")
        print("  3. Word文件中的表格格式不正确")
        print("  4. 表格中没有'序号'或'系统名称'列")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_read_word_file()
