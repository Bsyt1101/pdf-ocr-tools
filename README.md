# PDF 文档自动拆分和归档工具

**版本**: v1.6.0
**更新日期**: 2026-03-06

## 📖 项目简介

这是一个专为等保测评文档设计的自动化归档工具，能够：

- 📄 **自动拆分** - 将多页PDF拆分为单页文件
- 🔍 **智能识别** - 自动识别18种等保测评文档类型
- 🏷️ **规范命名** - 按照标准格式自动重命名文件
- 📁 **自动归档** - 搜索并移动文件到对应的文件夹
- 📋 **系统名称自动读取** - 从项目实施申请单Word文件自动读取系统名称
- 🔗 **智能页面合并** - 自动合并同一文档的多页（v1.4.0）
- 🎯 **多OCR引擎支持** - 支持本地PaddleOCR、阿里云OCR、SiliconFlow API（v1.5.0+）
- 🔧 **文件编号OCR修正** - 自动修正常见OCR错误（JD8/JD9 → JDB）（v1.5.0）
- 📂 **未分类文件夹自动创建** - 自动创建"未分类"文件夹存储未识别文档（v1.5.0）
- ⚡ **OCR并行识别** - 多线程并行OCR，默认5并发，速度提升3-5倍（v1.5.1）
- 🧠 **系统名称三级回退** - 文件编号映射 → 文本匹配 → 正则提取（v1.5.1）
- 🏠 **本地OCR支持** - 支持Apple Silicon本地运行PaddleOCR-VL，完全免费且隐私保护（v1.6.0）

### 技术特点

- ✅ 支持多种OCR引擎：本地PaddleOCR-VL（推荐）、阿里云OCR、SiliconFlow API
- ✅ 本地OCR：完全免费，隐私保护，Apple Silicon优化（MLX框架）
- ✅ OCR引擎自动选择：根据环境变量自动选择最佳引擎
- ✅ OCR并行识别：默认5并发（云端API），串行处理（本地直接加载）
- ✅ 文件编号OCR错误自动修正：JD8/JD9 → JDB、SMOR → SMQR
- ✅ 混合方案：优先提取PDF文本层，扫描件自动OCR
- ✅ 依赖少，安装简单
- ✅ 支持项目级和系统级文档分类
- ✅ 文件编号识别（格式：JDB项目编号-类型码-系统编号）
- ✅ 智能文件夹搜索，支持灵活的文件夹命名
- ✅ 系统名称三级回退：文件编号映射 → 文本匹配 → 正则提取
- ✅ 智能合并同一文档的多页
- ✅ Word表格自动适配（支持无「序号」列的表格）

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd pdf-ocr-tool

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 OCR 引擎

本工具支持三种 OCR 引擎，可根据需求选择：

| 引擎 | 速度 | 精度 | 成本 | 隐私 | 推荐度 |
|------|------|------|------|------|--------|
| **本地 PaddleOCR-VL** | 中（2-3秒/页） | 极高 | 免费 | 完全本地 | ⭐⭐⭐⭐⭐ |
| **阿里云 OCR** | 快（1-2秒/页） | 极高 | 低 | 上传云端 | ⭐⭐⭐⭐ |
| **SiliconFlow API** | 快（2-4秒/页） | 高 | 免费额度 | 上传云端 | ⭐⭐⭐⭐ |

#### OCR 引擎自动选择

工具会根据环境变量自动选择OCR引擎，优先级如下：

1. 如果设置了 `LOCAL_PADDLEOCR_DIRECT=true` → 使用 **本地 PaddleOCR-VL**（直接加载）
2. 如果本地 MLX-VLM 服务可用 → 使用 **本地 PaddleOCR-VL**（HTTP 服务）
3. 如果设置了 `ALIYUN_OCR_APPCODE` → 使用 **阿里云 OCR**
4. 如果设置了 `SILICONFLOW_API_KEY` → 使用 **SiliconFlow API**

#### 选项1：使用本地 PaddleOCR-VL（推荐，免费）

**优势**：完全免费、隐私保护、Apple Silicon 优化

详细安装配置请参考：[docs/LOCAL_OCR_SETUP.md](docs/LOCAL_OCR_SETUP.md)

**快速配置**：

```bash
# 1. 安装 MLX-VLM
pip install "mlx-vlm>=0.3.11"

# 2. 设置环境变量
export LOCAL_PADDLEOCR_DIRECT=true
export LOCAL_PADDLEOCR_MODEL=/path/to/PaddleOCR-VL-1.5-bf16

# 3. 运行
python main.py
```

**注意**：本地直接加载模式使用串行处理（避免崩溃），速度约 2-3 秒/页

#### 选项2：使用阿里云 OCR（推荐，付费）

**方法一：设置环境变量（推荐）**

```bash
# Linux/Mac
export ALIYUN_OCR_APPCODE="你的AppCode"

# 或添加到 ~/.bashrc 或 ~/.zshrc
echo 'export ALIYUN_OCR_APPCODE="你的AppCode"' >> ~/.zshrc
source ~/.zshrc
```

```cmd
# Windows CMD
set ALIYUN_OCR_APPCODE=你的AppCode

# Windows PowerShell
$env:ALIYUN_OCR_APPCODE="你的AppCode"
```

**方法二：在代码中配置**

```python
processor = PDFProcessor(
    app_code="你的AppCode",
    ocr_engine="aliyun"  # 默认值
)
```

#### 选项2：使用 PaddleOCR-VL-1.5

**设置环境变量**

```bash
# Linux/Mac
export SILICONFLOW_API_KEY="sk-xxxxx"

# 或添加到 ~/.bashrc 或 ~/.zshrc
echo 'export SILICONFLOW_API_KEY="sk-xxxxx"' >> ~/.zshrc
source ~/.zshrc
```

```cmd
# Windows CMD
set SILICONFLOW_API_KEY=sk-xxxxx

# Windows PowerShell
$env:SILICONFLOW_API_KEY="sk-xxxxx"
```

**在代码中配置**

```python
processor = PDFProcessor(
    api_key="sk-xxxxx",
    ocr_engine="deepseek"  # PaddleOCR-VL-1.5
)
```

**详细配置说明**: 查看 [OCR_ENGINES.md](OCR_ENGINES.md)

### 3. 运行程序

```bash
# 使用默认 OCR 引擎（自动检测）
python main.py

# 或指定 OCR 引擎
python main.py --ocr local       # 本地 PaddleOCR-VL
python main.py --ocr aliyun      # 阿里云 OCR
python main.py --ocr siliconflow # SiliconFlow API
```

按提示输入 PDF 文件路径、项目名称等信息。

## 📁 项目结构

```
pdf-ocr-tools/
├── main.py                      # 主入口文件 ⭐
├── README.md                    # 项目说明
├── requirements.txt             # 依赖列表
├── .gitignore                   # Git 忽略规则
│
├── src/                         # 源代码
│   ├── __init__.py
│   ├── pdf_processor.py         # PDF 处理主程序
│   └── doc_classifier.py        # 文档分类器
│
├── tests/                       # 测试文件
│   └── test_*.py
│
├── docs/                        # 文档
│   ├── CHANGELOG.md             # 更新日志
│   ├── GIT_GUIDE.md             # Git 使用指南
│   ├── LOCAL_OCR_SETUP.md       # 本地 OCR 配置
│   ├── guides/                  # 使用指南
│   └── development/             # 开发文档
│
├── scripts/                     # 辅助脚本
└── examples/                    # 示例代码
```

然后按提示输入：
- PDF文件路径
- 项目名称（可选）
- 系统名称（可选，如果不输入会自动从Word文件读取）
- 输出目录（默认当前目录）

### 4. 准备文件结构

为了使用系统名称自动读取功能，请按以下结构组织文件：

```
项目目录/
├── 项目文档.pdf                    # 待处理的PDF文件
├── 项目实施单/                     # 必须包含"项目实施单"关键词
│   └── 项目实施申请单.docx         # 必须包含"项目实施申请单"关键词
├── 01测评授权书/                   # 预先创建的文件夹
├── 02风险告知书/
├── 03测评调研表/
└── ...
```

**Word文件格式要求**：

| 序号 | 系统名称 | ... |
|------|---------|-----|
| 1 | 门户网站系统 | ... |
| 2 | 内部办公系统 | ... |
| 3 | 数据管理系统 | ... |

### 5. 运行示例

```bash
请输入 PDF 文件路径: xxx单位.pdf
请输入项目名称（可选）: JDB项目编号-xxx单位
请输入系统名称（可选）: [直接回车，自动从Word文件读取]
请输入输出目录（默认为当前目录）: .

# 程序会自动：
# 1. 搜索"项目实施单"文件夹
# 2. 读取"项目实施申请单.docx"
# 3. 提取系统名称映射：{1: "门户网站系统", 2: "内部办公系统", ...}
# 4. 处理PDF时自动使用对应的系统名称
```

## 📋 支持的文档类型

### 文件命名方式

工具使用**可读性强的命名方式**：

- **项目级文档**: `文档类型.pdf`
  - 示例：`现场测评授权书.pdf`、`风险告知书.pdf`

- **系统级文档**: `系统名-文档类型.pdf`
  - 示例：`门户网站系统-情况调查表确认签字.pdf`

**文件编号的作用**：
- ✅ 用于识别文档类型（通过类型码如 CPSQS、DCB）
- ✅ 用于提取系统编号（匹配系统名称）
- ❌ 不用于文件命名（优先使用可读性强的名称）

详见 [NAMING_RULES.md](docs/guides/NAMING_RULES.md)

### 项目级文档（7种）

| 简拼 | 文档类型 | 关键词 | 文件命名示例 |
|------|---------|--------|-------------|
| CPSQS | 现场测评授权书 | 授权书、测评 | `现场测评授权书.pdf` |
| FXGZS | 风险告知书 | 风险告知 | `风险告知书.pdf` |
| SCHY | 启动会议记录 | 启动会议 | `启动会议记录表及签到表.pdf` |
| MCHY | 末次会议记录 | 末次会议 | `末次会议记录表及签到表.pdf` |
| WDJJ | 现场接收归还文档清单 | 接收归还、文档清单 | `现场接收归还文档清单.pdf` |
| YSB | 项目验收评估表 | 验收评估 | `项目验收评估表.pdf` |
| BMCNS | 保密承诺书 | 保密承诺 | `保密承诺书.pdf` |
| RLCQR | 入离场确认单 | 入场/离场、确认 | `入场离场确认单.pdf` |

### 系统级文档（7种）

| 简拼 | 文档类型 | 关键词 | 文件命名示例 |
|------|---------|--------|-------------|
| DCB | 情况调查表 | 情况调查表 | `门户网站系统-情况调查表确认签字.pdf` |
| FAFS | 测评方案评审记录 | 测评方案、评审 | `门户网站系统-测评方案评审记录.pdf` |
| FACR | 测评方案确认书 | 测评方案、确认 | `门户网站系统-测评方案确认书.pdf` |
| CPJG | 测评结果记录 | 测评结果、记录 | `门户网站系统-测评结果记录签字页.pdf` |
| CPWT | 测评问题列表 | 问题列表 | `门户网站系统-测评问题列表签字页.pdf` |
| SMQR | 漏洞扫描记录 | 漏洞扫描 | `门户网站系统-漏洞扫描记录签字确认表.pdf` |
| CTCS | 渗透测试记录 | 渗透测试 | `门户网站系统-渗透测试记录签字确认表.pdf` |

## 📁 输出文件夹结构

```
output/
├── 测评授权书/
│   └── 现场测评授权书.pdf
├── 风险告知书/
│   └── 风险告知书.pdf
├── 测评调研表/
│   ├── 门户网站系统-情况调查表确认签字.pdf
│   └── 内部办公系统-情况调查表确认签字.pdf
├── 测评方案评审记录/
├── 测评方案确认书/
├── 首末次会议记录/
├── 测评记录及问题汇总/
├── 现场接收归还文档清单/
├── 入离场确认书/
├── 项目验收评估表/
├── 保密承诺书/
└── 未分类/           # 无法识别的文档
```

## 🔧 工作原理

### 1. PDF拆分

使用PyMuPDF将多页PDF拆分为单页文件，保存到临时目录。

### 2. 文本提取（混合方案）

```
┌─────────────────┐
│  读取PDF单页    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 提取PDF文本层   │
└────────┬────────┘
         │
         ▼
    文本 > 50字符？
         │
    ┌────┴────┐
   是│        │否
    │         │
    ▼         ▼
 使用文本  使用阿里云OCR
    │         │
    └────┬────┘
         │
         ▼
    返回文本内容
```

### 3. 文档分类

基于关键词匹配规则，自动识别文档类型：

```python
# 示例规则
if "授权书" in text and "测评" in text:
    return "测评授权书", False  # False表示项目级

if "情况调查表" in text:
    return "测评调研表", True   # True表示系统级
```

### 4. 文件归档

根据文档类型和级别，生成规范的文件名并移动到对应文件夹。

## ⚙️ 配置说明

### 修改文本提取阈值

编辑 `pdf_processor.py` 第114行：

```python
text_threshold: int = 50  # 少于50字符判断为扫描件
```

### 修改OCR图片DPI

编辑 `pdf_processor.py` 第115行：

```python
dpi: int = 200  # 默认200 DPI，可调整为150-300
```

### 自定义分类规则

编辑 `doc_classifier.py` 第29-49行，添加或修改分类规则：

```python
CLASSIFICATION_RULES = [
    # (关键词列表, 文档类型, 是否系统级)
    (["你的关键词1", "关键词2"], "文档类型名称", False),
    # ... 更多规则
]
```

## 📊 性能对比

| 特性 | PaddleOCR | 阿里云OCR |
|------|-----------|-----------|
| 识别速度 | 5-10分钟/18页 | 30-60秒/18页 |
| 依赖大小 | 大（需下载模型） | 小（仅requests） |
| 准确率 | 高 | 高 |
| 成本 | 免费 | 按调用次数收费 |
| 网络要求 | 首次需下载模型 | 每次需联网 |

## ❓ 常见问题

### Q1: 如何获取阿里云OCR AppCode？

A: 访问[阿里云市场](https://market.aliyun.com/)，搜索"通用OCR"，购买服务后即可获得AppCode。

### Q2: 文档识别不准确怎么办？

A:
1. 检查PDF是否清晰
2. 查看处理摘要中的"文本预览"
3. 修改 `doc_classifier.py` 中的关键词规则
4. 调整DPI提高OCR质量

### Q3: 文件名冲突怎么办？

A: 程序会自动添加数字后缀，如 `文件名_1.pdf`、`文件名_2.pdf`

### Q4: 可以批量处理多个PDF吗？

A: 当前版本不支持，需要逐个处理。可以编写简单的脚本循环调用。

### Q5: OCR识别失败怎么办？

A:
- 检查AppCode是否正确
- 检查网络连接
- 查看错误信息
- 确认阿里云账户余额充足

### Q6: 如何测试分类器？

A: 运行测试脚本：

```bash
python doc_classifier.py
```

会显示所有内置测试用例的分类结果。

## 📝 文件说明

```
pdf-ocr-tool/
├── pdf_processor.py      # 主程序
├── doc_classifier.py     # 文档分类器
├── requirements.txt      # 依赖列表
├── README.md            # 本文档
├── CHANGELOG.md         # 更新日志
└── examples/            # 示例文件（可选）
```

## 🔄 更新日志

### v1.0.0 (2026-03-03)

- ✨ 初始版本发布
- ✅ 支持11种等保测评文档类型识别
- ✅ 集成阿里云OCR API
- ✅ 混合文本提取方案
- ✅ 自动拆分和归档功能

## 📄 许可证

本项目仅供内部使用。


