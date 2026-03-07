#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试本地 PaddleOCR-VL-1.5 模型
"""

import torch
from PIL import Image
import time

def test_local_ocr():
    """测试本地 PaddleOCR-VL-1.5"""

    print("=" * 80)
    print("测试本地 PaddleOCR-VL-1.5 模型")
    print("=" * 80)

    # 检查设备
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"\n使用设备: {device}")

    # 加载模型（首次运行会自动下载，约 3-4GB）
    print("\n正在加载模型...")
    print("提示：首次运行会从 Hugging Face 下载模型（约 3-4GB），请耐心等待...")

    start_time = time.time()

    try:
        from transformers import AutoModel, AutoTokenizer

        model_name = "PaddlePaddle/PaddleOCR-VL-1.5"

        # 加载 tokenizer
        print("  - 加载 tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        # 加载模型
        print("  - 加载模型...")
        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "mps" else torch.float32
        )

        # 移动到设备
        if device == "mps":
            model = model.to(device)

        load_time = time.time() - start_time
        print(f"\n✓ 模型加载成功！耗时: {load_time:.2f} 秒")

        # 测试 OCR
        test_image_path = "/tmp/page26_preview.png"

        if not os.path.exists(test_image_path):
            print(f"\n⚠️  测试图片不存在: {test_image_path}")
            print("请先运行主程序生成测试图片")
            return

        print(f"\n正在识别图片: {test_image_path}")
        print("-" * 80)

        # 读取图片
        image = Image.open(test_image_path)
        print(f"图片尺寸: {image.size}")

        # OCR 识别
        ocr_start = time.time()

        # 准备输入
        prompt = "识别图片中的所有文字"
        inputs = tokenizer(
            prompt,
            images=image,
            return_tensors="pt"
        )

        if device == "mps":
            inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v
                     for k, v in inputs.items()}

        # 生成结果
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=False
            )

        # 解码结果
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        ocr_time = time.time() - ocr_start

        print(f"\n✓ OCR 识别完成！耗时: {ocr_time:.2f} 秒")
        print("\n识别结果:")
        print("=" * 80)
        print(result)
        print("=" * 80)

        print(f"\n识别文本长度: {len(result)} 字符")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()

        print("\n可能的原因:")
        print("1. 网络问题：无法从 Hugging Face 下载模型")
        print("2. 内存不足：模型需要约 2-3GB 内存")
        print("3. 依赖问题：缺少某些依赖库")

        print("\n建议:")
        print("- 检查网络连接")
        print("- 确保有足够的磁盘空间（至少 5GB）")
        print("- 或者继续使用 SiliconFlow API")


if __name__ == "__main__":
    import os
    test_local_ocr()
