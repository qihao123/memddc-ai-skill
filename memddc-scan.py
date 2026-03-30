#!/usr/bin/env python3
"""
MemDDC Scanner - 独立运行的Python代码扫描工具
完全独立，不依赖任何外部包

使用方法:
    python memddc-scan.py /path/to/project [--output report.json]
"""

import ast
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


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
        self.file_tree: Dict = {}

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

    def _build_file_tree(self, directory: Path, tree: Dict, depth: int = 0, max_depth: int = 10):
        """构建文件树"""
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

        # 构建文件树
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

    def save_report(self, output_path: str):
        report = self.get_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='MemDDC Scanner v1.0.2')
    parser.add_argument('project_root', nargs='?', default='.', help='Project root')
    parser.add_argument('--output', '-o', default=None, help='Output JSON path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose')

    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"Error: Directory not found: {project_root}")
        sys.exit(1)

    print(f"MemDDC Scanner v1.0.2")
    print(f"Scanning: {project_root}")
    print()

    scanner = PythonScanner(str(project_root))
    report = scanner.scan()

    stats = report['stats']
    print(f"Results:")
    print(f"  Modules: {stats['total_modules']}")
    print(f"  Classes: {stats['total_classes']}")
    print(f"  Functions: {stats['total_functions']}")
    print(f"  API Endpoints: {stats['total_api_endpoints']}")

    if report['errors']:
        print(f"  Errors: {len(report['errors'])}")

    if args.output:
        scanner.save_report(args.output)
        print()
        print(f"Report saved to: {args.output}")

    if args.verbose and report['errors']:
        print()
        print("Errors:")
        for err in report['errors'][:10]:
            print(f"  {err['file']}: {err['error']}")


if __name__ == '__main__':
    main()
