import sys

import tiktoken
import json

token_limit = 2048
file_type = ".jsonl"
# 记录check的结果
f = open("check_record.txt", 'w', encoding='utf-8')
sys.stdout = f
sys.stderr = f  # redirect std err, if necessary


def num_tokens_from_string(string: str, encoding_name: str="r50k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def read_prompt(filename):
    ok = filename + "_OK" + file_type
    no = filename + "_NO" + file_type
    okfile = []
    nofile = []
    cnt = 0
    with open(filename + ".jsonl","r",encoding="utf-8") as fp:
        lines  = fp.readlines();
        index = 1
        for line in lines:
            # 解析JSON数据
            try:
                data = json.loads(line)
                # 将数据转换为JSON字符串
                json_str = json.dumps(data)
                # 计算标记数量
                token_count = num_tokens_from_string(json_str)
                if token_count < token_limit:
                    okfile.append(data)
                else:
                    nofile.append(data)
                    cnt += 1
                    print("--------------\n{}\n{}[token num :{} ]--------------\n".format(line, index, token_count))
            except:
                print("--------------\n{}\nerror json--------------\n".format(line))
            finally:
                index += 1
    with open(ok, "w") as fok:
        json.dump(okfile,fok,indent=4)
    with open(no, "w") as fno:
        json.dump(nofile,fno,indent=4)


read_prompt("6times50+300_prepared")
