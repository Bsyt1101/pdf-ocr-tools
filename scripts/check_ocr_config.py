#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 OCR 引擎配置
"""

import os
import sys

sys.path.insert(0, '/Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool')

from pdf_processor import PDFProcessor, DeepSeekOCR, AliyunOCR


def check_config():
    """检查 OCR 引擎配置"""

    print("=" * 80)
    print("OCR 引擎配置检查")
    print("=" * 80)

    # 检查环境变量
    print("\n1. 环境变量检查:")

    aliyun_appcode = os.getenv('ALIYUN_OCR_APPCODE')
    siliconflow_key = os.getenv('SILICONFLOW_API_KEY')

    if aliyun_appcode:
        print(f"  ✓ ALIYUN_OCR_APPCODE: {aliyun_appcode[:10]}...{aliyun_appcode[-5:]}")
    else:
        print("  ⚠️  ALIYUN_OCR_APPCODE: 未设置")

    if siliconflow_key:
        print(f"  ✓ SILICONFLOW_API_KEY: {siliconflow_key[:15]}...{siliconflow_key[-10:]}")
    else:
        print("  ⚠️  SILICONFLOW_API_KEY: 未设置")

    # 测试阿里云 OCR
    print("\n2. 阿里云 OCR 初始化:")
    try:
        if aliyun_appcode:
            processor = PDFProcessor(ocr_engine="aliyun")
            print("  ✓ 初始化成功")
            print(f"    引擎: {processor.ocr_engine}")
        else:
            print("  ⚠️  跳过（未配置 AppCode）")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")

    # 测试 DeepSeek-OCR
    print("\n3. DeepSeek-OCR 初始化:")
    try:
        if siliconflow_key:
            processor = PDFProcessor(ocr_engine="deepseek")
            print("  ✓ 初始化成功")
            print(f"    引擎: {processor.ocr_engine}")
            print(f"    模型: deepseek-ai/DeepSeek-VL2")
        else:
            print("  ⚠️  跳过（未配置 API Key）")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")

    # 配置建议
    print("\n" + "=" * 80)
    print("配置建议")
    print("=" * 80)

    if not aliyun_appcode and not siliconflow_key:
        print("\n⚠️  未检测到任何 OCR 引擎配置")
        print("\n请至少配置一个 OCR 引擎:")
        print("\n阿里云 OCR:")
        print("  export ALIYUN_OCR_APPCODE='你的AppCode'")
        print("\nDeepSeek-OCR:")
        print("  export SILICONFLOW_API_KEY='sk-xxxxx'")
    elif aliyun_appcode and siliconflow_key:
        print("\n✓ 两个 OCR 引擎都已配置")
        print("\n使用建议:")
        print("  - 标准文档: 使用阿里云 OCR（速度快）")
        print("  - 复杂布局: 使用 DeepSeek-OCR（精度高）")
    elif aliyun_appcode:
        print("\n✓ 阿里云 OCR 已配置")
        print("\n如需使用 DeepSeek-OCR，请配置:")
        print("  export SILICONFLOW_API_KEY='sk-xxxxx'")
    elif siliconflow_key:
        print("\n✓ DeepSeek-OCR 已配置")
        print("\n如需使用阿里云 OCR，请配置:")
        print("  export ALIYUN_OCR_APPCODE='你的AppCode'")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    check_config()
