import json
import os

def process_file(file_name):
    datas = []
    # 读取文件内容
    with open(file_name, 'r',encoding="utf-8") as file:
        data_list = json.load(file)
    # 遍历json数组中的每个元素
    for index, data in enumerate(data_list):
        # 提取"Code"和"VulnerabilityDesc"的值
        code = data['Code']
        print(data['VulnerabilityDesc'][0]['Type'])
        type = data['VulnerabilityDesc'][0]['Type']
        description = data['VulnerabilityDesc'][0]['Description']
        location = data['VulnerabilityDesc'][0]['Location']

        # 生成新的json对象
        new_data = {
            "prompt": code + "\n\n###\n\n",
            "completion": "yes," + type + "." + "The vulnerability is in " + location + "."+ description + "###\n###"
        }

        datas.append(new_data)
    # 写入到新的文件
    new_file_name = "prompt_" + file_name 
    with open(new_file_name, 'w',encoding="utf-8") as new_file:
        
        for data in datas :
            new_file.write(json.dumps(data) + "\n")

def process_files(file_names):
    for file_name in file_names:
        if os.path.exists(file_name):
            process_file(file_name)
        else:
            print(f'File {file_name} does not exist.')

# 你的文件名数组，例如 ["file1.json", "file2.json"]
file_names = ["bug_erroneous_accounting.json",
              "bug_ID-related violations.json",
              "bug_precision.json",
              "bug_price_orcal.json",
              "bug_reentrancy.json"]
process_files(file_names)
