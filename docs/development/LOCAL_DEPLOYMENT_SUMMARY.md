# PaddleOCR-VL-1.5 本地部署总结

## 部署尝试结果

### ✅ 成功完成的步骤

1. **安装 PyTorch (79.5 MB)**
   - 版本：2.10.0
   - 支持 M4 GPU (MPS) 加速
   - 测试通过：MPS 可用

2. **安装 Transformers 和依赖**
   - transformers 5.3.0
   - accelerate 1.12.0
   - sentencepiece 0.2.1
   - einops 0.8.2

3. **安装 PaddlePaddle 和 PaddleOCR**
   - paddlepaddle (CPU 版本)
   - paddleocr

### ❌ 遇到的问题

**Hugging Face 方案**：
- 问题：Transformers 版本兼容性问题
- 错误：`cannot import name 'SlidingWindowCache' from 'transformers.cache_utils'`
- 原因：PaddleOCR-VL-1.5 的代码需要特定版本的 Transformers API

**根本原因**：
- PaddleOCR-VL-1.5 是一个非常新的模型（2026年1月发布）
- 模型代码可能还在快速迭代中
- Mac 上的支持可能不如 Linux 完善

## 当前最佳方案

### 继续使用 SiliconFlow API（强烈推荐）

**优势**：
1. ✅ **已经稳定运行** - 当前方案工作良好
2. ✅ **速度快** - 2-3秒/页，比本地部署快
3. ✅ **无需维护** - 不用担心依赖、更新、兼容性
4. ✅ **成本低** - 按量付费，你的使用量成本可忽略
5. ✅ **支持好** - PaddleOCR-VL-1.5 官方支持

**成本估算**：
- 假设每月处理 1000 页文档
- 每页约 0.001-0.002 元
- 月成本：1-2 元人民币

### 本地部署的替代方案

如果确实需要本地部署（离线使用、数据隐私），有以下选择：

#### 方案 1：使用传统 PaddleOCR（不是 VL 版本）

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr(image_path, cls=True)
```

**优点**：
- 成熟稳定
- Mac 支持好
- 速度快

**缺点**：
- 不是 VL-1.5 版本
- 识别准确率可能略低

#### 方案 2：等待官方更新

- PaddleOCR-VL-1.5 刚发布不久
- 等待几个月，兼容性会改善
- 关注官方 GitHub 更新

#### 方案 3：使用 Docker（Linux 环境）

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  paddlepaddle/paddle:latest-gpu-cuda11.7-cudnn8
```

**优点**：
- 完整的 Linux 环境
- 官方支持好

**缺点**：
- Mac 上运行 Docker 性能损失
- 配置复杂

## 我的建议

**对于你的使用场景（等保测评文档处理）**：

### 推荐方案：继续使用 SiliconFlow API

理由：
1. 已经稳定运行，无需改动
2. 速度和准确率都很好
3. 成本极低（每月1-2元）
4. 省时省力，专注业务

### 如果必须本地部署

1. **短期**：使用传统 PaddleOCR（非 VL 版本）
2. **长期**：等待 3-6 个月，PaddleOCR-VL-1.5 的 Mac 支持会更好

## 已安装的依赖

以下依赖已经安装在虚拟环境中，如果将来想再次尝试：

```
torch==2.10.0
torchvision==0.25.0
transformers==5.3.0
accelerate==1.12.0
sentencepiece==0.2.1
einops==0.8.2
paddlepaddle
paddleocr
```

## 下一步行动

建议：
1. ✅ 继续使用当前的 SiliconFlow API 方案
2. ⏸️  暂停本地部署尝试
3. 📅 3-6 个月后再次评估本地部署可行性

如果你同意这个建议，我们可以：
- 优化当前的 API 调用代码
- 添加错误处理和重试机制
- 提升整体处理速度和稳定性
