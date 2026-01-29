#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to Markdown Table Converter
将CSV文件转换为Markdown表格格式
"""

import csv
import sys
import os


def csv_to_markdown(csv_file_path, output_file_path=None):
    """
    将CSV文件转换为Markdown表格
    
    Args:
        csv_file_path: CSV文件路径
        output_file_path: 输出Markdown文件路径（可选，如果为None则输出到控制台）
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
            # 读取CSV文件（使用utf-8-sig自动处理BOM字符）
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            if not rows:
                print("CSV文件为空")
                return
            
            # 生成Markdown表格
            markdown_lines = []
            
            # 表头（去除每列的前后空格）
            header = [cell.strip() for cell in rows[0]]
            markdown_lines.append('| ' + ' | '.join(header) + ' |')
            
            # 分隔线
            separator = '| ' + ' | '.join(['---'] * len(header)) + ' |'
            markdown_lines.append(separator)
            
            # 数据行
            for row in rows[1:]:
                # 确保行长度与表头一致（填充空值）
                while len(row) < len(header):
                    row.append('')
                # 只取与表头相同数量的列
                row = row[:len(header)]
                # 去除每列的前后空格，并转义Markdown特殊字符
                escaped_row = [cell.strip().replace('|', '\\|') for cell in row]
                markdown_lines.append('| ' + ' | '.join(escaped_row) + ' |')
            
            markdown_content = '\n'.join(markdown_lines)
            
            # 输出结果
            if output_file_path:
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(markdown_content)
                print(f"Markdown表格已保存到: {output_file_path}")
            else:
                print(markdown_content)
                
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{csv_file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 如果没有提供参数，尝试使用当前目录下的preview.csv
        default_csv = 'preview.csv'
        if os.path.exists(default_csv):
            print(f"使用默认文件: {default_csv}")
            output_file = default_csv.replace('.csv', '.md')
            csv_to_markdown(default_csv, output_file)
        else:
            print("用法: python csv_to_markdown.py <csv_file> [output_file]")
            print("示例: python csv_to_markdown.py preview.csv output.md")
            sys.exit(1)
    else:
        csv_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else csv_file.replace('.csv', '.md')
        csv_to_markdown(csv_file, output_file)


if __name__ == '__main__':
    main()

