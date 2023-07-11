import json

def process_json_file(input_file, output_file):
    with open(input_file, 'r',encoding="utf-8") as f:
        data = f.readlines()

    processed_data = []
    for line in data:
        json_data = json.loads(line)
        prompt = json_data.get('prompt', '')
        completion = json_data.get('completion', '')

        if not prompt.endswith('\n\n###\n\n'):
            prompt += '\n\n###\n\n'
        if not completion.endswith('yes###\n###'):
            completion = 'yes###\n###'

        processed_data.append({'prompt': prompt, 'completion': completion})

    with open(output_file, 'w') as f:
        for item in processed_data:
            json_line = json.dumps(item)
            f.write(json_line + '\n')

# 用法示例
input_file = '300+0.json'
output_file = '300+0_stan.json'
process_json_file(input_file, output_file)
