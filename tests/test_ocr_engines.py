#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 DeepSeek-OCR 集成
"""

import sys
from pathlib import Path

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import DeepSeekOCR, AliyunOCR


def test_deepseek_ocr():
    """测试 DeepSeek-OCR 初始化和基本功能"""

    print("=" * 80)
    print("测试 DeepSeek-OCR 集成")
    print("=" * 80)

    # 测试1：初始化
    print("\n1. 测试初始化:")
    try:
        # 尝试从环境变量读取
        ocr = DeepSeekOCR()
        print("  ✓ DeepSeek-OCR 初始化成功（从环境变量）")
    except ValueError as e:
        print(f"  ⚠️  需要设置 SILICONFLOW_API_KEY 环境变量")
        print(f"     {e}")
        return

    # 测试2：检查配置
    print("\n2. 检查配置:")
    print(f"  API URL: {ocr.api_url}")
    print(f"  模型: {ocr.model}")
    print(f"  API Key: {ocr.api_key[:10]}...{ocr.api_key[-5:]}")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    print("\n提示：")
    print("  - 要测试实际 OCR 识别，请准备一张测试图片")
    print("  - 运行: ocr.recognize_general('test.png')")


def test_aliyun_ocr():
    """测试阿里云 OCR 初始化"""

    print("\n" + "=" * 80)
    print("测试阿里云 OCR")
    print("=" * 80)

    print("\n1. 测试初始化:")
    try:
        ocr = AliyunOCR()
        print("  ✓ 阿里云 OCR 初始化成功（从环境变量）")
        print(f"  API URL: {ocr.api_url}")
        print(f"  AppCode: {ocr.app_code[:10]}...{ocr.app_code[-5:]}")
    except ValueError as e:
        print(f"  ⚠️  需要设置 ALIYUN_OCR_APPCODE 环境变量")
        print(f"     {e}")


def test_processor_init():
    """测试 PDFProcessor 多引擎初始化"""

    from pdf_processor import PDFProcessor

    print("\n" + "=" * 80)
    print("测试 PDFProcessor 多引擎支持")
    print("=" * 80)

    # 测试阿里云引擎
    print("\n1. 测试阿里云引擎:")
    try:
        processor = PDFProcessor(ocr_engine="aliyun")
        print("  ✓ PDFProcessor 初始化成功（阿里云引擎）")
        print(f"  引擎: {processor.ocr_engine}")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")

    # 测试 DeepSeek 引擎
    print("\n2. 测试 DeepSeek 引擎:")
    try:
        processor = PDFProcessor(ocr_engine="deepseek")
        print("  ✓ PDFProcessor 初始化成功（DeepSeek 引擎）")
        print(f"  引擎: {processor.ocr_engine}")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")

    # 测试无效引擎
    print("\n3. 测试无效引擎:")
    try:
        processor = PDFProcessor(ocr_engine="invalid")
        print("  ✗ 应该抛出异常但没有")
    except ValueError as e:
        print(f"  ✓ 正确抛出异常: {e}")


if __name__ == "__main__":
    # 运行所有测试
    test_deepseek_ocr()
    test_aliyun_ocr()
    test_processor_init()

    print("\n" + "=" * 80)
    print("所有测试完成")
    print("=" * 80)
