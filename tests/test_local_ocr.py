#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试本地 PaddleOCR-VL 引擎
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor import PDFProcessor


def test_local_ocr():
    """测试本地 PaddleOCR-VL"""

    print("=" * 80)
    print("本地 PaddleOCR-VL 测试")
    print("=" * 80)

    # 检查本地服务是否运行
    print("\n1. 检查本地服务状态...")
    try:
        import requests
        response = requests.get("http://localhost:8111/health", timeout=2)
        if response.status_code == 200:
            print("  ✓ 本地 MLX-VLM 服务正在运行")
        else:
            print(f"  ⚠️  服务响应异常: HTTP {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("  ✗ 无法连接到本地服务")
        print("  请先启动服务: mlx_vlm.server --port 8111")
        return
    except Exception as e:
        print(f"  ✗ 检查失败: {e}")
        return

    # 初始化处理器
    print("\n2. 初始化处理器...")
    try:
        processor = PDFProcessor(ocr_engine="local", max_workers=5)
        print(f"  ✓ 处理器初始化成功")
        print(f"  OCR 引擎: {processor._get_ocr_display_name()}")
        print(f"  并发数: {processor.max_workers}")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")
        return

    # 测试 PDF 文件
    test_pdf = Path("../test.pdf")
    if not test_pdf.exists():
        print(f"\n⚠️  测试文件不存在: {test_pdf}")
        print("请提供一个测试 PDF 文件")
        return

    print(f"\n3. 测试 PDF: {test_pdf.name}")

    # 拆分 PDF
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    page_files = processor.split_pdf(str(test_pdf), str(temp_dir))
    print(f"  拆分完成: {len(page_files)} 页")

    # 只测试前 3 页
    test_pages = page_files[:3]
    print(f"\n4. 测试 OCR 识别（前 {len(test_pages)} 页）...")

    start_time = time.time()
    text_results = processor._extract_texts_parallel(test_pages)
    elapsed = time.time() - start_time

    print(f"\n  ✓ 识别完成")
    print(f"  总耗时: {elapsed:.2f} 秒")
    print(f"  平均每页: {elapsed/len(test_pages):.2f} 秒")

    # 显示识别结果
    print(f"\n5. 识别结果预览:")
    for tr in text_results:
        text_preview = tr['text'][:80].replace('\n', ' ') if tr['text'] else '(空)'
        print(f"  第 {tr['page_num']} 页: {text_preview}...")

    # 清理
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_local_ocr()
