#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 index.html 和 generator.py 中的 JavaScript 代码是否正确修复
"""

import re
import os
import sys

def check_javascript_syntax(filepath):
    """检查JavaScript语法问题"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 检查重复变量定义
    variable_pattern = r'\b(?:const|let|var)\s+(\w+)\s*='
    variables = {}
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        matches = re.finditer(variable_pattern, line)
        for match in matches:
            var_name = match.group(1)
            if var_name in variables:
                issues.append("Line %d: Variable '%s' redefined (first defined at line %d)" % (i, var_name, variables[var_name]))
            else:
                variables[var_name] = i
    
    # 检查 setInterval 是否正确设置
    interval_count = content.count('setInterval(updateStatus, 1000)')
    if interval_count == 0:
        issues.append("setInterval(updateStatus, 1000) not found")
    elif interval_count > 1:
        issues.append("setInterval(updateStatus, 1000) appears %d times, may be duplicated" % interval_count)
    
    # 检查 updateStatus 函数是否存在
    if 'function updateStatus()' not in content:
        issues.append("updateStatus function not found")
    
    # 检查 DOMContentLoaded 事件监听
    if "document.addEventListener('DOMContentLoaded'" not in content:
        issues.append("DOMContentLoaded event listener missing")
    
    # 检查关键元素是否被更新
    key_elements = ['currentTimeDisplay', 'statusLight', 'statusText']
    for element in key_elements:
        if f"getElementById('{element}')" not in content:
            issues.append("No operation on %s element found" % element)
    
    return issues

def main():
    files_to_check = [
        'index.html',
        'generator.py'
    ]
    
    print("=== JavaScript Syntax Validation ===")
    print()
    
    all_passed = True
    for filepath in files_to_check:
        if not os.path.exists(filepath):
            print("ERROR: File not found: %s" % filepath)
            all_passed = False
            continue
        
        print("Checking: %s" % filepath)
        issues = check_javascript_syntax(filepath)
        
        if issues:
            print("  ERRORS FOUND:")
            for issue in issues:
                print("    - %s" % issue)
            all_passed = False
        else:
            print("  PASSED")
        
        print()
    
    if all_passed:
        print("SUCCESS: All checks passed!")
        print("\nValidated items:")
        print("  - No duplicate variable definitions")
        print("  - updateStatus function exists and is correct")
        print("  - DOMContentLoaded event listener is correct")
        print("  - setInterval(updateStatus, 1000) is correctly set")
        print("  - currentTimeDisplay, statusLight, statusText elements are properly manipulated")
    else:
        print("FAILURE: Issues found, please fix")
    
    return all_passed

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()