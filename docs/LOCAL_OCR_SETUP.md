# 本地 PaddleOCR-VL 模型安装配置手册

**版本**: v1.0
**更新日期**: 2026-03-06
**适用平台**: macOS (Apple Silicon)

---

## 📋 目录

1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [配置说明](#配置说明)
4. [使用方法](#使用方法)
5. [性能优化](#性能优化)
6. [故障排查](#故障排查)

---

## 系统要求

### 硬件要求
- **处理器**: Apple Silicon (M1/M2/M3/M4)
- **内存**: 至少 8GB RAM（推荐 16GB）
- **存储空间**: 至少 3GB 可用空间

### 软件要求
- **操作系统**: macOS 12.0 或更高版本
- **Python**: 3.8 - 3.13
- **网络**: 首次下载模型需要网络连接（可选代理）

---

## 安装步骤

### 步骤 1：创建虚拟环境

```bash
# 进入项目目录
cd /Users/你的用户名/项目路径/pdf-ocr-tool

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 步骤 2：安装依赖库

```bash
# 安装 MLX-VLM 框架（Apple Silicon 优化）
pip install "mlx-vlm>=0.3.11"

# 安装其他必要库
pip install Pillow requests
```

### 步骤 3：下载模型

#### 方法 A：使用 git clone（推荐）

```bash
# 创建模型目录
mkdir -p ~/PaddleOCR-VL/models
cd ~/PaddleOCR-VL/models

# 如果需要代理
export https_proxy=http://127.0.0.1:7897
export http_proxy=http://127.0.0.1:7897

# 下载模型（约 1.8GB）
git clone https://huggingface.co/mlx-community/PaddleOCR-VL-1.5-bf16
```

**下载时间**: 根据网络速度，约 5-20 分钟

#### 方法 B：使用 Python 下载

```bash
cd ~/PaddleOCR-VL/models

python3 << EOF
from huggingface_hub import snapshot_download

snapshot_download(
    'mlx-community/PaddleOCR-VL-1.5-bf16',
    local_dir='./PaddleOCR-VL-1.5-bf16'
)
print("下载完成！")
EOF
```

### 步骤 4：验证模型文件

```bash
cd ~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16
ls -lh
```

应该看到以下文件：
```
-rw-r--r--  config.json
-rw-r--r--  model.safetensors          (约 1.8GB)
-rw-r--r--  tokenizer.json
-rw-r--r--  processor_config.json
... 其他配置文件
```

---

## 配置说明

### 环境变量配置

在使用前，需要设置以下环境变量：

```bash
# 启用直接加载模式（不使用 HTTP 服务）
export LOCAL_PADDLEOCR_DIRECT=true

# 指定模型路径（使用你的实际路径）
export LOCAL_PADDLEOCR_MODEL=/Users/你的用户名/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16
```

### 永久配置（可选）

如果想每次自动加载，可以添加到 shell 配置文件：

```bash
# 编辑 ~/.zshrc 或 ~/.bash_profile
echo 'export LOCAL_PADDLEOCR_DIRECT=true' >> ~/.zshrc
echo 'export LOCAL_PADDLEOCR_MODEL=~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

---

## 使用方法

### 方法 1：处理 PDF 文档

```bash
# 1. 进入项目目录
cd /Users/你的用户名/项目路径/pdf-ocr-tool

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 设置环境变量
export LOCAL_PADDLEOCR_DIRECT=true
export LOCAL_PADDLEOCR_MODEL=~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16

# 4. 运行处理程序
python main.py

# 5. 按提示输入 PDF 路径和项目信息
```

### 方法 2：测试单张图片

```bash
# 激活环境并设置变量（同上）
source venv/bin/activate
export LOCAL_PADDLEOCR_DIRECT=true
export LOCAL_PADDLEOCR_MODEL=~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16

# 运行测试脚本
python test_local_single.py
```

### 方法 3：测试多页 PDF

```bash
# 激活环境并设置变量（同上）
source venv/bin/activate
export LOCAL_PADDLEOCR_DIRECT=true
export LOCAL_PADDLEOCR_MODEL=~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16

# 运行测试脚本
python test_local_ocr.py
```

---

## 性能优化

### 并行处理配置

默认并行数为 5，可以根据机器性能调整：

```python
# 在 pdf_processor.py 中
processor = PDFProcessor(
    ocr_engine="local",
    max_workers=5  # 调整并发数：3-10
)
```

**推荐配置**：
- **8GB RAM**: `max_workers=3`
- **16GB RAM**: `max_workers=5`（默认）
- **32GB RAM**: `max_workers=8`

### 性能指标

| 指标 | 数值 |
|------|------|
| 首次模型加载 | 3-5 秒 |
| 单页识别速度 | 2-3 秒 |
| 10 页 PDF（串行） | 约 25 秒 |
| 10 页 PDF（5 并发） | 约 8 秒 |
| 内存占用 | 约 2-3 GB |

### 优化建议

1. **首次使用**: 模型加载需要 3-5 秒，之后会缓存在内存中
2. **批量处理**: 使用并行模式可提升 3-4 倍速度
3. **内存管理**: 处理完成后模型会保持在内存中，重复使用更快

---

## 故障排查

### 问题 1：模型加载失败

**错误信息**:
```
FileNotFoundError: [Errno 2] No such file or directory
```

**解决方法**:
1. 检查模型路径是否正确：
   ```bash
   ls -la ~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16/
   ```
2. 确认 `model.safetensors` 文件存在且大小约 1.8GB
3. 重新设置环境变量，使用绝对路径

### 问题 2：内存不足

**错误信息**:
```
MemoryError: Cannot allocate memory
```

**解决方法**:
1. 降低并发数：`max_workers=3`
2. 关闭其他占用内存的应用
3. 重启系统释放内存

### 问题 3：识别结果为空

**可能原因**:
- 图片质量太低
- 图片中没有文字
- 模型未正确加载

**解决方法**:
1. 检查输入图片是否清晰
2. 查看终端输出，确认模型加载成功
3. 运行测试脚本验证：
   ```bash
   python test_local_single.py
   ```

### 问题 4：速度太慢

**优化方法**:
1. 确认使用的是 Apple Silicon 优化版本（mlx-community）
2. 检查是否启用了并行处理
3. 确认环境变量 `LOCAL_PADDLEOCR_DIRECT=true` 已设置
4. 首次识别会加载模型，后续会快很多

### 问题 5：依赖库冲突

**错误信息**:
```
RequestsDependencyWarning: urllib3 doesn't match a supported version
```

**解决方法**:
```bash
# 更新依赖库
pip install --upgrade requests urllib3

# 或者忽略警告（不影响功能）
export PYTHONWARNINGS="ignore::RequestsDependencyWarning"
```

---

## 与其他 OCR 引擎对比

| 特性 | 本地 PaddleOCR | 阿里云 OCR | SiliconFlow API |
|------|----------------|------------|-----------------|
| **速度** | 2-3秒/页 | 1-2秒/页 | 2-4秒/页 |
| **成本** | 免费 | 付费 | 免费（有限额） |
| **网络要求** | 仅首次下载 | 每次需要 | 每次需要 |
| **准确度** | 高 | 高 | 高 |
| **隐私性** | 完全本地 | 上传云端 | 上传云端 |
| **并发支持** | ✅ | ✅ | ✅ |
| **Apple Silicon 优化** | ✅ | ❌ | ❌ |

---

## 切换 OCR 引擎

工具支持自动检测和手动切换 OCR 引擎：

### 自动检测优先级

1. **本地 PaddleOCR**（如果设置了 `LOCAL_PADDLEOCR_DIRECT=true`）
2. 阿里云 OCR（如果设置了 `ALIYUN_OCR_APPCODE`）
3. SiliconFlow API（如果设置了 `SILICONFLOW_API_KEY`）

### 手动切换

```bash
# 使用本地模型
export LOCAL_PADDLEOCR_DIRECT=true
export LOCAL_PADDLEOCR_MODEL=~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16

# 使用阿里云 OCR
unset LOCAL_PADDLEOCR_DIRECT
export ALIYUN_OCR_APPCODE=你的AppCode

# 使用 SiliconFlow API
unset LOCAL_PADDLEOCR_DIRECT
unset ALIYUN_OCR_APPCODE
export SILICONFLOW_API_KEY=你的API密钥
```

---

## 常见使用场景

### 场景 1：日常文档处理（推荐本地模型）

```bash
export LOCAL_PADDLEOCR_DIRECT=true
export LOCAL_PADDLEOCR_MODEL=~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16
python main.py
```

**优势**: 免费、快速、隐私保护

### 场景 2：大批量处理（推荐阿里云 OCR）

```bash
unset LOCAL_PADDLEOCR_DIRECT
export ALIYUN_OCR_APPCODE=你的AppCode
python main.py
```

**优势**: 速度最快、稳定性高

### 场景 3：临时使用（推荐 SiliconFlow）

```bash
unset LOCAL_PADDLEOCR_DIRECT
export SILICONFLOW_API_KEY=你的API密钥
python main.py
```

**优势**: 免费额度、无需本地配置

---

## 卸载说明

如果不再需要本地模型：

```bash
# 1. 删除模型文件
rm -rf ~/PaddleOCR-VL/models/PaddleOCR-VL-1.5-bf16

# 2. 删除环境变量配置（如果添加到了 shell 配置文件）
# 编辑 ~/.zshrc，删除相关的 export 行

# 3. 卸载 MLX-VLM（可选）
pip uninstall mlx-vlm
```

---

## 技术支持

### 相关链接

- **PaddleOCR 官网**: https://www.paddleocr.ai/
- **MLX-VLM GitHub**: https://github.com/Blaizzy/mlx-vlm
- **模型页面**: https://huggingface.co/mlx-community/PaddleOCR-VL-1.5-bf16

### 问题反馈

如遇到问题，请提供以下信息：
1. macOS 版本和芯片型号
2. Python 版本
3. 完整的错误信息
4. 使用的命令和配置

---

**版本**: v1.0
**更新日期**: 2026-03-06
**作者**: Bsyt1101
