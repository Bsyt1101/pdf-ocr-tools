# 系统名称自动读取功能说明

## 功能概述

参考 word-auto-tools 项目的实现，pdf-ocr-tools 现在支持从测评报告和项目实施单中自动读取系统名称。

## 实现逻辑

### 1. 从测评报告提取系统名称

新增方法：`extract_system_name_from_report(pdf_dir: Path) -> Optional[str]`

**搜索范围：**
- PDF所在目录
- PDF所在目录的父目录
- PDF所在目录下包含"测评报告"的子目录

**搜索条件：**
- 文件类型：`.docx` 或 `.doc`
- 文件名包含："测评报告" 或 "报告"
- 排除：包含"渗透"的文件（渗透测试报告）

**提取规则：**

从Word文件的前30段中查找系统名称，支持以下格式：

**核心规则：提取"网络安全等级保护"和"等级测评报告"之间的内容作为系统名称**

1. **单段格式**：`网络安全等级保护 xxx 等级测评报告`
   - 正则表达式：`网络安全等级保护\s*(.+?)\s*等级测评报告`
   - 示例：`网络安全等级保护 xxx运营系统 等级测评报告`
   - 示例：`网络安全等级保护 xxx服务云平台 等级测评报告`

2. **单段格式（简化）**：`xxx等级测评报告`（不包含"网络安全等级保护"）
   - 正则表达式：`^(.+?)等级测评报告$`
   - 示例：`xxx运营系统等级测评报告`
   - 示例：`xxx服务云平台等级测评报告`

3. **跨段格式**：第一段包含"网络安全等级保护"，第二段为"xxx等级测评报告"
   - 从第二段提取系统名称（去掉"等级测评报告"）
   - 支持任意系统名称格式（系统、平台、网络等）

### 2. 更新项目实施单

修改方法：`read_system_names_from_word(pdf_dir: Path) -> Dict[int, str]`

**处理流程：**

1. **提取测评报告系统名称**
   - 调用 `extract_system_name_from_report()` 获取系统名称

2. **读取项目实施单**
   - 搜索"项目实施单"文件夹
   - 查找"项目实施申请单"Word文件
   - 读取表格中的"序号"和"系统名称"列

3. **自动更新**
   - 如果测评报告中有系统名称，用它替换实施单中的系统名称
   - 更新实施单中的单元格内容
   - 保存更新后的实施单文件

4. **错误处理**
   - 如果未找到实施单文件夹，返回空字典并报错
   - 如果未找到实施单Word文件，返回空字典并报错
   - 如果未能从实施单读取到系统名称，返回空字典并报错

## 使用示例

### 代码调用

```python
from pdf_processor import PDFProcessor
from pathlib import Path

processor = PDFProcessor()
pdf_dir = Path("/path/to/project")

# 从测评报告提取系统名称
system_name = processor.extract_system_name_from_report(pdf_dir)
print(f"系统名称: {system_name}")

# 读取系统名称映射（会自动更新实施单）
system_names_map = processor.read_system_names_from_word(pdf_dir)
print(f"系统名称映射: {system_names_map}")
```

### 输出示例

```
找到测评报告: xxx服务云平台等级测评报告.docx
  从测评报告提取系统名称: xxx服务云平台
✓ 从测评报告获取系统名称: xxx服务云平台
找到项目实施单文件夹: 项目实施单
找到Word文件: 项目实施申请单.docx
  读取: 序号 1 → xxx服务云平台
成功读取 1 个系统名称
```

## 测试

运行测试脚本：

```bash
python tests/test_report_system_name.py
```

## 参考

- word-auto-tools 项目：`src/extractor/project_info_extractor.py`
- 方法：`extract_system_name_from_report()` 和 `extract()`

## 改进点

相比 word-auto-tools 的实现，pdf-ocr-tools 的改进：

1. **独立方法**：将测评报告系统名称提取独立为单独的方法
2. **严格验证**：如果实施单有问题（不存在或无法读取），直接返回空字典并报错，不使用默认值
3. **清晰日志**：提供更详细的处理日志输出

## 版本信息

- 实现日期：2026-03-08
- 参考项目：word-auto-tools
- 修改文件：`src/pdf_processor.py`
- 新增测试：`tests/test_report_system_name.py`
