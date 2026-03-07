#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 PaddleOCR-VL-1.5 模型
"""

import sys
import os

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

# 设置 API Key
os.environ['SILICONFLOW_API_KEY'] = 'your_siliconflow_api_key_here'

from pdf_processor import PDFProcessor

def test_paddleocr():
    """测试 PaddleOCR-VL-1.5"""

    pdf_path = "/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/JDB25136-惠州市惠城区政务服务和数据管理局-验收阶段归档/hcq.pdf"

    print("=" * 80)
    print("测试 PaddleOCR-VL-1.5 模型")
    print("=" * 80)

    # 初始化处理器
    processor = PDFProcessor(ocr_engine="deepseek")

    # 只测试第 1 页
    import fitz
    doc = fitz.open(pdf_path)
    page = doc[0]

    print("\n处理第 1 页...")
    print("-" * 80)

    # 提取文本
    text = page.get_text()
    print(f"原始文本长度: {len(text)} 字符")

    # 使用 OCR
    if len(text.strip()) < processor.text_threshold:
        print(f"\n使用 PaddleOCR-VL-1.5 进行 OCR 识别...")
        try:
            ocr_text = processor._ocr_page(page)
            print(f"\n✓ OCR 识别成功")
            print(f"识别文本长度: {len(ocr_text)} 字符")
            print(f"\n识别内容预览（前 500 字符）:")
            print("-" * 80)
            print(ocr_text[:500])
            print("-" * 80)

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
            else:
                print(f"\n✗ 未能提取文件编号")

        except Exception as e:
            print(f"\n✗ OCR 识别失败: {e}")
            import traceback
            traceback.print_exc()

    doc.close()
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_paddleocr()
