# 当前 OCR 配置

**配置日期**: 2026-03-22
**配置状态**: ✅ 多OCR引擎已配置
**默认引擎**: 根据环境变量自动选择
**当前版本**: v1.7.2

---

## 📋 OCR 引擎选择逻辑

工具会根据环境变量自动选择OCR引擎，优先级如下：

1. **优先级 1**: 如果设置了 `LOCAL_PADDLEOCR_DIRECT=true` → 使用 **本地 PaddleOCR-VL**（直接加载）
2. **优先级 2**: 如果本地 MLX-VLM 服务可用 → 使用 **本地 PaddleOCR-VL**（HTTP 服务）
3. **优先级 3**: 如果设置了 `ALIYUN_OCR_APPCODE` → 使用 **阿里云 OCR**
4. **优先级 4**: 如果设置了 `SILICONFLOW_API_KEY` → 使用 **SiliconFlow API**（PaddleOCR-VL-1.5）
5. **优先级 5**: 如果设置了 `BAIDU_PADDLEOCR_TOKEN` → 使用 **百度飞桨 PaddleOCR-VL-1.5**（默认端点，无需配置 URL）

---

## 🎯 已配置的引擎

### 本地 PaddleOCR-VL ⭐⭐⭐⭐⭐

- **状态**: 可配置
- **环境变量**: `LOCAL_PADDLEOCR_DIRECT=true`
- **速度**: 2-3秒/页
- **精度**: ⭐⭐⭐⭐⭐
- **成本**: 免费
- **隐私**: 完全本地
- **并发数**: 1
- **适用场景**: 数据隐私要求高、标准文档

### 百度飞桨 PaddleOCR-VL-1.5 ⭐⭐⭐⭐⭐

- **状态**: 可配置
- **环境变量**: `BAIDU_PADDLEOCR_TOKEN`（必填）、`BAIDU_PADDLEOCR_URL`（可选，默认 VL-1.5）
- **模型**: PaddleOCR-VL-1.5（默认），也支持 VL、PP-OCRv5、PP-StructureV3
- **提供商**: 百度 AI Studio
- **解析模式**: 同步解析（逐页调用，实时返回）
- **速度**: 1-3秒/页
- **精度**: ⭐⭐⭐⭐⭐（94.5%，OmniDocBench v1.5）
- **成本**: 免费额度
- **并发数**: 2
- **适用场景**: 扫描件、拍照件、复杂版面、印章识别

### 阿里云 OCR ⭐⭐⭐⭐

- **状态**: 可配置
- **环境变量**: `ALIYUN_OCR_APPCODE`
- **速度**: 1-2秒/页
- **精度**: ⭐⭐⭐⭐
- **成本**: 低
- **并发数**: 3
- **适用场景**: 标准文档、快速处理

### SiliconFlow API ⭐⭐⭐⭐

- **状态**: 可配置
- **环境变量**: `SILICONFLOW_API_KEY`
- **模型**: PaddlePaddle/PaddleOCR-VL-1.5
- **提供商**: SiliconFlow
- **速度**: 2-4秒/页
- **精度**: ⭐⭐⭐⭐⭐
- **成本**: 有免费额度
- **并发数**: 3
- **适用场景**: 复杂布局、高精度需求

---

## 🚀 使用方法

### 方式1：命令行指定引擎

```bash
python main.py --ocr local       # 本地 PaddleOCR-VL
python main.py --ocr baidu       # 百度飞桨 PaddleOCR-VL-1.5
python main.py --ocr aliyun      # 阿里云 OCR
python main.py --ocr siliconflow # SiliconFlow API
python main.py                   # 自动检测（按优先级选择）
```

### 方式2：代码中指定引擎

```python
from pdf_processor import PDFProcessor

processor = PDFProcessor(ocr_engine="baidu")      # 百度飞桨
processor = PDFProcessor(ocr_engine="local")      # 本地 PaddleOCR-VL
processor = PDFProcessor(ocr_engine="aliyun")     # 阿里云 OCR
processor = PDFProcessor(ocr_engine="siliconflow") # SiliconFlow API
```

---

## 📝 环境变量配置

在 `~/.zshrc` 中添加需要的环境变量：

```bash
# 百度飞桨 PaddleOCR（只需 TOKEN，默认使用 VL-1.5）
export BAIDU_PADDLEOCR_TOKEN="你的Token"
# export BAIDU_PADDLEOCR_URL="可选，自定义API地址"

# 本地 PaddleOCR-VL
# export LOCAL_PADDLEOCR_DIRECT=true

# 阿里云 OCR
# export ALIYUN_OCR_APPCODE="你的AppCode"

# SiliconFlow API
# export SILICONFLOW_API_KEY="sk-xxxxx"
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

> 注：识别速度受设备性能、网络状况等因素影响，以下数据仅供参考。

| 引擎 | 速度 | 精度 | 成本 | 并发数 | 推荐度 |
|------|------|------|------|--------|--------|
| 本地 PaddleOCR-VL | 2-3秒/页 | ⭐⭐⭐⭐⭐ | 免费 | 1 | ⭐⭐⭐⭐⭐ |
| 百度飞桨 VL-1.5 | 1-3秒/页 | ⭐⭐⭐⭐⭐ | 免费额度 | 2 | ⭐⭐⭐⭐⭐ |
| 阿里云 OCR | 1-2秒/页 | ⭐⭐⭐⭐ | 低 | 3 | ⭐⭐⭐⭐ |
| SiliconFlow API | 2-4秒/页 | ⭐⭐⭐⭐⭐ | 免费额度 | 3 | ⭐⭐⭐⭐ |

---

## 🔗 相关文档

- [OCR_ENGINES.md](../guides/OCR_ENGINES.md) - OCR 引擎详细说明
- [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) - 改进总结

---

## 💡 使用建议

1. **免费 + 高精度** → 百度飞桨 PaddleOCR-VL-1.5（只需设置 TOKEN）
2. **免费 + 隐私保护** → 本地 PaddleOCR-VL
3. **速度优先** → 阿里云 OCR
4. **首次使用** → 先用小文档测试（1-2页），确认识别效果

---

**配置日期**: 2026-03-22
**版本**: v1.7.2
**状态**: ✅ 已完成
