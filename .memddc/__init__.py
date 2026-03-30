"""
MemDDC - 项目文档生成工具

使用方法:
    from memddc import scan_and_generate

    # 扫描并生成文档
    results = scan_and_generate('/path/to/project')

    # 或者分步操作
    from memddc import PythonScanner, DocumentGenerator

    scanner = PythonScanner('/path/to/project')
    report = scanner.scan()
    scanner.save_report('/path/to/report.json')

    generator = DocumentGenerator(report, '/path/to/output')
    generated = generator.generate_all()
"""

from .scanner import PythonScanner, scan_project
from .generator import DocumentGenerator, generate_documents

__version__ = '1.0.2'
__all__ = [
    'PythonScanner',
    'DocumentGenerator',
    'scan_project',
    'generate_documents',
]


def scan_and_generate(project_root: str, output_dir: str = None) -> dict:
    """
    一站式扫描并生成文档

    Args:
        project_root: 项目根目录
        output_dir: 输出目录，默认为 .memddc/docs

    Returns:
        dict: 包含扫描报告和生成的文档路径
    """
    from pathlib import Path

    if output_dir is None:
        output_dir = Path(project_root) / '.memddc' / 'docs'
    else:
        output_dir = Path(output_dir)

    # 扫描
    scanner = PythonScanner(project_root)
    report = scanner.scan()

    # 生成
    generator = DocumentGenerator(report, str(output_dir))
    generated_docs = generator.generate_all()

    return {
        'report': report,
        'generated_docs': generated_docs,
        'stats': report['stats']
    }
