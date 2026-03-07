# OCR 引擎配置说明

**版本**: v1.5.0
**更新日期**: 2026-03-04

---

## 📋 支持的 OCR 引擎

本工具支持两种 OCR 引擎，可根据需求选择：

| 引擎 | 提供商 | 优势 | 适用场景 |
|------|--------|------|---------|
| **阿里云 OCR** | 阿里云市场 | 速度快、稳定、价格低 | 标准文档识别 |
| **DeepSeek-OCR** | SiliconFlow | 基于视觉模型、理解能力强 | 复杂布局、多语言 |

---

## 🚀 快速开始

### 1. 使用阿里云 OCR（默认）

```python
from pdf_processor import PDFProcessor

# 方式1：通过参数传入
processor = PDFProcessor(
    app_code="你的阿里云AppCode",
    ocr_engine="aliyun"  # 默认值，可省略
)

# 方式2：通过环境变量
# export ALIYUN_OCR_APPCODE="你的阿里云AppCode"
processor = PDFProcessor(ocr_engine="aliyun")
```

### 2. 使用 DeepSeek-OCR

```python
from pdf_processor import PDFProcessor

# 方式1：通过参数传入
processor = PDFProcessor(
    api_key="你的SiliconFlow API Key",
    ocr_engine="deepseek"
)

# 方式2：通过环境变量
# export SILICONFLOW_API_KEY="sk-xxxxx"
processor = PDFProcessor(ocr_engine="deepseek")
```

---

## 🔧 详细配置

### 阿里云 OCR

#### 获取 AppCode

1. 访问 [阿里云市场](https://market.aliyun.com/)
2. 搜索"通用文字识别"
3. 购买服务（有免费额度）
4. 在控制台获取 AppCode

#### 配置方式

**方式1：环境变量（推荐）**

```bash
# Linux/macOS
export ALIYUN_OCR_APPCODE="你的AppCode"

# Windows
set ALIYUN_OCR_APPCODE=你的AppCode
```

**方式2：代码传入**

```python
processor = PDFProcessor(
    app_code="你的AppCode",
    ocr_engine="aliyun"
)
```

#### 特点

- ✅ 速度快：单页识别 1-2 秒
- ✅ 稳定性高：成熟的商业服务
- ✅ 价格低：有免费额度
- ⚠️ 复杂布局识别能力一般

---

### DeepSeek-OCR

#### 获取 API Key

1. 访问 [SiliconFlow](https://siliconflow.cn/)
2. 注册账号
3. 在控制台创建 API Key
4. 复制 API Key（格式：`sk-xxxxx`）

#### 配置方式

**方式1：环境变量（推荐）**

```bash
# Linux/macOS
export SILICONFLOW_API_KEY="sk-xxxxx"

# Windows
set SILICONFLOW_API_KEY=sk-xxxxx
```

**方式2：代码传入**

```python
processor = PDFProcessor(
    api_key="sk-xxxxx",
    ocr_engine="deepseek"
)
```

#### 特点

- ✅ 理解能力强：基于 DeepSeek-VL2 视觉模型
- ✅ 复杂布局：表格、多栏、混排识别更好
- ✅ 多语言支持：中英文混合识别
- ⚠️ 速度较慢：单页识别 3-5 秒
- ⚠️ 成本较高：按 token 计费

#### API 参数

```python
# DeepSeek-OCR 使用的模型和参数
model = "deepseek-ai/DeepSeek-VL2"
max_tokens = 4096
temperature = 0.1  # 低温度保证稳定输出
top_p = 0.7
```

---

## 📊 性能对比

| 指标 | 阿里云 OCR | DeepSeek-OCR |
|------|-----------|--------------|
| 单页识别速度 | 1-2 秒 | 3-5 秒 |
| 18页PDF处理 | 30-60 秒 | 90-150 秒 |
| 标准文档准确率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 复杂布局准确率 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 表格识别 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 多语言支持 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 成本 | 低 | 中 |

---

## 💡 使用建议

### 选择阿里云 OCR 的场景

- ✅ 标准等保测评文档（推荐）
- ✅ 需要快速处理大量文档
- ✅ 预算有限
- ✅ 文档布局简单清晰

### 选择 DeepSeek-OCR 的场景

- ✅ 复杂表格文档
- ✅ 多栏布局文档
- ✅ 中英文混排文档
- ✅ 扫描质量较差的文档
- ✅ 需要更高的识别准确率

---

## 🔄 切换 OCR 引擎

### 在代码中切换

```python
# 使用阿里云 OCR
processor_aliyun = PDFProcessor(
    app_code="你的AppCode",
    ocr_engine="aliyun"
)

# 使用 DeepSeek-OCR
processor_deepseek = PDFProcessor(
    api_key="你的API Key",
    ocr_engine="deepseek"
)
```

### 通过环境变量切换

```bash
# 设置两个环境变量
export ALIYUN_OCR_APPCODE="你的AppCode"
export SILICONFLOW_API_KEY="sk-xxxxx"

# 在代码中只需指定引擎
processor = PDFProcessor(ocr_engine="aliyun")   # 使用阿里云
processor = PDFProcessor(ocr_engine="deepseek") # 使用 DeepSeek
```

---

## 🛠️ 完整示例

### 示例1：使用阿里云 OCR 处理文档

```python
#!/usr/bin/env python3
from pdf_processor import PDFProcessor

# 初始化处理器（阿里云 OCR）
processor = PDFProcessor(
    app_code="你的阿里云AppCode",
    ocr_engine="aliyun"
)

# 处理 PDF
pdf_path = "广东时代传媒.pdf"
processor.process_pdf(pdf_path)
```

### 示例2：使用 DeepSeek-OCR 处理文档

```python
#!/usr/bin/env python3
from pdf_processor import PDFProcessor

# 初始化处理器（DeepSeek-OCR）
processor = PDFProcessor(
    api_key="sk-xxxxx",
    ocr_engine="deepseek"
)

# 处理 PDF
pdf_path = "广东时代传媒.pdf"
processor.process_pdf(pdf_path)
```

### 示例3：使用环境变量

```python
#!/usr/bin/env python3
import os
from pdf_processor import PDFProcessor

# 从环境变量读取配置
ocr_engine = os.getenv("OCR_ENGINE", "aliyun")  # 默认使用阿里云

processor = PDFProcessor(ocr_engine=ocr_engine)
processor.process_pdf("广东时代传媒.pdf")
```

```bash
# 运行时指定引擎
OCR_ENGINE=aliyun python main.py    # 使用阿里云
OCR_ENGINE=deepseek python main.py  # 使用 DeepSeek
```

---

## ⚠️ 常见问题

### 1. 阿里云 OCR 报错：AppCode 无效

**原因**：AppCode 未正确设置或已过期

**解决**：
```bash
# 检查环境变量
echo $ALIYUN_OCR_APPCODE

# 重新设置
export ALIYUN_OCR_APPCODE="你的AppCode"
```

### 2. DeepSeek-OCR 报错：API Key 无效

**原因**：API Key 未正确设置或格式错误

**解决**：
```bash
# 检查环境变量
echo $SILICONFLOW_API_KEY

# 确保格式正确（以 sk- 开头）
export SILICONFLOW_API_KEY="sk-xxxxx"
```

### 3. DeepSeek-OCR 识别速度慢

**原因**：视觉模型推理需要更多时间

**解决**：
- 使用阿里云 OCR 处理标准文档
- 仅对复杂文档使用 DeepSeek-OCR
- 考虑批量处理以分摊时间成本

### 4. 识别结果不准确

**阿里云 OCR**：
- 提高扫描 DPI（默认 200，可设置为 300）
- 确保图片清晰度

**DeepSeek-OCR**：
- 调整 prompt（在 DeepSeekOCR 类中修改）
- 提高图片质量

---

## 📈 成本估算

### 阿里云 OCR

- 免费额度：通常有 500-1000 次/月
- 付费价格：约 0.001-0.005 元/次
- 18页PDF：约 0.02-0.09 元

### DeepSeek-OCR

- 按 token 计费
- 输入：约 1000 tokens/图（图片）
- 输出：约 500 tokens/页（文本）
- 价格：约 0.001 元/1K tokens
- 18页PDF：约 0.27 元

**建议**：标准文档使用阿里云 OCR，成本更低

---

## 🔗 相关文档

- [README.md](README.md) - 项目说明
- [CONFIG.md](CONFIG.md) - 高级配置
- [QUICKSTART.md](QUICKSTART.md) - 快速开始

---

**版本**: v1.5.0
**更新日期**: 2026-03-04
**开发单位**: 广东中科实数科技有限公司
