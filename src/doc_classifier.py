#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档分类器 - 基于关键词匹配识别等保测评文档类型
支持从文件编号提取信息进行命名
"""

import re
from typing import Optional, Tuple, Dict


class DocumentClassifier:
    """等保测评文档分类器"""

    # 文档类型简拼到全称的映射（系统级文档包含"xxx系统-"前缀）
    DOC_TYPE_CODE_MAP = {
        "CPSQS": "现场测评授权书",
        "FXGZS": "风险告知书",
        "DCB": "xxx系统-情况调查表确认签字",
        "FACS": "xxx系统-测评方案初审记录",
        "FAFS": "xxx系统-测评方案复审记录",
        "FAQR": "xxx系统-测评方案确认书",
        "SCHY": "启动会议记录表及签到表",
        "MCHY": "末次会议记录表及签到表",
        "CPJG": "xxx系统-测评结果记录签字页",
        "CPWT": "xxx系统-测评问题列表签字页",
        "SMQR": "xxx系统-漏洞扫描记录签字确认表",
        "CTCS": "xxx系统-渗透测试记录签字确认表",
        "BGFS": "xxx系统-报告复审记录",
        "BGCS": "xxx系统-报告初审记录",
        "WDJJ": "现场接收归还文档清单",
        "RLCQR": "入场离场确认单",
        "YSB": "项目验收评估表",
        "BMCNS": "保密承诺书",
        # 别名和常见 OCR 识别错误
        "STCS": "xxx系统-渗透测试记录签字确认表",  # STCS -> CTCS
        "WDJ": "现场接收归还文档清单",  # WDJ -> WDJJ
        "PACS": "xxx系统-测评方案初审记录",  # PACS -> FACS (OCR 将 F 误识别为 P)
        "SMOR": "xxx系统-漏洞扫描记录签字确认表",  # SMOR -> SMQR (OCR 将 Q 误识别为 O)
    }

    # 文档类型到文件夹的映射（使用实际文件夹名称的关键词）
    DOC_TYPE_TO_FOLDER = {
        "测评授权书": "测评授权书",
        "现场测评授权书": "测评授权书",
        "风险告知书": "风险告知书",
        "测评调研表": "测评调研表",
        "情况调查表": "测评调研表",
        "情况调查表确认签字": "测评调研表",
        "xxx系统-情况调查表确认签字": "测评调研表",
        "测评方案评审记录": "测评方案评审记录",
        "测评方案初审记录": "测评方案评审记录",
        "xxx系统-测评方案初审记录": "测评方案评审记录",
        "测评方案复审记录": "测评方案评审记录",
        "xxx系统-测评方案复审记录": "测评方案评审记录",
        "测评方案确认书": "测评方案确认书",
        "xxx系统-测评方案确认书": "测评方案确认书",
        "首末次会议记录": "首末次会议记录",
        "启动会议记录": "首末次会议记录",
        "启动会议记录表及签到表": "首末次会议记录",
        "末次会议记录": "首末次会议记录",
        "末次会议记录表及签到表": "首末次会议记录",
        "测评记录及问题汇总": "测评记录及问题汇总",
        "测评结果记录": "测评记录及问题汇总",
        "测评结果记录签字页": "测评记录及问题汇总",
        "xxx系统-测评结果记录签字页": "测评记录及问题汇总",
        "测评问题列表": "测评记录及问题汇总",
        "测评问题列表签字页": "测评记录及问题汇总",
        "xxx系统-测评问题列表签字页": "测评记录及问题汇总",
        "漏洞扫描记录": "漏洞扫描报告",
        "漏洞扫描记录签字确认表": "漏洞扫描报告",
        "xxx系统-漏洞扫描记录签字确认表": "漏洞扫描报告",
        "渗透测试记录": "渗透测试报告",
        "渗透测试记录签字确认表": "渗透测试报告",
        "xxx系统-渗透测试记录签字确认表": "渗透测试报告",
        "报告复审记录": "报告评审记录",
        "xxx系统-报告复审记录": "报告评审记录",
        "报告初审记录": "报告评审记录",
        "xxx系统-报告初审记录": "报告评审记录",
        "现场接收归还文档清单": "现场接收归还文档清单",
        "入离场确认书": "入离场确认书",
        "入离场确认单": "入离场确认书",
        "入场离场确认单": "入离场确认书",
        "项目验收评估表": "项目验收评估表",
        "保密承诺书": "保密承诺书",
    }

    # 分类规则：(关键词列表, 文档类型, 是否系统级文档)
    CLASSIFICATION_RULES = [
        # 项目级文档
        ([("授权书", "测评")], "现场测评授权书", False),
        (["风险告知"], "风险告知书", False),
        (["启动会议"], "启动会议记录表及签到表", False),
        (["末次会议"], "末次会议记录表及签到表", False),
        ([("接收归还", "文档清单")], "现场接收归还文档清单", False),
        (["验收评估"], "项目验收评估表", False),
        (["保密承诺"], "保密承诺书", False),
        ([("入场", "确认")], "入场离场确认单", False),
        ([("离场", "确认")], "入场离场确认单", False),
        ([("入场", "离场")], "入场离场确认单", False),

        # 系统级文档（包含"xxx系统-"前缀）
        (["情况调查表"], "xxx系统-情况调查表确认签字", True),
        ([("测评方案", "初审")], "xxx系统-测评方案初审记录", True),
        ([("测评方案", "评审")], "xxx系统-测评方案复审记录", True),
        ([("测评方案", "复审")], "xxx系统-测评方案复审记录", True),
        ([("测评方案", "确认")], "xxx系统-测评方案确认书", True),
        ([("测评结果", "记录")], "xxx系统-测评结果记录签字页", True),
        (["问题列表"], "xxx系统-测评问题列表签字页", True),
        (["漏洞扫描"], "xxx系统-漏洞扫描记录签字确认表", True),
        (["渗透测试"], "xxx系统-渗透测试记录签字确认表", True),
        ([("报告", "复审")], "xxx系统-报告复审记录", True),
        ([("报告", "初审")], "xxx系统-报告初审记录", True),
    ]

    # 系统级文档类型（用于判断是否需要系统编号）
    SYSTEM_LEVEL_TYPES = {
        "xxx系统-情况调查表确认签字",
        "xxx系统-测评方案初审记录",
        "xxx系统-测评方案复审记录",
        "xxx系统-测评方案确认书",
        "xxx系统-测评结果记录签字页",
        "xxx系统-测评问题列表签字页",
        "xxx系统-漏洞扫描记录签字确认表",
        "xxx系统-渗透测试记录签字确认表",
        "xxx系统-报告复审记录",
        "xxx系统-报告初审记录",
    }

    def extract_file_code(self, text: str) -> Optional[Dict[str, str]]:
        """
        从文本中提取文件编号信息

        格式：JDB25300-CPSQS-01
        - JDB25300: 项目编号
        - CPSQS: 文档类型简拼
        - 01: 系统编号

        支持格式：
        - 标准格式：JDB25300-CPSQS-01
        - 带空格：JDB25300 - CPSQS - 01
        - 大小写混合：JDB25300-Cpsqs-01
        - OCR 错误修正：JD925136 -> JDB25136（自动修正）

        优化策略：
        - 优先提取前20%文本（页眉区域）
        - 如果找不到，再搜索全文
        - 自动修正 OCR 识别错误（JD8/JD9 -> JDB）

        Args:
            text: 文档文本内容

        Returns:
            包含项目编号、文档类型、系统编号的字典，如果未找到则返回None
        """
        # 匹配格式：JD[B]数字-字母-数字（允许空格和大小写混合）
        # 支持 JDB 或 JD 开头（OCR 可能漏识别 B）
        # \s* 允许任意空白字符（空格、换行等）
        pattern = r'(JDB?\d+)\s*-\s*([A-Za-z]+)\s*-\s*(\d+)'

        # 策略1：优先在前20%的文本中查找（页眉区域）
        header_length = max(200, len(text) // 5)  # 至少200字符或前20%
        header_text = text[:header_length]
        match = re.search(pattern, header_text, re.IGNORECASE)

        # 策略2：如果页眉没找到，在全文查找
        if not match:
            match = re.search(pattern, text, re.IGNORECASE)

        if match:
            project_code = match.group(1).upper()  # JDB25300 或 JD925300
            doc_type_code = match.group(2).upper()  # CPSQS（转为大写）
            system_code = match.group(3)    # 01

            # OCR 错误修正：JD8/JD9 -> JDB
            # 如果是 JD 开头且后面紧跟数字（不是 JDB），自动修正为 JDB
            if project_code.startswith('JD') and not project_code.startswith('JDB'):
                # JD925136 -> JDB25136
                # JD825136 -> JDB25136
                original_code = project_code
                # 提取 JD 后面的数字部分
                digits = project_code[2:]  # 925136 或 825136
                # 如果第一位是 8 或 9，去掉第一位
                if digits and digits[0] in ['8', '9']:
                    digits = digits[1:]  # 25136
                project_code = 'JDB' + digits
                print(f"    [OCR 修正] {original_code} -> {project_code}")

            # 特殊处理：如果是 XXXX 占位符，通过内容推断类型
            if doc_type_code == "XXXX":
                print(f"    检测到占位符编号 XXXX，尝试通过内容推断类型...")

                # 通过关键词匹配推断文档类型
                inferred_type = None
                if "情况调查表" in text:
                    inferred_type = "DCB"
                elif "测评方案" in text and "初审" in text:
                    inferred_type = "FACS"
                elif "测评方案" in text and ("复审" in text or "评审" in text):
                    inferred_type = "FAFS"
                elif "测评方案" in text and "确认" in text:
                    inferred_type = "FAQR"
                elif "测评结果" in text and "记录" in text:
                    inferred_type = "CPJG"
                elif "问题列表" in text:
                    inferred_type = "CPWT"
                elif "漏洞扫描" in text:
                    inferred_type = "SMQR"
                elif "渗透测试" in text:
                    inferred_type = "CTCS"
                elif "报告" in text and "复审" in text:
                    inferred_type = "BGFS"
                elif "报告" in text and "初审" in text:
                    inferred_type = "BGCS"

                if inferred_type:
                    print(f"    推断类型代码: {inferred_type}")
                    doc_type_code = inferred_type
                else:
                    print(f"    无法推断类型，跳过此文件编号")
                    return None

            # 获取文档类型全称
            doc_type_name = self.DOC_TYPE_CODE_MAP.get(doc_type_code)

            if doc_type_name:
                # 重新构建完整编号（使用修正后的 project_code）
                full_code = f"{project_code}-{doc_type_code}-{system_code}"

                return {
                    'project_code': project_code,
                    'doc_type_code': doc_type_code,
                    'doc_type_name': doc_type_name,
                    'system_code': system_code,
                    'full_code': full_code  # 使用修正后的完整编号
                }

        return None

    def classify(self, text: str) -> Tuple[Optional[str], bool]:
        """
        根据文本内容分类文档

        Args:
            text: 文档文本内容

        Returns:
            (文档类型, 是否系统级文档) 或 (None, False) 如果无法分类
        """
        if not text:
            return None, False

        text = text.strip()

        # 先尝试从文件编号提取文档类型
        file_code = self.extract_file_code(text)
        if file_code:
            doc_type = file_code['doc_type_name']
            is_system_level = doc_type in self.SYSTEM_LEVEL_TYPES
            return doc_type, is_system_level

        # 如果没有文件编号，使用关键词匹配
        for keywords, doc_type, is_system_level in self.CLASSIFICATION_RULES:
            # 检查所有关键词是否都在文本中
            # keywords 可能是列表或包含元组的列表
            match = False
            if isinstance(keywords[0], tuple):
                # 元组格式：所有关键词都要匹配
                match = all(all(kw in text for kw in keyword_group) for keyword_group in keywords)
            else:
                # 列表格式：所有关键词都要匹配
                match = all(keyword in text for keyword in keywords)

            if match:
                return doc_type, is_system_level

        return None, False

    def extract_system_name_from_content(self, text: str) -> Optional[str]:
        """
        从文档内容中提取系统名称

        适用于无法从文件编号提取系统信息的情况

        Args:
            text: 文档文本内容

        Returns:
            系统名称，如果未找到则返回 None
        """
        if not text:
            return None

        # 常见的系统名称提取模式
        patterns = [
            r'提供(.+?)的系统情况',  # "提供XXX的系统情况"
            r'提供(.+?系统)的',      # "提供XXX系统的"
            r'关于(.+?系统)',        # "关于XXX系统"
            r'(.+?系统)等级保护',    # "XXX系统等级保护"
            r'等级保护(.+?系统)等级', # "等级保护XXX系统等级"（报告评审记录格式）
            r'报\s*告\s*名\s*称.*?([^，。\n]{4,30}系统)', # "报告名称 XXX系统"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                system_name = match.group(1).strip()
                # 过滤掉过长或过短的结果
                if 4 <= len(system_name) <= 50:
                    return system_name

        return None

    def get_folder_name(self, doc_type: str) -> Optional[str]:
        """获取文档类型对应的文件夹名称"""
        return self.DOC_TYPE_TO_FOLDER.get(doc_type)

    def generate_filename(
        self,
        doc_type: str,
        text: str = "",
        project_name: str = "",
        system_name: str = "",
        is_system_level: bool = False,
        page_num: int = 1
    ) -> str:
        """
        生成规范的文件名

        系统级文档：将"xxx系统"替换为实际系统名
        项目级文档：仅使用文档类型名称（不带项目名）

        Args:
            doc_type: 文档类型（可能包含"xxx系统-"前缀）
            text: 文档文本内容（保留参数以兼容调用）
            project_name: 项目名称（保留参数，但项目级文档不使用）
            system_name: 系统名称
            is_system_level: 是否系统级文档
            page_num: 页码（保留参数以兼容调用，但不使用）

        Returns:
            规范的文件名（不含扩展名）
        """
        # 系统级文档：将"xxx系统"替换为实际系统名
        if is_system_level:
            if system_name:
                # 有系统名称，替换"xxx系统"
                filename = doc_type.replace("xxx系统", system_name)
                print(f"    [生成文件名] 系统级文档，替换'xxx系统'为'{system_name}': {filename}")
            else:
                # 没有系统名称，保持"xxx系统"
                filename = doc_type
                print(f"    [生成文件名] 系统级文档，未提供系统名称，保持原样: {filename}")
        else:
            # 项目级文档：仅使用文档类型名称
            filename = doc_type
            print(f"    [生成文件名] 项目级文档: {filename}")

        return filename


if __name__ == "__main__":
    # 测试分类器
    classifier = DocumentClassifier()

    test_cases = [
        # 带文件编号的测试
        "文档编号：JDB25300-CPSQS-01\n现场测评授权书",
        "文件编号：JDB25300-FXGZS-01\n风险告知书",
        "文档编号：JDB25300-DCB-01\n系统情况调查表确认签字",
        "文件编号：JDB25300-FAFS-02\n测评方案评审记录",
        "文档编号：JDB25300-RLCQR-01\n入场离场确认单",

        # 不带文件编号的测试（使用关键词匹配）
        "现场测评授权书",
        "风险告知书",
        "XXX系统-情况调查表确认签字",
        "启动会议记录表及签到表",
        "保密承诺书",
    ]

    print("文档分类测试：")
    print("=" * 60)
    for text in test_cases:
        doc_type, is_system = classifier.classify(text)
        if doc_type:
            folder = classifier.get_folder_name(doc_type)
            filename = classifier.generate_filename(
                doc_type, text, "测试项目", "测试系统", is_system
            )

            # 提取文件编号信息
            file_code = classifier.extract_file_code(text)

            print(f"文本: {text[:50]}...")
            if file_code:
                print(f"  → 文件编号: {file_code['full_code']}")
                print(f"  → 项目编号: {file_code['project_code']}")
                print(f"  → 文档类型码: {file_code['doc_type_code']}")
                print(f"  → 系统编号: {file_code['system_code']}")
            print(f"  → 类型: {doc_type} ({'系统级' if is_system else '项目级'})")
            print(f"  → 文件夹: {folder}")
            print(f"  → 文件名: {filename}.pdf")
        else:
            print(f"文本: {text[:50]}...")
            print(f"  → 无法分类")
        print()
