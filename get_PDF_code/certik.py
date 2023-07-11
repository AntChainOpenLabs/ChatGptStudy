############
# 获取cyberscope内容
############

import re

from pdf import *
import json

certik_pdf_path = "..\\..\\SolBugReports\\certik"
txt_path = "txt\\certik"
write_file = "certik_Suspected_vulnerability.txt"
matched_bug = []


def certik_match_func(content , file_name):
    # 先判断是否有漏洞， 根据pdf转txt的效果写，每种类型pdf类型可能不同
    # if "High Risk: 0" and "Medium Risk: 0" in content and "Low Risk: 0" in content:
    #     # 提取良性样本，可能有些pdf没有良性样本则跳过
    #     # get_Benign_sample(content,file_name)
    #     pass
    # 根据pdf格式截断不同的漏洞
    print("finding tittle")
    lines = content.split("\n")
    len_lines = len(lines)
    index = 0
    title_premix = ["MT","BT","ELFM","ST","OCTD","ULTW","BC","OTUT",]
    # ps ：不同pdf格式不同，可能有多级标题，根据具体格式书写
    while index < len_lines:
        # 找到题目 , 根据不同pdf格式进行替换，
        # 第一种规则：类似Certik_Final_Report_for_DoraHacks.pdf
        if "-" in lines[index] and ":" in lines[index]:
            title = lines[index].split(':', 1)[1]
            # 进行title判断是否是需要的漏洞类型
            type = suspected_vulnerability(title)
            if type != "":
                matched_bug.append(type + " $ " + file_name + "  :  " + title)
            index += 1
            continue
        
        # 第二种规则：类似Certik+Audit+Report+for+LockTrip.pdf
        if "Detail for Request" in lines[index] and ":" in lines[index]:
            title = lines[index].split(':', 1)[1]
            # 进行title判断是否是需要的漏洞类型
            type = suspected_vulnerability(title)
            if type != "":
                matched_bug.append(type + " $ " + file_name + "  :  " + title)
            index += 1
            continue

        # 第三种规则：类似CertiK+Security+Assessment+for+BrickChain.pdf
        if "|" in lines[index] and ":" in lines[index]:
            title = lines[index].split(':', 1)[1]
            # 进行title判断是否是需要的漏洞类型
            type = suspected_vulnerability(title)
            if type != "":
                matched_bug.append(type + " $ " + file_name + "  :  " + title)
            index += 1
            continue

        # 第四种规则：类似CertiK+Security+Assessment+for+BrickChain.pdf
        if "|" in lines[index] and ":" in lines[index]:
            title = lines[index].split(':', 1)[1]
            # 进行title判断是否是需要的漏洞类型
            type = suspected_vulnerability(title)
            if type != "":
                matched_bug.append(type + " $ " + file_name + "  :  " + title)
            index += 1
            continue
        # 忽略的规则1，AOK_Updated.pdf。因为不是以太坊
        # 忽略的规则2，CertiK_Verification_Report_for_DeFiScale.pdf，因为是对已有传统漏洞进行检测

        index+=1


# 进行标题模糊匹配，确定是否是需要的漏洞
def suspected_vulnerability(bug_title):
    bug_title = bug_title.lower().split(" ")
    # Price oracle manipulation
    # TODO 进行进一步完善
    if "price" in bug_title or "oracle" in bug_title or "manipulation" in bug_title  or "AMM" in bug_title:
        return "Price oracle manipulation"
    # ID-related violations
    # TODO 进行进一步完善
    if "ID-related" in bug_title or "violations" in bug_title  or "fake" in bug_title or "arbitrary" in bug_title or "arbitrarily" in bug_title or "access" in bug_title:
        return "ID-related violations"

    return ""


if __name__ == "__main__":
    print("--------------start")
    read_pdf(certik_pdf_path,txt_path,certik_match_func,"parse_text")
    print("--------------end")
    f = open(write_file,"a")
    print("have bugs " + str(len(matched_bug)))
    f.write("have bugs " + str(len(matched_bug)) + "\n")
    for s in matched_bug:
        print(s.encode('gbk', 'ignore'))
        f.write(str(s.encode('gbk', 'ignore'))[2:-2])
        f.write("\n")