# 配置指南

## 阿里云OCR配置

### 获取AppCode

1. 访问[阿里云市场](https://market.aliyun.com/)
2. 搜索"通用OCR文字识别"
3. 选择合适的套餐购买
4. 在"已购买的服务"中查看AppCode

### 当前配置信息

```
服务名称：通用OCR文字识别/图像识别/图片识别
AppKey：204983371
AppSecret：ZCbWnydUACvFI7sFETjMCQD0G5FiJoQR
AppCode：your_aliyun_appcode_here

接口地址：https://tysbgpu.market.alicloudapi.com/api/predict/ocr_general
请求方式：POST
返回类型：JSON
```

### 配置方法

#### 方法1：环境变量（推荐）

**优点**：安全，不会泄露到代码中

**Linux/Mac**
```bash
# 临时设置
export ALIYUN_OCR_APPCODE="your_aliyun_appcode_here"

# 永久设置（bash）
echo 'export ALIYUN_OCR_APPCODE="your_aliyun_appcode_here"' >> ~/.bashrc
source ~/.bashrc

# 永久设置（zsh）
echo 'export ALIYUN_OCR_APPCODE="your_aliyun_appcode_here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows CMD**
```cmd
# 临时设置
set ALIYUN_OCR_APPCODE=your_aliyun_appcode_here

# 永久设置
setx ALIYUN_OCR_APPCODE "your_aliyun_appcode_here"
```

**Windows PowerShell**
```powershell
# 临时设置
$env:ALIYUN_OCR_APPCODE="your_aliyun_appcode_here"

# 永久设置（用户级）
[System.Environment]::SetEnvironmentVariable('ALIYUN_OCR_APPCODE', 'your_aliyun_appcode_here', 'User')

# 永久设置（系统级，需管理员权限）
[System.Environment]::SetEnvironmentVariable('ALIYUN_OCR_APPCODE', 'your_aliyun_appcode_here', 'Machine')
```

#### 方法2：代码中配置

**优点**：简单直接

**缺点**：AppCode会暴露在代码中

编辑 `pdf_processor.py`，在第384行修改：

```python
# 原代码
processor = PDFProcessor()

# 修改为
processor = PDFProcessor(app_code="your_aliyun_appcode_here")
```

#### 方法3：配置文件（推荐用于生产环境）

创建 `config.ini` 文件：

```ini
[aliyun]
app_code = your_aliyun_appcode_here
```

修改 `pdf_processor.py`，添加配置读取：

```python
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['aliyun']['app_code']

# 在 main() 函数中
app_code = load_config()
processor = PDFProcessor(app_code=app_code)
```

**注意**：将 `config.ini` 添加到 `.gitignore`，避免提交到版本控制。

---

## 文本提取配置

### 文本阈值

控制何时使用OCR识别。

**位置**：`pdf_processor.py` 第114行

```python
text_threshold: int = 50  # 默认50字符
```

**说明**：
- 提取的文本 < 阈值 → 判断为扫描件，使用OCR
- 提取的文本 ≥ 阈值 → 直接使用提取的文本

**建议值**：
- 30-50：适合大部分场景
- 100：更严格，更多使用OCR
- 10：更宽松，尽量使用文本层

### OCR图片DPI

控制OCR识别质量。

**位置**：`pdf_processor.py` 第115行

```python
dpi: int = 200  # 默认200 DPI
```

**说明**：
- DPI越高，识别越准确，但速度越慢
- DPI越低，速度越快，但可能影响准确率

**建议值**：
- 150：快速处理，质量尚可
- 200：平衡速度和质量（推荐）
- 300：高质量，速度较慢

---

## 文档分类配置

### 添加新的文档类型

**步骤1**：编辑 `doc_classifier.py`，添加文件夹映射（第14行）

```python
DOC_TYPE_TO_FOLDER = {
    "测评授权书": "测评授权书",
    "风险告知书": "风险告知书",
    # 添加新类型
    "你的文档类型": "目标文件夹名称",
}
```

**步骤2**：添加分类规则（第29行）

```python
CLASSIFICATION_RULES = [
    # 项目级文档
    (["授权书", "测评"], "测评授权书", False),
    # 添加新规则
    (["关键词1", "关键词2"], "你的文档类型", False),  # False=项目级
    # 或
    (["关键词1", "关键词2"], "你的文档类型", True),   # True=系统级
]
```

**步骤3**：测试分类器

```bash
python doc_classifier.py
```

### 修改现有规则

**示例**：修改"测评授权书"的关键词

```python
# 原规则
(["授权书", "测评"], "测评授权书", False),

# 修改为（更宽松）
(["授权书"], "测评授权书", False),

# 或（更严格）
(["授权书", "测评", "现场"], "测评授权书", False),
```

### 规则优先级

规则按照列表顺序匹配，**第一个匹配的规则生效**。

```python
CLASSIFICATION_RULES = [
    # 这个规则会先匹配
    (["测评方案", "评审"], "测评方案评审记录", True),

    # 如果上面没匹配，才会匹配这个
    (["测评方案", "确认"], "测评方案确认书", True),
]
```

**建议**：将更具体的规则放在前面。

---

## 文件命名配置

### 命名规则

**位置**：`doc_classifier.py` 第78-110行

```python
def generate_filename(
    self,
    doc_type: str,
    project_name: str = "",
    system_name: str = "",
    is_system_level: bool = False,
    page_num: int = 1
) -> str:
    if is_system_level and system_name:
        # 系统级文档：系统名-文档类型
        base_name = f"{system_name}-{doc_type}"
    elif project_name:
        # 项目级文档：项目名-文档类型
        base_name = f"{project_name}-{doc_type}"
    else:
        # 未指定名称：文档类型
        base_name = doc_type

    # 如果页码>1，添加页码后缀
    if page_num > 1:
        base_name = f"{base_name}-{page_num}"

    return base_name
```

### 自定义命名格式

**示例1**：添加日期

```python
from datetime import datetime

def generate_filename(self, ...):
    date_str = datetime.now().strftime("%Y%m%d")
    base_name = f"{project_name}-{doc_type}-{date_str}"
    return base_name
```

**示例2**：使用序号代替页码

```python
# 维护一个计数器
self.doc_counters = {}

def generate_filename(self, ...):
    # 获取当前类型的计数
    count = self.doc_counters.get(doc_type, 0) + 1
    self.doc_counters[doc_type] = count

    base_name = f"{project_name}-{doc_type}-{count:02d}"
    return base_name
```

---

## 输出目录配置

### 默认输出目录

**位置**：`pdf_processor.py` 第380行

```python
output_dir = input("请输入输出目录（默认为当前目录）: ").strip() or "."
```

**修改为固定目录**：

```python
output_dir = input("请输入输出目录（默认为./output）: ").strip() or "./output"
```

### 自定义文件夹结构

**位置**：`doc_classifier.py` 第14行

```python
DOC_TYPE_TO_FOLDER = {
    "测评授权书": "01-测评授权书",  # 添加序号
    "风险告知书": "02-风险告知书",
    # ...
}
```

或按类别分组：

```python
DOC_TYPE_TO_FOLDER = {
    "测评授权书": "项目级文档/测评授权书",
    "风险告知书": "项目级文档/风险告知书",
    "测评调研表": "系统级文档/测评调研表",
    # ...
}
```

---

## 性能优化配置

### 并发处理

v1.5.1 已内置 OCR 并行识别，默认 5 并发：

```python
# 默认配置（5 并发）
processor = PDFProcessor(ocr_engine="aliyun", max_workers=5)

# 自定义并发数
processor = PDFProcessor(ocr_engine="aliyun", max_workers=3)   # 降低并发
processor = PDFProcessor(ocr_engine="aliyun", max_workers=8)   # 提高并发
```

**并发数建议**：
| OCR 引擎 | 建议并发数 | 说明 |
|----------|----------|------|
| 阿里云 OCR | 5-8 | API 限流宽松 |
| PaddleOCR-VL-1.5 | 3-5 | SiliconFlow 免费用户限流 |
| Claude Sonnet 4.6 | 3-5 | Anthropic API 限流 |

**性能提升**：14 页 PDF 从 ~28 秒降至 ~8 秒（约 3.4 倍加速）。

**注意**：并发数过高会触发API限流错误。

### 缓存OCR结果

避免重复识别相同的页面：

```python
import hashlib
import json

class PDFProcessor:
    def __init__(self, ...):
        self.ocr_cache = {}
        self.cache_file = "ocr_cache.json"
        self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                self.ocr_cache = json.load(f)

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.ocr_cache, f)

    def _ocr_page(self, page):
        # 计算页面哈希
        pix = page.get_pixmap(dpi=self.dpi)
        page_hash = hashlib.md5(pix.samples).hexdigest()

        # 检查缓存
        if page_hash in self.ocr_cache:
            return self.ocr_cache[page_hash]

        # OCR识别
        text = self.ocr.recognize_general(tmp_path)

        # 保存到缓存
        self.ocr_cache[page_hash] = text
        self.save_cache()

        return text
```

---

## 日志配置

### 添加日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_processor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 在代码中使用
logger.info(f"开始处理PDF: {pdf_path}")
logger.error(f"OCR识别失败: {e}")
```

---

## 安全配置

### 保护敏感信息

1. **不要将AppCode提交到版本控制**

   创建 `.gitignore`：
   ```
   config.ini
   *.log
   __pycache__/
   *.pyc
   venv/
   ```

2. **使用环境变量**

   推荐使用环境变量而不是硬编码。

3. **限制文件访问权限**

   ```bash
   chmod 600 config.ini  # 只有所有者可读写
   ```

---

## 故障排查配置

### 启用详细输出

在 `pdf_processor.py` 中添加：

```python
DEBUG = True  # 设置为True启用调试模式

if DEBUG:
    print(f"[DEBUG] 提取的原始文本: {text}")
    print(f"[DEBUG] 文本长度: {len(text)}")
    print(f"[DEBUG] 分类结果: {doc_type}, {is_system_level}")
```

### 保存中间结果

```python
# 保存拆分的PDF
temp_dir = output_base_dir / "temp_split"

# 保存OCR识别的图片
ocr_images_dir = output_base_dir / "ocr_images"
ocr_images_dir.mkdir(exist_ok=True)
pix.save(ocr_images_dir / f"page_{page_num:03d}.png")

# 保存识别的文本
text_dir = output_base_dir / "extracted_text"
text_dir.mkdir(exist_ok=True)
with open(text_dir / f"page_{page_num:03d}.txt", 'w') as f:
    f.write(text)
```
