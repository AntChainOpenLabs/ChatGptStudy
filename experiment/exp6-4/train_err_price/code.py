import re

input_file = 'err_price_ben.txt'
output_file_temp = 'err_price_ben_temp.jsonl'
output_file= 'price_err_ben_ok.jsonl'

string1 = "yes,Price oracle manipulation."
string2 = "###"

string3 = "yes,Erroneous state updates."

# 正则表达式匹配模式
pattern1 = re.escape(string1) + r'([\s\S]*?)' + re.escape(string2)
pattern2 = re.escape(string3) + r'([\s\S]*?)' + re.escape(string2)

with open(input_file, 'r') as file_in, open(output_file_temp, 'w') as file_out:
    for line in file_in:
        # 在每一行中搜索匹配的内容，并替换为空字符串
        processed_line = re.sub(pattern2, 'other. ###', line)
        file_out.write(processed_line)
with open(output_file_temp, 'r') as file_in, open(output_file, 'w') as file_out:
    for line in file_in:
        # 在每一行中搜索匹配的内容，并替换为空字符串
        processed_line = re.sub(pattern1, 'yes,Price oracle manipulation. ###', line)
        file_out.write(processed_line)
