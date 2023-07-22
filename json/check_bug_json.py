from token_check import *
import json
import sys
token_limit = 1500

# 记录check的结果
f = open("bug_json/check/check_record.txt", 'w', encoding='utf-8')
sys.stdout = f
sys.stderr = f  # redirect std err, if necessary

def read_json_to_check_code_token(path , filename):
    countOK = 0
    countNo = 0
    okfile = []
    nofile = []
    noindexs = []
    with open(path + filename + ".json", 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        index = 1
        for bug in data:
            # check bug code limit
            # check 1 - code
            num1_jrk = num_tokens_from_string(bug["Code"])
            num1_yyq = count_tokens(bug["Code"])
            flag = True
            # TODO check 2 - prompt
            # num2 = num_tokens_from_string()
            if num1_jrk < token_limit and num1_yyq < token_limit:
                countOK +=1
                okfile.append(bug)
            else:
                countNo += 1
                noindexs.append(index)
                flag = False
                nofile.append(bug)
            if not flag:
                print("{}:{} \t [num1_jrk :{}  , num1_yyq {}  ]".format(index,flag , num1_jrk , num1_yyq) )
            index += 1
    print("合格 code 长度 :\t" + str(countOK))
    print("不合格 code 长度 :\t" + str(countNo))
    print(noindexs)
    # 将两者分开
    with open(path + "check/" + filename + "_OK"+ ".json", 'w', encoding='utf-8') as f1:
        json.dump(okfile , f1 , indent=4)
    with open(path + "check/" + filename + "_NO"+ ".json", 'w', encoding='utf-8') as f2:
        json.dump(nofile, f2, indent=4)

if __name__ == "__main__":
    path  = "bug_json/"
    json_list = [
        "bug_erroneous_accounting",
        # "bug_fake_deposit",
        "bug_ID-related violations",
        "bug_precision",
        "bug_price_orcal",
        "bug_reentrancy"
    ]

    for filename in json_list:
        print(filename)
        print("--------------------------------------------------------------")
        read_json_to_check_code_token(path , filename)
        print("--------------------------------------------------------------")
