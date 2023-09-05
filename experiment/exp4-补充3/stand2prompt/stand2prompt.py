import json
import os
datas = []
def process_bug_file(file_name):
    
    # 读取文件内容
    with open(file_name, 'r',encoding="utf-8") as file:
        data_list = json.load(file)
    # 遍历json数组中的每个元素
    for index, data in enumerate(data_list):
        # 提取"Code"和"VulnerabilityDesc"的值
        print(data['VulnerabilityDesc'][0]['Name'])
        code = data['Code']
        type = data['VulnerabilityDesc'][0]['Type']
        location = data['VulnerabilityDesc'][0]['Location']

        # 生成新的json对象
        new_data = {
            "prompt": code + "\n\n###\n\n",
            "completion": "Yes," + "{'type':'" + type + "','location':'"+location + "'}" + "###\n###"
        }

        datas.append(new_data)


def process_ben_file(file_name):
    
    # 读取文件内容
    with open(file_name, 'r',encoding="utf-8") as file:
        data_list = json.load(file)
    # 遍历json数组中的每个元素
    for index, data in enumerate(data_list):
        # 提取"Code"和"VulnerabilityDesc"的值
        print(data['VulnerabilityDesc'][0]['Name'])
        code = data['Code']
        

        # 生成新的json对象
        new_data = {
            "prompt": code + "\n\n###\n\n",
            "completion": "No." + "###\n###"
        }

        datas.append(new_data)

def write_file(new_file_name):
    # 写入到新的文件
    with open(new_file_name, 'w',encoding="utf-8") as new_file:
        
        for data in datas :
            new_file.write(json.dumps(data) + "\n")

def clen_cash():
    global datas
    datas = []


process_bug_file("standard/train_bug_fake_deposit.json")
process_ben_file("standard/train_ben_fake_deposit.json")
write_file("prompt/train_prompt_fake_depsot.json")
clen_cash()


process_bug_file("standard/train_bug_reentrancy.json")
process_ben_file("standard/train_ben_reentrancy.json")
write_file("prompt/train_prompt_reentrancy.json")
clen_cash()
