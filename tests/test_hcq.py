#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 hcq.pdf 文件，定位识别问题
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

# 设置 API Key
os.environ['SILICONFLOW_API_KEY'] = 'your_siliconflow_api_key_here'

from pdf_processor import PDFProcessor

def test_hcq_pdf():
    """测试 hcq.pdf 文件"""

    pdf_path = "/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/JDB25136-惠州市惠城区政务服务和数据管理局-验收阶段归档/hcq.pdf"

    print("=" * 80)
    print(f"测试文件: {pdf_path}")
    print("=" * 80)

    # 初始化处理器
    processor = PDFProcessor(ocr_engine="deepseek")

    # 只处理前 5 页来快速定位问题
    print("\n只处理前 5 页来定位问题...")

    import fitz
    doc = fitz.open(pdf_path)

    for page_num in range(min(5, len(doc))):
        page = doc[page_num]
        print(f"\n{'='*80}")
        print(f"处理第 {page_num + 1} 页:")
        print(f"{'='*80}")

        # 提取文本
        text = page.get_text()
        print(f"提取的文本长度: {len(text)} 字符")
        print(f"文本预览（前 200 字符）:\n{text[:200]}")

        # 如果文本太少，使用 OCR
        if len(text.strip()) < processor.text_threshold:
            print(f"\n文本少于 {processor.text_threshold} 字符，使用 OCR...")
            ocr_text = processor._ocr_page(page)
            print(f"OCR 识别文本长度: {len(ocr_text)} 字符")
            print(f"OCR 文本预览（前 500 字符）:\n{ocr_text[:500]}")

            # 尝试提取文件编号
            from doc_classifier import DocumentClassifier
            classifier = DocumentClassifier()
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

                # 尝试分类
                doc_type, is_system = classifier.classify(ocr_text)
                if doc_type:
                    print(f"  但通过关键词识别到类型: {doc_type}")
        else:
            print(f"\n文本充足，不需要 OCR")

    doc.close()
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_hcq_pdf()
