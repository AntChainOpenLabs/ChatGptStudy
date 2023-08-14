import openai
import re
import json
import jsonpath
import os
# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = "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"

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
    Code_stuct_arr = [Code_state()]*305
    obj = json.load(open('re.json','r'))
    Code_list = jsonpath.jsonpath(obj,'$..Code')
    print(len(Code_list))
    max_tokens = 2000
    Code_json_True_list = []
    Code_json_False_list = []
    for i in range(len(Code_list)):
        Code_list[i] = Code_list[i] + "\n\n###\n\n"
        Code_stuct_arr[i].check_token = check_token_limit(Code_list[i], max_tokens)
        Code_stuct_arr[i].id = i
        print("ID:",(Code_stuct_arr[i].id+1),"check_token:",Code_stuct_arr[i].check_token)
        if(Code_stuct_arr[i].check_token == 1):
            cnt_True = cnt_True+1
            Code_json = {"prompt":Code_list[i],"completion":"yes,Reentrancy###\n###"}
            Code_json_True_list.append(Code_json)
        else:
            cnt_False = cnt_False + 1

            Code_json = {"ID":i+1,"prompt":Code_list[i],"completion":"yes"}
            Code_json_False_list.append(Code_json)
    with open('re_200.json','w') as ft:
        json.dump(Code_json_True_list, ft)
    #with open('fake_deposit_final_False.json','w') as ff:
    #    json.dump(Code_json_False_list, ff)
    print("Ture num:",cnt_True,"False num:",cnt_False)
    #os.system("openai tools fine_tunes.prepare_data -f Check_token_True.json")