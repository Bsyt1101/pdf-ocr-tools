#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试本地 PaddleOCR-VL 单张图片识别
"""

import sys
import time
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor import LocalPaddleOCR


def test_single_image():
    """测试单张图片识别"""

    print("=" * 80)
    print("本地 PaddleOCR-VL 单图测试")
    print("=" * 80)

    # 创建测试图片
    print("\n1. 创建测试图片...")
    img = Image.new('RGB', (800, 200), color='white')
    draw = ImageDraw.Draw(img)

    # 绘制测试文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
    except:
        font = ImageFont.load_default()

    draw.text((50, 80), "文件编号：JDB25245-CPJG-01", fill='black', font=font)

    # 保存到临时文件
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        test_img_path = f.name
        img.save(test_img_path, 'JPEG', quality=95)

    print(f"  ✓ 测试图片已创建: {test_img_path}")

    # 初始化 OCR
    print("\n2. 初始化本地 OCR...")
    try:
        ocr = LocalPaddleOCR()
        print(f"  ✓ 初始化成功")
        print(f"  服务地址: {ocr.base_url}")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")
        return

    # 识别文字
    print("\n3. 识别文字...")
    print("  （首次识别会加载模型，可能需要 30-60 秒）")

    start_time = time.time()
    try:
        text = ocr.recognize_general(test_img_path)
        elapsed = time.time() - start_time

        print(f"\n  ✓ 识别完成")
        print(f"  耗时: {elapsed:.2f} 秒")
        print(f"\n  识别结果:")
        print(f"  {'-' * 60}")
        print(f"  {text if text else '(空)'}")
        print(f"  {'-' * 60}")

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n  ✗ 识别失败 (耗时 {elapsed:.2f} 秒)")
        print(f"  错误: {e}")

    # 清理
    import os
    try:
        os.unlink(test_img_path)
    except:
        pass

    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_single_image()
