"""
MemDDC 文档生成器
基于扫描结果生成Markdown文档
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DocumentGenerator:
    """文档生成器"""

    def __init__(self, scan_report: Dict[str, Any], output_dir: str):
        self.report = scan_report
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self) -> List[str]:
        """生成所有文档"""
        generated = []

        # 生成项目概览
        path = self._generate_overview()
        if path:
            generated.append(path)

        # 生成API文档
        path = self._generate_api_docs()
        if path:
            generated.append(path)

        # 生成模块树
        path = self._generate_module_tree()
        if path:
            generated.append(path)

        # 生成依赖关系
        path = self._generate_dependencies()
        if path:
            generated.append(path)

        return generated

    def _generate_overview(self) -> Optional[str]:
        """生成项目概览文档"""
        stats = self.report.get('stats', {})
        project_root = self.report.get('project_root', '')

        content = f"""# 项目概览

## 基本信息

| 属性 | 值 |
|------|-----|
| 项目路径 | `{project_root}` |
| 编程语言 | {self.report.get('language', 'unknown')} |
| 扫描时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |

## 统计信息

| 指标 | 数量 |
|------|------|
| 模块数量 | {stats.get('total_modules', 0)} |
| 类数量 | {stats.get('total_classes', 0)} |
| 函数数量 | {stats.get('total_functions', 0)} |
| API端点 | {stats.get('total_api_endpoints', 0)} |

## 扫描错误

"""

        errors = self.report.get('errors', [])
        if errors:
            content += f"扫描过程中发现 {len(errors)} 个错误：\n\n"
            for err in errors[:10]:
                content += f"- **{err['file']}**: {err['error']}\n"
        else:
            content += "✅ 未发现扫描错误\n"

        content += "\n## 模块列表\n\n"

        modules = self.report.get('modules', {})
        for name, info in sorted(modules.items()):
            docstring = info.get('docstring', '')
            brief = docstring.split('\n')[0] if docstring else '无描述'
            content += f"- **{name}** - {brief}\n"

        output_path = self.output_dir / 'architecture.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_api_docs(self) -> Optional[str]:
        """生成API文档"""
        endpoints = self.report.get('api_endpoints', [])

        if not endpoints:
            return None

        content = f"""# API 文档

## 概述

共检测到 **{len(endpoints)}** 个API端点

## 端点列表

"""

        # 按模块分组
        by_module = {}
        for ep in endpoints:
            module = ep.get('module', 'unknown')
            if module not in by_module:
                by_module[module] = []
            by_module[module].append(ep)

        for module, eps in sorted(by_module.items()):
            content += f"### {module}\n\n"
            content += "| 方法 | 函数 | 文件位置 |\n"
            content += "|------|------|----------|\n"

            for ep in eps:
                decorators = ', '.join(ep.get('decorators', []))
                func_name = ep.get('function', '')
                file_path = ep.get('file', '')
                line = ep.get('line', '')
                content += f"| {decorators} | `{func_name}` | {file_path}:{line} |\n"

            content += "\n"

        output_path = self.output_dir / 'api.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_module_tree(self) -> Optional[str]:
        """生成模块树"""
        modules = self.report.get('modules', {})

        if not modules:
            return None

        content = "# 模块结构\n\n"
        content += "```\n"

        # 构建树结构
        def build_tree(modules_dict):
            tree = {}
            for name in modules_dict.keys():
                parts = name.split('.')
                current = tree
                for i, part in enumerate(parts):
                    if part not in current:
                        current[part] = {}
                    current = current[part]
            return tree

        def print_tree(tree, prefix='', is_last=True):
            lines = []
            items = list(tree.items())
            for i, (name, children) in enumerate(items):
                is_last_item = i == len(items) - 1
                connector = '└── ' if is_last_item else '├── '
                lines.append(f"{prefix}{connector}{name}/")

                if children:
                    extension = '    ' if is_last_item else '│   '
                    lines.extend(print_tree(children, prefix + extension, is_last_item))

            return lines

        tree = build_tree(modules)
        lines = print_tree(tree)
        content += '\n'.join(lines)
        content += "\n```\n"

        # 添加模块详情
        content += "\n## 模块详情\n\n"

        for name, info in sorted(modules.items()):
            content += f"### {name}\n\n"

            classes = info.get('classes', [])
            functions = info.get('functions', [])

            if classes:
                content += f"#### 类 ({len(classes)})\n\n"
                for cls in classes:
                    doc = cls.get('docstring', '') or '无描述'
                    brief = doc.split('\n')[0]
                    content += f"- **{cls['name']}** - {brief}\n"
                content += "\n"

            if functions:
                content += f"#### 函数 ({len(functions)})\n\n"
                for func in functions:
                    doc = func.get('docstring', '') or '无描述'
                    brief = doc.split('\n')[0]
                    content += f"- **{func['name']}** - {brief}\n"
                content += "\n"

        output_path = self.output_dir / 'module-tree.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_dependencies(self) -> Optional[str]:
        """生成依赖关系文档"""
        modules = self.report.get('modules', {})

        if not modules:
            return None

        content = "# 依赖关系\n\n"

        # 收集所有导入
        all_imports = {}
        for name, info in modules.items():
            imports = info.get('imports', [])
            if imports:
                all_imports[name] = imports

        if not all_imports:
            content += "未检测到模块间依赖关系\n"
        else:
            content += "## 模块导入关系\n\n"
            content += "| 模块 | 导入 |\n"
            content += "|------|------|\n"

            for name, imports in sorted(all_imports.items()):
                # 过滤外部包
                internal = [imp for imp in imports if not imp.startswith(('_', '.'))]
                if internal:
                    content += f"| {name} | {', '.join(internal[:5])} |\n"

        output_path = self.output_dir / 'dependencies.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)


def generate_documents(scan_report_path: str, output_dir: str) -> List[str]:
    """
    根据扫描报告生成文档

    Args:
        scan_report_path: 扫描报告JSON文件路径
        output_dir: 输出目录

    Returns:
        生成的文档路径列表
    """
    with open(scan_report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)

    generator = DocumentGenerator(report, output_dir)
    return generator.generate_all()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generator.py <scan_report.json> <output_dir>")
        sys.exit(1)

    report_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './.memddc/docs'

    generated = generate_documents(report_path, output_dir)

    print(f"\nGenerated {len(generated)} documents:")
    for path in generated:
        print(f"  - {path}")
