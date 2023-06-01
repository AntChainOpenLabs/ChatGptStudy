import json
from staVul2proComp import *

# 创建一个空列表来存储所有字典
vulnerabilities = []
benign = []
# prompt&completion文件
wirtefilename = r"experiment\1\1A\prompt_completion_1A.jsonl"
wirtefilename2 = r"experiment\1\1A\prompt_completion_1A_benign.jsonl"
testfilename = r"experiment\1\1A\prompt_completion_1A_test.jsonl"
testfilename_bug = r"experiment\1\1A\prompt_completion_1A_test_bug.jsonl"
# prompt优化字符
prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###"



# 将标准漏洞格式文件加载到内存
def read_file(filename,num_bug):
    # 打开JSON文件并加载数据
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)

    # 遍历JSON中的每个对象
    i = 0
    for item in data:
        # 创建一个字典来存储此对象的信息
        vulnerability = {}
        vulnerability['Code'] = item['prompt']
        vulnerability["IsBug"] = item["completion"]

        # 将此漏洞字典添加到漏洞列表中
        vulnerabilities.append(vulnerability)
        i += 1
        if i > num_bug:
            break

def read_benign_file(filename,num_bug):
    # 打开JSON文件并加载数据
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)

    # 遍历JSON中的每个对象
    i = 0
    for item in data:
        # 创建一个字典来存储此对象的信息
        benign_example = {}
        benign_example['Code'] = item['prompt']
        benign_example["IsBug"] = item["completion"]

        # 将此漏洞字典添加到漏洞列表中
        benign.append(benign_example)
        i+=1
    if i<num_bug:
        print("benign example not enough")

def generate_prompt_completion(filename, dic, choice):
    with open(filename,"w") as f :
        for vul in dic:
            if choice == 1:
                prompt_completion_fake_deposit(f, vul)
            elif choice == 2:
                prompt_completion_benign(f,vul)


def prompt_completion_fake_deposit(f, vul):
    prompt = "Does this  smart contract  have  fake deposit vulnerability?  "  + "\n" + vul['Code']
    completion = vul['IsBug'] + "\n"

    prompt_completion = prompt_optimization(prompt, completion)
    write_file(prompt_completion,f)


def prompt_completion_benign(f, vul):
    prompt = "Does this  smart contract  have  fake deposit vulnerability?  " + "\n" + vul['Code']

    prompt_completion = {"prompt": prompt}
    write_file(prompt_completion, f)

if __name__ == "__main__":
    good = 300
    bad = 300
    read_file(r"experiment\1\fake_deposit_final.json",bad)
    read_benign_file(r"experiment\1\Benign_sample_Check_token_True.json",good)
    generate_prompt_completion(wirtefilename,vulnerabilities,1)
    # generate_prompt_completion(wirtefilename2,benign[:good],1)
    # generate_prompt_completion(testfilename,benign[good+1:],2)


    # read_file(r"experiment\1\fake_deposit_test.json",10)
    # generate_prompt_completion(testfilename_bug,vulnerabilities,1)







