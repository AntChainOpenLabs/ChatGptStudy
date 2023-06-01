import time

import openai
import json
import random

prompt_start = ""
prompt_start = "You are a senior smart contract security engineer ."

prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###"

# FINE_TUNED_MODEL = "davinci:ft-antchainopenlab-2023-05-29-14-14-47" #1G
FINE_TUNED_MODEL = "davinci:ft-antchainopenlab-2023-06-01-08-15-25" #1A


testfilename = r"experiment\1\prompt_completion_test_bug.jsonl"
testfilename2 = r"experiment\1\prompt_completion_test_benign.jsonl"

testResult = r"experiment\1\1A\prompt_completion_1G_result_bug"
testResult2 = r"experiment\1\1A\prompt_completion_1G_result_benign"


def read_testFile(file, testCaseNum):
    i = 1
    testCase = []
    with open(file,"r") as f:
        content = f.readlines()
        if len(content) > testCaseNum:
            tst = random.sample(content, testCaseNum) #随机取样本数
        else:
            tst = content
        for line in tst:
            line = json.loads(line)
            testCase.append(line["prompt"])
    return testCase


def fineTune(FINE_TUNED_MODEL , testCase , file , temperature):
    ans_js =  {}
    for i in range(len(testCase)):
        PROMPT = testCase[i]
        ans = []
        print("正在测试第{}个样本".format(i))
        for j in range(1):
            response = openai.Completion.create(
                model= FINE_TUNED_MODEL,
                prompt= prompt_start + PROMPT + prompt_end,
                stop=completion_end,
                temperature= temperature,
                n = 10
            )
            for choice in response["choices"]:
                ans.append(choice["text"].replace("\n"," ").replace("\r"," "))
        ans_js[i] = ans

    with open(file,"w") as f:
        json.dump(ans_js,f,indent=4)

# filename : 测试文件
# testResult : 保存测试结果的文件
# testCaseNum : 测试数量
def run(filename, testResultFile, testCaseNum):
    testCase = read_testFile(filename, testCaseNum)
    for temperature in range(0,1):
        print("---------------------")
        print("正在测试 temperatur 为 {} 时 ".format(temperature))
        fineTune(FINE_TUNED_MODEL, testCase, testResultFile +"_" + str(temperature) + ".jsonl", temperature)
        time.sleep(2)
        print("正在测试 temperatur 为 {} 时 / 加了角色描述".format(temperature))
        fineTune(FINE_TUNED_MODEL, testCase, testResultFile +"_addRole_"  + str(temperature) + ".jsonl", temperature)

if __name__ == "__main__":
    run(testfilename,testResult, 10)
    run(testfilename2,testResult2, 10)