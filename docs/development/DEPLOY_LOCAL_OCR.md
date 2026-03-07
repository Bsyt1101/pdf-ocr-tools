# 本地部署 PaddleOCR-VL-1.5 快速指南

## 推荐方案：使用 Hugging Face Transformers

你的 MacBook Air M4 (16GB RAM) 完全可以运行这个 0.9B 参数的模型。

## 快速开始

### 1. 安装依赖（约 5 分钟）

```bash
cd /Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf
source venv/bin/activate

# 安装 PyTorch（支持 M4 GPU 加速）
pip install torch torchvision

# 安装 Transformers 和其他依赖
pip install transformers accelerate sentencepiece protobuf
```

### 2. 测试是否支持 GPU 加速

```bash
python -c "import torch; print('MPS 可用:', torch.backends.mps.is_available())"
```

如果输出 `MPS 可用: True`，说明可以使用 M4 的 GPU 加速。

### 3. 下载并测试模型

首次运行会自动下载模型（约 3-4GB），需要良好的网络连接。

**注意**：由于网络原因，从 Hugging Face 下载可能较慢。建议：
- 使用镜像站点（如 hf-mirror.com）
- 或者继续使用 SiliconFlow API（已经很快了）

## 性能对比

| 方式 | 速度 | 成本 | 网络依赖 | 推荐度 |
|------|------|------|----------|--------|
| SiliconFlow API | 快（2-3秒/页） | 低（按量付费） | 需要 | ⭐⭐⭐⭐⭐ |
| 本地部署 | 中等（5-10秒/页） | 无 | 仅首次下载 | ⭐⭐⭐ |

## 建议

**对于你的使用场景（等保测评文档处理）**：

1. **继续使用 SiliconFlow API**（当前方案）
   - 优点：速度快、无需维护、成本低
   - 缺点：需要网络连接
   
2. **本地部署作为备用**
   - 优点：离线可用、数据隐私
   - 缺点：首次设置复杂、速度较慢

## 如果你想尝试本地部署

我可以帮你：
1. 安装所有依赖
2. 下载模型
3. 集成到现有代码
4. 测试性能

是否需要我继续？
