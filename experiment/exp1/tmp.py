import json

def copy_json_fields(input_file, output_file):
    with open(input_file, 'r',encoding="utf-8") as f:
        data = json.load(f)

    with open(output_file, 'w') as f:
        for item in data:
            prompt = item.get('prompt', '')
            completion = item.get('completion', '')
            json_line = json.dumps({'prompt': prompt, 'completion': completion})
            f.write(json_line + '\n')

# 用法示例
input_file = 'input.json'
output_file = 'output.json'
copy_json_fields(input_file, output_file)
