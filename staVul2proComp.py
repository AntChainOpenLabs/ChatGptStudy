import json

# 创建一个空列表来存储所有字典
vulnerabilities = []
# 标准漏洞格式数据文件
readfilename = 'standardVulnerability.json'
# prompt&completion文件
wirtefilename = "prompt_completion.jsonl"

#结束优化
prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###"

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
            if counter_example(f,vul):
                continue
            # prompt_completion_1(f, vul)
            # prompt_completion_2(f, vul)
            # prompt_completion_3(f, vul)
            # prompt_completion_4(f, vul)
            # prompt_completion_5(f, vul)
            prompt_completion_6(f, vul)
            prompt_completion_7(f, vul)
            prompt_completion_8(f, vul)

def prompt_optimization(prompt, completion):
    prompt_completion = {}
    prompt_completion['prompt'] = prompt + prompt_end
    prompt_completion['completion'] = completion_start + completion + completion_end
    return prompt_completion

def write_file(prompt_completion,f):
    json.dump(prompt_completion,f)
    f.write("\n")

def counter_example(f,vul):
    flag = False
    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            flag = True
            prompt_completion = {}
            prompt_completion['prompt'] = "Does this  smart contract  have any vulnerabilities?  " + vul['Code'] + prompt_end
            prompt_completion[
                'completion'] = completion_start + "here are no vulnerabilities in the given smart contract:  " + Desc["Description"] + completion_end
            json.dump(prompt_completion, f)
            f.write("\n")
    return flag


def prompt_completion_1(f, vul):
    prompt = "Does this  smart contract  have any vulnerabilities?  " + vul['Code']
    completion = "here are some potential vulnerabilities in the given smart contract:  " + str(vul['VulnerabilityDesc'])

    prompt_completion = prompt_optimization(prompt, completion)
    write_file(prompt_completion,f)

def prompt_completion_2(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            continue

        prompt = "Does this  smart contract  have any vulnerabilities? What is its vulnerability type?  " + vul['Code']
        completion = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description'] + "The vulnerability type is:  " + Desc['Type']

        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)

def prompt_completion_3(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Repair'] == "":
            continue

        prompt = "Does this  smart contract  have any vulnerabilities? How to fix it?  " + vul['Code']
        completion = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description'] + "To repair this Vulnerability:  " + Desc['Repair']
        
        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)

def prompt_completion_4(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Location'] == "":
            continue

        prompt = "Does this  smart contract  have any vulnerabilities? Where is the vulnerability?  " + vul['Code']
        completion = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description'] + "The vulnerability locates at:  " + Desc['Location']
        
        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)

def prompt_completion_5(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            continue

        prompt = "Does this  smart contract  have any vulnerabilities of " + Desc['Type'] +  "? "+ vul['Code']
        completion = "here are some potential vulnerabilities in the given smart contract:  " + Desc['Description']
        
        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)


def prompt_completion_6(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            continue
        if Desc['Location'] == "":
            continue
        prompt = "Does this  smart contract  have any vulnerabilities of " + Desc['Type'] +  "? "+ vul['Code']
        completion = "Yes , the vulnerabilities happens at " + Desc['Location']
        
        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)

def prompt_completion_7(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            continue
        if Desc['Location'] == "":
            continue
        prompt = "Does this  smart contract  have any vulnerabilities at " + Desc['Location'] +  "? "+ vul['Code']
        completion = "Yes , the contract have " + Desc['Type']
        
        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)

def prompt_completion_8(f, vul):

    for Desc in vul['VulnerabilityDesc']:
        if Desc['Type'] == "":
            continue
        if Desc['Location'] == "":
            continue
        prompt = "Does this  smart contract  have any vulnerabilities ? "+ vul['Code']
        completion = "Yes , the contract have " + Desc['Type'] + " at " + Desc['Location']
        
        prompt_completion = prompt_optimization(prompt, completion)
        write_file(prompt_completion,f)




if __name__=="__main__":
    read_standard_vulnerability(readfilename)
    generate_prompt_completion(wirtefilename)