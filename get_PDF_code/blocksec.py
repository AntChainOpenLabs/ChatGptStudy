############
# 获取blocksec内容
############
import re

from pdf import *
import json

blocksec_pdf_path = "..\\..\\SolBugReports\\blocksec"
txt_path = "txt\\blocksec"
write_file = "blocksec_Suspected_vulnerability.txt"
matched_bug = []

# json 模板, 使用前deep copy
bug_json_sample = {
        "Code": "",
        "VulnerabilityDesc": []
    }
VulnerabilityDesc_sample = {
        "Name": "" ,       #"report链接/name + 标题"
        "Location": "" ,   #"填写【函数/具体位置】",
        "Type": "",        #"填写【大分类】",
        "Description": "", #"填写【小分类.Description】 + 如果报告中有的话",
        "Repair": "" ,     #"空【看情况,如果报告中有的话例如Suggestion】"
}

# 根据每个pdf 写单独的match函数
# content : txt文本内容
# file_name : pdf的名字
def blocksec_match_func(content , file_name):
    # 先判断是否有漏洞， 根据pdf转txt的效果写，每种类型pdf类型可能不同
    if "High Risk: 0" and "Medium Risk: 0" in content and "Low Risk: 0" in content:
        # 提取良性样本，可能有些pdf没有良性样本则跳过
        # get_Benign_sample(content,file_name)
        pass
    # 根据pdf格式截断不同的漏洞
    lines = content.split("\n")
    len_lines = len(lines)
    index = 0
    # ps ：不同pdf格式不同，可能有多级标题，根据具体格式书写
    while index < len_lines:
        # 找到题目 , 根据不同pdf格式进行替换，
        # 匹配 ”2.1.1 “形式开头的为 标题的开始
        if re.match(r'^2\.\d+\.\d+ ',lines[index]) and  not lines[index][-1].isdigit():
            title = lines[index].split(' ', 1)[1]
            # 进行title判断是否是需要的漏洞类型
            if suspected_vulnerability(title):
                matched_bug.append(file_name + "  :  "+ title)
            index += 1

        else:
            index += 1





def empty(content , file_name):
    pass

if __name__ == "__main__":
    print("--------------start")
    read_pdf(blocksec_pdf_path,txt_path,blocksec_match_func,"parse_text")
    print("--------------end")
    f = open(write_file,"w+")
    print("have bugs " + str(len(matched_bug)))
    f.write("have bugs " + str(len(matched_bug)) + "\n")
    for s in matched_bug:
        print(s)
        f.write(s + "\n")