#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek-OCR 使用示例
演示如何使用 DeepSeek-OCR 处理 PDF 文档
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import PDFProcessor


def example_deepseek_ocr():
    """使用 DeepSeek-OCR 处理 PDF"""

    print("=" * 80)
    print("DeepSeek-OCR 使用示例")
    print("=" * 80)

    # 方式1：通过环境变量配置（推荐）
    print("\n方式1：使用环境变量")
    print("  export SILICONFLOW_API_KEY='sk-xxxxx'")
    print("  然后运行:")
    print("  processor = PDFProcessor(ocr_engine='deepseek')")

    # 方式2：直接传入 API Key
    print("\n方式2：直接传入 API Key")
    print("  processor = PDFProcessor(")
    print("      api_key='sk-xxxxx',")
    print("      ocr_engine='deepseek'")
    print("  )")

    # 示例代码
    print("\n完整示例代码:")
    print("-" * 80)
    print("""
from pdf_processor import PDFProcessor

# 初始化处理器（使用 DeepSeek-OCR）
processor = PDFProcessor(
    api_key="sk-xxxxx",  # 或从环境变量读取
    ocr_engine="deepseek"
)

# 处理 PDF
pdf_path = "test.pdf"
processor.process_pdf(pdf_path)
    """)
    print("-" * 80)

    print("\n特点:")
    print("  ✓ 基于 DeepSeek-VL2 视觉模型")
    print("  ✓ 复杂布局识别能力强")
    print("  ✓ 表格识别准确")
    print("  ✓ 中英文混排支持好")
    print("  ⚠️ 速度较慢（3-5秒/页）")

    print("\n适用场景:")
    print("  - 复杂表格文档")
    print("  - 多栏布局文档")
    print("  - 扫描质量较差的文档")
    print("  - 需要高精度识别的场景")


def example_aliyun_ocr():
    """使用阿里云 OCR 处理 PDF"""

    print("\n" + "=" * 80)
    print("阿里云 OCR 使用示例（默认）")
    print("=" * 80)

    print("\n方式1：使用环境变量")
    print("  export ALIYUN_OCR_APPCODE='你的AppCode'")
    print("  processor = PDFProcessor(ocr_engine='aliyun')")

    print("\n方式2：直接传入 AppCode")
    print("  processor = PDFProcessor(")
    print("      app_code='你的AppCode',")
    print("      ocr_engine='aliyun'  # 默认值，可省略")
    print("  )")

    print("\n特点:")
    print("  ✓ 速度快（1-2秒/页）")
    print("  ✓ 稳定性高")
    print("  ✓ 成本低")
    print("  ✓ 标准文档识别准确")

    print("\n适用场景:")
    print("  - 标准等保测评文档（推荐）")
    print("  - 需要快速处理大量文档")
    print("  - 预算有限")


def example_switch_engine():
    """演示如何切换 OCR 引擎"""

    print("\n" + "=" * 80)
    print("切换 OCR 引擎示例")
    print("=" * 80)

    print("\n场景：根据文档类型选择不同的 OCR 引擎")
    print("-" * 80)
    print("""
import os
from pdf_processor import PDFProcessor

def process_pdf_smart(pdf_path, is_complex=False):
    '''根据文档复杂度选择 OCR 引擎'''

    if is_complex:
        # 复杂文档使用 DeepSeek-OCR
        print("检测到复杂文档，使用 DeepSeek-OCR...")
        processor = PDFProcessor(ocr_engine="deepseek")
    else:
        # 标准文档使用阿里云 OCR
        print("标准文档，使用阿里云 OCR...")
        processor = PDFProcessor(ocr_engine="aliyun")

    processor.process_pdf(pdf_path)

# 使用示例
process_pdf_smart("标准文档.pdf", is_complex=False)  # 使用阿里云
process_pdf_smart("复杂表格.pdf", is_complex=True)   # 使用 DeepSeek
    """)
    print("-" * 80)


if __name__ == "__main__":
    example_deepseek_ocr()
    example_aliyun_ocr()
    example_switch_engine()

    print("\n" + "=" * 80)
    print("更多信息请查看: OCR_ENGINES.md")
    print("=" * 80)
