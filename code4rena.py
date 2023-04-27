import markdown
import os
import os.path
import re
from bs4 import BeautifulSoup
import json
import requests
import time

from pdf import *
from Embedding_Vul_Text_for_serarch import *
from Question_answering_using_embeddings import *


# test_path = "..\\SolBugReports\\code4rena\\2021-08-gravitybridge"
test_path = "..\\SolBugReports\\code4rena\\2021-04-basedloans"

code4rena_path = "..\\SolBugReports\\code4rena"

download_pdf_path = "pdf\\code4rena"
json_path = "json\\code4rena2"
txt_path = "txt\\code4rena"
high_count = 0
mid_count = 0


def report(dir_path):
    code_paths = read_code_path(dir_path)

    if not os.path.exists(dir_path + "-findings"):  # 如果不存在报告目录
        return
    pdf_path, file_path = read_md_path(dir_path + "-findings")
    if pdf_path == "":
        if file_path != "":
            # read_md(file_path,code_paths)     #直接为md模式
            get_md_section(file_path, code_paths)
        else:
            return
    else:
        # read_pdf(pdf_path,code_paths)      #下载pdf模式
        pass
    # result = parse_md_to_json(md_paths, code_paths)
    # 写入JSON文件
    # with open('output.json', 'w') as f:
    #     json.dump(result, f,indent=4)


# 根据md提取分段信息
def get_md_section(file_path, code_paths):
    start_time = time.time()  # 记录程序开始运行时间
    # code4rena_sections_file =  open("code4rena_sections.txt", "w+", encoding="utf-8")

    final_json = []
    json_name = json_path + "\\" + file_path.split("\\")[-3] + ".json"
    # if os.path.exists(json_name):
    #     return

    VulnerabilityDesc = {}
    # SAVE_PATH = json_path + "\\" + "file_path.split("\\")[-3] "+ ".csv"
    SAVE_PATH = json_path + "\\" + "test" + ".csv"


    global high_count, mid_count


    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 匹配一级标题
        high_mid = []
        high = []
        mid = []
        try:
            # 取high
            if "# High Risk Findings" in content:
                bugs = re.split('# High Risk Findings', content)[1]
                if "# Medium Risk Findings" in content:
                    bugs = re.split('# Medium Risk Findings', bugs)
                    high = re.split('## \[', bugs[0])[1:]

                    if "# Low Risk Findings" in content:
                        mid += re.split('## \[', re.split("# Low Risk Findings", bugs[1])[0])[1:]

                elif "# Low Risk Findings" in content:
                    bugs = re.split('# Low Risk Findings', bugs)
                    high = re.split('## \[', bugs[0])[1:]

                elif "# Non-Critical Findings" in content:
                    bugs = re.split('# Non-Critical Findings', bugs)
                    high = re.split('## \[', bugs[0])[1:]
                elif "# Disclosures" in content:
                    bugs = re.split('# Disclosures', bugs)
                    high = re.split('## \[', bugs[0])[1:]

            elif "# Medium Risk Findings" in content:
                # 取mid
                bugs = re.split('# Medium Risk Findings', content)[1]
                if "# Low Risk Findings" in content:
                    bugs = re.split('# Low Risk Findings', bugs)
                    mid = re.split('## \[', bugs[0])[1:]
                elif "# Non-Critical Findings" in content:
                    bugs = re.split('# Non-Critical Findings', bugs)
                    mid = re.split('## \[', bugs[0])[1:]
                elif "# Disclosures" in content:
                    bugs = re.split('# Disclosures', bugs)
                    mid = re.split('## \[', bugs[0])[1:]
        except:
            print(file_path)
            return
        # 发送到gpt中解析
        high_mid = high + mid
        high_count += len(high)
        mid_count += len(mid)

        # md_sections = []
        for bug in high_mid:
            lines = bug.split("\n")
            head = lines[0].split("]")
            head1 = "["+head[0][1:]+"]"
            head2 = head[1].replace("`", " ").replace("**", "")

            # ---------------------------------------------------------------------
            if head1.startswith("H"):
                title = ["High Severity", head1, head2]
            else:
                title = ["Medium Severity", head1, head2]
            # title = [head2]
            index = 1
            if lines[1].startswith("_Submitted by"):
                index = 2
            body = ""
            for line in lines[index:]:
                if line.startswith("#"):
                    continue
                body += clear_md_line(line)

            # 创建分词csv文件
            split_sections([(title,body)], SAVE_PATH)

            section = get_section_json(SAVE_PATH)
            # ---------------------------------------------------------------------
            #
            item_json = json.loads(section)
            bug_json = {
                "Name": head1 + head2,
                "Location": "",
                "Type": "",
                "Description": "",
                "Repair": ""
            }
            bug_json["Type"] = item_json["Vulnerability Type"]
            bug_json["Location"] = item_json["Vulnerability Location"].replace("`","")
            bug_json["Repair"] = item_json["Repair Method"].replace("`","")
            bug_json["Description"] = item_json["Vulnerability Information"].replace("`","")

            # final_json.append(bug_json)

            # ---------------------------------------------------------------------
            # 处理code
            functions = set()  # 通过驼峰命名匹配的函数
            contracts = set()  # 出现合约名字
            contracts2 = set() # 通过函数名匹配出现的合约

            for word in bug_json["Location"].split(" "):
                if word in code_paths.keys():
                    contracts.add(word)
                elif word+".sol" in code_paths.keys():
                    contracts.add(word+".sol")
                elif  "." in word: #例如MarginRouter.crossSwapExactTokensForTokens的形式
                    if " " not in word:
                        temp = word.split(".")
                        contract = temp[0] + ".sol"
                        if contract in code_paths.keys(): #如果是合约的代码
                            contracts.add(contract)
                        continue
                elif word.endswith(")"):
                    functions.add(word.split("(")[0])
                elif is_camel_case(word):
                    if word[-1].isalpha():
                        functions.add(word)
                    continue

            for func in list(functions):
                for code_name, code_path in code_paths.items():
                    try:
                        with open(code_path, "r", encoding="utf-8") as cd:
                            code_content = cd.read()
                            if func in code_content:
                                contracts2.add(code_name)
                                break
                    except:
                        # print(code_path)
                        continue

            contracts  = list(set(list(contracts) + list(contracts2)))
            contracts_name = "/".join(list(contracts))
            if VulnerabilityDesc.__contains__(contracts_name):
                VulnerabilityDesc[contracts_name].append(bug_json)
            else:
                VulnerabilityDesc[contracts_name] = [bug_json]


    # # 将section以json格式存储到文件
    # json_file = open(json_name, "w+", encoding="utf-8")
    # json.dump(final_json, json_file, indent=4)
    # json_file.close()

    # 处理json数据
    json_file = open(json_name, "w")
    for sol_names, bug_jsons in VulnerabilityDesc.items():
        j = {
            "Code": "",
            "CodeNames": [],
            "VulnerabilityDesc": []
        }
        sol_names = list(sol_names.split("/"))
        codes = ""
        # 拼接code
        for sol_name in sol_names:
            if sol_name not in code_paths.keys():
                continue
            sol_path = code_paths[sol_name]
            with open(sol_path, "r", encoding="utf-8") as sol:
                codes += sol.read() + "\n\n"
        j["Code"] = codes
        j["CodeNames"] = sol_names
        j["VulnerabilityDesc"] = bug_jsons

        # json.dump(j,json_file,indent=4)
        # json_file.write("\n")
        final_json.append(j)
    json.dump(final_json, json_file, indent=4)

    json_file.close()

    end_time = time.time()  # 记录程序结束运行时间
    print('cost %f second' % (end_time - start_time))




# 根据md提取漏洞信息
def read_md(file_path,code_paths):
    VulnerabilityDesc = {}

    json_name = json_path + "\\" + file_path.split("\\")[-3] + ".json"


    global high_count,mid_count

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 匹配一级标题
        high_mid = []
        high = []
        mid = []
        try:
            # 取high
            if "# High Risk Findings" in content:
                bugs = re.split('# High Risk Findings', content)[1]
                if "# Medium Risk Findings" in content:
                    bugs = re.split('# Medium Risk Findings', bugs)
                    high = re.split('## \[', bugs[0])[1:]

                    if "# Low Risk Findings" in content:
                        mid += re.split('## \[',re.split("# Low Risk Findings",bugs[1])[0])[1:]

                elif "# Low Risk Findings" in content:
                    bugs = re.split('# Low Risk Findings', bugs)
                    high = re.split('## \[', bugs[0])[1:]

                elif "# Non-Critical Findings" in content:
                    bugs = re.split('# Non-Critical Findings', bugs)
                    high = re.split('## \[', bugs[0])[1:]
                elif "# Disclosures" in content:
                    bugs = re.split('# Disclosures', bugs)
                    high = re.split('## \[', bugs[0])[1:]

            elif "# Medium Risk Findings" in content:
                # 取mid
                bugs = re.split('# Medium Risk Findings', content)[1]
                if "# Low Risk Findings" in content:
                    bugs = re.split('# Low Risk Findings', bugs)
                    mid = re.split('## \[', bugs[0])[1:]
                elif "# Non-Critical Findings" in content:
                    bugs = re.split('# Non-Critical Findings', bugs)
                    mid = re.split('## \[', bugs[0])[1:]
                elif "# Disclosures" in content:
                    bugs = re.split('# Disclosures', bugs)
                    mid = re.split('## \[', bugs[0])[1:]
        except:
            print(file_path)
            return
        # first_heading = re.split('## ', content)[1:]
        #解析bug
        high_mid = high + mid
        high_count += len(high)
        mid_count += len(mid)

        count = 1

        if len(high_mid) > 0:
            for bug in high_mid:
                bug_json = {
                    "Name": "",
                    "Location": "",
                    "Type": "",
                    "Description": "",
                    "Repair": ""
                }

                lines = bug.split("\n")
                head = lines[0].split("]")


                bug_json["Name"] = head[0][1:]
                bug_json["Type"] = head[1].replace("`"," ").replace("**","")


                # ---------------------------------------------------------------------
                index = 1
                Description = ""
                Repair = ""
                if lines[1].startswith("_Submitted by"):
                    index = 2

                if "### " not in bug:
                    # 获取description 格式1
                    while index < len(lines) and not lines[index].startswith("Recommend"):
                        line = clear_md_line(lines[index])
                        Description += line + "\n"
                        index += 1
                    if index < len(lines) and lines[index].startswith("Recommend"):
                        while index < len(lines):
                            line = clear_md_line(lines[index])
                            Repair += line + "\n"
                            index += 1
                else:
                    # 获取description 格式2 含有 ”### Impact“或者别的三级标签
                    while  index < len(lines) and not lines[index].endswith("### Recommendation") and not lines[index].endswith("### Recommended Mitigation Steps"):
                        if lines[index].startswith("###"):
                            index +=1
                            continue
                        line = clear_md_line(lines[index])
                        Description += line + "\n"
                        index += 1
                    if index < len(lines) and (lines[index].endswith("### Recommendation") or lines[index].endswith("### Recommended Mitigation Steps")):
                        index += 1 #去掉三级标题行
                        while index < len(lines):
                            line = clear_md_line(lines[index])
                            Repair += line + "\n"
                            index += 1

                bug_json["Description"] = Description.replace("`","").replace("\n[","\n")
                bug_json["Repair"] = Repair.replace("`","").replace("\n[","\n")




                # ---------------------------------------------------------------------
                # 长代码
                code = re.compile(r"```(.*?)```", re.S)
                codes = []
                codes += code.findall(Description)

                # 短代码
                small_codes = []
                small_code = re.compile(r" `(.*?)`", re.S)
                small_code2 = re.compile(r"\n`(.*?)`", re.S)
                small_codes += small_code.findall(Description + head[1]) + small_code2.findall(Description)
                # 去掉small_codes冗余
                small_codes = set(small_codes)
                small_codes = {re.sub(r'\d(.+)', '', elem) for elem in small_codes}  # 去掉数字
                small_codes = list(filter(None, small_codes))
                temp = []
                for s in small_codes:
                    if len(s) > 2:
                        temp.append(s)
                small_codes = temp

                # bug涉及到的contract
                contracts1 = set()  #直接提到的
                contracts2 = set()  #函数代码包含的

                # bug涉及到的Location
                Location = set()

                # 处理code
                if len(codes) == 0 and len(small_codes) == 0:
                    continue
                if len(small_codes) > 0:
                    for c in small_codes:
                        # 检测是否短代码是否包含在文件名中
                        if c in code_paths.keys():
                            contracts1.add(c)
                            continue
                        if c + ".sol" in code_paths.keys():
                            contracts1.add(c + ".sol")
                            continue
                        if "." in c: #例如MarginRouter.crossSwapExactTokensForTokens的形式
                            if " " not in c:
                                temp = c.split(".")
                                contract = temp[0] + ".sol"
                                if contract in code_paths.keys(): #如果是合约的代码
                                    contracts2.add(contract)
                                    Location.add(temp[1].strip())
                                continue
                        # 检测是否短代码包含在文件中
                        temp = c
                        c = c.split("(")[0]  #处理短代码，取出函数名或者变量名
                        for code_name, code_path in code_paths.items():
                            try:
                                with open(code_path, "r", encoding="utf-8") as cd:
                                    code_content = cd.read()
                                    if c in code_content:
                                        contracts2.add(code_name)
                                        Location.add(temp.strip())
                                        break
                            except:
                                # print(code_path)
                                continue

                # 获取location
                # 如果有codes则使用codes,没有直接用Location
                if len(codes) >= 1:
                    bug_json["Location"] = [code.replace("solidity", "//solidity").replace("rust","//rust") for code in codes]
                else:
                    if len(small_codes) >= 1:
                        bug_json["Location"] = list(Location)

                # 获取code
                if len(contracts2) > 0:
                    CodeNames = contracts2
                else:
                    CodeNames = contracts1
                contracts = "/".join(CodeNames)
                if not VulnerabilityDesc.__contains__(contracts):
                    VulnerabilityDesc[contracts] = [bug_json]
                else:
                    VulnerabilityDesc[contracts] += [bug_json]
        else:
            #没有high、mid的bug存在
            return

        # 处理json数据
        json_file = open(json_name, "w")
        final_json = []
        for sol_names, bug_jsons in VulnerabilityDesc.items():
            j = {
                "Code": "",
                "CodeNames": [],
                "VulnerabilityDesc": []
            }
            sol_names = list(sol_names.split("/"))
            codes = ""
            # 拼接code
            for sol_name in sol_names:
                if sol_name not in code_paths.keys():
                    continue
                sol_path = code_paths[sol_name]
                with open(sol_path, "r", encoding="utf-8") as sol:
                    codes += sol.read() + "\n\n"
            j["Code"] = codes
            j["CodeNames"] = sol_names
            j["VulnerabilityDesc"] = bug_jsons

            # json.dump(j,json_file,indent=4)
            # json_file.write("\n")
            final_json.append(j)
        json.dump(final_json, json_file, indent=4)

        json_file.close()



def clear_line(line):
    line = line.replace(u'\xa0', " ").replace("̀"," ").replace('“'," ")
    line = ' '.join(line.split())
    return line


def clear_md_line(line):
    line = line.replace("<br />","").replace("- ","").replace("**","").replace(">","").replace("\n[","\n").replace(" ["," ").replace("](","(").replace("\\","")
    # line =
    return line

def read_pdf(dir_path,code_paths):
    #pdf转文字
    pdf_name = dir_path.split("\\")[-1]
    to_file = txt_path + "\\" + pdf_name + ".txt"
    pdf2txt(dir_path, to_file)

    json_name = json_path + "\\" + pdf_name + ".json"
    json_file = open(json_name,"w")


    VulnerabilityDesc = {}

    high_mid = {}
    #获取bug数据
    with open(to_file,"r",encoding="utf-8") as f:
        lines = f.readlines()
        len_lines = len(lines)
        i = 0
        while i < len_lines:
            line = clear_line(lines[i])
            if line.startswith("High Severity") :
                while i<len_lines and not line.startswith("Medium Severity"):
                    if line.startswith("[H-"):
                        high_mid[line] = ""
                        line2 = ""
                        while i<len_lines-1 and not line2.startswith("[H-") and not line2.startswith("Medium Severity"):
                            high_mid[line] += line2 + " "
                            i += 1

                            line2 = clear_line(lines[i])
                        line = line2
                    else:
                        i+=1
                        if i<len_lines:
                            line = clear_line(lines[i])

            if line ==  "Medium Severity":
                while i < len_lines - 1 and not line.startswith("Low Severity"):
                    if line.startswith("[M-"):
                        high_mid[line] = ""
                        line2 = ""
                        while i < len_lines - 1 and not line2.startswith("[M-") and not line2.startswith("Low Severity"):
                            if line2 == "\n":
                                high_mid[line] += line2
                            else:
                                high_mid[line] += line2.replace("\n"," ")
                            i += 1
                            line2 = clear_line(lines[i])
                        line = line2
                    else:
                        i += 1
                        if i<len_lines : line = clear_line(lines[i])
            if line.startswith("Low Severity"):
                pass

            i+=1

    #处理bug数据
    for head,description in high_mid.items():
        bug_json = {
            "Name": "",
            "Location": [],
            "Type": "",
            "Description": "",
            "Repair": ""
        }
        bug_json["Name"] = pdf_name + "_" + head[1:5]
        bug_json["Type"] = head[6:].replace("\n","")
        bug_json["Description"] = description
        description = description.replace(".", " . ").replace("\n", " ")

        functions = set(re.findall(r"\b\w+\(\)", head)
                        + re.findall(r"\b\w+\(\)", description)
                        + re.findall(r"\b\w+\(.*?\)", description)
                        ) #出现的函数，以function()形式
        functions2 = set() #通过驼峰命名匹配的函数
        contracts = set()  #出现合约名字

        for word in bug_json["Type"].split(" ") + description.split(" "):
            if is_camel_case(word):
                if word[-1].isalpha():
                    functions2.add(word)
            for code_name in code_paths.keys():
                if  code_name.split(".")[0] == word:
                    contracts.add(word)
        # print("----------------")
        # print(functions)
        # print(functions2)
        # print(contracts)

        # {'executeTrades(DAI, WETH, 1000, [], 0, alice)', 'rescueTokens()', 'executeTrades()',
        #  'executeTrades(DAI, WETH, 0, [{TradeData}], 0, eve)'}
        # {'fromToken', 'finalAmountMin'}
        # {'Slingshot'}

        #处理Location
        if len(functions)==0 and len(functions2) == 0:
            bug_json["Location"] = []
        else:
            for fn2 in functions2:
                flag = True # functions2 不包含在 functions中
                for fn in functions:
                    if fn.startswith(fn2):
                        flag = False
                        break
                if flag:
                    functions.add(fn2)
            funcs = []
            for func in functions:
                funcs.append(func.replace(" . ","."))
            functions = funcs
            bug_json["Location"] = functions


        #处理code
        # print(contracts)
        if len(contracts) > 0:
            contract_names = ""
            for c in contracts:
                c = c + ".sol"
                contract_names += c + "/"
            if contract_names in VulnerabilityDesc.keys():
                VulnerabilityDesc[contract_names].append(bug_json)
            else:
                VulnerabilityDesc[contract_names] = [bug_json]
        else:
            for fn in functions:
                #处理fn，只保留function name

                fn = fn.split("(")[0]

                for code_name,code_path in code_paths.items():
                    with open(code_path,"r",encoding="utf-8") as c:
                        sol_content  = c.read()
                        if fn in sol_content:
                            contracts.add(code_name)
            contract_names = ""
            for c in contracts:
                contract_names += c + "/"
            if contract_names in VulnerabilityDesc.keys():
                VulnerabilityDesc[contract_names].append(bug_json)
            else:
                VulnerabilityDesc[contract_names] = [bug_json]
        # print(contracts)

    #处理json数据
    final_json = []
    for sol_names,bug_jsons in VulnerabilityDesc.items():
        j = {
            "Code": "",
            "CodeNames": [],
            "VulnerabilityDesc" : []
        }
        sol_names = sol_names.replace("/"," ").split(" ")
        codes = ""
        #拼接code
        for sol_name in sol_names:
            if sol_name not in code_paths.keys():
                continue
            sol_path = code_paths[sol_name]
            with open(sol_path,"r",encoding="utf-8") as sol:
                codes += sol.read() + "\n\n"
        j["Code"] = codes
        j["CodeNames"] = sol_names
        j["VulnerabilityDesc"] = bug_jsons

        # json.dump(j,json_file,indent=4)
        # json_file.write("\n")
        final_json.append(j)
    json.dump(final_json,json_file,indent=4)

    json_file.close()



def is_camel_case(word):

    # 匹配非字母字符
    non_alpha_regex = re.compile(r'[^a-zA-Z]')
    # 检查单词是否包含下划线
    if '_' in word:
        return True
    if not any([c for c in word if c.isupper()]) or not any([c for c in word if c.islower()]):
        return False
    # if word[0].isupper():
        # return False
    # 按大写字母拆分单词
    words = re.findall('[A-Z][^A-Z]*', word)
    # 检查单词是否都是首字母大写
    if len(words) <2 :
        return False
    return all(w[0].isupper() for w in words[1:])


def read_md_path(dir_path):
    # 读取sol code的列表

    # md_paths = {}
    pdf_path = ""
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            # 拼接文件的完整路径
            if file_name.endswith(".md"):
                file_path = os.path.join(root, file_name)
                # print(file_path)
                if file_name == "report.md":
                    # 下载report
                    pdf_path = download_pdf(file_path)
                    return pdf_path,file_path
                elif file_name == "README.md":
                    pass
                else:
                    pass
                    # 其他文件
                    # md_paths[file_name]=file_path
    return pdf_path,""


#读取sol code的路径
def read_code_path(dir_path):
    code_paths = {}
    # "filename":"filepath"
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            # 拼接文件的完整路径
            if file_name.endswith(".sol"):
                file_path = os.path.join(root, file_name)
                code_paths[file_name]=file_path
    return code_paths



def download_pdf(file_path):
    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        line = f.readline()
        line = f.readline()

        # 下载pdf
        if line.startswith("[PDF report]"):
            href = line.split("(")[-1][:-2]
            name =  str(href.split("/")[-1]).replace("%20"," ")
            name = name.split("?filename=")[-1]
            # print(href)
            if '.pdf' in href:
                # print("download pdf report: " + name)
                file_name = os.path.join(download_pdf_path, name)
                if os.path.exists(file_name): #如果存在文件则不用重复下载
                    return file_name
                with open(file_name, 'wb') as f:
                    f.write(requests.get(href).content)
                    # print('Downloaded:', file_name)
                return file_name
        else:
            return ""



def parse_md_to_json(md_paths, code_paths):


    VulnerabilityDesc = {}

    for file_name,file_path in md_paths.items():
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # 匹配一级标题
            first_heading = re.split('## \[',content)[1:]
            print("---------------------------------------"+file_name)
            print("bugs :"+ str(len(first_heading)))

            #每个bug
            for index in range(len(first_heading)):
                bug = first_heading[index]
                # 处理bug
                bug_json = {
                    "Name": "",
                    "Location": "",
                    "Type": "",
                    "Description": "",
                    "Repair": ""
                }
                bug_json["Name"] = file_name +"_"+ str(index)

                #长代码
                code = re.compile(r"```(.*?)```", re.S)
                codes = []

                #短代码
                small_codes = []
                small_code = re.compile(r" `(.*?)`", re.S)

                # print("/////////////////////////////////////////////")
                #以二级标签分段
                items = re.split("## " ,bug)[1:]
                for item in items:
                    # print("+++++++++++++++++++++++++++++++++++++++++")
                    lines = item.split("\n")
                    flag = True
                    #获取纯净文本
                    text = "".join(lines[1:]).replace("`", "")
                    pattern = re.compile(r'\(http(.+?)\)') #去掉链接
                    text = re.sub(pattern,'',text).replace("[","").replace("]","") # 用前后查找的方式获取中间的文本，并删除整个匹配
                    # blob = TextBlob(text)
                    # print(blob.sentences[0].noun_phrases)

                    #去掉空行
                    while flag:
                        if '' in lines :
                            lines.remove('')
                        else:
                            flag = False

                    # print(lines)
                    if lines[0] == "Summary":

                        bug_json["Type"] = text
                        # 提取短代码
                        small_codes += small_code.findall(item)
                        # print(bug_json)


                    elif lines[0] == "Risk Rating":
                        #如果为1则跳过
                        risk_rating  = "".join(lines[1:]).strip(" ")
                        if "1" in risk_rating or "low" in risk_rating.lower():
                            bug_json = {} #清空
                            break
                        pass
                    elif lines[0] == "Vulnerability Details":
                        #处理description
                        bug_json["Description"] = text
                        # 提取长代码
                        codes += code.findall(item)
                    elif lines[0] == "Recommended Mitigation Steps":
                        #处理repair
                        bug_json["Repair"] = "".join(lines[1:]).replace("`","")
                        # 提取短代码
                        small_codes += small_code.findall(item)
                    else:
                        #去掉其余信息
                        pass

                #如果bug_json为空则表示不是目标，不记录
                if bug_json == {}:
                    continue

                # 去掉small_codes冗余
                small_codes = set(small_codes)
                small_codes = {re.sub(r'\d+', '', elem) for elem in small_codes}  # 去掉数字
                small_codes = list(filter(None, small_codes))
                temp = []
                for s in small_codes:
                    if len(s) > 1:
                        temp.append(s)
                small_codes = temp

                # 处理code
                if len(codes) == 0 and len(small_codes) == 0:
                    continue
                if len(small_codes) > 0:
                    for code_name, code_path in code_paths.items():
                        for c in small_codes:
                            #检测是否短代码是否包含在文件名中
                            if c.lower() in code_name.lower():
                                if VulnerabilityDesc.__contains__(code_name):
                                    if bug_json not in VulnerabilityDesc[code_name]:
                                        VulnerabilityDesc[code_name].append(bug_json)
                                else:
                                    VulnerabilityDesc[code_name] = [bug_json]
                                continue
                            #检测是否短代码包含在文件中
                            with open(code_path, "r", encoding="utf-8") as cd:
                                code_content = cd.read()
                                if c in code_content:
                                    if VulnerabilityDesc.__contains__(code_name):
                                        if bug_json not in VulnerabilityDesc[code_name]:
                                            VulnerabilityDesc[code_name].append(bug_json)
                                    else:
                                        VulnerabilityDesc[code_name] = [bug_json]

                # 处理location
                flag_use_small_code = False
                # 如果有codes则使用codes
                if len(codes) >= 1:
                    bug_json["Location"] = " \n".join(codes).replace("solidity", "")
                else:
                    if len(small_codes) >= 1:
                        temp = {re.sub(r'(.+).sol', '', elem) for elem in
                                small_codes}  # 去掉例如Slingshot.sol
                        temp = list(filter(None, temp))
                        bug_json["Location"] = "\n".join(temp)

                        flag_use_small_code = True

    return VulnerabilityDesc




if __name__ == "__main__":
    path = code4rena_path
    # dir_path = "../2021-02-slingshot"
    # 获取目录下所有子元素
    sub_elements = os.listdir(path)
    dir_paths = []
    # 遍历子元素并打印目录
    for element in sub_elements:
        if os.path.isdir(os.path.join(path, element)):
            if not element.endswith("-findings"):
                dir_paths.append(os.path.join(path, element))
            # print(element)
    count = 0
    print("--------------------------------start")
    for dir_path in dir_paths:
        # print(dir_path)
        report(dir_path)
        if count %20 == 0 :
            print("-------------------------" + str(count))
        count+=1
    print("----------------------------------end")
    print("total report: " + str(count))
    print("high: " + str(high_count))
    print("mid: " + str(mid_count))

    # report(test_path)

    # pdf_sections = []
    # with open("code4rena_sections.txt", "r", encoding="utf=8") as f:
    #     data = json.load(f)
    #     for item in data:
    #         pdf_sections.append((item["title"],item["body"]))
    #     print()
    # print()

