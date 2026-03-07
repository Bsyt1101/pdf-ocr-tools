# tempfile 导入错误修复

**修复日期**: 2026-03-05
**错误**: `UnboundLocalError: cannot access local variable 'tempfile'`

---

## 🐛 问题描述

运行 PDF 处理时出现错误：

```python
UnboundLocalError: cannot access local variable 'tempfile' where it is not associated with a value
```

### 错误位置

`pdf_processor.py:508` - `_ocr_page()` 方法

### 原因分析

```python
if is_landscape:
    from PIL import Image
    import tempfile  # 只在 if 分支导入
    ...
else:
    # 这里使用 tempfile，但未导入！
    with tempfile.NamedTemporaryFile(...):  # ❌ 错误
```

**问题**：
- `tempfile` 在 `if` 分支内导入
- `else` 分支中使用时，变量未定义
- Python 作用域规则导致 `UnboundLocalError`

---

## ✅ 修复方案

将 `tempfile` 和 `PIL.Image` 导入移到方法开头：

```python
def _ocr_page(self, page) -> str:
    # 延迟初始化 OCR
    self._init_ocr()

    # 导入必要的模块（在方法开头）
    import tempfile
    from PIL import Image

    # 检查页面方向
    rect = page.rect
    is_landscape = rect.width > rect.height
    ...
```

**修复后**：
- ✅ 模块在方法开头导入
- ✅ 所有分支都可以访问
- ✅ 避免作用域问题

---

## 🧪 验证

```bash
cd /Users/pr0xy/Pr0xyDrive/中科实数工作资料（公司笔记本）/pdf/pdf-ocr-tool
python main.py
```

预期：
- ✅ 不再出现 `UnboundLocalError`
- ✅ 横向页面正常处理
- ✅ 纵向页面正常处理

---

## 📝 技术说明

### Python 作用域规则

```python
# 错误示例
if condition:
    import module  # 局部导入
    ...
else:
    module.function()  # ❌ NameError/UnboundLocalError

# 正确示例
import module  # 全局导入
if condition:
    ...
else:
    module.function()  # ✅ 正常工作
```

### 最佳实践

1. **模块导入位置**
   - 文件顶部：全局使用的模块
   - 函数开头：仅函数内使用的模块
   - 避免：条件分支内导入

2. **延迟导入**
   - 可以在函数内导入（提高启动速度）
   - 但要确保所有分支都能访问

---

## 🔄 相关修复

同时修复了其他潜在问题：
- ✅ 确保 `PIL.Image` 在所有分支可用
- ✅ 统一导入位置
- ✅ 提高代码可读性

---

**修复日期**: 2026-03-05
**状态**: ✅ 已完成
