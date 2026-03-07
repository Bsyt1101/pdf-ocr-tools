# PDF文档自动拆分和归档工具 - 文档索引

**当前版本**: v1.6.3
**更新日期**: 2026-03-07

---

## 📚 文档导航

### 🚀 快速开始
- **[README.md](README.md)** - 项目完整说明
  - 适合：所有用户
  - 内容：功能介绍、安装说明、使用方法、FAQ

- **[QUICKSTART.md](QUICKSTART.md)** - 5分钟快速上手指南
  - 适合：第一次使用的用户
  - 内容：安装、配置、运行

### 📋 核心功能文档

#### 文档类型与命名
- **[DOC_TYPES.md](DOC_TYPES.md)** - 支持的18种文档类型
  - 文档类型完整列表
  - 文件编号对照表
  - 识别关键词

- **[NAMING_RULES.md](NAMING_RULES.md)** - 文件命名规则详解
  - 文件编号格式说明
  - 命名规则和示例
  - 项目级vs系统级文档

#### 文件夹管理
- **[FOLDER_MAPPING.md](FOLDER_MAPPING.md)** - 文件夹映射关系 ⭐ 重要
  - 完整的文档类型到文件夹映射表
  - 18种文档的归档位置
  - 文件夹命名要求

- **[FOLDER_SEARCH.md](FOLDER_SEARCH.md)** - 文件夹搜索逻辑
  - 搜索规则和匹配方式
  - 关键词列表
  - 故障排查

#### 系统名称管理
- **[SYSTEM_NAMES.md](docs/guides/SYSTEM_NAMES.md)** - 系统名称自动读取 ⭐ v1.3.0
  - 从Word文件自动读取系统名称
  - 文件结构要求
  - 工作流程说明

- **[SYSTEM_NAME_VALIDATION.md](docs/guides/SYSTEM_NAME_VALIDATION.md)** - 系统名称一致性验证 ⭐ v1.6.2
  - 自动检测文件编号与系统名称的一致性
  - 验证逻辑和使用示例
  - 处理建议

- **[SYSTEM_LEVEL_DOWNGRADE.md](docs/guides/SYSTEM_LEVEL_DOWNGRADE.md)** - 系统级文档自动降级 ⭐ v1.6.3
  - 文件编号无法识别时自动降级为项目级命名
  - 降级规则和映射表
  - 设计理念和实际效果

#### 页面合并
- **[PAGE_MERGE.md](PAGE_MERGE.md)** - 智能页面合并 ⭐ v1.4.0
  - 自动合并同一文档的多页
  - 合并规则和逻辑
  - 使用示例

#### OCR 引擎
- **[OCR_ENGINES.md](OCR_ENGINES.md)** - OCR引擎配置 ⭐ v1.5.0
  - 支持3种OCR引擎：PaddleOCR-VL-1.5、阿里云OCR、Claude Sonnet 4.6
  - 引擎对比和选择建议
  - 配置方法和使用示例

- **[CURRENT_CONFIG.md](CURRENT_CONFIG.md)** - 当前OCR配置 ⭐ v1.5.0
  - OCR引擎自动选择逻辑
  - 环境变量配置
  - 性能对比

### 💡 使用指南
- **[EXAMPLE.md](EXAMPLE.md)** - 完整使用示例
  - 真实项目案例
  - 完整处理流程
  - 预期结果展示

- **[EXAMPLES.md](EXAMPLES.md)** - 多场景使用示例
  - 6个实际使用场景
  - 详细步骤说明

### ⚙️ 配置与开发
- **[CONFIG.md](CONFIG.md)** - 高级配置说明
  - OCR配置
  - 分类规则自定义
  - 性能优化

- **[STRUCTURE.md](STRUCTURE.md)** - 项目结构说明
  - 文件说明
  - 代码结构
  - 扩展点

### 📊 改进和总结
- **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)** - 改进总结 ⭐ v1.5.0
  - 文件编号识别优化
  - OCR引擎配置优化
  - 性能对比

- **[LOCAL_DEPLOYMENT_SUMMARY.md](LOCAL_DEPLOYMENT_SUMMARY.md)** - 本地部署总结 ⭐ v1.5.0
  - PaddleOCR-VL-1.5本地部署尝试
  - 遇到的问题和解决方案
  - 建议方案

- **[DEEPSEEK_INTEGRATION.md](DEEPSEEK_INTEGRATION.md)** - DeepSeek集成总结
  - DeepSeek-OCR集成过程
  - 配置说明

- **[SUMMARY.md](SUMMARY.md)** - 项目总结
  - 功能概览
  - 技术特点

### 📝 版本信息
- **[CHANGELOG.md](CHANGELOG.md)** - 版本更新记录
  - v1.5.0: 多OCR引擎支持、文件编号OCR修正、未分类文件夹自动创建
  - v1.4.0: 智能页面合并
  - v1.3.1: 文件夹映射优化
  - v1.3.0: 系统名称自动读取
  - 历史版本记录

- **[DOCUMENTATION_CHECK.md](DOCUMENTATION_CHECK.md)** - 文档一致性检查 ⭐ v1.5.0
  - 文档完整性检查
  - 版本一致性检查
  - 功能实现检查

### 🔧 技术文档
- **[DEEPSEEK_TOKEN_FIX.md](DEEPSEEK_TOKEN_FIX.md)** - DeepSeek Token修复
- **[DEFAULT_ENGINE_SWITCH.md](DEFAULT_ENGINE_SWITCH.md)** - 默认引擎切换
- **[DEPLOY_LOCAL_OCR.md](DEPLOY_LOCAL_OCR.md)** - 本地OCR部署
- **[LANDSCAPE_OPTIMIZATION.md](LANDSCAPE_OPTIMIZATION.md)** - 横向页面优化
- **[TEMPFILE_IMPORT_FIX.md](TEMPFILE_IMPORT_FIX.md)** - Tempfile导入修复
- **[UPDATE_FINAL.md](UPDATE_FINAL.md)** - 最终更新
- **[UPDATE_v1.1.md](UPDATE_v1.1.md)** - v1.1更新
- **[VERIFICATION_V1.2.md](VERIFICATION_V1.2.md)** - v1.2验证
- **[DELIVERY.md](DELIVERY.md)** - 交付文档

---

## 🎯 根据需求选择文档

### 我是新用户，想快速上手
→ 阅读 [README.md](README.md) 或 [QUICKSTART.md](QUICKSTART.md)

### 我想了解支持哪些文档类型
→ 阅读 [DOC_TYPES.md](DOC_TYPES.md) 或 [FOLDER_MAPPING.md](FOLDER_MAPPING.md)

### 我想知道文件会归档到哪个文件夹
→ 阅读 [FOLDER_MAPPING.md](FOLDER_MAPPING.md) ⭐ 重要

### 我想了解系统名称自动读取功能
→ 阅读 [SYSTEM_NAMES.md](docs/guides/SYSTEM_NAMES.md)

### 我想了解系统名称一致性验证功能
→ 阅读 [SYSTEM_NAME_VALIDATION.md](docs/guides/SYSTEM_NAME_VALIDATION.md)

### 我想了解页面合并功能
→ 阅读 [PAGE_MERGE.md](PAGE_MERGE.md)

### 我需要具体的使用案例
→ 阅读 [EXAMPLE.md](EXAMPLE.md) 或 [EXAMPLES.md](EXAMPLES.md)

### 我想自定义分类规则
→ 阅读 [CONFIG.md](CONFIG.md) 的"文档分类配置"部分

### 我想了解文件编号格式
→ 阅读 [NAMING_RULES.md](NAMING_RULES.md)

### 我遇到了问题
→ 先查看 [README.md](README.md) 的"常见问题"部分
→ 再查看对应功能的文档（如 [FOLDER_SEARCH.md](FOLDER_SEARCH.md)、[SYSTEM_NAMES.md](SYSTEM_NAMES.md)）

---

## 📊 功能特性速查

| 功能 | 版本 | 文档 |
|------|------|------|
| 18种文档类型识别 | v1.2.0 | [DOC_TYPES.md](docs/guides/DOC_TYPES.md) |
| 文件编号识别 | v1.1.0 | [NAMING_RULES.md](docs/guides/NAMING_RULES.md) |
| 智能文件夹搜索 | v1.3.0 | [FOLDER_SEARCH.md](docs/guides/FOLDER_SEARCH.md) |
| 系统名称自动读取 | v1.3.0 | [SYSTEM_NAMES.md](docs/guides/SYSTEM_NAMES.md) |
| 智能页面合并 | v1.4.0 | [PAGE_MERGE.md](PAGE_MERGE.md) |
| 文件夹映射 | v1.3.1 | [FOLDER_MAPPING.md](docs/guides/FOLDER_MAPPING.md) |
| 多OCR引擎支持 | v1.5.0 | [OCR_ENGINES.md](docs/guides/OCR_ENGINES.md) |
| 系统名称一致性验证 | v1.6.2 | [SYSTEM_NAME_VALIDATION.md](docs/guides/SYSTEM_NAME_VALIDATION.md) |

---

## 📝 核心文件

| 文件 | 说明 | 行数 |
|------|------|------|
| pdf_processor.py | 主程序（含OCR、合并逻辑） | ~600 |
| doc_classifier.py | 文档分类器（含18种文档类型） | ~300 |
| requirements.txt | 依赖列表 | 9 |

---

## 🔗 快速链接

### 安装与配置
- [安装依赖](README.md#安装依赖)
- [配置OCR引擎](OCR_ENGINES.md)

### 功能说明
- [支持的文档类型](DOC_TYPES.md)
- [文件夹映射关系](FOLDER_MAPPING.md)
- [系统名称自动读取](SYSTEM_NAMES.md)
- [页面合并功能](PAGE_MERGE.md)
- [OCR引擎选择](OCR_ENGINES.md)

### 使用指南
- [完整使用示例](EXAMPLE.md)
- [多场景示例](EXAMPLES.md)

### 高级配置
- [添加新文档类型](CONFIG.md#添加新的文档类型)
- [自定义命名格式](CONFIG.md#自定义命名格式)
- [修改文件夹映射](FOLDER_MAPPING.md#自定义文件夹映射)

### 故障排查
- [常见问题](README.md#常见问题)
- [文件夹搜索问题](FOLDER_SEARCH.md#故障排查)
- [系统名称读取问题](SYSTEM_NAMES.md#故障排查)

---

## 📦 文档完整性检查

✅ 核心文档（必读）
- [x] README.md - 项目说明
- [x] FOLDER_MAPPING.md - 文件夹映射
- [x] DOC_TYPES.md - 文档类型

✅ 功能文档
- [x] SYSTEM_NAMES.md - 系统名称自动读取
- [x] PAGE_MERGE.md - 页面合并
- [x] FOLDER_SEARCH.md - 文件夹搜索
- [x] NAMING_RULES.md - 命名规则

✅ 使用指南
- [x] QUICKSTART.md - 快速开始
- [x] EXAMPLE.md - 完整示例
- [x] EXAMPLES.md - 多场景示例

✅ 开发文档
- [x] CONFIG.md - 配置说明
- [x] STRUCTURE.md - 项目结构
- [x] CHANGELOG.md - 更新日志

---

**版本**: v1.6.2
**更新日期**: 2026-03-07
**开发单位**: 广东中科实数科技有限公司
