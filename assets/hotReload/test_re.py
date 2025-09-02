import re

text = """
import   math,   Math,  sMath
import numpy, os, sys
"""

pat_line = re.compile(
    r"(?:^|\n)\s*import\s+([ \t]*[A-Za-z_][A-Za-z0-9_]*"
    r"(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*)\s*(?:\n|$|;)",
    re.M
)

modules = []
for m in pat_line.finditer(text):
    # 把捕获的整串再按逗号拆
    modules.extend([x.strip() for x in m.group(1).split(',')])

for line in text.split('\n'):
    find = pat_line.search(line)
    if find:
        print('find', find.group(1))

print(modules)   # ['math', 'Math', 'sMath', 'numpy', 'os', 'sys']
