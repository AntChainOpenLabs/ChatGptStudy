import time

import openai
import json
import random

prompt_start_0 = ""
prompt_start_1 = "You are a senior smart contract security engineer ."

prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###\n###"


s6_1_delete_explation_davinci_002 = "ft:davinci-002:antchainopenlab::8G9aF2kS"



vul_bug_Incorrect_calculating_order_delete_explation_file = "s6-1-delete-explation-2/vul_bug_Incorrect_calculating_order.json"
vul_ben_Incorrect_calculating_order_delete_explation_file = "s6-1-delete-explation-2/vul_ben_Incorrect_calculating_order.json"


vul_ben_Incorrect_calculating_order_delete_explation_result = "result/s6-1-delete-explation-2/davinci-002/ben_Incorrect_calculating_order/vul_ben_Incorrect_calculating_order_result"
vul_bug_Incorrect_calculating_order_delete_explation_result = "result/s6-1-delete-explation-2/davinci-002/bug_Incorrect_calculating_order/vul_bug_Incorrect_calculating_order_result"


def read_testFile(file):
    testCase = []
    with open(file,"r",encoding="utf-8") as f:
        tst = json.load(f)
        for item in tst:
            testCase.append(item["Code"])
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
        # 问几次就是几
        for j in range(1):
            try:
                response = openai.Completion.create(
                    model= FINE_TUNED_MODEL,
                    prompt= prompt_start + PROMPT,
                    stop=completion_end,
                    temperature= temperature,
                    # 问一次生成几个completion
                    n = 5
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
def run(fine_tuned_model, prompt_start, filename, testResultFile, testCaseNum):
    testCase = read_testFile(filename)
    for temperature in range(0,3):
        print("---------------------")
        print("正在测试 temperatur 为 {} 时 ".format(temperature))
        fineTune(fine_tuned_model, testCase,testCaseNum, testResultFile +"_" + str(temperature) + ".jsonl", prompt_start ,temperature)

if __name__ == "__main__":

    openai.api_key = "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"


    # run(s6_1_delete_explation_davinci_002, prompt_start_0, vul_bug_Incorrect_calculating_order_delete_explation_file, vul_bug_Incorrect_calculating_order_delete_explation_result, 13)

    run(s6_1_delete_explation_davinci_002,prompt_start_0,vul_ben_Incorrect_calculating_order_delete_explation_file,vul_ben_Incorrect_calculating_order_delete_explation_result,10)