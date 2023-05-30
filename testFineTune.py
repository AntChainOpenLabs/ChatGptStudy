import openai
import json
prompt_end = "\n\n###\n\n"
completion_start = " "
completion_end = "###"
FINE_TUNED_MODEL = "davinci:ft-antchainopenlab-2023-05-29-14-14-47"
testfilename = r"experiment\1\prompt_completion_1G_test.jsonl"
testResult = r"experiment\1\prompt_completion_1G_result2.jsonl"


def read_testFile(file, testCaseNum):
    i = 1
    testCase = []
    with open(file,"r") as f:
        for line in f.readlines():
            if i > testCaseNum : #只取适量的测试样本
                break
            line = json.loads(line)
            testCase.append(line["prompt"])
            i+=1
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
                temperature= 1,
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