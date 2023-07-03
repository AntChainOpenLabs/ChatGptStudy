############
# 获取cyberscope内容
############
import re

from pdf import *
import json

blocksec_pdf_path = "..\\..\\SolBugReports\\cyberscope"
txt_path = "txt\\cyberscope"
write_file = "cyberscope_Suspected_vulnerability.txt"
matched_bug = []


def empty(content , file_name):
    pass

if __name__ == "__main__":
    print("--------------start")
    read_pdf(blocksec_pdf_path,txt_path,empty,"parse_text")
    print("--------------end")
    f = open(write_file,"w+")
    print("have bugs " + str(len(matched_bug)))
    f.write("have bugs " + str(len(matched_bug)) + "\n")
    for s in matched_bug:
        print(s)
        f.write(s + "\n")