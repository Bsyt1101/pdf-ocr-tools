# PDF OCR Tools
# 等保测评 PDF 文档自动拆分和归档工具

__version__ = "1.6.0"
__author__ = "Bsyt1101"

from .pdf_processor import PDFProcessor
from .doc_classifier import DocumentClassifier

__all__ = ['PDFProcessor', 'DocumentClassifier']
