# OCR 引擎配置说明

**版本**: v1.7.2
**更新日期**: 2026-03-22

---

## 📋 支持的 OCR 引擎

本工具支持四种 OCR 引擎，可根据需求选择：

| 引擎 | 提供商 | 速度 | 精度 | 成本 | 推荐度 |
|------|--------|------|------|------|--------|
| **本地 PaddleOCR-VL** | 本地部署 | 中（2-3秒/页） | 极高 | 免费 | ⭐⭐⭐⭐⭐ |
| **百度飞桨 PaddleOCR-VL-1.5** | 百度 AI Studio | 快（1-3秒/页） | 极高（94.5%） | 免费额度 | ⭐⭐⭐⭐⭐ |
| **阿里云 OCR** | 阿里云市场 | 快（1-2秒/页） | 极高 | 低 | ⭐⭐⭐⭐ |
| **SiliconFlow API** | SiliconFlow | 快（2-4秒/页） | 高 | 免费额度 | ⭐⭐⭐⭐ |

> 注：识别速度受设备性能、网络状况、PDF 页面复杂度等因素影响，以上数据仅供参考。

---

## 🚀 引擎自动选择

工具会根据环境变量自动选择 OCR 引擎，优先级如下：

1. 如果设置了 `LOCAL_PADDLEOCR_DIRECT=true` → 使用 **本地 PaddleOCR-VL**（直接加载）
2. 如果本地 MLX-VLM 服务可用 → 使用 **本地 PaddleOCR-VL**（HTTP 服务）
3. 如果设置了 `ALIYUN_OCR_APPCODE` → 使用 **阿里云 OCR**
4. 如果设置了 `SILICONFLOW_API_KEY` → 使用 **SiliconFlow API**
5. 如果设置了 `BAIDU_PADDLEOCR_TOKEN` → 使用 **百度飞桨 PaddleOCR-VL-1.5**（默认端点）

也可通过命令行 `--ocr` 参数强制指定：

```bash
python main.py --ocr local       # 本地 PaddleOCR-VL
python main.py --ocr baidu       # 百度飞桨 PaddleOCR-VL-1.5
python main.py --ocr aliyun      # 阿里云 OCR
python main.py --ocr siliconflow # SiliconFlow API
```

---

## 🔧 各引擎配置

### 1. 本地 PaddleOCR-VL（免费，隐私保护）

完全在本地运行，无需联网（首次需下载模型）。

```bash
# 方式1：直接加载模型
export LOCAL_PADDLEOCR_DIRECT=true

# 方式2：通过 MLX-VLM 服务
# 启动服务后程序自动检测
```

**特点**：
- ✅ 完全免费，无 API 限额
- ✅ 数据不出本机，隐私保护
- ✅ Apple Silicon 优化
- ⚠️ 首次需下载模型（约 1.8GB）
- ⚠️ 识别速度取决于设备性能

---

### 2. 百度飞桨 PaddleOCR-VL-1.5（推荐，免费额度）

基于百度 AI Studio 免费 API，默认使用 PaddleOCR-VL-1.5 模型（同步解析模式）。

#### 获取 Token

1. 访问 [PaddleOCR 官网](https://aistudio.baidu.com/paddleocr/task) 注册并登录
2. 在 API 调用示例中复制 `TOKEN`

#### 配置方式

```bash
# 只需设置 TOKEN，默认使用 PaddleOCR-VL-1.5
export BAIDU_PADDLEOCR_TOKEN="你的Token"

# 可选：自定义 API 地址（切换其他模型时使用）
# export BAIDU_PADDLEOCR_URL="你的API地址"
```

#### 可选模型

不同模型对应不同的 API_URL，TOKEN 通用，程序自动识别模型类型：

| 模型 | 特点 | 推荐场景 |
|------|------|----------|
| **PaddleOCR-VL-1.5**（默认） | 94.5% 精度，支持异形框、印章识别 | 扫描件、拍照件、复杂版面 |
| PaddleOCR-VL | 版式解析 + OCR | 标准文档 |
| PP-OCRv5 | 轻量级，速度快 | 简单文字识别 |
| PP-StructureV3 | 结构化解析 | 表格、公式提取 |

#### 同步解析 vs 异步解析

本工具使用**同步解析**模式（逐页图片调用 API，等待返回结果），适合单页识别+分类的工作流。

| | 同步解析（当前使用） | 异步解析 |
|--|---------|---------|
| 调用方式 | POST 发送图片，等待返回 | 提交任务，轮询查询状态 |
| 适合场景 | 单页图片，实时处理 | 大文件、多页PDF批量 |
| 认证方式 | `token {TOKEN}` | `bearer {TOKEN}` |

**特点**：
- ✅ 精度极高（94.5%，OmniDocBench v1.5 评测集）
- ✅ 免费额度，只需设置 TOKEN
- ✅ 支持异形框定位、印章识别
- ✅ 依赖小（仅 requests）
- ⚠️ 数据上传云端处理
- ⚠️ 默认并发数 2，避免限流

---

### 3. 阿里云 OCR

#### 获取 AppCode

1. 访问 [阿里云市场](https://market.aliyun.com/)
2. 搜索"通用文字识别"
3. 购买服务（有免费额度）
4. 在控制台获取 AppCode

#### 配置方式

```bash
export ALIYUN_OCR_APPCODE="你的AppCode"
```

**特点**：
- ✅ 速度快：单页识别 1-2 秒
- ✅ 稳定性高：成熟的商业服务
- ✅ 价格低：有免费额度
- ⚠️ 复杂布局识别能力一般

---

### 4. SiliconFlow API

#### 获取 API Key

1. 访问 [SiliconFlow](https://siliconflow.cn/)
2. 注册账号并创建 API Key

#### 配置方式

```bash
export SILICONFLOW_API_KEY="sk-xxxxx"
```

**特点**：
- ✅ 基于 PaddleOCR-VL-1.5 视觉模型
- ✅ 复杂布局识别能力强
- ⚠️ 速度较慢：单页识别 2-4 秒
- ⚠️ 按 token 计费

---

## 📊 性能对比

> 注：识别速度受设备性能、网络状况、PDF 页面复杂度等因素影响，以下数据仅供参考。

| 特性 | 本地 PaddleOCR-VL | 百度飞桨 VL-1.5 | 阿里云 OCR | SiliconFlow API |
|------|-------------------|-----------------|-----------|-----------------|
| 识别速度 | 2-3秒/页 | 1-3秒/页 | 1-2秒/页 | 2-4秒/页 |
| 依赖大小 | 大（模型约1.8GB） | 小（仅requests） | 小（仅requests） | 小（仅requests） |
| 准确率 | 极高 | 极高（94.5%） | 极高 | 高 |
| 成本 | 免费 | 免费额度 | 按调用次数收费 | 有免费额度 |
| 隐私 | 完全本地 | 上传云端 | 上传云端 | 上传云端 |
| 网络要求 | 首次需下载模型 | 每次需联网 | 每次需联网 | 每次需联网 |
| 默认并发数 | 1 | 2 | 3 | 3 |

---

## 💡 使用建议

| 场景 | 推荐引擎 |
|------|---------|
| 标准等保测评文档 | 本地 PaddleOCR-VL 或百度飞桨 VL-1.5 |
| 需要快速处理大量文档 | 阿里云 OCR |
| 数据隐私要求高 | 本地 PaddleOCR-VL |
| 免费使用、精度优先 | 百度飞桨 PaddleOCR-VL-1.5 |
| 扫描件、拍照件、复杂版面 | 百度飞桨 PaddleOCR-VL-1.5 |

---

## ⚠️ 常见问题

### 1. 百度飞桨报错：Token 无效

```bash
# 检查环境变量
echo $BAIDU_PADDLEOCR_TOKEN

# 重新设置（从 PaddleOCR 官网获取）
export BAIDU_PADDLEOCR_TOKEN="你的Token"
```

### 2. 阿里云 OCR 报错：AppCode 无效

```bash
echo $ALIYUN_OCR_APPCODE
export ALIYUN_OCR_APPCODE="你的AppCode"
```

### 3. SiliconFlow 报错：API Key 无效

```bash
echo $SILICONFLOW_API_KEY
export SILICONFLOW_API_KEY="sk-xxxxx"
```

### 4. 识别结果不准确

- 提高扫描 DPI（默认 200，可设置为 300）
- 确保图片清晰度
- 尝试切换其他 OCR 引擎

---

## 🔗 相关文档

- [README.md](../../README.md) - 项目说明
- [CURRENT_CONFIG.md](../development/CURRENT_CONFIG.md) - 当前配置
- [QUICKSTART.md](../QUICKSTART.md) - 快速开始

---

**版本**: v1.7.2
**更新日期**: 2026-03-22
**开发单位**: 广东中科实数科技有限公司
