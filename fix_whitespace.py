#!/usr/bin/env python3
"""临时脚本：修复空白行中的空格"""
import re

with open('engine/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换包含空格的空白行为真正的空白行
content = re.sub(r'^[ \t]+$', '', content, flags=re.MULTILINE)

with open('engine/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("已修复空白行中的空格")

