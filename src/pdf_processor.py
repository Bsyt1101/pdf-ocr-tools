#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 文档自动拆分和重命名处理器
支持多种 OCR 引擎：阿里云 OCR、DeepSeek-OCR
"""

import os
import sys
import fitz  # PyMuPDF
import base64
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from doc_classifier import DocumentClassifier

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("警告：未安装 python-docx，无法读取Word文件。请运行: pip install python-docx")


class AliyunOCR:
    """阿里云市场 OCR 客户端"""

    def __init__(self, app_code: str = None):
        """
        初始化阿里云市场 OCR 客户端

        Args:
            app_code: 阿里云市场 AppCode（可从环境变量读取）
        """
        self.app_code = app_code or os.getenv('ALIYUN_OCR_APPCODE')

        if not self.app_code:
            raise ValueError(
                "请设置阿里云市场 AppCode！\n"
                "方法1: 设置环境变量 ALIYUN_OCR_APPCODE\n"
                "方法2: 在初始化时传入 app_code 参数"
            )

        self.api_url = "https://tysbgpu.market.alicloudapi.com/api/predict/ocr_general"
        print("阿里云市场 OCR 客户端初始化成功")

    def get_display_name(self) -> str:
        """获取 OCR 引擎的显示名称"""
        return "阿里云 OCR"

    def recognize_general(self, image_path: str) -> str:
        """
        通用文字识别

        Args:
            image_path: 图片文件路径

        Returns:
            识别的文本内容
        """
        try:
            import requests
            import json

            # 读取图片并转为 base64
            with open(image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')

            # 构建请求
            headers = {
                'Authorization': f'APPCODE {self.app_code}',
                'Content-Type': 'application/json; charset=UTF-8'
            }

            body = {
                "image": image_base64,
                "configure": {
                    "min_size": 16,
                    "output_prob": False,
                    "output_keypoints": False
                }
            }

            # 调用 API
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(body),
                timeout=30
            )

            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('ret'):
                    # 提取所有文本行
                    text_lines = []
                    for item in result['ret']:
                        if 'word' in item:
                            text_lines.append(item['word'])
                    return '\n'.join(text_lines)
                else:
                    print(f"    OCR 识别失败: {result.get('message', '未知错误')}")
                    return ""
            else:
                print(f"    API 调用失败: HTTP {response.status_code}")
                return ""

        except ImportError:
            print("错误：requests 库未安装")
            print("请运行: pip install requests")
            return ""
        except Exception as e:
            print(f"    阿里云 OCR 识别失败: {e}")
            return ""


class DeepSeekOCR:
    """DeepSeek-OCR 客户端（通过 SiliconFlow API）"""

    def __init__(self, api_key: str = None):
        """
        初始化 DeepSeek-OCR 客户端

        Args:
            api_key: SiliconFlow API Key（可从环境变量读取）
        """
        self.api_key = api_key or os.getenv('SILICONFLOW_API_KEY')

        if not self.api_key:
            raise ValueError(
                "请设置 SiliconFlow API Key！\n"
                "方法1: 设置环境变量 SILICONFLOW_API_KEY\n"
                "方法2: 在初始化时传入 api_key 参数"
            )

        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model = "PaddlePaddle/PaddleOCR-VL-1.5"
        print("PaddleOCR-VL-1.5 客户端初始化成功")

    def get_display_name(self) -> str:
        """获取 OCR 引擎的显示名称"""
        return "PaddleOCR-VL-1.5"

    def recognize_general(self, image_path: str) -> str:
        """
        通用文字识别

        Args:
            image_path: 图片文件路径

        Returns:
            识别的文本内容
        """
        try:
            import requests
            import json
            from PIL import Image

            # 读取并压缩图片（降低 token 消耗）
            img = Image.open(image_path)

            # 如果图片太大，压缩到合适的尺寸
            max_size = 1024  # 最大边长
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # 转换为 RGB（如果是 RGBA）
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # 保存到临时文件
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                img.save(tmp_path, 'JPEG', quality=85)

            try:
                # 读取压缩后的图片并转为 base64
                with open(tmp_path, 'rb') as f:
                    image_data = f.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
            finally:
                # 删除临时文件
                try:
                    os.unlink(tmp_path)
                except:
                    pass

            # 判断图片格式
            mime_type = 'image/jpeg'

            # 构建请求（OpenAI 兼容格式）
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            # 根据模型类型选择合适的 prompt
            if "PaddleOCR" in self.model or "DeepSeek-OCR" in self.model:
                # PaddleOCR-VL 和 DeepSeek-OCR 是专门的 OCR 模型，使用最简单的 prompt
                ocr_prompt = "识别图片中的所有文字"
            else:
                # DeepSeek-VL2 等通用模型，使用详细的 prompt
                ocr_prompt = "请识别图片中的所有文字内容。重要提示：\n1. 优先识别页面顶部的文件编号（格式如：JDB25300-XXXX-01）\n2. 按从上到下、从左到右的顺序输出\n3. 保持原始布局\n4. 不要添加任何解释或说明"

            body = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": ocr_prompt
                            }
                        ]
                    }
                ],
                "stream": False,
                "max_tokens": 2048,  # 降低到 2048，为图片 token 留出空间
                "temperature": 0.1,
                "top_p": 0.7
            }

            # 调用 API
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(body),
                timeout=60
            )

            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    return content.strip()
                else:
                    print(f"    OCR 识别失败: 响应格式错误")
                    return ""
            else:
                error_msg = response.text
                print(f"    API 调用失败: HTTP {response.status_code}")
                print(f"    错误信息: {error_msg}")
                return ""

        except ImportError as e:
            if 'PIL' in str(e):
                print("错误：Pillow 库未安装")
                print("请运行: pip install Pillow")
            else:
                print("错误：requests 库未安装")
                print("请运行: pip install requests")
            return ""
        except Exception as e:
            print(f"    DeepSeek-OCR 识别失败: {e}")
            return ""


class LocalPaddleOCR:
    """本地 PaddleOCR-VL 客户端（直接加载模型或通过 MLX-VLM 服务）"""

    # 类级别的模型缓存（单例模式）
    _shared_model = None
    _shared_processor = None
    _model_lock = None

    def __init__(self, base_url: str = None, model_path: str = None, use_direct: bool = False):
        """
        初始化本地 PaddleOCR-VL 客户端

        Args:
            base_url: 本地服务地址（默认 http://localhost:8111）
            model_path: 模型路径或模型名称
            use_direct: 是否直接加载模型（不使用 HTTP 服务）
        """
        self.base_url = base_url or os.getenv('LOCAL_PADDLEOCR_URL', 'http://localhost:8111')
        self.model_path = model_path or os.getenv('LOCAL_PADDLEOCR_MODEL', 'mlx-community/PaddleOCR-VL-1.5-bf16')
        self.use_direct = use_direct or os.getenv('LOCAL_PADDLEOCR_DIRECT', '').lower() == 'true'

        # 初始化锁（用于线程安全的模型加载）
        if LocalPaddleOCR._model_lock is None:
            import threading
            LocalPaddleOCR._model_lock = threading.Lock()

        if self.use_direct:
            print(f"本地 PaddleOCR-VL 客户端初始化（直接加载模型）")
            print(f"  模型: {self.model_path}")
        else:
            print(f"本地 PaddleOCR-VL 客户端初始化成功（{self.base_url}）")
            print(f"  模型: {self.model_path}")

    def get_display_name(self) -> str:
        """获取 OCR 引擎的显示名称"""
        return "PaddleOCR-VL-1.5（本地）"

    def recognize_general(self, image_path: str) -> str:
        """
        通用文字识别

        Args:
            image_path: 图片文件路径

        Returns:
            识别的文本内容
        """
        if self.use_direct:
            return self._recognize_direct(image_path)
        else:
            return self._recognize_via_api(image_path)

    def _recognize_direct(self, image_path: str) -> str:
        """直接加载模型进行识别（线程安全）"""
        try:
            from mlx_vlm import load, generate
            from mlx_vlm.prompt_utils import apply_chat_template
            from PIL import Image

            # 使用锁确保模型只加载一次（线程安全）
            with LocalPaddleOCR._model_lock:
                if LocalPaddleOCR._shared_model is None:
                    print(f"  正在加载模型: {self.model_path}")
                    LocalPaddleOCR._shared_model, LocalPaddleOCR._shared_processor = load(self.model_path)
                    print(f"  ✓ 模型加载完成")

            # 加载图片（使用 PIL）
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # 构建 prompt
            prompt = apply_chat_template(
                LocalPaddleOCR._shared_processor,
                config=LocalPaddleOCR._shared_model.config,
                prompt="识别图片中的所有文字",
                num_images=1
            )

            # 生成结果（image 作为关键字参数）
            output = generate(
                LocalPaddleOCR._shared_model,
                LocalPaddleOCR._shared_processor,
                prompt,
                image=image,
                max_tokens=2048,
                temperature=0.0
            )

            # 提取文本内容
            if hasattr(output, 'text'):
                return output.text.strip()
            elif isinstance(output, str):
                return output.strip()
            else:
                return str(output).strip()

        except ImportError as e:
            print(f"    错误: mlx_vlm 或 PIL 库未安装")
            print(f"    请运行: pip install mlx-vlm>=0.3.11 Pillow")
            return ""
        except Exception as e:
            print(f"    本地模型识别失败: {e}")
            import traceback
            traceback.print_exc()
            return ""

    def _recognize_via_api(self, image_path: str) -> str:
        """通过 HTTP API 进行识别"""
        try:
            import requests
            import json
            from PIL import Image

            # 读取并压缩图片
            img = Image.open(image_path)

            # 压缩到合适的尺寸
            max_size = 1024
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # 转换为 RGB
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # 保存到临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                img.save(tmp_path, 'JPEG', quality=85)

            try:
                # 读取图片并转为 base64
                with open(tmp_path, 'rb') as f:
                    image_data = f.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
            finally:
                # 删除临时文件
                try:
                    os.unlink(tmp_path)
                except:
                    pass

            # 构建请求（MLX-VLM 格式）
            headers = {
                'Content-Type': 'application/json'
            }

            body = {
                "model": self.model_path,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "识别图片中的所有文字"},
                            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_base64}"}
                        ]
                    }
                ],
                "max_output_tokens": 2048
            }

            # 调用本地 API
            response = requests.post(
                f"{self.base_url}/responses",
                headers=headers,
                data=json.dumps(body),
                timeout=60
            )

            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if 'output' in result and len(result['output']) > 0:
                    if 'content' in result['output'][0] and len(result['output'][0]['content']) > 0:
                        content = result['output'][0]['content'][0].get('text', '')
                        return content.strip()
                print(f"    OCR 识别失败: 响应格式错误")
                return ""
            else:
                error_msg = response.text
                print(f"    本地 API 调用失败: HTTP {response.status_code}")
                print(f"    错误信息: {error_msg}")
                return ""

        except requests.exceptions.ConnectionError:
            print(f"    连接失败: 无法连接到本地服务 {self.base_url}")
            print(f"    请确保 MLX-VLM 服务正在运行: mlx_vlm.server --port 8111")
            return ""
        except ImportError as e:
            if 'PIL' in str(e):
                print("错误：Pillow 库未安装")
                print("请运行: pip install Pillow")
            else:
                print("错误：requests 库未安装")
                print("请运行: pip install requests")
            return ""
        except Exception as e:
            print(f"    本地 PaddleOCR-VL 识别失败: {e}")
            return ""



class PDFProcessor:
    """PDF 文档处理器（支持多种 OCR 引擎）"""

    def __init__(
        self,
        app_code: str = None,
        api_key: str = None,
        ocr_engine: str = "aliyun",
        text_threshold: int = 50,
        dpi: int = 300,
        max_workers: int = 5
    ):
        """
        初始化处理器

        Args:
            app_code: 阿里云市场 AppCode（使用阿里云 OCR 时需要）
            api_key: SiliconFlow API Key（使用 PaddleOCR 时需要）
            ocr_engine: OCR 引擎选择，可选值：
                - "aliyun": 阿里云 OCR（默认）
                - "deepseek": PaddleOCR-VL-1.5（通过 SiliconFlow）
                - "local": PaddleOCR-VL-1.5（本地 MLX-VLM）
            text_threshold: 文本提取阈值，少于此字符数则使用 OCR
            dpi: OCR 时的图片 DPI
            max_workers: OCR 并发数，默认 5
        """
        self.text_threshold = text_threshold
        self.dpi = dpi
        self.classifier = DocumentClassifier()
        self.ocr = None  # 延迟加载 OCR
        self.ocr_engine = ocr_engine.lower()
        self.app_code = app_code
        self.api_key = api_key
        self.max_workers = max_workers

        # 验证 OCR 引擎选择
        if self.ocr_engine not in ["aliyun", "deepseek", "local"]:
            raise ValueError(f"不支持的 OCR 引擎: {ocr_engine}，可选值: aliyun, deepseek, local")

    def _init_ocr(self):
        """延迟初始化 OCR（避免不需要时加载）"""
        if self.ocr is None:
            if self.ocr_engine == "aliyun":
                print("正在初始化阿里云市场 OCR...")
                self.ocr = AliyunOCR(self.app_code)
            elif self.ocr_engine == "deepseek":
                print("正在初始化 DeepSeek-OCR...")
                self.ocr = DeepSeekOCR(self.api_key)
            elif self.ocr_engine == "local":
                print("正在初始化本地 PaddleOCR-VL...")
                self.ocr = LocalPaddleOCR()

    def _get_ocr_display_name(self) -> str:
        """
        获取 OCR 引擎的显示名称

        Returns:
            OCR 引擎的显示名称
        """
        # 如果 OCR 已初始化，直接从实例获取
        if self.ocr and hasattr(self.ocr, 'get_display_name'):
            return self.ocr.get_display_name()

        # 如果未初始化，返回默认名称
        if self.ocr_engine == "deepseek":
            return "PaddleOCR-VL-1.5"
        elif self.ocr_engine == "local":
            return "PaddleOCR-VL-1.5（本地）"
        else:
            return "阿里云 OCR"


    def read_system_names_from_word(self, pdf_dir: Path) -> Dict[int, str]:
        """
        从项目实施申请单Word文件中读取系统名称

        在PDF所在目录下搜索"项目实施单"文件夹，读取"项目实施申请单"Word文件
        提取"序号"列和"系统名称"列的对应关系

        Args:
            pdf_dir: PDF文件所在目录

        Returns:
            字典：{序号: 系统名称}，例如 {1: "门户网站系统", 2: "内部办公系统"}
        """
        if not DOCX_AVAILABLE:
            print("警告：未安装 python-docx，无法读取系统名称")
            return {}

        # 搜索"项目实施单"文件夹（先在当前目录，再在父目录）
        impl_folder = None
        search_dirs = [pdf_dir, pdf_dir.parent]  # 当前目录和父目录

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for item in search_dir.iterdir():
                if item.is_dir() and "项目实施单" in item.name:
                    impl_folder = item
                    break
            if impl_folder:
                break

        if not impl_folder:
            print(f"警告：未找到包含'项目实施单'的文件夹（已搜索当前目录和父目录）")
            return {}

        print(f"找到项目实施单文件夹: {impl_folder.name}")

        # 搜索"项目实施申请单"Word文件
        word_file = None
        for item in impl_folder.iterdir():
            if item.is_file() and "项目实施申请单" in item.name and item.suffix in ['.docx', '.doc']:
                word_file = item
                break

        if not word_file:
            print(f"警告：未找到'项目实施申请单'Word文件")
            return {}

        print(f"找到Word文件: {word_file.name}")

        try:
            # 读取Word文件
            doc = Document(word_file)
            system_names = {}

            # 遍历所有表格
            for table in doc.tables:
                # 查找表头行
                header_row = None
                seq_col_idx = None
                system_col_idx = None

                for row_idx, row in enumerate(table.rows):
                    cells_text = [cell.text.strip() for cell in row.cells]

                    # 查找"序号"和"系统名称"列
                    for col_idx, text in enumerate(cells_text):
                        if "序号" in text:
                            seq_col_idx = col_idx
                        if "系统名称" in text:
                            system_col_idx = col_idx

                    # 找到"系统名称"列即可（序号列可选）
                    if system_col_idx is not None:
                        header_row = row_idx
                        break

                # 如果找到了表头，读取数据行
                if header_row is not None:
                    auto_seq = 1  # 无序号列时自动编号
                    for row_idx in range(header_row + 1, len(table.rows)):
                        row = table.rows[row_idx]
                        try:
                            system_text = row.cells[system_col_idx].text.strip()

                            if not system_text:
                                continue

                            # 跳过非系统名称的行（如"其他要求"等）
                            skip_keywords = ["其他要求", "项目实施", "备注"]
                            if any(kw in system_text for kw in skip_keywords):
                                continue

                            if seq_col_idx is not None:
                                # 有序号列，使用序号
                                seq_text = row.cells[seq_col_idx].text.strip()
                                if seq_text:
                                    try:
                                        seq_num = int(seq_text)
                                        system_names[seq_num] = system_text
                                        print(f"  读取: 序号 {seq_num} → {system_text}")
                                        continue
                                    except ValueError:
                                        pass

                            # 无序号列或序号无效，自动编号
                            system_names[auto_seq] = system_text
                            print(f"  读取: 序号 {auto_seq}（自动） → {system_text}")
                            auto_seq += 1

                        except (ValueError, IndexError):
                            continue

            if system_names:
                print(f"成功读取 {len(system_names)} 个系统名称")
            else:
                print("警告：未能从Word文件中读取到系统名称")

            return system_names

        except Exception as e:
            print(f"读取Word文件失败: {e}")
            return {}

    def split_pdf(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        拆分 PDF 为单页文件

        Args:
            pdf_path: PDF 文件路径
            output_dir: 输出目录

        Returns:
            拆分后的单页 PDF 文件路径列表
        """
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(pdf_path)
        page_files = []

        print(f"\n正在拆分 PDF: {pdf_path.name}")
        print(f"总页数: {len(doc)}")

        for page_num in range(len(doc)):
            # 创建新的 PDF 包含单页
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

            # 保存单页 PDF
            output_file = output_dir / f"page_{page_num + 1:03d}.pdf"
            new_doc.save(output_file)
            new_doc.close()

            page_files.append(str(output_file))
            print(f"  拆分第 {page_num + 1} 页 → {output_file.name}")

        doc.close()
        return page_files

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        从 PDF 提取文本（混合方案）

        Args:
            pdf_path: PDF 文件路径

        Returns:
            提取的文本内容
        """
        doc = fitz.open(pdf_path)
        page = doc[0]  # 单页 PDF

        # 1. 尝试提取文本层
        text = page.get_text()

        # 2. 如果文本太少，判断为扫描件，使用 OCR
        if len(text.strip()) < self.text_threshold:
            ocr_name = self._get_ocr_display_name()
            print(f"    扫描件，OCR识别中...", end='', flush=True)
            text = self._ocr_page(page)
            # 显示识别结果预览
            preview = text[:50].replace('\n', ' ') if text else '(空)'
            print(f" ✓ 识别完成: {preview}...")

        doc.close()
        return text.strip()

    def _ocr_page(self, page) -> str:
        """
        对页面进行 OCR 识别

        Args:
            page: PyMuPDF 页面对象

        Returns:
            识别的文本
        """
        # 延迟初始化 OCR
        self._init_ocr()

        # 导入必要的模块
        import tempfile
        from PIL import Image

        # 检查页面方向（横向/纵向）
        rect = page.rect
        is_landscape = rect.width > rect.height

        # 将页面转为图片并保存为临时文件
        pix = page.get_pixmap(dpi=self.dpi)

        # 检测内容方向：如果页面是纵向但内容可能是横向的
        # 通过检查文本块的方向来判断
        if not is_landscape:
            # 尝试提取文本块来判断内容方向
            text_blocks = page.get_text("blocks")
            if text_blocks:
                # 计算文本块的平均宽高比
                total_ratio = 0
                count = 0
                for block in text_blocks:
                    if len(block) >= 5:  # 确保有坐标信息
                        x0, y0, x1, y1 = block[:4]
                        width = x1 - x0
                        height = y1 - y0
                        if height > 0:
                            ratio = width / height
                            total_ratio += ratio
                            count += 1

                # 如果平均宽高比 < 0.5，说明内容可能是横向排版（文本块很窄很高）
                if count > 0 and (total_ratio / count) < 0.5:
                    print(f"    检测到纵向页面但内容横向排版，旋转处理...")
                    is_landscape = True  # 标记为需要旋转

        # 如果是横向页面或内容横向排版，旋转90度以便更好地识别
        if is_landscape:
            print(f"    检测到横向页面 ({rect.width:.0f}x{rect.height:.0f})，旋转处理...")

            # 保存原始图片
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                tmp_path_orig = tmp_file.name
                pix.save(tmp_path_orig)

            # 使用 PIL 旋转图片
            img = Image.open(tmp_path_orig)
            # 尝试旋转90度（顺时针），使页眉在顶部
            img_rotated = img.rotate(-90, expand=True)

            # 保存旋转后的图片
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                img_rotated.save(tmp_path)

            # 清理原始临时文件
            try:
                os.unlink(tmp_path_orig)
            except:
                pass
        else:
            # 纵向页面，直接保存
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                pix.save(tmp_path)

        # OCR 识别
        try:
            text = self.ocr.recognize_general(tmp_path)
            return text
        finally:
            # 删除临时文件
            try:
                os.unlink(tmp_path)
            except:
                pass

    def _extract_text_single(self, page_file: str) -> dict:
        """
        提取单页文本（线程池任务）

        Args:
            page_file: 单页 PDF 文件路径

        Returns:
            包含 page_num、page_file、text 的字典
        """
        page_num = int(Path(page_file).stem.split('_')[1])
        try:
            text = self.extract_text_from_pdf(page_file)
        except Exception as e:
            print(f"  ⚠️ 第 {page_num} 页文本提取失败: {e}")
            text = ""
        return {'page_num': page_num, 'page_file': page_file, 'text': text}

    def _extract_texts_parallel(self, page_files: list) -> list:
        """
        并行提取所有页面文本（本地直接加载模式自动切换为串行）

        Args:
            page_files: 单页 PDF 文件路径列表

        Returns:
            按原始顺序排列的文本提取结果列表
        """
        # 预初始化 OCR（避免多线程竞争）
        self._init_ocr()

        total = len(page_files)

        # 检查是否使用本地直接加载模式
        use_serial = False
        if self.ocr_engine == "local":
            if hasattr(self.ocr, 'use_direct') and self.ocr.use_direct:
                use_serial = True
                print("  （本地直接加载模式，使用串行处理以避免崩溃）")

        if use_serial:
            # 串行处理（本地直接加载模式）
            results = []
            for i, page_file in enumerate(page_files):
                try:
                    result = self._extract_text_single(page_file)
                    results.append(result)
                    print(f"  [{i+1}/{total}] 第 {result['page_num']} 页 文本提取完成")
                except Exception as e:
                    page_num = int(Path(page_file).stem.split('_')[1])
                    print(f"  [{i+1}/{total}] 第 {page_num} 页 ⚠️ 提取异常: {e}")
                    results.append({
                        'page_num': page_num,
                        'page_file': page_file,
                        'text': ''
                    })
            return results
        else:
            # 并行处理（其他 OCR 引擎）
            from concurrent.futures import ThreadPoolExecutor, as_completed

            results = [None] * total
            completed_count = 0

            with ThreadPoolExecutor(max_workers=min(self.max_workers, total)) as executor:
                future_to_idx = {
                    executor.submit(self._extract_text_single, pf): i
                    for i, pf in enumerate(page_files)
                }
                for future in as_completed(future_to_idx):
                    idx = future_to_idx[future]
                    completed_count += 1
                    try:
                        result = future.result()
                        results[idx] = result
                        print(f"  [{completed_count}/{total}] 第 {result['page_num']} 页 文本提取完成")
                    except Exception as e:
                        page_num = int(Path(page_files[idx]).stem.split('_')[1])
                        print(f"  [{completed_count}/{total}] 第 {page_num} 页 ⚠️ 提取异常: {e}")
                        results[idx] = {
                            'page_num': page_num,
                            'page_file': page_files[idx],
                            'text': ''
                        }

            return results

    def process_pdf(
        self,
        pdf_path: str,
        project_name: str = "",
        system_name: str = "",
        output_base_dir: str = "."
    ):
        """
        处理 PDF：拆分、识别、重命名、归档

        Args:
            pdf_path: PDF 文件路径
            project_name: 项目名称
            system_name: 系统名称（可选，如果不提供则从Word文件读取）
            output_base_dir: 输出基础目录
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            print(f"错误：文件不存在 {pdf_path}")
            return

        output_base_dir = Path(output_base_dir)
        pdf_dir = pdf_path.parent

        # 0. 读取系统名称（如果未提供）
        system_names_map = {}
        if not system_name:
            print("\n尝试从项目实施申请单读取系统名称...")
            system_names_map = self.read_system_names_from_word(pdf_dir)

        # 1. 拆分 PDF
        temp_dir = output_base_dir / "temp_split"
        page_files = self.split_pdf(pdf_path, temp_dir)

        # 2. 并行提取所有页面文本
        print(f"\n开始识别文档类型...（{min(self.max_workers, len(page_files))} 并发）")
        text_results = self._extract_texts_parallel(page_files)

        # 3. 串行处理分类
        results = []

        for tr in text_results:
            page_num = tr['page_num']
            page_file = tr['page_file']
            text = tr['text']
            print(f"\n处理第 {page_num} 页:")
            print(f"  提取文本: {text[:100]}..." if len(text) > 100 else f"  提取文本: {text}")

            # 分类文档
            doc_type, is_system_level = self.classifier.classify(text)

            if doc_type:
                print(f"  识别类型: {doc_type} ({'系统级' if is_system_level else '项目级'})")

                # 确定使用的系统名称
                current_system_name = system_name
                system_name_source = None  # 记录系统名称来源：'file_code', 'fuzzy_match', 'content_extract'
                file_code_system_seq = None  # 记录文件编号中的系统序号

                if is_system_level and not system_name:
                    # 方式1：从文件编号 + Word映射表获取系统名称
                    if system_names_map:
                        file_code = self.classifier.extract_file_code(text)
                        print(f"  提取文件编号: {file_code}")
                        if file_code:
                            try:
                                system_seq = int(file_code['system_code'])
                                file_code_system_seq = system_seq  # 保存文件编号中的系统序号
                                print(f"  系统序号: {system_seq}")
                                print(f"  系统名称映射: {system_names_map}")
                                if system_seq in system_names_map:
                                    current_system_name = system_names_map[system_seq]
                                    system_name_source = 'file_code'
                                    print(f"  ✓ 使用系统名称: {current_system_name} (序号 {system_seq})")
                                else:
                                    print(f"  ✗ 未找到序号 {system_seq} 对应的系统名称")
                            except (ValueError, KeyError) as e:
                                print(f"  ✗ 转换失败: {e}")

                    # 方式2：从 Word 系统名称列表中匹配 OCR 文本（模糊匹配）
                    if not current_system_name and system_names_map:
                        matched_seq = None
                        for seq, name in system_names_map.items():
                            # 去掉常见后缀进行模糊匹配
                            name_core = name.replace('系统', '').replace('平台', '').strip()
                            if name in text or name_core in text:
                                current_system_name = name
                                matched_seq = seq
                                system_name_source = 'fuzzy_match'
                                print(f"  ✓ 从文本匹配系统名称: {current_system_name} (模糊匹配，序号 {seq})")
                                break

                        # 验证：如果有文件编号，检查匹配的系统序号是否一致
                        if current_system_name and file_code_system_seq is not None and matched_seq != file_code_system_seq:
                            print(f"  ⚠️  警告：系统名称不一致！")
                            print(f"      - 文件编号中的系统序号: {file_code_system_seq}")
                            print(f"      - 匹配到的系统名称: {current_system_name} (序号 {matched_seq})")
                            print(f"      - 建议检查文件编号或系统名称是否正确")

                    # 方式3：从 OCR 文本内容提取系统名称
                    if not current_system_name:
                        extracted_name = self.classifier.extract_system_name_from_content(text)
                        if extracted_name:
                            current_system_name = extracted_name
                            system_name_source = 'content_extract'
                            print(f"  ✓ 从内容提取系统名称: {current_system_name}")

                            # 验证：如果有文件编号和Word映射表，检查提取的系统名称是否与文件编号一致
                            if file_code_system_seq is not None and system_names_map:
                                expected_name = system_names_map.get(file_code_system_seq)
                                if expected_name and expected_name != current_system_name:
                                    # 检查是否是同一个系统（去掉"系统"/"平台"后缀比较）
                                    extracted_core = current_system_name.replace('系统', '').replace('平台', '').strip()
                                    expected_core = expected_name.replace('系统', '').replace('平台', '').strip()
                                    if extracted_core not in expected_core and expected_core not in extracted_core:
                                        print(f"  ⚠️  警告：系统名称不一致！")
                                        print(f"      - 文件编号中的系统序号: {file_code_system_seq}")
                                        print(f"      - 实施单中对应的系统名称: {expected_name}")
                                        print(f"      - 页面提取的系统名称: {current_system_name}")
                                        print(f"      - 建议检查文件编号或页面内容是否正确")
                        else:
                            print(f"  ✗ 未能提取系统名称")

                # 生成文件名（不使用文件编号，不添加页码）
                filename = self.classifier.generate_filename(
                    doc_type, text, project_name, current_system_name, is_system_level, page_num
                )

                # 获取目标文件夹
                folder = self.classifier.get_folder_name(doc_type)

                # 提取文件编号（用于后续合并判断）
                file_code = self.classifier.extract_file_code(text)

                results.append({
                    'page': page_num,
                    'source': page_file,
                    'doc_type': doc_type,
                    'is_system_level': is_system_level,
                    'system_name': current_system_name,
                    'file_code': file_code,  # 保存文件编号用于合并
                    'filename': filename,
                    'folder': folder,
                    'text_preview': text[:200]
                })
            else:
                print(f"  识别类型: 未识别")
                results.append({
                    'page': page_num,
                    'source': page_file,
                    'doc_type': None,
                    'is_system_level': False,
                    'system_name': "",
                    'file_code': None,
                    'filename': f"未分类-page_{page_num:03d}",
                    'folder': "未分类",
                    'text_preview': text[:200]
                })

        # 3. 显示处理结果摘要
        self._print_summary(results, project_name, system_name)

        # 4. 询问是否执行归档
        print("\n" + "=" * 60)
        confirm = input("是否执行文件归档？(y/n): ").strip().lower()

        if confirm == 'y':
            # 4.1 合并同一文档的多页
            print("\n检查是否需要合并页面...")
            merged_results = self._merge_pages(results, temp_dir)

            # 4.2 使用PDF文件所在目录作为搜索基础目录
            pdf_dir = pdf_path.parent
            self._archive_files(merged_results, pdf_dir)
            print("\n归档完成！")
        else:
            print("\n已取消归档。拆分的文件保存在:", temp_dir)

    def _get_merge_key(self, result: dict) -> str:
        """
        生成合并键，用于判断哪些页面应该合并

        优先级：
        1. 如果有文件编号，使用文件编号作为键
        2. 如果没有文件编号，使用文档类型+系统名称作为键

        Args:
            result: 页面处理结果

        Returns:
            合并键字符串
        """
        file_code = result.get('file_code')

        if file_code:
            # 方案A：基于文件编号（最准确）
            project_code = file_code.get('project_code', '')
            doc_type_code = file_code.get('doc_type_code', '')
            system_code = file_code.get('system_code', '')
            return f"{project_code}-{doc_type_code}-{system_code}"
        else:
            # 方案B：基于文档类型+系统名称（备用）
            doc_type = result.get('doc_type', '')
            system_name = result.get('system_name', '')
            is_system_level = result.get('is_system_level', False)

            if is_system_level and system_name:
                # 系统级文档：使用系统名称+文档类型
                return f"{system_name}-{doc_type}"
            else:
                # 项目级文档：使用文档类型
                return doc_type or 'unknown'

    def _merge_pages(self, results: List[dict], temp_dir: Path) -> List[dict]:
        """
        合并同一文档的多页

        Args:
            results: 页面处理结果列表
            temp_dir: 临时目录

        Returns:
            合并后的结果列表
        """
        # 1. 按合并键分组
        groups = {}
        for result in results:
            merge_key = self._get_merge_key(result)

            if merge_key not in groups:
                groups[merge_key] = []

            groups[merge_key].append(result)

        # 2. 处理每个组
        merged_results = []
        merge_count = 0

        for merge_key, group in groups.items():
            if len(group) == 1:
                # 单页，不需要合并
                merged_results.append(group[0])
            else:
                # 多页，需要合并
                print(f"\n发现多页文档: {merge_key}")
                print(f"  页面: {[r['page'] for r in group]}")

                # 检查页面间隔
                page_nums = sorted([r['page'] for r in group])
                max_gap = 5  # 允许的最大页面间隔

                has_large_gap = False
                for i in range(len(page_nums) - 1):
                    gap = page_nums[i + 1] - page_nums[i]
                    if gap > max_gap:
                        print(f"  警告：页面 {page_nums[i]} 和 {page_nums[i + 1]} 间隔较大 (间隔 {gap})")
                        has_large_gap = True

                # 询问是否合并
                if has_large_gap:
                    confirm = input(f"  页面间隔较大，是否仍要合并？(y/n): ").strip().lower()
                    if confirm != 'y':
                        print(f"  跳过合并，保留为单页")
                        merged_results.extend(group)
                        continue

                # 执行合并
                merged_file = self._merge_pdf_files(group, temp_dir)

                if merged_file:
                    # 使用第一页的信息，但更新source
                    merged_result = group[0].copy()
                    merged_result['source'] = merged_file
                    merged_result['page'] = f"{page_nums[0]}-{page_nums[-1]}"  # 显示页面范围
                    merged_results.append(merged_result)
                    merge_count += 1
                    print(f"  ✓ 已合并 {len(group)} 页")
                else:
                    # 合并失败，保留原始页面
                    print(f"  ✗ 合并失败，保留为单页")
                    merged_results.extend(group)

        if merge_count > 0:
            print(f"\n共合并 {merge_count} 个文档")

        return merged_results

    def _merge_pdf_files(self, pages: List[dict], temp_dir: Path) -> Optional[str]:
        """
        合并多个PDF文件

        Args:
            pages: 要合并的页面列表
            temp_dir: 临时目录

        Returns:
            合并后的文件路径，失败返回None
        """
        try:
            # 按页码排序
            pages = sorted(pages, key=lambda p: p['page'])

            # 创建新的PDF
            merged_pdf = fitz.open()

            # 逐页添加
            for page in pages:
                src_pdf = fitz.open(page['source'])
                merged_pdf.insert_pdf(src_pdf)
                src_pdf.close()

            # 生成合并后的文件名
            first_page = pages[0]['page']
            last_page = pages[-1]['page']
            merged_filename = f"merged_{first_page}_{last_page}.pdf"
            merged_path = temp_dir / merged_filename

            # 保存
            merged_pdf.save(str(merged_path))
            merged_pdf.close()

            return str(merged_path)

        except Exception as e:
            print(f"  合并失败: {e}")
            return None

    def _print_summary(self, results: List[dict], project_name: str, system_name: str):
        """打印处理结果摘要"""
        print("\n" + "=" * 60)
        print("处理结果摘要")
        print("=" * 60)
        print(f"项目名称: {project_name or '(未指定)'}")
        print(f"系统名称: {system_name or '(未指定)'}")
        print(f"总页数: {len(results)}")
        print()

        # 按文档类型分组统计
        type_counts = {}
        for r in results:
            doc_type = r['doc_type'] or '未识别'
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1

        print("文档类型统计:")
        for doc_type, count in sorted(type_counts.items()):
            print(f"  {doc_type}: {count} 页")

        print("\n详细列表:")
        for r in results:
            print(f"  第 {r['page']:2d} 页 → {r['filename']}.pdf")
            print(f"           类型: {r['doc_type'] or '未识别'}")
            print(f"           文件夹: {r['folder']}")
            print()

    def _find_matching_folder(self, base_dir: Path, folder_keyword: str) -> Optional[Path]:
        """
        在基础目录下搜索包含关键词的文件夹

        Args:
            base_dir: 基础目录（PDF文件所在目录）
            folder_keyword: 文件夹关键词（如：现场接收归还文档清单）

        Returns:
            匹配的文件夹路径，如果未找到则返回None
        """
        if not base_dir.exists():
            return None

        # 遍历基础目录下的所有文件夹
        for item in base_dir.iterdir():
            if item.is_dir():
                # 检查文件夹名称是否包含关键词
                if folder_keyword in item.name:
                    return item

        return None

    def _archive_files(self, results: List[dict], pdf_dir: Path):
        """
        归档文件到对应文件夹

        在PDF文件所在目录下搜索匹配的文件夹，而不是创建新文件夹

        Args:
            results: 处理结果列表
            pdf_dir: PDF文件所在目录
        """
        print("\n开始归档文件...")
        print(f"搜索目录: {pdf_dir}")

        for r in results:
            folder_keyword = r['folder']

            # 搜索匹配的文件夹
            target_folder = self._find_matching_folder(pdf_dir, folder_keyword)

            if target_folder is None:
                # 如果是"未分类"文件夹，自动创建
                if folder_keyword == "未分类":
                    target_folder = pdf_dir / "未分类"
                    target_folder.mkdir(exist_ok=True)
                    print(f"  创建文件夹: {target_folder.name}")
                else:
                    print(f"  警告：未找到包含 '{folder_keyword}' 的文件夹，跳过 {r['filename']}.pdf")
                    continue
            else:
                print(f"  找到文件夹: {target_folder.name}")

            # 目标文件路径
            target_file = target_folder / f"{r['filename']}.pdf"

            # 处理文件名冲突
            counter = 1
            while target_file.exists():
                target_file = target_folder / f"{r['filename']}_{counter}.pdf"
                counter += 1

            # 移动文件
            source = Path(r['source'])
            try:
                source.rename(target_file)
                print(f"  ✓ {source.name} → {target_folder.name}/{target_file.name}")
            except Exception as e:
                print(f"  ✗ 移动失败: {source.name} - {e}")


def main():
    """主函数 - 交互式命令行界面"""
    import argparse

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='PDF 文档自动拆分和归档工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
OCR 引擎选项:
  local     - 本地 PaddleOCR-VL（免费，隐私保护）
  aliyun    - 阿里云 OCR（快速稳定，付费）
  siliconflow - SiliconFlow API（免费额度）

示例:
  python main.py --ocr local
  python main.py --ocr aliyun
  python main.py --ocr siliconflow
        """
    )
    parser.add_argument(
        '--ocr',
        choices=['local', 'aliyun', 'siliconflow'],
        help='指定 OCR 引擎'
    )

    args = parser.parse_args()

    # 自动检测或使用指定的 OCR 引擎
    ocr_engine = "aliyun"  # 默认
    ocr_display_name = "阿里云 OCR（快速稳定）"

    # 如果命令行指定了引擎，优先使用
    if args.ocr:
        ocr_engine = args.ocr if args.ocr != 'siliconflow' else 'deepseek'
        engine_names = {
            'local': 'PaddleOCR-VL-1.5（本地）',
            'aliyun': '阿里云 OCR（快速稳定）',
            'siliconflow': 'PaddleOCR-VL-1.5（SiliconFlow API）'
        }
        ocr_display_name = engine_names.get(args.ocr, ocr_display_name)
    else:
        # 自动检测
        # 优先检测直接加载模式
        if os.getenv('LOCAL_PADDLEOCR_DIRECT', '').lower() == 'true':
            ocr_engine = "local"
            model_path = os.getenv('LOCAL_PADDLEOCR_MODEL', 'mlx-community/PaddleOCR-VL-1.5-bf16')
            ocr_display_name = f"PaddleOCR-VL-1.5（本地直接加载）"
        else:
            # 检测本地 PaddleOCR-VL HTTP 服务
            local_url = os.getenv('LOCAL_PADDLEOCR_URL', 'http://localhost:8111')
            local_available = False
            try:
                import requests
                response = requests.get(f"{local_url}/health", timeout=2)
                if response.status_code == 200:
                    local_available = True
            except:
                pass

            if local_available:
                ocr_engine = "local"
                ocr_display_name = "PaddleOCR-VL-1.5（本地 MLX-VLM 服务）"
            elif os.getenv('ALIYUN_OCR_APPCODE'):
                ocr_engine = "aliyun"
                ocr_display_name = "阿里云 OCR（快速稳定）"
            elif os.getenv('SILICONFLOW_API_KEY'):
                ocr_engine = "deepseek"
                ocr_display_name = "PaddleOCR-VL-1.5（专业OCR模型）"

    print("=" * 60)
    print("PDF 文档自动拆分和重命名工具")
    print(f"使用 {ocr_display_name}")
    print("=" * 60)

    # 输入 PDF 路径
    pdf_path = input("\n请输入 PDF 文件路径: ").strip().strip("'\"")
    if not pdf_path:
        print("错误：未输入文件路径")
        return

    # 输入项目信息
    project_name = input("请输入项目名称（可选）: ").strip()
    system_name = input("请输入系统名称（可选）: ").strip()

    # 输出目录
    output_dir = input("请输入输出目录（默认为当前目录）: ").strip() or "."

    # 创建处理器并处理
    try:
        processor = PDFProcessor(ocr_engine=ocr_engine, max_workers=5)
        processor.process_pdf(pdf_path, project_name, system_name, output_dir)
    except ValueError as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
