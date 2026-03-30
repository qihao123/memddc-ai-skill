# MemDDC

## 技能信息

- **技能名称**: MemDDC
- **版本**: 1.0.2
- **作者**: qihao123
- **描述**: 实用的Python项目文档生成工具，通过AST解析真正分析代码结构，生成结构化文档
- **触发关键词**: `MemDDC`, `memddc-generate`, `生成文档`
- **适用场景**: Python项目文档生成、API接口文档、项目结构分析

## v1.0.2 核心改进

### 真实落地的功能

| 功能 | 实现方式 | 状态 |
|------|---------|------|
| AST代码扫描 | `memddc.py` 脚本，使用Python ast模块 | ✅ 已实现 |
| 文件树扫描 | 递归扫描目录，生成树形结构 | ✅ 已实现 |
| API端点检测 | 识别Flask/FastAPI装饰器 | ✅ 已实现 |
| Markdown文档生成 | 基于扫描结果生成文档 | ✅ 已实现 |
| JSON报告导出 | 保存扫描结果供后续使用 | ✅ 已实现 |

### 删除的过度承诺

| 承诺 | 原因 |
|------|------|
| 智能触发 | 无法实现，改为手动触发 |
| 压缩记忆 | 概念大于实质，已删除 |
| 代码生成 | Skill只生成文档，不生成代码 |
| 自动同步 | 用户手动触发更新 |

## 工具文件

### 主工具：`memddc.py`

**位置**: 项目根目录 `memddc.py`

**功能**: 一站式扫描+文档生成

**使用方法**:
```bash
# 扫描并生成文档到 .memddc/docs/
python memddc.py /path/to/project

# 指定输出目录
python memddc.py /path/to/project -o ./docs

# 仅扫描，生成JSON报告
python memddc.py /path/to/project --scan-only -r report.json

# 显示详细输出
python memddc.py /path/to/project -v
```

### 工作原理

```
用户触发 Skill
     ↓
Skill 调用 Python 脚本: python memddc.py .
     ↓
memddc.py 使用 ast 模块解析所有 .py 文件
     ↓
生成扫描报告 (JSON) + 文档 (Markdown)
     ↓
Skill 展示结果给用户
```

## 功能详情

### 1. AST代码扫描

memddc.py 使用 Python 内置的 `ast` 模块进行代码分析：

- **模块解析**: 识别包结构和模块层级
- **类提取**: 名称、父类、方法列表、docstring
- **函数提取**: 参数、返回值类型注解、docstring
- **导入分析**: 外部依赖和内部依赖
- **装饰器识别**: Flask/FastAPI 路由装饰器

### 2. 文件树扫描

- 递归扫描项目目录结构
- 跳过 `venv`, `__pycache__`, `.git` 等目录
- 生成树形结构表示

### 3. 文档生成

生成的文档包括：

| 文档 | 内容 |
|------|------|
| `architecture.md` | 项目概览、统计信息、模块列表 |
| `file-tree.md` | 完整文件目录树 |
| `dependencies.md` | 外部依赖列表 |
| `code-summary.md` | 类和函数汇总 |
| `api.md` | API端点列表（如有） |

### 4. API端点检测

自动识别以下框架的路由装饰器：

| 框架 | 装饰器 |
|------|--------|
| Flask | `@app.route()`, `@app.get()`, `@app.post()` 等 |
| FastAPI | `@app.get()`, `@app.post()` 等 |

## 使用示例

### 示例 1: 基本使用

```bash
$ python memddc.py .
🔍 MemDDC v1.0.2
   项目: /path/to/project

📊 扫描中...
   ✓ 模块: 12
   ✓ 类: 45
   ✓ 函数: 128
   ✓ API端点: 8

📝 生成文档中...
   ✓ 生成 5 个文档:
     - .memddc/docs/architecture.md
     - .memddc/docs/file-tree.md
     - .memddc/docs/dependencies.md
     - .memddc/docs/code-summary.md
     - .memddc/docs/api.md

✅ 完成!
```

### 示例 2: Skill交互

```
用户: MemDDC

技能: 好的，我来运行文档生成工具。

      $ python memddc.py .

🔍 MemDDC v1.0.2
   项目: /path/to/project

📊 扫描中...
   ✓ 模块: 12
   ✓ 类: 45
   ✓ 函数: 128
   ✓ API端点: 8

📝 生成文档中...
   ✓ 生成 5 个文档

✅ 完成!

技能: 文档已生成到 .memddc/docs/ 目录：
      - architecture.md - 项目概览
      - file-tree.md - 文件结构
      - dependencies.md - 依赖关系
      - code-summary.md - 代码汇总
      - api.md - API文档

      ⚠️ 注意：代码变更后请重新运行 "MemDDC" 更新文档
```

## Python项目要求

### 包结构要求

```
my_project/
├── __init__.py          # 必须有，标识为包
├── main.py              # 入口文件
├── module_a/
│   ├── __init__.py      # 必须有
│   └── utils.py
└── module_b/
    ├── __init__.py      # 必须有
    └── models.py
```

**为什么必须有 `__init__.py`**：
- Python ast模块只会解析被识别为包的目录
- 没有 `__init__.py` 的目录会被当作普通文件夹
- 这是Python语言特性，不是工具限制

### 导入语句规范

**推荐**:
```python
from .module_a import utils      # 相对导入
from module_a import utils        # 绝对导入
```

**避免**:
```python
module = __import__('dynamic_name')  # 动态导入，无法静态分析
```

## 目录结构

### 生成的文档结构

```
project/
├── .memddc/
│   └── docs/
│       ├── architecture.md    # 项目概览
│       ├── file-tree.md       # 文件结构
│       ├── dependencies.md    # 依赖关系
│       ├── code-summary.md    # 代码汇总
│       └── api.md             # API文档
├── memddc.py                  # 主工具
├── scanner.py                 # 扫描器模块
├── generator.py               # 生成器模块
└── [项目源代码]
```

## 技术实现

### 核心模块

1. **PythonScanner**
   - `_scan_directory()`: 递归扫描目录
   - `_scan_file()`: 解析单个Python文件
   - `_extract_class()`: 提取类信息
   - `_extract_function()`: 提取函数信息
   - `_detect_api_endpoints()`: 检测API端点
   - `_build_file_tree()`: 构建文件树

2. **DocumentGenerator**
   - `_generate_overview()`: 生成项目概览
   - `_generate_file_tree()`: 生成文件树
   - `_generate_dependencies()`: 生成依赖文档
   - `_generate_summary()`: 生成代码汇总
   - `_generate_api_docs()`: 生成API文档

### 依赖

- **仅使用Python标准库**:
  - `ast` - Python代码解析
  - `pathlib` - 路径操作
  - `json` - JSON序列化
  - `argparse` - 命令行参数

**无外部依赖，可在任何Python 3.6+环境运行**

## 已知限制

| 限制 | 说明 |
|------|------|
| 手动触发 | 无法自动检测代码变更，需要手动运行 |
| 仅Python | 目前仅支持Python项目 |
| 静态分析 | 无法处理运行时行为和动态导入 |
| 文档需维护 | 代码变更后需要重新运行工具 |

## 故障排除

### 1. 模块未被识别

**检查清单**:
- [ ] 目录是否有 `__init__.py`？
- [ ] Python语法是否正确？
- [ ] 文件编码是否为UTF-8？

### 2. API文档为空

**检查清单**:
- [ ] 是否使用了Flask或FastAPI？
- [ ] 装饰器是否在函数正上方？

**正确写法**:
```python
@app.route('/api/users')
def get_users():
    """获取用户列表"""
    return users
```

### 3. 扫描失败

**调试方法**:
```bash
# 仅扫描不生成，查看输出
python memddc.py /path/to/project --scan-only -v
```

## 替代工具推荐

| 需求 | 推荐工具 |
|------|---------|
| Python API文档 | `pdoc` |
| 完整文档系统 | `sphinx` |
| Java文档 | `Javadoc` |
| API文档 | `Swagger` |

## 版本历史

- **v1.0.2** - 务实改进版 (当前版本)
  - ✅ 提供真实的 `memddc.py` 工具
  - ✅ 使用AST解析真正分析代码
  - ✅ 生成可用的Markdown文档
  - ✅ 仅依赖Python标准库

- **v1.0.1** - 团队协作升级版（未实现）
- **v1.0.0** - 初始版本（概念验证）

## 许可协议

MIT License

## 联系方式

- 项目主页: <https://github.com/qihao123/memddc-ai-skill>
- 作者: qihao123
- 邮件支持: <qihoo2017@gmail.com>
