# 快速开始指南

## 5分钟上手

### 第一步：安装依赖（1分钟）

```bash
cd pdf-ocr-tool
pip install -r requirements.txt
```

### 第二步：配置 OCR 引擎（30秒）

任选其一：

```bash
# 方式1：百度飞桨 PaddleOCR-VL-1.5（推荐，免费额度）
export BAIDU_PADDLEOCR_TOKEN="你的Token"

# 方式2：阿里云 OCR
export ALIYUN_OCR_APPCODE="你的AppCode"
```

> Token 获取：访问 https://aistudio.baidu.com/paddleocr/task

### 第三步：运行程序（30秒）

```bash
python main.py               # 自动检测引擎
python main.py --ocr baidu   # 或指定百度飞桨
```

### 第四步：输入信息（1分钟）

```
请输入 PDF 文件路径: 你的文件.pdf
请输入项目名称（可选）: JDB25245-项目名称
请输入系统名称（可选）: 系统名称
请输入输出目录（默认为当前目录）: ./output
```

### 第五步：等待处理（1-2分钟）

程序会自动：
1. 拆分PDF
2. 识别文档类型
3. 显示处理摘要
4. 询问是否归档

输入 `y` 确认归档。

### 完成！

查看 `output/` 目录，所有文档已按类型归档。

---

## 常见问题速查

### Q: 提示"请设置 OCR 引擎"？

A: 设置任一引擎的环境变量：
```bash
# 百度飞桨（推荐）
export BAIDU_PADDLEOCR_TOKEN="你的Token"

# 或阿里云 OCR
export ALIYUN_OCR_APPCODE="你的AppCode"
```

### Q: 提示"requests 库未安装"？

A: 运行：
```bash
pip install requests
```

### Q: 提示"PyMuPDF 未安装"？

A: 运行：
```bash
pip install PyMuPDF
```

### Q: 文档识别不准确？

A: 查看 `EXAMPLES.md` 中的"示例5：自定义分类规则"。

### Q: 想批量处理多个PDF？

A: 目前需要逐个处理，或参考 `EXAMPLES.md` 中的批处理脚本。

---

## 下一步

- 📖 阅读 [README.md](README.md) 了解详细功能
- 📝 查看 [EXAMPLES.md](EXAMPLES.md) 学习使用示例
- ⚙️ 参考 [CONFIG.md](CONFIG.md) 进行高级配置
- 📋 查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史

---

## 获取帮助

如有问题，请联系技术支持团队。
