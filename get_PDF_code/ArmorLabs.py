############
# 获取ArmorLabs内容
############

import os
from pdf import *
import json

ArmorLabs_pdf_path = "../../SolBugReports/Armor Labs"
txt_path = "txt/ArmorLabs"

Benign_sample_path = "../json/ArmorLabs/Benign_sample.json"
Benign_sample_json = []
Benign_sample_count = 0

def read_ArmorLabs_pdf(dir_path):
    have_bug = []
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            # 拼接文件的完整路径
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                pdf_name = file_name
                to_file = txt_path + "\\" + pdf_name + ".txt"
                if not os.path.exists(to_file):
                    pdf2txt(file_path, to_file)
                with open(to_file,"r",encoding="utf-8") as f:
                    content = f.read()
                    if "Critical severity 0" and "High severity 0" in content and "Medium severity 0" in content:
                        get_Benign_sample(content,file_name)
                    else:
                        have_bug += [pdf_name]
    print("have_bug: {}".format(have_bug))

def get_Benign_sample(content,file_name):
    lines = content.split("\n")
    len_lines = len(lines)
    index = 0

    j = {
        "PdfName": file_name,
        "Code": []
    }
    while index < len_lines:
        line = lines[index]
        if line.startswith("pragma solidity"):
            code = "" + line + "\n"
            index += 1
            while index < len_lines and (not lines[index].startswith("Description: ") and not lines[index].startswith("pragma solidity")):
                line = lines[index]
                if len(line) == 0 or line.startswith("Contract file") or line.startswith("0X") or line.split("/")[0].strip().isdigit() or line.startswith("// SPDX-License-Identifier:"):
                    pass
                else:
                    code += line + "\n"
                index += 1
            j["Code"].append(code)
        else:
            index += 1

    # add to json
    global Benign_sample_json,Benign_sample_count
    Benign_sample_json.append(j)
    Benign_sample_count += len(j["Code"])





if __name__ == "__main__":
    read_ArmorLabs_pdf(ArmorLabs_pdf_path)
    print("Benign_sample_count: {}".format(Benign_sample_count))
    with open(Benign_sample_path,"w+",encoding="utf-8") as json_file:
        json.dump(Benign_sample_json,json_file , indent=4)



