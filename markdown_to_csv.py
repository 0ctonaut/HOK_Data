#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown Table to CSV Converter
Convert Markdown tables to CSV files
"""

import csv
import sys
import os
import re


def parse_markdown_table(markdown_file_path):
    """
    Parse Markdown table file
    
    Args:
        markdown_file_path: Path to Markdown file
    
    Returns:
        list: List containing header and data rows, format: [[header], [row1], [row2], ...]
    """
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("Error: Markdown file is empty")
            return None
        
        rows = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip separator lines (lines containing ---)
            if re.match(r'^\|[\s\-\|:]+$', line):
                continue
            
            # Parse table rows (starting and ending with |)
            if line.startswith('|') and line.endswith('|'):
                # Remove leading and trailing |
                content = line[1:-1]
                # Split columns (considering escaped |)
                # Use regex to split but preserve escaped |
                cells = []
                current_cell = ""
                i = 0
                while i < len(content):
                    if content[i] == '\\' and i + 1 < len(content) and content[i + 1] == '|':
                        # Escaped |, preserve it
                        current_cell += '|'
                        i += 2
                    elif content[i] == '|':
                        # Column separator
                        cells.append(current_cell.strip())
                        current_cell = ""
                        i += 1
                    else:
                        current_cell += content[i]
                        i += 1
                
                # Add last column
                cells.append(current_cell.strip())
                
                # Filter empty rows (if all columns are empty or only empty strings)
                if any(cell for cell in cells):
                    rows.append(cells)
        
        if not rows:
            print("Error: No valid table data found")
            return None
        
        return rows
        
    except FileNotFoundError:
        print(f"Error: File not found '{markdown_file_path}'")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def markdown_to_csv(markdown_file_path, output_file_path=None):
    """
    Convert Markdown table to CSV file
    
    Args:
        markdown_file_path: Path to Markdown file
        output_file_path: Output CSV file path (optional, auto-generated if None)
    """
    rows = parse_markdown_table(markdown_file_path)
    
    if rows is None:
        sys.exit(1)
    
    # Determine output file path
    if output_file_path is None:
        output_file_path = markdown_file_path.replace('.md', '.csv')
        # If input file is not .md, add .csv extension
        if not output_file_path.endswith('.csv'):
            output_file_path = markdown_file_path + '.csv'
    
    try:
        # Write to CSV file
        with open(output_file_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        
        print(f"CSV file saved to: {output_file_path}")
        print(f"Converted {len(rows)} rows (including header)")
        
    except Exception as e:
        print(f"Error: Failed to write CSV file: {str(e)}")
        sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        # If no arguments provided, try using preview.md in current directory
        default_md = 'preview.md'
        if os.path.exists(default_md):
            print(f"Using default file: {default_md}")
            markdown_to_csv(default_md)
        else:
            print("Usage: python markdown_to_csv.py <markdown_file> [output_file]")
            print("Example: python markdown_to_csv.py preview.md output.csv")
            sys.exit(1)
    else:
        md_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        markdown_to_csv(md_file, output_file)


if __name__ == '__main__':
    main()

