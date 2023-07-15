############
# 获取cyberscope内容
############

import re

from pdf import *
import json

hacken_pdf_path = "..\\..\\SolBugReports\\hacken"
txt_path = "txt\\hacken"
write_file = "hacken_Suspected_vulnerability.txt"
matched_bug = []


def hacken_match_func(content , file_name):
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
        title = lines[index]
        # 进行title判断是否是需要的漏洞类型
        type = suspected_vulnerability(title)
        if type != "":
            matched_bug.append(type + " $ " + file_name + "  :  " + title)



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
    read_pdf(hacken_pdf_path,txt_path,hacken_match_func,"parse_text")
    print("--------------end")
    f = open(write_file,"a")
    print("have bugs " + str(len(matched_bug)))
    f.write("have bugs " + str(len(matched_bug)) + "\n")
    for s in matched_bug:
        print(s.encode('gbk', 'ignore'))
        f.write(str(s.encode('gbk', 'ignore'))[2:-2])
        f.write("\n")