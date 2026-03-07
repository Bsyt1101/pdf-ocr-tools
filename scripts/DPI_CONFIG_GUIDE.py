#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不同场景的 DPI 和图片尺寸配置建议
"""

# 场景配置建议
SCENE_CONFIGS = {
    "标准文档": {
        "dpi": 200,
        "max_size": 1024,
        "说明": "适用于大部分标准打印文档，文字清晰，页眉在顶部",
        "优点": "速度快，准确率高，token 消耗适中",
        "适用": "等保测评文档、合同、报告等标准文档"
    },

    "小字文档": {
        "dpi": 250,
        "max_size": 1280,
        "说明": "适用于包含小字、页眉页脚的文档",
        "优点": "能识别更小的文字",
        "缺点": "可能导致页眉被裁剪（需要测试）",
        "适用": "包含大量小字注释的文档"
    },

    "高质量扫描": {
        "dpi": 150,
        "max_size": 800,
        "说明": "适用于高质量扫描件，原始图片已经很清晰",
        "优点": "速度最快，token 消耗最少",
        "适用": "现代扫描仪生成的高质量 PDF"
    },

    "低质量扫描": {
        "dpi": 300,
        "max_size": 1536,
        "说明": "适用于老旧、模糊的扫描件",
        "优点": "最大化识别准确率",
        "缺点": "速度慢，可能超过 token 限制",
        "适用": "传真件、老旧文档、拍照文档"
    },

    "横向页面": {
        "dpi": 200,
        "max_size": 1024,
        "说明": "横向页面会自动旋转，使用标准配置即可",
        "注意": "竖排文字可能识别困难"
    }
}

# 当前推荐配置（基于测试结果）
RECOMMENDED_CONFIG = {
    "dpi": 200,
    "max_size": 1024,
    "原因": [
        "DPI 200 能识别出页眉文件编号",
        "max_size 1024 不会裁剪页眉",
        "DPI 250 + max_size 1280 会导致页眉丢失",
        "速度和准确率的最佳平衡点"
    ]
}

if __name__ == "__main__":
    print("=" * 80)
    print("DPI 和图片尺寸配置建议")
    print("=" * 80)

    for scene, config in SCENE_CONFIGS.items():
        print(f"\n【{scene}】")
        print(f"  DPI: {config['dpi']}")
        print(f"  图片尺寸: {config['max_size']}px")
        print(f"  说明: {config['说明']}")
        if '优点' in config:
            print(f"  优点: {config['优点']}")
        if '缺点' in config:
            print(f"  缺点: {config['缺点']}")
        if '适用' in config:
            print(f"  适用: {config['适用']}")
        if '注意' in config:
            print(f"  注意: {config['注意']}")

    print("\n" + "=" * 80)
    print("当前推荐配置（基于实际测试）")
    print("=" * 80)
    print(f"DPI: {RECOMMENDED_CONFIG['dpi']}")
    print(f"图片尺寸: {RECOMMENDED_CONFIG['max_size']}px")
    print("\n原因:")
    for reason in RECOMMENDED_CONFIG['原因']:
        print(f"  • {reason}")
