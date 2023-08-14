import time

import openai
import json
import random

prompt_start_0 = ""
prompt_start_1 = "You are a senior smart contract security engineer ."

prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###\n###"


FINE_TUNED_MODEL_supplement = "davinci:ft-antchainopenlab-2023-08-12-12-42-12" #4A

vul_erroneous_accounting_file = "vul_erroneous_accounting.json"
vul_fake_deposit_file = "vul_new_fake_deposit.json"
vul_ID_related_violations_file = "vul_ID-related violations.json"
vul_precision_file = "vul_precision.json"
vul_price_orcal_file = "vul_price_orcal.json"
vul_reentrancy_file = "vul_new_reentrancy.json"


vul_erroneous_accounting_result = "result/erroneous_accounting/vul_erroneous_accounting_result_4A"
vul_fake_deposit_result = "result/fake_deposit/vul_fake_deposit_result_4A"
vul_ID_related_violations_result = "result/ID_related_violations/vul_ID_related_violations_result_4A"
vul_precision_result = "result/precision/vul_precision_result_4A"
vul_price_orcal_result = "result/price_orcal/vul_price_orcal_result_4A"
vul_reentrancy_result = "result/reentrancy/vul_reentrancy_result_4A"


ben_valid_file_4A = "ben_valid_prompt.json"
ben_result_file =  "result/ben_result_4A"



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


    # 测试4A
    # 恶性样本测试
    #run(FINE_TUNED_MODEL_supplement, promspt_start_0, vul_precision_file, vul_precision_result , 5)
    #run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_price_orcal_file, vul_price_orcal_result, 5)
    #run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_erroneous_accounting_file, vul_erroneous_accounting_result, 5)
    #run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_ID_related_violations_file, vul_ID_related_violations_result, 5)
    run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_fake_deposit_file, vul_fake_deposit_result, 5)
    run(FINE_TUNED_MODEL_supplement, prompt_start_0, vul_reentrancy_file, vul_reentrancy_result, 5)


    # 良性样本测试
   # run(FINE_TUNED_MODEL_4A, prompt_start_0, ben_valid_file_4A, ben_result_file , 5)
    
