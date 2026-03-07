#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 DeepSeek-OCR
使用已配置的 API Key 测试 OCR 功能
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import PDFProcessor


def quick_test():
    """快速测试 DeepSeek-OCR"""

    print("=" * 80)
    print("DeepSeek-OCR 快速测试")
    print("=" * 80)

    # 初始化处理器
    print("\n1. 初始化 DeepSeek-OCR...")
    try:
        processor = PDFProcessor(ocr_engine="deepseek")
        print("  ✓ 初始化成功")
        print(f"  引擎: {processor.ocr_engine}")
        print(f"  模型: deepseek-ai/DeepSeek-VL2")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")
        print("\n请确保已设置环境变量:")
        print("  export SILICONFLOW_API_KEY='your_siliconflow_api_key_here'")
        return

    print("\n2. 准备测试")
    print("  提示: 要测试实际 OCR 识别，请准备一个 PDF 文件")
    print("  然后运行:")
    print("    processor.process_pdf('你的文件.pdf')")

    print("\n3. 使用示例")
    print("-" * 80)
    print("""
# 处理单个 PDF 文件
from pdf_processor import PDFProcessor

processor = PDFProcessor(ocr_engine="deepseek")
processor.process_pdf("test.pdf")

# 程序会自动：
# 1. 拆分 PDF 为单页
# 2. 使用 DeepSeek-OCR 识别每页内容
# 3. 识别文档类型
# 4. 自动命名和归档
    """)
    print("-" * 80)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n下一步:")
    print("  1. 准备一个测试 PDF 文件")
    print("  2. 运行: processor.process_pdf('测试文件.pdf')")
    print("  3. 查看处理结果")

    print("\n相关文档:")
    print("  - OCR_ENGINES.md - OCR 引擎详细说明")
    print("  - CURRENT_CONFIG.md - 当前配置说明")
    print("  - example_deepseek_ocr.py - 更多使用示例")


if __name__ == "__main__":
    quick_test()
