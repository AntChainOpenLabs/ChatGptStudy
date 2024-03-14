from openai import OpenAI
import os
os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
print(os.environ['http_proxy'])
print(os.environ['https_proxy'])
client = OpenAI()


if 0:
  file_obj = client.files.create(
    file=open("/home/yyq/桌面/project/chatgpt_Antchain/3_5/train_err_price_3_5/price_err_ben_35.jsonl", "rb"),
    purpose="fine-tune"
  )
  print(file_obj)
 
#id='file-A1YegSudXvjmMRKZ4aWaRcsA'

if 1:
  train_obj=client.fine_tuning.jobs.create(
      training_file="file-A1YegSudXvjmMRKZ4aWaRcsA", 
      model="gpt-3.5-turbo"
    )
  print(train_obj)