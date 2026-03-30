#!/usr/bin/env python3
"""
MemDDC - 一站式Python项目文档生成工具 v1.0.2
使用方法: python memddc.py /path/to/project [--output docs/]
"""

import ast
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# ============================================================================
# 扫描器部分
# ============================================================================

class PythonEntity:
    def __init__(self, name, etype, file_path, line_number):
        self.name = name
        self.type = etype
        self.file_path = file_path
        self.line_number = line_number
        self.docstring = None
        self.decorators = []
        self.parameters = []
        self.returns = None
        self.base_classes = []


class ModuleInfo:
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        self.classes = []
        self.functions = []
        self.imports = []
        self.docstring = None


class PythonScanner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.modules: Dict[str, ModuleInfo] = {}
        self.api_endpoints: List[Dict] = []
        self.errors: List[Dict] = []

    def scan(self) -> Dict[str, Any]:
        self._scan_directory(self.project_root)
        self._detect_api_endpoints()
        return self.get_report()

    def _should_skip_dir(self, directory: Path) -> bool:
        skip_names = {
            'venv', '.venv', 'env', '.env',
            '__pycache__', '.git', '.svn', '.hg',
            'tests', 'test', 'pytest_cache', '.pytest_cache',
            'node_modules', '.mypy_cache', '.tox',
            'dist', 'build', 'eggs', '.eggs',
        }
        name = directory.name
        if name in skip_names:
            return True
        if name.startswith('.') and name not in {'.memddc'}:
            return True
        return False

    def _scan_directory(self, directory: Path):
        if not directory.is_dir() or self._should_skip_dir(directory):
            return

        py_files = []
        subdirs = []

        try:
            for item in directory.iterdir():
                if item.is_file() and item.suffix == '.py':
                    py_files.append(item)
                elif item.is_dir():
                    subdirs.append(item)
        except PermissionError:
            return

        for file_path in py_files:
            self._scan_file(file_path)

        for sub_dir in subdirs:
            self._scan_directory(sub_dir)

    def _scan_file(self, file_path: Path):
        try:
            relative_path = file_path.relative_to(self.project_root)

            module_parts = []
            for part in relative_path.parts[:-1]:
                if not part.startswith('.') and part != '__pycache__':
                    module_parts.append(part)
            module_name = '.'.join(module_parts) if module_parts else 'root'

            if module_name == 'root':
                module_name = file_path.stem

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            module_info = ModuleInfo(module_name, str(relative_path))
            module_info.docstring = ast.get_docstring(tree)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    entity = self._extract_class(node, str(relative_path))
                    module_info.classes.append(entity)
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    entity = self._extract_function(node, str(relative_path))
                    module_info.functions.append(entity)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_info.imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            module_info.imports.append(f"{node.module}.{alias.name}")

            self.modules[module_name] = module_info

        except SyntaxError as e:
            self.errors.append({
                'file': str(file_path),
                'error': f'Syntax error at line {e.lineno}: {e.msg}'
            })
        except Exception as e:
            self.errors.append({
                'file': str(file_path),
                'error': str(e)
            })

    def _extract_class(self, node: ast.ClassDef, file_path: str) -> PythonEntity:
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)

        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        entity = PythonEntity(node.name, 'class', file_path, node.lineno)
        entity.docstring = ast.get_docstring(node)
        entity.decorators = decorators
        entity.base_classes = base_classes
        entity.parameters = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]

        return entity

    def _extract_function(self, node: ast.FunctionDef, file_path: str) -> PythonEntity:
        params = [arg.arg for arg in node.args.args]

        returns = None
        if node.returns and isinstance(node.returns, ast.Name):
            returns = node.returns.id

        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        entity = PythonEntity(node.name, 'function', file_path, node.lineno)
        entity.docstring = ast.get_docstring(node)
        entity.parameters = params
        entity.returns = returns
        entity.decorators = decorators

        return entity

    def _get_decorator_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_decorator_name(node.func)
        elif isinstance(node, ast.Attribute):
            parts = []
            while isinstance(node, ast.Attribute):
                parts.append(node.attr)
                node = node.value
            if isinstance(node, ast.Name):
                parts.append(node.id)
            return '.'.join(reversed(parts))
        return str(node)

    def _detect_api_endpoints(self):
        framework_decorators = {
            'flask': ['route', 'get', 'post', 'put', 'delete', 'patch'],
            'fastapi': ['get', 'post', 'put', 'delete', 'patch', 'head', 'options'],
        }

        for module_name, module_info in self.modules.items():
            for func in module_info.functions:
                for decorator in func.decorators:
                    for framework, endpoints in framework_decorators.items():
                        if any(ep in decorator.lower() for ep in endpoints):
                            self.api_endpoints.append({
                                'module': module_name,
                                'function': func.name,
                                'decorators': func.decorators,
                                'file': func.file_path,
                                'line': func.line_number,
                                'framework': framework
                            })
                            break

    def get_report(self) -> Dict[str, Any]:
        total_classes = sum(len(m.classes) for m in self.modules.values())
        total_functions = sum(len(m.functions) for m in self.modules.values())

        file_tree = {}
        self._build_file_tree(self.project_root, file_tree)

        return {
            'project_root': str(self.project_root),
            'language': 'python',
            'scan_time': datetime.now().isoformat(),
            'stats': {
                'total_modules': len(self.modules),
                'total_classes': total_classes,
                'total_functions': total_functions,
                'total_api_endpoints': len(self.api_endpoints),
                'scan_errors': len(self.errors)
            },
            'file_tree': file_tree,
            'modules': {
                name: {
                    'file_path': m.file_path,
                    'docstring': m.docstring,
                    'classes': [
                        {
                            'name': c.name,
                            'line': c.line_number,
                            'docstring': c.docstring,
                            'decorators': c.decorators,
                            'base_classes': c.base_classes,
                            'methods': c.parameters
                        } for c in m.classes
                    ],
                    'functions': [
                        {
                            'name': f.name,
                            'line': f.line_number,
                            'docstring': f.docstring,
                            'decorators': f.decorators,
                            'parameters': f.parameters,
                            'returns': f.returns
                        } for f in m.functions
                    ],
                    'imports': m.imports
                } for name, m in self.modules.items()
            },
            'api_endpoints': self.api_endpoints,
            'errors': self.errors
        }

    def _build_file_tree(self, directory: Path, tree: Dict, depth: int = 0, max_depth: int = 10):
        if depth > max_depth:
            return

        try:
            for item in sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name)):
                if item.name.startswith('.') and item.name not in {'.memddc'}:
                    continue

                rel_path = item.relative_to(self.project_root)

                if item.is_file():
                    tree[item.name] = {
                        'type': 'file',
                        'path': str(rel_path)
                    }
                elif item.is_dir() and not self._should_skip_dir(item):
                    tree[item.name + '/'] = {
                        'type': 'dir',
                        'path': str(rel_path),
                        'children': {}
                    }
                    self._build_file_tree(item, tree[item.name + '/']['children'], depth + 1, max_depth)
        except PermissionError:
            pass

    def save_report(self, output_path: str):
        report = self.get_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


# ============================================================================
# 文档生成器部分
# ============================================================================

class DocumentGenerator:
    def __init__(self, report: Dict[str, Any], output_dir: str):
        self.report = report
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self) -> List[str]:
        generated = []

        path = self._generate_overview()
        if path:
            generated.append(path)

        path = self._generate_api_docs()
        if path:
            generated.append(path)

        path = self._generate_file_tree()
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

    def _generate_file_tree(self) -> Optional[str]:
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
            content += "未检测到外部依赖\n"
        else:
            content += "## 外部依赖\n\n"
            content += "| 模块 | 导入 |\n"
            content += "|------|------|\n"

            for name, imports in sorted(all_imports.items()):
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

        output_path = self.output_dir / 'dependencies.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_summary(self) -> Optional[str]:
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

                    if params or returns:
                        content += f"签名: `{func['name']}({params})`"
                        if returns:
                            content += f" → `{returns}`"
                        content += "\n\n"

        if not has_content:
            return None

        output_path = self.output_dir / 'code-summary.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)


# ============================================================================
# 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='MemDDC - 一站式Python项目文档生成工具 v1.0.2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python memddc.py .                    # 扫描并生成文档到 .memddc/docs/
    python memddc.py /path/to/project   # 扫描指定目录
    python memddc.py . -o ./docs         # 指定输出目录
    python memddc.py . --scan-only       # 仅扫描，生成JSON报告
        """
    )

    parser.add_argument('project_root', nargs='?', default='.', help='项目根目录')
    parser.add_argument('--output', '-o', default=None, help='文档输出目录')
    parser.add_argument('--report', '-r', default=None, help='保存扫描报告到JSON文件')
    parser.add_argument('--scan-only', '-s', action='store_true', help='仅扫描，不生成文档')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"❌ 错误: 目录不存在: {project_root}")
        sys.exit(1)

    if not project_root.is_dir():
        print(f"❌ 错误: 不是有效的目录: {project_root}")
        sys.exit(1)

    print(f"🔍 MemDDC v1.0.2")
    print(f"   项目: {project_root}")
    print()

    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = project_root / '.memddc' / 'docs'

    print("📊 扫描中...")
    scanner = PythonScanner(str(project_root))
    report = scanner.scan()

    stats = report['stats']
    print(f"   ✓ 模块: {stats['total_modules']}")
    print(f"   ✓ 类: {stats['total_classes']}")
    print(f"   ✓ 函数: {stats['total_functions']}")
    print(f"   ✓ API端点: {stats['total_api_endpoints']}")

    if report['errors']:
        print(f"   ⚠ 错误: {len(report['errors'])}")

    if args.report:
        report_path = Path(args.report)
        scanner.save_report(str(report_path))
        print(f"\n📄 报告已保存: {report_path}")

    if not args.scan_only:
        print(f"\n📝 生成文档中...")
        generator = DocumentGenerator(report, str(output_dir))
        generated = generator.generate_all()

        print(f"   ✓ 生成 {len(generated)} 个文档:")
        for path in generated:
            rel_path = Path(path).relative_to(project_root)
            print(f"     - {rel_path}")

    print("\n✅ 完成!")

    if args.verbose and report['errors']:
        print("\n⚠ 错误详情:")
        for err in report['errors'][:10]:
            print(f"   {err['file']}: {err['error']}")


if __name__ == '__main__':
    main()
