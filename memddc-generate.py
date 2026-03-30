#!/usr/bin/env python3
"""
MemDDC Generator - 基于扫描报告生成Markdown文档
完全独立，不依赖任何外部包

使用方法:
    python memddc-generate.py scan-report.json [--output docs/]
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class DocumentGenerator:
    """文档生成器"""

    def __init__(self, report: Dict[str, Any], output_dir: str):
        self.report = report
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self) -> List[str]:
        """生成所有文档"""
        generated = []

        path = self._generate_overview()
        if path:
            generated.append(path)

        path = self._generate_api_docs()
        if path:
            generated.append(path)

        path = self._generate_module_tree()
        if path:
            generated.append(path)

        path = self._generate_dependencies()
        if path:
            generated.append(path)

        path = self._generate_summary()
        if path:
            generated.append(path)

        return generated

    def _generate_overview(self) -> Optional[str]:
        """生成项目概览文档"""
        stats = self.report.get('stats', {})
        project_root = self.report.get('project_root', '')
        scan_time = self.report.get('scan_time', '')

        content = f"""# 项目概览

## 基本信息

| 属性 | 值 |
|------|-----|
| 项目路径 | `{project_root}` |
| 编程语言 | {self.report.get('language', 'unknown')} |
| 扫描时间 | {scan_time} |

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
            content += f"⚠️ 扫描过程中发现 {len(errors)} 个错误：\n\n"
            for err in errors[:20]:
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

        by_module = {}
        for ep in endpoints:
            module = ep.get('module', 'unknown')
            if module not in by_module:
                by_module[module] = []
            by_module[module].append(ep)

        for module, eps in sorted(by_module.items()):
            content += f"### {module}\n\n"
            content += "| 框架 | 方法 | 函数 | 位置 |\n"
            content += "|------|------|------|------|\n"

            for ep in eps:
                framework = ep.get('framework', '')
                decorators = ', '.join(ep.get('decorators', []))
                func_name = ep.get('function', '')
                file_path = ep.get('file', '')
                line = ep.get('line', '')
                content += f"| {framework} | {decorators} | `{func_name}` | {file_path}:{line} |\n"

            content += "\n"

        output_path = self.output_dir / 'api.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_module_tree(self) -> Optional[str]:
        """生成模块树"""
        file_tree = self.report.get('file_tree', {})

        if not file_tree:
            return None

        content = "# 文件结构\n\n"
        content += "```\n"

        def print_tree(tree: Dict, prefix: str = '', is_last: bool = True) -> List[str]:
            lines = []
            items = sorted(tree.items(), key=lambda x: (x[0].endswith('/'), x[0]))
            for i, (name, info) in enumerate(items):
                is_last_item = i == len(items) - 1
                connector = '└── ' if is_last_item else '├── '
                lines.append(f"{prefix}{connector}{name}")

                if 'children' in info and info['children']:
                    extension = '    ' if is_last_item else '│   '
                    lines.extend(print_tree(info['children'], prefix + extension, is_last_item))

            return lines

        lines = print_tree(file_tree)
        content += '\n'.join(lines)
        content += "\n```\n"

        output_path = self.output_dir / 'file-tree.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_dependencies(self) -> Optional[str]:
        """生成依赖关系文档"""
        modules = self.report.get('modules', {})

        if not modules:
            return None

        content = "# 依赖关系\n\n"

        all_imports = {}
        for name, info in modules.items():
            imports = info.get('imports', [])
            if imports:
                all_imports[name] = imports

        if not all_imports:
            content += "未检测到模块间依赖关系\n"
        else:
            content += "## 外部依赖\n\n"
            content += "| 模块 | 导入 |\n"
            content += "|------|------|\n"

            for name, imports in sorted(all_imports.items()):
                # 过滤标准库和外部包
                external = []
                for imp in imports:
                    if not imp.startswith('_') and '.' not in imp:
                        external.append(imp)
                    elif imp.startswith('.'):
                        continue
                    else:
                        external.append(imp.split('.')[0])

                external = list(set(external))[:5]
                if external:
                    content += f"| {name} | {', '.join(external)} |\n"

        content += "\n## 模块间依赖\n\n"

        internal_deps = {}
        for name, info in modules.items():
            imports = info.get('imports', [])
            for imp in imports:
                if imp.startswith('.'):
                    continue
                for other_name in modules.keys():
                    if other_name != name and imp.startswith(other_name):
                        if name not in internal_deps:
                            internal_deps[name] = []
                        internal_deps[name].append(other_name)

        if internal_deps:
            content += "| 模块 | 依赖 |\n"
            content += "|------|------|\n"
            for name, deps in sorted(internal_deps.items()):
                content += f"| {name} | {', '.join(set(deps))} |\n"
        else:
            content += "未检测到模块间依赖\n"

        output_path = self.output_dir / 'dependencies.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_summary(self) -> Optional[str]:
        """生成类/函数汇总文档"""
        modules = self.report.get('modules', {})

        content = "# 代码汇总\n\n"

        has_content = False

        for name, info in sorted(modules.items()):
            classes = info.get('classes', [])
            functions = info.get('functions', [])

            if not classes and not functions:
                continue

            has_content = True
            content += f"## {name}\n\n"

            if classes:
                content += f"### 类 ({len(classes)})\n\n"
                for cls in classes:
                    doc = cls.get('docstring', '') or '无描述'
                    brief = doc.split('\n')[0]
                    base = ', '.join(cls.get('base_classes', [])) if cls.get('base_classes') else ''
                    content += f"#### {cls['name']}"
                    if base:
                        content += f" ({base})"
                    content += f"\n\n{brief}\n\n"

                    methods = cls.get('methods', [])
                    if methods:
                        content += f"方法: {', '.join(methods)}\n\n"

            if functions:
                content += f"### 函数 ({len(functions)})\n\n"
                for func in functions:
                    doc = func.get('docstring', '') or '无描述'
                    brief = doc.split('\n')[0]
                    params = ', '.join(func.get('parameters', []))
                    returns = func.get('returns', '')

                    content += f"#### {func['name']}\n\n"
                    content += f"{brief}\n\n"

                    sig_parts = []
                    if params:
                        sig_parts.append(params)
                    if returns:
                        sig_parts.append(f"→ {returns}")

                    if sig_parts:
                        content += f"签名: `{func['name']}({params})` → `{returns}`\n\n"

        if not has_content:
            return None

        output_path = self.output_dir / 'code-summary.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)


def main():
    parser = argparse.ArgumentParser(description='MemDDC Generator v1.0.2')
    parser.add_argument('report', help='Scan report JSON file')
    parser.add_argument('--output', '-o', default='./.memddc/docs', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose')

    args = parser.parse_args()

    if not Path(args.report).exists():
        print(f"Error: Report file not found: {args.report}")
        sys.exit(1)

    print(f"MemDDC Generator v1.0.2")
    print(f"Loading: {args.report}")
    print()

    with open(args.report, 'r', encoding='utf-8') as f:
        report = json.load(f)

    generator = DocumentGenerator(report, args.output)
    generated = generator.generate_all()

    print(f"Generated {len(generated)} documents:")
    for path in generated:
        print(f"  - {path}")

    if args.verbose:
        print()
        print(f"Project: {report['project_root']}")
        print(f"Modules: {report['stats']['total_modules']}")
        print(f"Classes: {report['stats']['total_classes']}")
        print(f"Functions: {report['stats']['total_functions']}")


if __name__ == '__main__':
    main()
