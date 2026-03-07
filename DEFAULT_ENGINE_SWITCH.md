# 默认 OCR 引擎切换说明

**切换日期**: 2026-03-04
**原默认引擎**: 阿里云 OCR
**新默认引擎**: DeepSeek-OCR

---

## ✅ 已完成的修改

### 1. PDFProcessor 默认参数

**文件**: `pdf_processor.py:236`

**修改前**:
```python
def __init__(
    self,
    ocr_engine: str = "aliyun",  # 默认阿里云
    ...
):
```

**修改后**:
```python
def __init__(
    self,
    ocr_engine: str = "deepseek",  # 默认 DeepSeek
    ...
):
```

### 2. 主程序提示信息

**文件**: `pdf_processor.py:840`

**修改前**:
```python
print("使用阿里云 OCR API")
```

**修改后**:
```python
print("使用 DeepSeek-OCR（高精度视觉模型）")
```

### 3. 文档更新

- ✅ README.md - 更新技术特点说明
- ✅ CURRENT_CONFIG.md - 标注为默认引擎
- ✅ DEFAULT_ENGINE_SWITCH.md - 本文档

---

## 🎯 影响范围

### 对现有代码的影响

**无影响的场景**:
- 显式指定引擎的代码不受影响
- 环境变量配置不受影响

**有影响的场景**:
- 未指定 `ocr_engine` 参数的代码，现在默认使用 DeepSeek-OCR

### 示例

**场景1：显式指定引擎（无影响）**
```python
# 这些代码不受影响
processor = PDFProcessor(ocr_engine="aliyun")   # 仍使用阿里云
processor = PDFProcessor(ocr_engine="deepseek") # 仍使用 DeepSeek
```

**场景2：使用默认引擎（有影响）**
```python
# 修改前：使用阿里云 OCR
processor = PDFProcessor()

# 修改后：使用 DeepSeek-OCR
processor = PDFProcessor()
```

**场景3：命令行运行（有影响）**
```bash
# 修改前：显示"使用阿里云 OCR API"
python main.py

# 修改后：显示"使用 DeepSeek-OCR（高精度视觉模型）"
python main.py
```

---

## 🔄 如何切换回阿里云 OCR

如果需要使用阿里云 OCR，有以下方式：

### 方式1：代码中指定

```python
from pdf_processor import PDFProcessor

processor = PDFProcessor(
    app_code="你的AppCode",
    ocr_engine="aliyun"
)
```

### 方式2：修改默认值

编辑 `pdf_processor.py:236`，将默认值改回：
```python
ocr_engine: str = "aliyun"
```

---

## 📊 性能对比

| 指标 | 阿里云 OCR | DeepSeek-OCR (默认) |
|------|-----------|---------------------|
| 速度 | 1-2秒/页 | 3-5秒/页 |
| 精度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 复杂布局 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 表格识别 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 成本 | 低 | 中 |

---

## 💡 切换原因

1. **更高的识别精度**
   - DeepSeek-VL2 是先进的视觉语言模型
   - 对复杂布局和表格识别更准确

2. **更好的等保文档支持**
   - 等保测评文档通常包含复杂表格
   - DeepSeek-OCR 在这类文档上表现更好

3. **已配置 API Key**
   - SiliconFlow API Key 已配置到环境变量
   - 可以直接使用，无需额外配置

4. **保持灵活性**
   - 仍然支持阿里云 OCR
   - 可以根据需要随时切换

---

## ⚠️ 注意事项

1. **速度变化**
   - DeepSeek-OCR 比阿里云 OCR 慢 2-3 倍
   - 18页 PDF 处理时间从 30-60秒 增加到 90-150秒

2. **成本变化**
   - DeepSeek-OCR 按 token 计费
   - 成本约为阿里云 OCR 的 3-5 倍

3. **API Key 配置**
   - 确保 SILICONFLOW_API_KEY 环境变量已设置
   - 新终端会自动加载（已写入 ~/.zshrc）

4. **向后兼容**
   - 所有现有代码仍然可以正常工作
   - 只是默认引擎发生变化

---

## 🧪 验证切换

运行以下命令验证切换成功：

```bash
cd /Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool

# 检查默认引擎
python -c "from pdf_processor import PDFProcessor; p = PDFProcessor(); print(f'默认引擎: {p.ocr_engine}')"

# 预期输出：默认引擎: deepseek
```

---

## 📚 相关文档

- [OCR_ENGINES.md](OCR_ENGINES.md) - OCR 引擎详细说明
- [CURRENT_CONFIG.md](CURRENT_CONFIG.md) - 当前配置
- [README.md](README.md) - 项目说明

---

**切换日期**: 2026-03-04
**状态**: ✅ 已完成
