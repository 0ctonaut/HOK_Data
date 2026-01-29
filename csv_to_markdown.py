#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to Markdown Table Converter
Convert CSV files to Markdown table format
"""

import csv
import sys
import os
import re


def generate_markdown_table(csv_file_path):
    """
    Generate Markdown table content from CSV file
    
    Args:
        csv_file_path: Path to CSV file
    
    Returns:
        str: Markdown table content string
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
            # Read CSV file (using utf-8-sig to automatically handle BOM characters)
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            if not rows:
                print("Error: CSV file is empty")
                return None
            
            # Generate Markdown table
            markdown_lines = []
            
            # Header row (strip whitespace from each column)
            header = [cell.strip() for cell in rows[0]]
            markdown_lines.append('| ' + ' | '.join(header) + ' |')
            
            # Separator line
            separator = '| ' + ' | '.join(['---'] * len(header)) + ' |'
            markdown_lines.append(separator)
            
            # Data rows
            for row in rows[1:]:
                # Ensure row length matches header (pad with empty values)
                while len(row) < len(header):
                    row.append('')
                # Only take columns matching header count
                row = row[:len(header)]
                # Strip whitespace from each column and escape Markdown special characters
                escaped_row = [cell.strip().replace('|', '\\|') for cell in row]
                markdown_lines.append('| ' + ' | '.join(escaped_row) + ' |')
            
            return '\n'.join(markdown_lines)
                
    except FileNotFoundError:
        print(f"Error: File not found '{csv_file_path}'")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def csv_to_markdown(csv_file_path, output_file_path=None):
    """
    Convert CSV file to Markdown table
    
    Args:
        csv_file_path: Path to CSV file
        output_file_path: Output Markdown file path (optional, if None outputs to console)
    """
    markdown_content = generate_markdown_table(csv_file_path)
    
    if markdown_content is None:
        sys.exit(1)
    
    # Output result
    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(markdown_content)
        print(f"Markdown table saved to: {output_file_path}")
    else:
        print(markdown_content)


def update_readme_preview(readme_path, table_content):
    """
    Update the ## Preview section in README.md file
    
    Args:
        readme_path: Path to README.md file
        table_content: Table content to insert
    """
    try:
        # Read README.md content
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Use regex to match ## Preview section
        # Match from ## Preview to next ## heading or end of file
        pattern = r'(## Preview\s*\n)(.*?)(?=\n## |\Z)'
        
        # Replace with new content (ensure clean formatting)
        replacement = r'\1\n' + table_content + '\n'
        new_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
        
        # If ## Preview not found, try adding at end of file
        if new_content == readme_content:
            # Check if ## Preview heading exists
            if '## Preview' not in readme_content:
                # Add at end of file
                new_content = readme_content.rstrip() + '\n\n## Preview\n\n' + table_content + '\n'
            else:
                # Found heading but replacement failed, try more lenient matching
                pattern = r'(## Preview\s*\n)(.*)'
                new_content = re.sub(pattern, r'\1\n' + table_content + '\n', readme_content, flags=re.DOTALL)
        
        # Clean up excessive blank lines (keep at most two consecutive newlines)
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)
        
        # Write back to file
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"README.md ## Preview section updated")
        
    except FileNotFoundError:
        print(f"Warning: README.md file not found, skipping update")
    except Exception as e:
        print(f"Warning: Error updating README.md: {str(e)}")


def main():
    """Main function"""
    update_readme = True  # Whether to automatically update README.md
    
    if len(sys.argv) < 2:
        # If no arguments provided, try using preview.csv in current directory
        default_csv = 'preview.csv'
        if os.path.exists(default_csv):
            print(f"Using default file: {default_csv}")
            output_file = default_csv.replace('.csv', '.md')
            
            # Generate table content
            table_content = generate_markdown_table(default_csv)
            if table_content is None:
                sys.exit(1)
            
            # Save to preview.md
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(table_content)
            print(f"Markdown table saved to: {output_file}")
            
            # Update README.md
            if update_readme:
                readme_path = 'README.md'
                if os.path.exists(readme_path):
                    update_readme_preview(readme_path, table_content)
        else:
            print("Usage: python csv_to_markdown.py <csv_file> [output_file]")
            print("Example: python csv_to_markdown.py preview.csv output.md")
            sys.exit(1)
    else:
        csv_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else csv_file.replace('.csv', '.md')
        
        # Generate table content
        table_content = generate_markdown_table(csv_file)
        if table_content is None:
            sys.exit(1)
        
        # Save to output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(table_content)
        print(f"Markdown table saved to: {output_file}")
        
        # If processing preview.csv, automatically update README.md
        if update_readme and 'preview' in csv_file.lower():
            readme_path = 'README.md'
            if os.path.exists(readme_path):
                update_readme_preview(readme_path, table_content)


if __name__ == '__main__':
    main()

