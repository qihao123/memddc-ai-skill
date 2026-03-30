#!/usr/bin/env python3
"""
MemDDC CLI - 命令行入口

用法:
    python -m memddc /path/to/project          # 扫描并生成
    python -m memddc /path/to/project --scan   # 仅扫描
    python -m memddc /path/to/project --report # 保存报告
"""

import sys
import argparse
from pathlib import Path

# 添加父目录到路径以便导入memddc包
sys.path.insert(0, str(Path(__file__).parent))

from memddc import scan_and_generate, PythonScanner


def main():
    parser = argparse.ArgumentParser(
        description='MemDDC - 项目文档生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python -m memddc .                 # 扫描当前目录
    python -m memddc /path/to/project  # 扫描指定目录
    python -m memddc . --report       # 保存JSON报告
    python -m memddc . --no-generate  # 仅扫描不生成文档
        """
    )

    parser.add_argument(
        'project_root',
        nargs='?',
        default='.',
        help='项目根目录路径 (默认: 当前目录)'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='文档输出目录 (默认: ./.memddc/docs)'
    )

    parser.add_argument(
        '--report', '-r',
        default=None,
        help='保存扫描报告到指定JSON文件'
    )

    parser.add_argument(
        '--scan-only', '-s',
        action='store_true',
        help='仅扫描，不生成文档'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )

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

    # 确定输出目录
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = project_root / '.memddc' / 'docs'

    # 扫描
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

    # 保存报告
    if args.report:
        report_path = Path(args.report)
        scanner.save_report(str(report_path))
        print(f"\n📄 报告已保存: {report_path}")

    # 生成文档
    if not args.scan_only:
        print(f"\n📝 生成文档中...")
        from memddc import DocumentGenerator

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
