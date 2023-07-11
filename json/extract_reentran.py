import json
import os

# 输出的文件
output_file = "output.json"

# 文件夹路径
folder_path = "code4rena2"

# 用于保存筛选出来的json
output_jsons = []

# 遍历文件夹
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # 打开每一个文件
    with open(file_path, 'r') as f:
        data = json.load(f)  # 读取json文件
        for item in data:
            # 读取json-A格式中的“code”字段
            code = item.get("Code")
            if code:  # 如果code字段的值不为空
                # 读取"VulnerabilityDesc"字段
                vulnerability_desc = item.get("VulnerabilityDesc", [])
                for desc in vulnerability_desc:
                    # 读取json-B格式中的“Type”字段
                    type_value = desc.get("Type")
                    # 如果“Type”字段的值包含“reentran”字符串
                    if "reentran" in type_value or "Reentran" in type_value:
                        # 创建新的json对象
                        new_json = {
                            "Code": code,
                            "VulnerabilityDesc": [
                                {
                                    "Name": file_path,
                                    "Location": desc.get("Location", ""),
                                    "Type": "Reentrancy",
                                    "Description": desc.get("Description", ""),
                                    "Repair": desc.get("Repair", "")
                                }
                            ]
                        }
                        output_jsons.append(new_json)
with open(output_file, 'w',encoding="utf-8") as f:
    json.dump(output_jsons, f, ensure_ascii=False, indent=4)
