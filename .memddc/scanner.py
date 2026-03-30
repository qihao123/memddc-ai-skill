"""
MemDDC 代码扫描器
使用AST解析Python项目，真正分析代码结构
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json


@dataclass
class PythonEntity:
    """Python代码实体"""
    name: str
    type: str  # 'class', 'function', 'method'
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    parameters: List[Dict] = field(default_factory=list)
    returns: Optional[str] = None
    imports: List[str] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)


@dataclass
class ModuleInfo:
    """模块信息"""
    name: str
    file_path: str
    classes: List[PythonEntity] = field(default_factory=list)
    functions: List[PythonEntity] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    docstring: Optional[str] = None


class PythonScanner:
    """Python项目扫描器"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.modules: Dict[str, ModuleInfo] = {}
        self.api_endpoints: List[Dict] = []
        self.errors: List[Dict] = []

    def scan(self) -> Dict[str, Any]:
        """扫描整个项目"""
        self._scan_directory(self.project_root)
        self._detect_api_endpoints()
        return self.get_report()

    def _scan_directory(self, directory: Path):
        """递归扫描目录"""
        if not directory.is_dir():
            return

        # 跳过虚拟环境和测试目录
        skip_dirs = {'venv', '.venv', 'env', '__pycache__', '.git', 'tests', '.pytest_cache', 'node_modules'}
        if directory.name in skip_dirs or directory.name.startswith('.'):
            return

        # 确保是Python包（有__init__.py或包含.py文件）
        has_init = (directory / '__init__.py').exists()
        has_py_files = any(f.suffix == '.py' for f in directory.iterdir())

        if not (has_init or has_py_files):
            return

        # 扫描Python文件
        for file_path in directory.iterdir():
            if file_path.suffix == '.py':
                self._scan_file(file_path)

        # 递归扫描子目录
        for sub_dir in directory.iterdir():
            if sub_dir.is_dir() and not sub_dir.name.startswith('.'):
                self._scan_directory(sub_dir)

    def _scan_file(self, file_path: Path):
        """扫描单个Python文件"""
        try:
            relative_path = file_path.relative_to(self.project_root)
            module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            module_info = ModuleInfo(
                name=module_name,
                file_path=str(relative_path)
            )

            # 获取模块docstring
            module_info.docstring = ast.get_docstring(tree)

            # 遍历AST节点
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    entity = self._extract_class(node, str(relative_path))
                    module_info.classes.append(entity)
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    # 顶层函数
                    entity = self._extract_function(node, str(relative_path))
                    module_info.functions.append(entity)

            # 收集导入
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
                'error': f'Syntax error: {e}'
            })
        except Exception as e:
            self.errors.append({
                'file': str(file_path),
                'error': str(e)
            })

    def _extract_class(self, node: ast.ClassDef, file_path: str) -> PythonEntity:
        """提取类信息"""
        # 获取基类
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(self._get_attr_name(base))

        # 获取装饰器
        decorators = []
        for decorator in node.decorator_list:
            decorators.append(self._getDecorator_name(decorator))

        # 获取方法
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)

        entity = PythonEntity(
            name=node.name,
            type='class',
            file_path=file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node),
            decorators=decorators,
            base_classes=base_classes
        )
        entity.parameters = [{'name': m.name, 'args': [a.arg for a in m.args.args]} for m in methods if hasattr(m, 'args')]
        return entity

    def _extract_function(self, node: ast.FunctionDef, file_path: str) -> PythonEntity:
        """提取函数信息"""
        # 获取参数
        params = []
        for arg in node.args.args:
            param_info = {'name': arg.arg}
            # 获取默认值的简化表示
            if arg.default:
                param_info['default'] = '...'
            params.append(param_info)

        # 获取返回类型注解
        returns = None
        if node.returns:
            if isinstance(node.returns, ast.Name):
                returns = node.returns.id
            elif isinstance(node.returns, ast.Constant):
                returns = str(node.returns.value)

        entity = PythonEntity(
            name=node.name,
            type='function',
            file_path=file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node),
            parameters=params,
            returns=returns
        )

        # 检查装饰器
        for decorator in node.decorator_list:
            entity.decorators.append(self._getDecorator_name(decorator))

        return entity

    def _get_attr_name(self, node: ast.Attribute) -> str:
        """获取属性节点的名称"""
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return '.'.join(reversed(parts))

    def _getDecorator_name(self, node) -> str:
        """获取装饰器名称"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._getDecorator_name(node.func)
        elif isinstance(node, ast.Attribute):
            return self._get_attr_name(node)
        return str(node)

    def _detect_api_endpoints(self):
        """检测API端点（Flask/Django/FastAPI风格）"""
        framework_imports = {
            'flask': ['route', 'get', 'post', 'put', 'delete', 'patch'],
            'fastapi': ['get', 'post', 'put', 'delete', 'patch'],
            'django': ['path', 're_path', 'route']
        }

        for module_name, module_info in self.modules.items():
            for import_name in module_info.imports:
                # 检测使用的框架
                for framework, endpoints in framework_imports.items():
                    if import_name.startswith(framework):
                        # 查找使用了这些端点装饰器的函数
                        for func in module_info.functions:
                            if any(decorator in endpoints for decorator in func.decorators):
                                self.api_endpoints.append({
                                    'module': module_name,
                                    'function': func.name,
                                    'decorators': func.decorators,
                                    'file': func.file_path,
                                    'line': func.line_number
                                })

    def get_report(self) -> Dict[str, Any]:
        """获取扫描报告"""
        total_classes = sum(len(m.classes) for m in self.modules.values())
        total_functions = sum(len(m.functions) for m in self.modules.values())

        return {
            'project_root': str(self.project_root),
            'language': 'python',
            'stats': {
                'total_modules': len(self.modules),
                'total_classes': total_classes,
                'total_functions': total_functions,
                'total_api_endpoints': len(self.api_endpoints),
                'scan_errors': len(self.errors)
            },
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
                            'methods': [p['name'] for p in c.parameters]
                        } for c in m.classes
                    ],
                    'functions': [
                        {
                            'name': f.name,
                            'line': f.line_number,
                            'docstring': f.docstring,
                            'decorators': f.decorators,
                            'parameters': [p['name'] for p in f.parameters],
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
        """保存报告到JSON文件"""
        report = self.get_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return output_path


def scan_project(project_root: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    扫描Python项目的便捷函数

    Args:
        project_root: 项目根目录路径
        output_path: 可选，输出JSON报告的路径

    Returns:
        包含扫描结果的字典
    """
    scanner = PythonScanner(project_root)
    result = scanner.scan()

    if output_path:
        scanner.save_report(output_path)

    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scanner.py <project_root> [output_json]")
        sys.exit(1)

    root = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    result = scan_project(root, output)

    print(f"\nScan Complete!")
    print(f"  Modules: {result['stats']['total_modules']}")
    print(f"  Classes: {result['stats']['total_classes']}")
    print(f"  Functions: {result['stats']['total_functions']}")
    print(f"  API Endpoints: {result['stats']['total_api_endpoints']}")

    if result['errors']:
        print(f"\n  Errors: {len(result['errors'])}")
        for err in result['errors'][:5]:
            print(f"    - {err['file']}: {err['error']}")

    if output:
        print(f"\nReport saved to: {output}")
