import json

# 创建一个空列表来存储所有字典
vulnerabilities = []
# 标准漏洞格式数据文件
readfilename = 'standardVulnerability.json'
# prompt&completion文件
wirtefilename = "prompt_completion.jsonl"

# 将标准漏洞格式文件加载到内存
def read_standard_vulnerability(filename):
    # 打开JSON文件并加载数据
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)

    # 遍历JSON中的每个对象
    for item in data:
        # 创建一个字典来存储此对象的信息
        vulnerability = {}
        vulnerability['Code'] = item['Code']
        
        # 创建一个空列表来存储漏洞描述信息
        desc_list = []
        for desc in item['VulnerabilityDesc']:
            # 将每个漏洞描述信息存储到字典中
            desc_dict = {}
            desc_dict['Name'] = desc['Name']
            desc_dict['Location'] = desc['Location']
            desc_dict['Type'] = desc['Type']
            desc_dict['Description'] = desc['Description']
            desc_dict['Repair'] = desc['Repair']
            # 将此漏洞描述信息字典添加到漏洞描述列表中
            desc_list.append(desc_dict)
        
        # 将漏洞描述列表添加到漏洞字典中
        vulnerability['VulnerabilityDesc'] = desc_list
        
        # 将此漏洞字典添加到漏洞列表中
        vulnerabilities.append(vulnerability)

# 根据标准漏洞格式和多种提示生成规则，生成prompt和completion对。并写入文件
def generate_prompt_completion(filename):
    with open(filename,"w") as f :
        for vul in vulnerabilities:
            prompt_completion_1(f, vul)
            prompt_completion_2(f, vul)
            prompt_completion_3(f, vul)
            prompt_completion_4(f, vul)


def prompt_completion_1(f, vul):
    prompt_completion = {}
    prompt_completion['prompt'] = "Does this  smart contract  have any vulnerabilities?  " + vul['Code']
    prompt_completion['completion'] = "here are some potential vulnerabilities in the given smart contract:  " + str(vul['VulnerabilityDesc'])
    json.dump(prompt_completion,f)
    f.write("\n")

def prompt_completion_2(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            continue

        prompt_completion = {}
        prompt_completion['prompt'] = "Does this  smart contract  have any vulnerabilities? What is its vulnerability type?  " + vul['Code']
        prompt_completion['completion'] = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description'] + "The vulnerability type is:  " + Desc['Type']
        json.dump(prompt_completion,f)
        f.write("\n")

def prompt_completion_3(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Repair'] == "":
            continue

        prompt_completion = {}
        prompt_completion['prompt'] = "Does this  smart contract  have any vulnerabilities? How to fix it?  " + vul['Code']
        prompt_completion['completion'] = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description'] + "To repair this Vulnerability:  " + Desc['Repair']
        json.dump(prompt_completion,f)
        f.write("\n")

def prompt_completion_4(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Location'] == "":
            continue

        prompt_completion = {}
        prompt_completion['prompt'] = "Does this  smart contract  have any vulnerabilities? Where is the vulnerability?  " + vul['Code']
        prompt_completion['completion'] = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description'] + "The vulnerability locates at:  " + Desc['Location']
        json.dump(prompt_completion,f)
        f.write("\n")

if __name__=="__main__":
    read_standard_vulnerability(readfilename)
    generate_prompt_completion(wirtefilename)