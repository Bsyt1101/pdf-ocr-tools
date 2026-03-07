#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 文档自动拆分和归档工具 - 主入口

使用方法:
    python main.py [--ocr {local,aliyun,siliconflow}]

示例:
    python main.py --ocr local
    python main.py --ocr aliyun
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pdf_processor import main

if __name__ == "__main__":
    main()
