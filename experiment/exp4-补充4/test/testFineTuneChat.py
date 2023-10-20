import time

import openai
import json
import random




FINE_TUNED_MODEL_supplement = "gpt-3.5-turbo-0613" # exp4-补充4-1


vul_ben_Incorrect_calculating_order_file = ""
vul_bug_Incorrect_calculating_order_file = ""

vul_ben_Incorrect_calculating_order_result = "result/ben_Incorrect_calculating_order/vul_ben_Incorrect_calculating_order_result"
vul_bug_Incorrect_calculating_order_result = "result/bug_Incorrect_calculating_order/vul_bug_Incorrect_calculating_order_result"


def read_testFile(file):
    testCase = []
    with open(file,"r",encoding="utf-8") as f:
        tst = json.load(file)
        for item in tst:
            testCase.append(item["Code"])
    return testCase


def fineTune(FINE_TUNED_MODEL , testCase , testCaseNum, file  , temperature):
    ans_js =  {}
    index = 0
    for i in range(len(testCase)):
        if index == testCaseNum: # 如果测试了指定数目的样本
            break
        code = testCase[i]
        ans = []
        print("正在测试第{}个样本".format(i))
        # 问几次就是几
        for j in range(1):
            try:
                response = openai.ChatCompletion.create(
                    model= FINE_TUNED_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a smart contract vulnerability audit expert."},
                        {"role": "user", "content": "Does this  smart contract  have any vulnerabilities?\n\n" + code + "\n\n###\n\n"},
                    ],
                    # 问一次生成几个completion
                    n = 5,
                    temperature=temperature,
                )
                print(response)
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
def run(fine_tuned_model, filename, testResultFile, testCaseNum):
    testCase = read_testFile(filename, testCaseNum)
    for temperature in range(0,1):
        print("---------------------")
        print("正在测试 temperatur 为 {} 时 ".format(temperature))
        fineTune(fine_tuned_model, testCase,testCaseNum, testResultFile +"_" + str(temperature) + ".jsonl" ,temperature)

if __name__ == "__main__":

    openai.api_key = "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"


    run(FINE_TUNED_MODEL_supplement, vul_bug_Incorrect_calculating_order_file ,vul_bug_Incorrect_calculating_order_result, 1)


    
