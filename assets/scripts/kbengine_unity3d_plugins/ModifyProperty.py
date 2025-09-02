import os
import re

# 获取当前脚本所在的路径
script_path = os.path.dirname(os.path.abspath(__file__))

# 定义要排除的文件列表
exclude_files = ['MessageReaderBase.cs', 'NetworkInterfaceBase.cs', 'PacketReceiverBase.cs', 'PacketSenderBase.cs']

# 获取当前路径下的所有.cs文件，排除以"EntityCall"开头、以"Base.cs"结尾的文件
files = [f for f in os.listdir(script_path) if f.endswith('Base.cs') and not f.startswith('EntityCall') and f not in exclude_files]

# 读取Common.cs文件内容
common_file_path = os.path.join(script_path, 'EntityCommonProperty.cs')
with open(common_file_path, 'r') as common_file:
    common_content = common_file.read()

# 处理每个文件
for file_name in files:
    file_path = os.path.join(script_path, file_name)

    # 排除不需要处理的文件
    if file_name in exclude_files:
        continue
        
    print("file_name:", file_name)

    # 读取文件内容
    with open(file_path, 'r') as current_file:
        current_content = current_file.read()

    # 使用正则表达式匹配Common.cs中的属性
    common_pattern = re.compile(r'\bpublic\s+\w+\s+(\w+)\s*=\s*.+;')
    common_matches = common_pattern.findall(common_content)

    # 构建匹配当前文件中要删除属性的正则表达式
    delete_pattern = re.compile(r'\bpublic\s+\w+\s+({})\s*=\s*.+;'.format('|'.join(common_matches)))

    # 删除当前文件中与Common.cs相同的属性
    current_content_modified = delete_pattern.sub('', current_content)

    # 将修改后的内容写回当前文件
    with open(file_path, 'w') as current_file_modified:
        current_file_modified.write(current_content_modified)

    print(f'文件 {file_name} 中与Common.cs相同的属性已删除。')
