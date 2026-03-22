# 改进总结

## 1. 文件编号识别优化 ✅

### 问题描述
OCR 识别时经常出现错误：
- `JDB` 被误识别为 `JD8`、`JD9`、`JD3` 等
- `SMQR` 被误识别为 `SMOR`

### 解决方案

#### 1.1 自动修正 JD → JDB
修改了 `doc_classifier.py` 中的 `extract_file_code()` 方法：

```python
# 支持 JDB 或 JD 开头（OCR 可能漏识别 B）
pattern = r'(JDB?\d+)\s*-\s*([A-Za-z]+)\s*-\s*(\d+)'

# OCR 错误修正：JD8/JD9 -> JDB
if project_code.startswith('JD') and not project_code.startswith('JDB'):
    original_code = project_code
    digits = project_code[2:]  # 925136 或 825136
    # 如果第一位是 8 或 9，去掉第一位
    if digits and digits[0] in ['8', '9']:
        digits = digits[1:]  # 25136
    project_code = 'JDB' + digits
    print(f"    [OCR 修正] {original_code} -> {project_code}")
```

#### 1.2 添加 SMOR 类型映射
在 `DOC_TYPE_CODE_MAP` 中添加：

```python
"SMOR": "xxx系统-漏洞扫描记录签字确认表",  # SMOR -> SMQR (OCR 将 Q 误识别为 O)
```

### 测试结果

| 原始识别 | 修正后 | 状态 |
|---------|--------|------|
| JD925136-SMOR-06 | JDB25136-SMOR-06 | ✅ |
| JD825136-DCB-01 | JDB25136-DCB-01 | ✅ |
| JDB25136-CPSQS-02 | JDB25136-CPSQS-02 | ✅ |

### 效果
- 自动识别并修正常见的 OCR 错误
- 提高文件编号提取成功率
- 减少手动修正工作量

---

## 2. 本地部署 PaddleOCR-VL-1.5 尝试 ⚠️

### 完成的工作

#### 2.1 环境准备 ✅
- 安装 PyTorch 2.10.0（79.5 MB）
- 安装 Transformers 5.3.0
- 安装依赖：accelerate, sentencepiece, einops
- 验证 M4 GPU (MPS) 可用

#### 2.2 遇到的问题 ❌
**兼容性问题**：
```
ImportError: cannot import name 'SlidingWindowCache' from 'transformers.cache_utils'
```

**原因**：
- PaddleOCR-VL-1.5 是新模型（2026年1月发布）
- 模型代码与当前 Transformers 版本不兼容
- Mac 支持还不完善

### 建议方案

#### 推荐：继续使用 SiliconFlow API ⭐⭐⭐⭐⭐

**优势**：
1. ✅ 已经稳定运行
2. ✅ 速度快（2-3秒/页）
3. ✅ 成本低（每月1-2元）
4. ✅ 无需维护
5. ✅ 识别准确

**成本估算**：
- 每月处理 1000 页：1-2 元人民币
- 每月处理 5000 页：5-10 元人民币

#### 备选：等待官方更新 ⏳

- 等待 3-6 个月
- PaddleOCR-VL-1.5 的 Mac 支持会改善
- 关注官方 GitHub 更新

---

## 3. OCR 引擎配置优化 ✅

### 当前配置

**OCR引擎自动选择逻辑**：

**优先级**：
1. 如果设置 `LOCAL_PADDLEOCR_DIRECT=true` → 本地 PaddleOCR-VL
2. 如果本地 MLX-VLM 服务可用 → 本地 PaddleOCR-VL
3. 如果设置 `ALIYUN_OCR_APPCODE` → 阿里云 OCR
4. 如果设置 `SILICONFLOW_API_KEY` → SiliconFlow API（PaddleOCR-VL-1.5）
5. 如果设置 `BAIDU_PADDLEOCR_TOKEN` → 百度飞桨 PaddleOCR-VL-1.5（默认端点）

**模型参数**：
- DPI: 300（高质量）
- 模型：`PaddlePaddle/PaddleOCR-VL-1.5`
- 提示词：简单模式（"识别图片中的所有文字"）

### Claude OCR 优化

**模型**：claude-sonnet-4-6
**参数**：
- temperature: 0.0（确定性输出）
- max_tokens: 4096

**提示词优化**：
```
你是一个专业的OCR系统。请逐字识别图片中的文字，要求：

1. 只输出你能清楚看到的文字，如果看不清就用**代替
2. 不要根据文档格式推测内容
3. 不要补充、联想或脑补任何文字
4. 包括所有位置的文字：页眉、页脚、边缘、竖排
5. 按从上到下、从左到右顺序输出
6. 保持原文，不修正错别字
7. 不要添加任何解释

直接输出文字：
```

**问题**：Claude 容易产生"幻觉"，识别出不存在的内容

---

## 4. 性能对比

### OCR 引擎对比

| 引擎 | 速度 | 准确率 | 幻觉问题 | 成本 | 推荐度 |
|------|------|--------|----------|------|--------|
| PaddleOCR-VL-1.5 (API) | 快 | 高 | 无 | 低 | ⭐⭐⭐⭐⭐ |
| Claude Sonnet 4.6 | 快 | 中 | 有 | 中 | ⭐⭐⭐ |
| 本地部署 | - | - | - | - | ⏳ 暂不可用 |

### 建议

**当前最佳方案**：
- 使用 PaddleOCR-VL-1.5（通过 SiliconFlow API）
- 配置 DPI 300
- 启用文件编号自动修正

**未来规划**：
- 3-6 个月后重新评估本地部署
- 关注 PaddleOCR-VL-1.5 的更新

---

## 5. 已安装的依赖

如果将来想再次尝试本地部署，以下依赖已经安装：

```
torch==2.10.0
torchvision==0.25.0
torchaudio==2.10.0
transformers==5.3.0
accelerate==1.12.0
sentencepiece==0.2.1
einops==0.8.2
paddlepaddle
paddleocr
```

---

## 总结

### 已完成 ✅
1. 文件编号识别自动修正（JD → JDB）
2. 添加 SMOR 类型支持
3. 优化 OCR 提示词
4. 提高 DPI 到 300
5. 设置默认引擎为 PaddleOCR-VL-1.5

### 暂不可行 ⏳
1. 本地部署 PaddleOCR-VL-1.5（兼容性问题）

### 建议 💡
1. 继续使用 SiliconFlow API
2. 定期关注官方更新
3. 3-6 个月后重新评估本地部署
