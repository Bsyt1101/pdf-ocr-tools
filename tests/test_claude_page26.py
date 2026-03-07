#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Claude OCR 识别第 26 页（竖排文件编号）
"""

import sys
import os

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import PDFProcessor
from doc_classifier import DocumentClassifier

def test_claude_page26():
    """测试 Claude OCR 识别第 26 页"""

    pdf_path = "/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/JDB25136-惠州市惠城区政务服务和数据管理局-验收阶段归档/hcq.pdf"

    print("=" * 80)
    print("测试 Claude OCR 识别第 26 页（竖排文件编号）")
    print("=" * 80)

    # 初始化处理器（使用 Claude OCR）
    processor = PDFProcessor(ocr_engine="claude")
    classifier = DocumentClassifier()

    # 打开 PDF
    import fitz
    doc = fitz.open(pdf_path)

    # 第 26 页（索引 25）
    page = doc[25]

    print("\n处理第 26 页...")
    print("-" * 80)

    # 提取文本
    text = page.get_text()
    print(f"原始文本长度: {len(text)} 字符")

    # 使用 OCR
    if len(text.strip()) < processor.text_threshold:
        print(f"\n使用 Claude OCR 进行识别...")
        try:
            ocr_text = processor._ocr_page(page)
            print(f"\n✓ OCR 识别成功")
            print(f"识别文本长度: {len(ocr_text)} 字符")
            print(f"\n完整识别内容:")
            print("=" * 80)
            print(ocr_text)
            print("=" * 80)

            # 尝试提取文件编号
            file_code = classifier.extract_file_code(ocr_text)

            if file_code:
                print(f"\n✓ 成功提取文件编号:")
                print(f"  完整编号: {file_code['full_code']}")
                print(f"  项目编号: {file_code['project_code']}")
                print(f"  类型代码: {file_code['doc_type_code']}")
                print(f"  文档类型: {file_code['doc_type_name']}")
                print(f"  系统编号: {file_code['system_code']}")
            else:
                print(f"\n✗ 未能提取文件编号")
                print(f"\n尝试通过关键词识别类型...")
                doc_type, is_system = classifier.classify(ocr_text)
                if doc_type:
                    print(f"  识别到类型: {doc_type} ({'系统级' if is_system else '项目级'})")

                    # 尝试从内容提取系统名称
                    if is_system:
                        system_name = classifier.extract_system_name_from_content(ocr_text)
                        if system_name:
                            print(f"  提取系统名称: {system_name}")

        except Exception as e:
            print(f"\n✗ OCR 识别失败: {e}")
            import traceback
            traceback.print_exc()

    doc.close()
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_claude_page26()
