# 当前 OCR 配置

**配置日期**: 2026-03-05
**配置状态**: ✅ 多OCR引擎已配置
**默认引擎**: 根据环境变量自动选择
**OCR 并发数**: 5（v1.5.1）

---

## 📋 OCR 引擎选择逻辑

工具会根据环境变量自动选择OCR引擎，优先级如下：

1. **优先级 1**: 如果设置了 `ALIYUN_OCR_APPCODE` → 使用 **阿里云 OCR**（推荐）
2. **优先级 2**: 如果设置了 `SILICONFLOW_API_KEY` → 使用 **PaddleOCR-VL-1.5**
3. **优先级 3**: 如果设置了 `ANTHROPIC_API_KEY` → 使用 **Claude Sonnet 4.6**
4. **默认**: 如果都没设置 → 使用 **阿里云 OCR**（需要配置 `ALIYUN_OCR_APPCODE`）

---

## 🎯 已配置的引擎

### 阿里云 OCR ⭐⭐⭐⭐⭐ (推荐)

- **状态**: 可配置
- **AppCode**: 需要配置
- **速度**: 1-2秒/页
- **精度**: ⭐⭐⭐⭐
- **幻觉问题**: 无
- **成本**: 低
- **适用场景**: 标准文档（推荐）

### PaddleOCR-VL-1.5 ⭐⭐⭐⭐

- **状态**: 已配置
- **API Key**: sk-dmhuq...（已写入 ~/.zshrc）
- **模型**: PaddlePaddle/PaddleOCR-VL-1.5
- **提供商**: SiliconFlow
- **速度**: 2-3秒/页
- **精度**: ⭐⭐⭐⭐⭐
- **幻觉问题**: 无
- **成本**: 低（每月1-2元处理1000页）
- **适用场景**: 复杂布局、高精度需求

### Claude Sonnet 4.6 ⭐⭐⭐

- **状态**: 已配置
- **API Key**: 已写入 ~/.zshrc
- **模型**: claude-sonnet-4-6
- **速度**: 2-3秒/页
- **精度**: ⭐⭐⭐
- **幻觉问题**: 有（可能识别出不存在的内容）
- **成本**: 中
- **适用场景**: 备用方案

---

## 🚀 使用方法

### 方式1：使用默认配置（推荐）

```python
from pdf_processor import PDFProcessor

# 直接初始化，自动根据环境变量选择OCR引擎
# 优先级：ALIYUN_OCR_APPCODE > SILICONFLOW_API_KEY > ANTHROPIC_API_KEY
processor = PDFProcessor()
processor.process_pdf("文档.pdf")
```

### 方式2：显式指定引擎

```python
from pdf_processor import PDFProcessor

# 使用阿里云 OCR（推荐）
processor = PDFProcessor(ocr_engine="aliyun")

# 使用 PaddleOCR-VL-1.5
processor = PDFProcessor(ocr_engine="deepseek")

# 使用 Claude Sonnet 4.6
processor = PDFProcessor(ocr_engine="claude")

# 使用阿里云 OCR
processor = PDFProcessor(ocr_engine="aliyun")
```

### 方式3：命令行直接运行

```bash
cd /Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool
python main.py
```

程序会显示当前使用的OCR引擎：
```
============================================================
PDF 文档自动拆分和重命名工具
使用 阿里云 OCR（快速稳定）
============================================================
```

---

## 🔧 验证配置

运行配置检查脚本：

```bash
cd /Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool
python check_ocr_config.py
```

预期输出：
```
✓ ALIYUN_OCR_APPCODE: xxxxx
✓ 阿里云 OCR 初始化成功
```

或

```
✓ SILICONFLOW_API_KEY: sk-dmhuq...
✓ PaddleOCR-VL-1.5 初始化成功
```

或

```
✓ ANTHROPIC_API_KEY: sk-ant-...
✓ Claude Sonnet 4.6 初始化成功
```

---

## 📝 配置文件位置

- **配置文件**: `~/.zshrc`
- **配置行**:
  ```bash
  # 阿里云 OCR AppCode（推荐）
  export ALIYUN_OCR_APPCODE="xxxxx"

  # SiliconFlow API Key for PaddleOCR-VL-1.5
  export SILICONFLOW_API_KEY="your_siliconflow_api_key_here"

  # Anthropic API Key for Claude Sonnet 4.6
  export ANTHROPIC_API_KEY="sk-ant-xxxxx"
  ```

---

## 🔄 重新加载配置

如果修改了 `~/.zshrc`，需要重新加载：

```bash
source ~/.zshrc
```

或者打开新的终端窗口。

---

## ⚠️ 安全提示

1. **不要分享 API Key**
   - API Key 已配置在本地环境变量中
   - 不要将 API Key 提交到版本控制系统
   - 不要在公开场合分享

2. **定期检查使用量**
   - 访问 [SiliconFlow 控制台](https://siliconflow.cn/) 查看使用情况
   - 监控 API 调用次数和费用

3. **备份配置**
   - 建议备份 `~/.zshrc` 文件
   - 记录 API Key 到安全的地方

---

## 📊 性能对比

| 引擎 | 速度 | 精度 | 幻觉问题 | 成本 | 推荐度 |
|------|------|------|----------|------|--------|
| 阿里云 OCR | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 无 | 低 | ⭐⭐⭐⭐⭐ |
| PaddleOCR-VL-1.5 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 无 | 低 | ⭐⭐⭐⭐ |
| Claude Sonnet 4.6 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 有 | 中 | ⭐⭐⭐ |

### 阿里云 OCR（推荐）

- **速度**: 1-2 秒/页
- **精度**: ⭐⭐⭐⭐
- **成本**: 低
- **适用场景**:
  - ✅ 标准文档
  - ✅ 快速处理
  - ✅ 成本敏感场景

### PaddleOCR-VL-1.5

- **速度**: 2-3 秒/页
- **精度**: ⭐⭐⭐⭐⭐
- **成本**: 每月1-2元（处理1000页）
- **适用场景**:
  - ✅ 复杂表格文档
  - ✅ 多栏布局文档
  - ✅ 中英文混排文档
  - ✅ 扫描质量较差的文档

### Claude Sonnet 4.6

- **速度**: 2-3 秒/页
- **精度**: ⭐⭐⭐
- **幻觉问题**: 可能识别出不存在的内容
- **适用场景**: 备用方案

---

## 🔗 相关文档

- [OCR_ENGINES.md](OCR_ENGINES.md) - OCR 引擎详细说明
- [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) - 改进总结
- [LOCAL_DEPLOYMENT_SUMMARY.md](LOCAL_DEPLOYMENT_SUMMARY.md) - 本地部署尝试总结
- [example_deepseek_ocr.py](example_deepseek_ocr.py) - 使用示例

---

## 💡 使用建议

1. **推荐配置**
   - 优先使用阿里云 OCR（速度快、稳定、成本低）
   - 设置 ALIYUN_OCR_APPCODE 环境变量
   - 适合大部分标准文档处理场景

2. **高精度需求**
   - 使用 PaddleOCR-VL-1.5（精度最高）
   - 设置 SILICONFLOW_API_KEY 环境变量
   - 成本：每月1-2元（处理1000页）
   - 适合复杂布局、表格文档

3. **首次使用**
   - 先用小文档测试（1-2页）
   - 验证识别效果
   - 确认 API 调用正常

4. **批量处理**
   - 注意 API 调用频率限制
   - 监控成本
   - 阿里云 OCR 适合大批量快速处理

4. **故障排查**
   - 运行 `check_ocr_config.py` 检查配置
   - 查看错误日志
   - 确认网络连接正常
   - 检查环境变量是否正确设置

---

**配置日期**: 2026-03-05
**配置人**: pr0xy
**版本**: v1.5.1
**状态**: ✅ 已完成
