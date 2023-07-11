import json
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str="p50k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def deduplicate_prompts(input_file, output_file):
    prompt_completion_map = {}

    with open(input_file, 'r',encoding="utf-8") as f:
        for line in f:
            json_data = json.loads(line)
            prompt = json_data.get('prompt', '')
            completion = json_data.get('completion', '')

            # 去重
            # if prompt not in prompt_completion_map:
            #     prompt_completion_map[prompt] = completion

        for prompt, completion in prompt_completion_map.items():
            token = num_tokens_from_string(prompt)
            print(token)

    with open(output_file, 'w') as f:
        for prompt, completion in prompt_completion_map.items():
            token = num_tokens_from_string(prompt)
            # 去超出token限制
            # if token >= 2500  and token < 2800:
            #     print(token)
            #     json_line = json.dumps({'prompt': prompt, 'completion': completion})
            #     p.write(json_line + '\n')
            if token < 2048 :
                json_line = json.dumps({'prompt': prompt, 'completion': completion})
                f.write(json_line + '\n')

# 用法示例
input_file = 'vul_raw_all_prompt.json'
# input_file = '2048-2500.json'
output_file = 'vul_regular_all_prompt.json'

deduplicate_prompts(input_file, output_file)
