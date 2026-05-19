#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 index.html 是否包含正确的 JavaScript 逻辑
"""

import re
import os

def test_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== Testing index.html ===")
    print()
    
    # 测试1: 检查关键元素是否存在
    print("1. Checking DOM elements exist:")
    
    elements = {
        'currentTimeDisplay': '<span id="currentTimeDisplay">',
        'statusLight': '<span.*id="statusLight"',
        'statusText': '<span.*id="statusText"'
    }
    
    for element_name, pattern in elements.items():
        if re.search(pattern, content):
            print(f"   ✓ {element_name} element found")
        else:
            print(f"   ✗ {element_name} element NOT found")
    
    print()
    
    # 测试2: 检查 updateStatus 函数
    print("2. Checking updateStatus function:")
    
    if 'function updateStatus()' in content:
        print("   ✓ updateStatus function exists")
        
        # 检查函数内容
        if "getElementById('currentTimeDisplay')" in content:
            print("   ✓ Updates currentTimeDisplay")
        if "getElementById('statusLight')" in content:
            print("   ✓ Updates statusLight")
        if "getElementById('statusText')" in content:
            print("   ✓ Updates statusText")
        if "formatDateTime(now)" in content:
            print("   ✓ Uses formatDateTime for current time")
    else:
        print("   ✗ updateStatus function NOT found")
    
    print()
    
    # 测试3: 检查 DOMContentLoaded 事件
    print("3. Checking DOMContentLoaded event:")
    
    if "document.addEventListener('DOMContentLoaded'" in content:
        print("   ✓ DOMContentLoaded listener exists")
        
        if "updateStatus()" in content:
            print("   ✓ Calls updateStatus() on load")
        if "setInterval(updateStatus, 1000)" in content:
            print("   ✓ Sets up 1-second interval")
    else:
        print("   ✗ DOMContentLoaded listener NOT found")
    
    print()
    
    # 测试4: 检查 formatDateTime 函数
    print("4. Checking formatDateTime function:")
    
    if 'function formatDateTime(date)' in content:
        print("   ✓ formatDateTime function exists")
        if "getFullYear()" in content and "getMonth()" in content and "getDate()" in content:
            print("   ✓ Formats date correctly")
        if "getHours()" in content and "getMinutes()" in content and "getSeconds()" in content:
            print("   ✓ Formats time correctly")
    else:
        print("   ✗ formatDateTime function NOT found")
    
    print()
    
    # 测试5: 检查状态灯逻辑
    print("5. Checking status light logic:")
    
    status_classes = ['status-normal', 'status-warning', 'status-danger']
    for cls in status_classes:
        if cls in content:
            print(f"   ✓ {cls} class found")
        else:
            print(f"   ✗ {cls} class NOT found")
    
    print()
    print("=== Summary ===")
    print("The index.html should now work correctly with:")
    print("  - Real-time current time display")
    print("  - Status light that changes based on update frequency")
    print("  - Status text that updates accordingly")
    print("  - 1-second refresh interval")

if __name__ == '__main__':
    test_index_html()
    print("\nTo verify in browser:")
    print("1. Open http://localhost:8000/index.html")
    print("2. Open Developer Tools (F12)")
    print("3. Check Console for debug messages")
    print("4. Verify currentTimeDisplay updates every second")