import time

import openai
import json
import random

prompt_start_0 = ""
prompt_start_1 = "You are a senior smart contract security engineer ."

prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###\n###"
#davinci:ft-antchainopenlab-2023-09-05-04-08-28
#davinci:ft-antchainopenlab-2023-09-05-09-50-26
#davinci:ft-antchainopenlab-2023-09-05-14-57-20

FINE_TUNED_MODEL_supplement = 'davinci:ft-antchainopenlab-2024-01-06-12-44-32'#ID-related






vul_bug_price = "vul_price_orcal.jsonl"
vul_bug_err = "vul_erroneous_accounting.jsonl"
vul_ben = "vul_ben.jsonl"

#err
vul_bug_price_result = "result/price/bug_price"
vul_bug_err_result = "result/err/bug_err"
vul_ben_result = "result/ben/ben"




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
    testCase = read_testFile(filename, testCaseNum)
    for temperature in range(0,3):
        print("---------------------")
        print("正在测试 temperatur 为 {} 时 ".format(temperature))
        fineTune(fine_tuned_model, testCase,testCaseNum, testResultFile +"_" + str(temperature) + ".jsonl", prompt_start ,temperature)
        # time.sleep(2)
        # print("正在测试 temperatur 为 {} 时 / 加了角色描述".format(temperature))
        # fineTune(FINE_TUNED_MODEL ,testCase,testCaseNum, testResultFile +"_addRole_"  + str(temperature) + ".jsonl", prompt_start_1 ,temperature)

if __name__ == "__main__":
    # run(testfilename,testResult, 15)
    # time.sleep(5)

    openai.api_key = "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"

    
    run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_bug_price, vul_bug_price_result, 5)
    run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_bug_err, vul_bug_err_result, 5)
    run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_ben, vul_ben_result, 5)



    # 良性样本测试
   # run(FINE_TUNED_MODEL_4A, prompt_start_0, ben_valid_file_4A, ben_result_file , 5)
    
