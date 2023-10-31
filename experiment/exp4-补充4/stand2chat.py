import json
import os

datas = []


def process_bug_file(file_name):
    # 读取文件内容
    with open(file_name, 'r', encoding="utf-8") as file:
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
            "messages": [
                {"role": "system", "content": "You are a smart contract vulnerability audit expert."},
                {"role": "user", "content": "Does this  smart contract  have any vulnerabilities?\n\n" + code + "\n\n###\n\n"},
                {"role": "assistant", "content": " Yes," + "{'type':'" + type + "','location':'" + location + "'}" + "###\n###"}
            ]
        }

        datas.append(new_data)


def process_ben_file(file_name):
    # 读取文件内容
    with open(file_name, 'r', encoding="utf-8") as file:
        data_list = json.load(file)
    # 遍历json数组中的每个元素
    for index, data in enumerate(data_list):
        # 提取"Code"和"VulnerabilityDesc"的值
        print(data['VulnerabilityDesc'][0]['Name'])
        code = data['Code']

        # 生成新的json对象
        new_data = {
            "messages":[
                {"role": "system", "content": "You are a smart contract vulnerability audit expert."},
                {"role": "user", "content": "Does this  smart contract  have any vulnerabilities?\n\n" + code + "\n\n###\n\n"},
                {"role": "assistant", "content": "No."+ "###\n###"}
            ]
        }

        datas.append(new_data)


def write_file(new_file_name):
    # 写入到新的文件
    with open(new_file_name, 'w', encoding="utf-8") as new_file:
        for data in datas:
            new_file.write(json.dumps(data) + "\n")


def clen_cash():
    global datas
    datas = []


process_bug_file("stand2/standard/s6-1-delete-explation-2/Incorrect_calculating_order.json")
process_ben_file("stand2/standard/s6-1-delete-explation-2/ben_Incorrect_calculating_order.json")
write_file("stand2/chat/train_chat_Incorrect_calculating_order_delete_explation_2.jsonl")
clen_cash()

