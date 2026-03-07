# 版本更新说明 - v1.6.4

## 更新日期
2026-03-08

## 新增功能

### 1. 从测评报告自动读取系统名称

参考 word-auto-tools 项目实现，新增从测评报告Word文件中自动提取系统名称的功能。

**核心功能：**
- 自动搜索测评报告Word文件（支持子目录搜索）
- 提取"网络安全等级保护"和"等级测评报告"之间的内容作为系统名称
- 自动更新项目实施单中的系统名称
- 支持任意系统名称格式（系统、平台、网络等）

**搜索范围：**
- PDF所在目录
- PDF所在目录的父目录
- PDF所在目录下包含"测评报告"的子目录

**提取规则：**
1. 单段格式：`网络安全等级保护 xxx 等级测评报告`
2. 单段格式（简化）：`xxx等级测评报告`
3. 跨段格式：第一段"网络安全等级保护"，第二段"xxx等级测评报告"

**使用方式：**
```python
from pdf_processor import PDFProcessor
from pathlib import Path

processor = PDFProcessor()
pdf_dir = Path("/path/to/project")

# 从测评报告提取系统名称
system_name = processor.extract_system_name_from_report(pdf_dir)

# 读取系统名称映射（会自动更新实施单）
system_names_map = processor.read_system_names_from_word(pdf_dir)
```

### 2. 敏感信息保护规则

新增开发规则，要求所有代码、注释、文档、测试用例中禁止使用真实的单位名称、系统名称等敏感信息。

**规则：**
- ✅ 使用占位符：`xxx单位`、`xxx系统`、`xxx平台`
- ❌ 禁止使用：具体的公司名称、机构名称、系统名称

## 修改文件

### 核心代码
- `src/pdf_processor.py`
  - 新增 `extract_system_name_from_report()` 方法
  - 增强 `read_system_names_from_word()` 方法
  - 支持子目录搜索
  - 简化正则表达式，支持任意系统名称格式

### 文档
- `CLAUDE.md` - 新增敏感信息保护规则和系统名称读取说明
- `docs/SYSTEM_NAME_EXTRACTION.md` - 详细功能说明文档
- `docs/SENSITIVE_INFO_CLEANUP.md` - 敏感信息清理记录

### 测试
- `tests/test_report_system_name.py` - 系统名称提取测试
- `tests/test_jdb25027.py` - JDB25027 项目测试
- `tests/check_report_format.py` - 测评报告格式检查工具

## 测试结果

✅ 使用 JDB25027 项目测试通过
- 成功从测评报告提取系统名称：`xxx服务云平台`
- 成功读取项目实施单系统名称映射
- 系统名称一致性验证通过

## 参考项目

- word-auto-tools 项目：`src/extractor/project_info_extractor.py`
- 方法：`extract_system_name_from_report()` 和 `extract()`

## 改进点

相比 word-auto-tools 的实现：

1. **独立方法**：将测评报告系统名称提取独立为单独的方法
2. **子目录搜索**：支持搜索包含"测评报告"的子目录
3. **简化规则**：提取"网络安全等级保护"和"等级测评报告"之间的内容，不限制格式
4. **严格验证**：如果实施单有问题，直接返回空字典并报错
5. **清晰日志**：提供更详细的处理日志输出

## 下一步计划

- [ ] 集成到主处理流程中
- [ ] 添加更多测试用例
- [ ] 优化错误处理
