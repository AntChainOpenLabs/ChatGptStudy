
import pandas as pd
import json

def xls2json(xlsx_file, bug_type):
    # 读取XLSX表格
    data = pd.read_excel(xlsx_file)

    # 将数据转换为JSON
    # json_data = data.to_json(orient='records')

    json_data_bug = []
    json_data_benign = []
    for index, row in data.iterrows():
        code = row['vul']
        code_ben = row['fix']
        name = str(row['n'])
        location = row['location']
        description = row['description']
        repair = ""

        vulnerability_bug = {
            "Name": name,
            "Location": location,
            "Type": bug_type,
            "Description": description,
            "Repair": ""
        }

        vulnerability_ben = {
            "Name": "ben_"+name,
            "Location": "",
            "Type": bug_type,
            "Description": "",
            "Repair": ""
        }

        entry_bug = {
            "Code": code,
            "VulnerabilityDesc": vulnerability_bug
        }

        entry_ben = {
            "Code": code_ben,
            "VulnerabilityDesc": vulnerability_ben
        }

        json_data_bug.append(entry_bug)
        json_data_benign.append(entry_ben)

    # 输出JSON数据
    with open("blew_2000_token/"+bug_type+".json",'w+') as f:
        json.dump(json_data_bug,f, indent=4)
    with open("blew_2000_token/"+"ben_"+bug_type+".json",'w+') as f2:
        json.dump(json_data_benign,f2, indent=4)

if __name__ == "__main__":
    xlsx_file =  ['raw/s6-1-2.xlsx']

    xls2json(xlsx_file[0], "Incorrect calculating order".replace(" ","_"))

