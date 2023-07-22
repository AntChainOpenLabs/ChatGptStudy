import re
import json
import jsonpath
import os

class Code_state:
    def __init__(self):
        self.id = 0
        self.check_token = 0
def count_tokens(prompt):
    # 正则
    tokens = re.findall(r'\w+|[^\w\s]', prompt)
    return len(tokens)

def check_token_limit(prompt, max_tokens):
    token_count = count_tokens(prompt)
    if token_count > max_tokens:
        print(f"prompt：{token_count} max_tokens：{max_tokens}.")
        return -1
    else:
        return 1

if __name__ == "__main__":
    cnt_True = 0
    cnt_False = 0
    Code_stuct_arr = [Code_state()]*505
    obj = json.load(open('Benign_sample.json','r'))

    #根据json格式去找对应的内容
    Code_list_tmp = jsonpath.jsonpath(obj,'$..Code')


    Code_hang = []
    Code_list = []
    cnt = 0
    for i in range(49):
        print(len(Code_list_tmp[i]))    
        Code_hang.append(len(Code_list_tmp[i]))
        cnt = cnt + len(Code_list_tmp[i])
    print(cnt)
    for i in range(49):
        for j in range(Code_hang[i]):
            Code_list.append(Code_list_tmp[i][j])
    print(len(Code_list))
    max_tokens = 1500
    Code_json_True_list = []
    Code_json_False_list = []
    for i in range(len(Code_list)):
        Code_stuct_arr[i].check_token = check_token_limit(Code_list[i], max_tokens)
        Code_stuct_arr[i].id = i
        print("ID:",(Code_stuct_arr[i].id+1),"check_token:",Code_stuct_arr[i].check_token)
        if(Code_stuct_arr[i].check_token == 1):
            cnt_True = cnt_True+1
            Code_json = {"prompt":Code_list[i],"completion":"no"}
            Code_json_True_list.append(Code_json)
        else:
            cnt_False = cnt_False + 1

            Code_json = {"ID":cnt_False,"prompt":Code_list[i],"completion":"yes"}
            Code_json_False_list.append(Code_json)
    with open('Benign_sample_Check_token_True.json','w') as ft:
        json.dump(Code_json_True_list, ft)
    with open('Benign_sample_Check_token_False.json','w') as ff:
        json.dump(Code_json_False_list, ff)
    print("Ture num:",cnt_True,"False num:",cnt_False)
    #转化成jsonl
    #os.system("openai tools fine_tunes.prepare_data -f xxx.json")
