# 项目结构说明

```
pdf-ocr-tool/
│
├── README.md                 # 项目主文档（必读）
├── QUICKSTART.md            # 快速开始指南（5分钟上手）
├── EXAMPLES.md              # 使用示例（详细案例）
├── CONFIG.md                # 配置指南（高级配置）
├── CHANGELOG.md             # 更新日志
├── .gitignore               # Git忽略文件
│
├── requirements.txt         # Python依赖列表
├── test.py                  # 测试脚本
│
├── pdf_processor.py         # 主程序（核心）
└── doc_classifier.py        # 文档分类器（核心）
```

## 文件说明

### 📖 文档文件

| 文件 | 用途 | 适合人群 |
|------|------|---------|
| README.md | 完整的项目说明 | 所有用户 |
| QUICKSTART.md | 5分钟快速上手 | 新用户 |
| EXAMPLES.md | 详细使用示例 | 需要参考的用户 |
| CONFIG.md | 高级配置说明 | 需要自定义的用户 |
| CHANGELOG.md | 版本更新记录 | 关注更新的用户 |

### 💻 代码文件

| 文件 | 说明 | 可修改 |
|------|------|--------|
| pdf_processor.py | 主程序，包含PDF处理和OCR调用 | ✓ |
| doc_classifier.py | 文档分类器，定义分类规则 | ✓ |
| test.py | 测试脚本，验证环境配置 | ✗ |

### ⚙️ 配置文件

| 文件 | 说明 |
|------|------|
| requirements.txt | Python依赖包列表 |
| .gitignore | Git版本控制忽略规则 |

## 使用流程

```
1. 阅读 QUICKSTART.md
   ↓
2. 安装依赖: pip install -r requirements.txt
   ↓
3. 配置 AppCode
   ↓
4. 运行测试: python test.py
   ↓
5. 开始使用: python main.py
   ↓
6. 需要自定义？查看 CONFIG.md
   ↓
7. 需要示例？查看 EXAMPLES.md
```

## 核心代码结构

### pdf_processor.py

```
AliyunOCR 类
├── __init__()          # 初始化OCR客户端
└── recognize_general() # 调用阿里云OCR API

PDFProcessor 类
├── __init__()              # 初始化处理器
├── split_pdf()             # 拆分PDF为单页
├── extract_text_from_pdf() # 提取文本（混合方案）
├── _ocr_page()             # OCR识别单页
├── process_pdf()           # 主处理流程
├── _print_summary()        # 打印处理摘要
└── _archive_files()        # 归档文件

main()                      # 交互式命令行界面
```

### doc_classifier.py

```
DocumentClassifier 类
├── DOC_TYPE_TO_FOLDER      # 文档类型→文件夹映射
├── CLASSIFICATION_RULES    # 分类规则列表
├── classify()              # 分类文档
├── get_folder_name()       # 获取文件夹名称
└── generate_filename()     # 生成文件名

main()                      # 测试分类器
```

## 数据流程

```
输入PDF
  ↓
拆分为单页PDF
  ↓
逐页处理
  ├→ 提取PDF文本层
  │   ↓
  │  文本 < 50字符？
  │   ├→ 是：使用阿里云OCR
  │   └→ 否：使用提取的文本
  ↓
文档分类（关键词匹配）
  ↓
生成规范文件名
  ↓
显示处理摘要
  ↓
用户确认
  ↓
归档到对应文件夹
  ↓
完成
```

## 扩展点

### 1. 添加新的文档类型

修改 `doc_classifier.py`:
- `DOC_TYPE_TO_FOLDER` - 添加文件夹映射
- `CLASSIFICATION_RULES` - 添加分类规则

### 2. 修改文件命名规则

修改 `doc_classifier.py` 的 `generate_filename()` 方法

### 3. 更换OCR引擎

修改 `pdf_processor.py` 的 `AliyunOCR` 类

### 4. 添加新功能

在 `PDFProcessor` 类中添加新方法

## 依赖关系

```
pdf_processor.py
  ├── 依赖: PyMuPDF (fitz)
  ├── 依赖: requests
  └── 导入: doc_classifier.py

doc_classifier.py
  └── 无外部依赖（纯Python）

test.py
  ├── 导入: pdf_processor.py
  └── 导入: doc_classifier.py
```

## 配置优先级

```
1. 代码中硬编码的值（最低优先级）
   ↓
2. 配置文件（config.ini）
   ↓
3. 环境变量（最高优先级）
```

## 常见修改场景

### 场景1：修改默认输出目录

文件：`pdf_processor.py` 第380行
```python
output_dir = input("...").strip() or "./output"  # 修改这里
```

### 场景2：添加新的文档类型

文件：`doc_classifier.py`
1. 第14行：添加文件夹映射
2. 第29行：添加分类规则

### 场景3：修改OCR阈值

文件：`pdf_processor.py` 第114行
```python
text_threshold: int = 50  # 修改这里
```

### 场景4：更换OCR服务

文件：`pdf_processor.py`
修改 `AliyunOCR` 类的实现

## 版本信息

- 当前版本：v1.0.0
- 发布日期：2026-03-03
- Python版本：3.8+
- 开发单位：广东中科实数科技有限公司
