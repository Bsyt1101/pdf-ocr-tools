#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整 PDF 处理流程测试
"""

import sys
import time
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor import PDFProcessor


def test_complete_workflow():
    """测试完整的 PDF 处理流程"""

    print("=" * 80)
    print("完整 PDF 处理流程测试（本地 PaddleOCR-VL）")
    print("=" * 80)

    # 初始化处理器
    print("\n1. 初始化处理器...")
    processor = PDFProcessor(ocr_engine="local", max_workers=5)
    print(f"  ✓ OCR 引擎: {processor._get_ocr_display_name()}")
    print(f"  ✓ 并发数: {processor.max_workers}")

    # 测试 PDF
    test_pdf = Path(__file__).parent.parent / "2_PDFsam_20260304140500.pdf"
    if not test_pdf.exists():
        print(f"\n⚠️  测试文件不存在: {test_pdf}")
        print("请提供一个测试 PDF 文件")
        return

    print(f"\n2. 测试文件: {test_pdf.name}")
    print(f"  文件大小: {test_pdf.stat().st_size / 1024:.1f} KB")

    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp())
    print(f"\n3. 临时目录: {temp_dir}")

    try:
        # 拆分 PDF
        print("\n4. 拆分 PDF...")
        page_files = processor.split_pdf(str(test_pdf), str(temp_dir))
        print(f"  ✓ 拆分完成: {len(page_files)} 页")

        # 只处理前 3 页
        test_pages = page_files[:min(3, len(page_files))]
        print(f"\n5. 测试前 {len(test_pages)} 页（并行识别）...")

        # 并行提取文本
        start_time = time.time()
        text_results = processor._extract_texts_parallel(test_pages)
        elapsed = time.time() - start_time

        print(f"\n  ✓ 文本提取完成")
        print(f"  总耗时: {elapsed:.2f} 秒")
        print(f"  平均每页: {elapsed/len(test_pages):.2f} 秒")

        # 显示识别结果
        print(f"\n6. 识别结果:")
        print("=" * 80)
        for tr in text_results:
            print(f"\n第 {tr['page_num']} 页:")
            print(f"{tr['text']}")
            print("-" * 80)

    finally:
        # 清理
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_complete_workflow()
