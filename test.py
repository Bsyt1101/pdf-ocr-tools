#!/usr/bin/env python3
"""
测试脚本 - 验证工具是否正常工作
"""

import os
import sys

def test_imports():
    """测试依赖是否安装"""
    print("=" * 60)
    print("测试1: 检查依赖")
    print("=" * 60)

    try:
        import fitz
        print("✓ PyMuPDF 已安装")
    except ImportError:
        print("✗ PyMuPDF 未安装，请运行: pip install PyMuPDF")
        return False

    try:
        import requests
        print("✓ requests 已安装")
    except ImportError:
        print("✗ requests 未安装，请运行: pip install requests")
        return False

    return True


def test_appcode():
    """测试AppCode配置"""
    print("\n" + "=" * 60)
    print("测试2: 检查AppCode配置")
    print("=" * 60)

    app_code = os.getenv('ALIYUN_OCR_APPCODE')
    if app_code:
        print(f"✓ AppCode 已配置: {app_code[:10]}...")
        return True
    else:
        print("✗ AppCode 未配置")
        print("请运行: export ALIYUN_OCR_APPCODE='你的AppCode'")
        return False


def test_classifier():
    """测试文档分类器"""
    print("\n" + "=" * 60)
    print("测试3: 测试文档分类器")
    print("=" * 60)

    try:
        from doc_classifier import DocumentClassifier

        classifier = DocumentClassifier()

        # 测试用例
        test_cases = [
            ("现场测评授权书", "测评授权书"),
            ("风险告知书", "风险告知书"),
            ("情况调查表确认签字", "测评调研表"),
        ]

        all_passed = True
        for text, expected_type in test_cases:
            doc_type, _ = classifier.classify(text)
            if doc_type == expected_type:
                print(f"✓ '{text}' → {doc_type}")
            else:
                print(f"✗ '{text}' → {doc_type} (期望: {expected_type})")
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"✗ 分类器测试失败: {e}")
        return False


def test_ocr_client():
    """测试OCR客户端初始化"""
    print("\n" + "=" * 60)
    print("测试4: 测试OCR客户端")
    print("=" * 60)

    try:
        from pdf_processor import AliyunOCR

        app_code = os.getenv('ALIYUN_OCR_APPCODE')
        if not app_code:
            print("⚠ 跳过OCR测试（未配置AppCode）")
            return True

        ocr = AliyunOCR(app_code=app_code)
        print("✓ OCR客户端初始化成功")
        return True

    except Exception as e:
        print(f"✗ OCR客户端初始化失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "PDF OCR 工具测试" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    results = []

    # 运行测试
    results.append(("依赖检查", test_imports()))
    results.append(("AppCode配置", test_appcode()))
    results.append(("文档分类器", test_classifier()))
    results.append(("OCR客户端", test_ocr_client()))

    # 显示结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✓ 所有测试通过！工具可以正常使用。")
        print("\n下一步：运行 python main.py 开始处理PDF")
        return 0
    else:
        print("\n✗ 部分测试失败，请根据提示修复问题。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
