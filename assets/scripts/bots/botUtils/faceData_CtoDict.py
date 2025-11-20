import re
import os
import random



class FACE_DATA:
    def __init__(self):
        # 创角默认外观数据
        self.suitId = 2  
        self.hairIdFaceId = 257
        self.hairColorIdSkinColorId = 259
        self.faceData_list = {
            # #对应职业对应部位可选的部件流水号，分别是脸部、肤色、头发、发色；具体长这样
            # 1001:{"faceOpt":[],"skinColorOpt":[],"hairOpt":[],"hairColorOpt":[]},
            # 1003:{"faceOpt":[],"skinColorOpt":[],"hairOpt":[],"hairColorOpt":[]},
            # 1002:{"faceOpt":[],"skinColorOpt":[],"hairOpt":[],"hairColorOpt":[]},
        }
        #在初始化时填充faceData_list
        self._load_face_data()

    def _load_face_data(self):
        """加载外观数据"""
        self.faceData_list = main()
        if not self.faceData_list:
            print("加载外观数据失败")
        else:
            print("加载外观数据成功")


    def toSavedDict(self):
        return {
            'suitId': self.suitId,
            'hairIdFaceId': self.hairIdFaceId,
            'hairColorIdSkinColorId': self.hairColorIdSkinColorId,
        }
        
    def SetfaceData(self, faceId, skinColorId, hairId, hairColorId):
        "face,脸型"
        if ((self.hairIdFaceId & 0x00ff) == faceId):
            pass
        else:
            self.hairIdFaceId = (self.hairIdFaceId & 0xff00) + faceId
        "skinColor,肤色"
        if ((self.hairColorIdSkinColorId & 0x00ff) == skinColorId):
            pass
        else:
            self.hairColorIdSkinColorId = (self.hairColorIdSkinColorId & 0xff00) + skinColorId
        "hair,发型"
        if (((self.hairIdFaceId & 0xff00) >> 8) == hairId):
            pass
        else:
            self.hairIdFaceId = (self.hairIdFaceId & 0x00ff) + (hairId << 8)
        "hairColor,发色"
        if (((self.hairColorIdSkinColorId & 0xff00) >> 8) == hairColorId):
            pass
        else:
            self.hairColorIdSkinColorId = (self.hairColorIdSkinColorId & 0x00ff) + (hairColorId << 8)
    


    def random_set_face_data_by_id(self, char_id):
        """根据传入的ID从faceData_list中随机选择外观数据并设置"""
        faceData_list = self.faceData_list
        # 若为0则机器人随机选择一个职业
        if char_id == 0:
            char_id = random.choice([1001,1002,1003])
        if faceData_list:
        # 获取该职业对应的外观选项
            face_options = faceData_list[char_id]
            face_id = random.choice(face_options['faceOpt'])
            skin_color_id = random.choice(face_options['skinColorOpt'])
            hair_id = random.choice(face_options['hairOpt'])
            hair_color_id = random.choice(face_options['hairColorOpt'])
            self.SetfaceData(face_id, skin_color_id, hair_id, hair_color_id)  
        else:
            print('捏脸数据未初始化，使用默认')
    
 


def parse_character_data_detailed(file_path):
    """
    更详细地解析角色数据
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 提取模板数据
    templates = extract_templates(content)

    # 提取角色数据
    characters = extract_characters(content, templates)
    
    return characters

def extract_templates(content):
    """提取模板数据"""
    templates = {}
    
    # 匹配简单的List<int>模板
    simple_pattern = r'.*?List<int> m_Template_(\d+) = new List<int>\{([^\}]+)\};'
    matches = re.findall(simple_pattern, content)
    for template_id, values in matches:
        numbers = [int(x.strip()) for x in values.split(',') if x.strip().isdigit()]
        templates[template_id] = numbers
    
    # 匹配List<List<int>>模板
    nested_pattern = r'.*?List<List<int>> m_Template_(\d+) = new List<List<int>>\{([^}]+)\};'
    nested_matches = re.findall(nested_pattern, content)
    for template_id, values in nested_matches:
        # 解析嵌套列表
        list_pattern = r'new List<int>\{([^\}]+)\}'
        inner_lists = re.findall(list_pattern, values)
        parsed_lists = []
        for inner_list in inner_lists:
            numbers = [int(x.strip()) for x in inner_list.split(',') if x.strip().isdigit()]
            parsed_lists.append(numbers)
        templates[template_id] = parsed_lists
    
    return templates

def extract_characters(content, templates):
    """提取角色数据"""
    characters = {}
    
    # 匹配角色数据行
    pattern = r'\{(\d+),new character_roleData_line\(([^)]+)\)\}'
    matches = re.findall(pattern, content)
    
    for ID, params_str in matches:
        # 按逗号分割参数，但要注意嵌套的列表
        params = split_params_safely(params_str)
        
        if len(params) >= 20:  # 确保参数数量足够
            # 根据C#代码，外观选项是倒数第4到倒数第1个参数
            charID = int(params[0].strip())
            face_opt_param = params[-5].strip()
            skin_color_opt_param = params[-4].strip()
            hair_opt_param = params[-3].strip()
            hair_color_opt_param = params[-2].strip()
            
            characters[charID] = {
                'faceOpt': resolve_template_reference(face_opt_param, templates),
                'skinColorOpt': resolve_template_reference(skin_color_opt_param, templates),
                'hairOpt': resolve_template_reference(hair_opt_param, templates),
                'hairColorOpt': resolve_template_reference(hair_color_opt_param, templates)
            }
    
    return characters

def split_params_safely(params_str):
    """安全地分割参数，处理嵌套的括号"""
    params = []
    current_param = ""
    bracket_count = 0
    
    for char in params_str:
        if char == ',' and bracket_count == 0:
            params.append(current_param.strip())
            current_param = ""
        else:
            if char == '{':
                bracket_count += 1
            elif char == '}':
                bracket_count -= 1
            current_param += char
    
    if current_param:
        params.append(current_param.strip())
    
    return params

def resolve_template_reference(param, templates):
    """解析模板引用"""
    if param.startswith("m_Template_"):
        template_id = param.replace("m_Template_", "")
        return templates.get(template_id, [])
    elif "new List<int>" in param:
        # 直接定义的列表
        match = re.search(r'new List<int>\{([^\}]+)\}', param)
        if match:
            numbers = [int(x.strip()) for x in match.group(1).split(',') if x.strip().isdigit()]
            return numbers
    return []


# 使用示例
def main():
    file_path = r"/Client/Assets/CSHotUpdate/Scripts/ConfigData/character_roleData.cs"
    # file_path = r"\Client\Assets\CSHotUpdate\Scripts\ConfigData\character_roleData.cs"  # 替换为你的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("当前机器人工具目录:", current_dir)
    # 向上查找game目录，若是windows则是Dev，同时file_path换成第二个
    root_dir = current_dir
    while root_dir and os.path.basename(root_dir) != 'game':
        parent_dir = os.path.dirname(root_dir)
        if parent_dir == root_dir:  # 到达文件系统根目录
            break
        root_dir = parent_dir
    print("game目录:", root_dir)
    if not root_dir:
        print("未找到game目录")
        return
    else:
        c_file_path = root_dir + file_path

    try:
        data = parse_character_data_detailed(c_file_path)
        
        #打印结果
        print("捏脸数据读取完成",data)


        return data
    except FileNotFoundError:
        print(f"文件 {c_file_path} 未找到")
    except Exception as e:
        print(f"处理文件时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()