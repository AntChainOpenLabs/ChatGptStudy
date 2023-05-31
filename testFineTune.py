import openai
import json
import random
prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###"
FINE_TUNED_MODEL = "davinci:ft-antchainopenlab-2023-05-29-14-14-47"
testfilename = r"experiment\1\prompt_completion_test_bug.jsonl"
testfilename2 = r"experiment\1\prompt_completion_test_benign.jsonl"

testResult = r"experiment\1\prompt_completion_1G_result_bug_1.jsonl"


def read_testFile(file, testCaseNum):
    i = 1
    testCase = []
    with open(file,"r") as f:
        tst = random.sample(f.readlines(), testCaseNum) #随机取样本数
        for line in tst:
            line = json.loads(line)
            testCase.append(line["prompt"])
    return testCase


def fineTune(FINE_TUNED_MODEL , testCase , file):
    ans_js =  {}
    for i in range(len(testCase)):
        PROMPT = testCase[i]
        ans = []
        print("正在测试第{}个样本\n".format(i))
        for j in range(10):
            response = openai.Completion.create(
                model= FINE_TUNED_MODEL,
                prompt= PROMPT + prompt_end,
                stop=completion_end,
                temperature= 0,
                n = 10
            )
            for choice in response["choices"]:
                ans.append(choice["text"].replace("\n",""))
        ans_js[i] = ans

    with open(file,"w") as f:
        json.dump(ans_js,f,indent=4)


if __name__ == "__main__":
    testCase = read_testFile( testfilename , 10)
    fineTune(FINE_TUNED_MODEL, testCase , testResult)