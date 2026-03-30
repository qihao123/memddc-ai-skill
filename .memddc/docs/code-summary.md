# 代码汇总

## __init__

### 函数 (1)

#### scan_and_generate

一站式扫描并生成文档

签名: `scan_and_generate(project_root, output_dir)` → `dict`

## cli

### 函数 (1)

#### main

无描述

## generator

### 类 (1)

#### DocumentGenerator

文档生成器

方法: __init__, generate_all, _generate_overview, _generate_api_docs, _generate_module_tree, _generate_dependencies

### 函数 (1)

#### generate_documents

根据扫描报告生成文档

签名: `generate_documents(scan_report_path, output_dir)`

## memddc

### 类 (4)

#### PythonEntity

无描述

方法: __init__

#### ModuleInfo

无描述

方法: __init__

#### PythonScanner

无描述

方法: __init__, scan, _should_skip_dir, _scan_directory, _scan_file, _extract_class, _extract_function, _get_decorator_name, _detect_api_endpoints, get_report, _build_file_tree, save_report

#### DocumentGenerator

无描述

方法: __init__, generate_all, _generate_overview, _generate_api_docs, _generate_file_tree, _generate_dependencies, _generate_summary

### 函数 (1)

#### main

无描述

## memddc-generate

### 类 (1)

#### DocumentGenerator

文档生成器

方法: __init__, generate_all, _generate_overview, _generate_api_docs, _generate_module_tree, _generate_dependencies, _generate_summary

### 函数 (1)

#### main

无描述

## memddc-scan

### 类 (3)

#### PythonEntity

无描述

方法: __init__

#### ModuleInfo

无描述

方法: __init__

#### PythonScanner

无描述

方法: __init__, scan, _should_skip_dir, _build_file_tree, _scan_directory, _scan_file, _extract_class, _extract_function, _get_decorator_name, _detect_api_endpoints, get_report, save_report

### 函数 (1)

#### main

无描述

## scanner

### 类 (3)

#### PythonEntity

Python代码实体

#### ModuleInfo

模块信息

#### PythonScanner

Python项目扫描器

方法: __init__, scan, _scan_directory, _scan_file, _extract_class, _extract_function, _get_attr_name, _getDecorator_name, _detect_api_endpoints, get_report, save_report

### 函数 (1)

#### scan_project

扫描Python项目的便捷函数

签名: `scan_project(project_root, output_path)`

