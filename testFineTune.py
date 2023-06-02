import time

import openai
import json
import random

prompt_start_0 = ""
prompt_start_1 = "You are a senior smart contract security engineer ."

prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###"

FINE_TUNED_MODEL = "davinci:ft-antchainopenlab-2023-06-01-14-37-42" #1G
# FINE_TUNED_MODEL = "davinci:ft-antchainopenlab-2023-06-01-08-15-25" #1A


testfilename = r"experiment\1\prompt_completion_bug_valid.jsonl"
testfilename2 = r"experiment\1\prompt_completion_benign_valid.jsonl"

# testfile = r"experiment\1\1G\prompt_completion_1G_bug_vaild.jsonl"
testResult = r"experiment\1\1G\prompt_completion_1G_result_bug"
testResult2 = r"experiment\1\1G\prompt_completion_1G_result_benign"


def read_testFile(file , testCaseNum):
    testCase = []
    with open(file,"r",encoding="utf-8") as f:
        content = f.readlines()
        tst = content
        # if len(content) > testCaseNum:
        #     tst = content
        #     # tst = random.sample(content, testCaseNum) #随机取样本数
        #     # tst = content[:testCaseNum]
        # else:
        #     tst = content
        for line in tst:
            line = json.loads(line)
            testCase.append(line["prompt"])
    return testCase


def fineTune(FINE_TUNED_MODEL , testCase , testCaseNum, file , prompt_start , temperature):
    ans_js =  {}
    index = 0
    for i in range(len(testCase)):
        if index == testCaseNum: # 如果测试了指定数目的样本
            break
        PROMPT = testCase[i]
        ans = []
        print("正在测试第{}个样本".format(i))
        for j in range(1):
            try:
                response = openai.Completion.create(
                    model= FINE_TUNED_MODEL,
                    prompt= prompt_start + PROMPT,
                    stop=completion_end,
                    temperature= temperature,
                    n = 5
                )
                for choice in response["choices"]:
                    ans.append(choice["text"].replace("\n"," ").replace("\r"," "))
                index += 1
            except:
                print(" 第{}个样本 测试失败 ".format(i))
                # print(PROMPT)
        if ans :
            ans_js[i] = ans

    with open(file,"w") as f:
        json.dump(ans_js,f,indent=4)

# filename : 测试文件
# testResult : 保存测试结果的文件
# testCaseNum : 测试数量
def run(filename, testResultFile, testCaseNum):
    testCase = read_testFile(filename, testCaseNum)
    for temperature in range(0,3):
        print("---------------------")
        # print("正在测试 temperatur 为 {} 时 ".format(temperature))
        # fineTune(FINE_TUNED_MODEL, testCase,testCaseNum, testResultFile +"_" + str(temperature) + ".jsonl", prompt_start_0 ,temperature)
        # time.sleep(2)
        print("正在测试 temperatur 为 {} 时 / 加了角色描述".format(temperature))
        fineTune(FINE_TUNED_MODEL ,testCase,testCaseNum, testResultFile +"_addRole_"  + str(temperature) + ".jsonl", prompt_start_1 ,temperature)

if __name__ == "__main__":
    run(testfilename,testResult, 10)
    # time.sleep(5)
    run(testfilename2,testResult2, 10)