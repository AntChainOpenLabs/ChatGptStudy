from openai import OpenAI
import os
os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
print(os.environ['http_proxy'])
print(os.environ['https_proxy'])
client = OpenAI()


if 0:
  file_obj = client.files.create(
    file=open("/home/yyq/桌面/project/chatgpt_Antchain/3_5De/name/30/price_err_ben_30.jsonl", "rb"),
    purpose="fine-tune"
  )
  print(file_obj)
  print(file_obj.id)
#file-7DbrfzYrWq6L6VIdp607sboU'

if 1:
  train_obj=client.fine_tuning.jobs.create(
      training_file="file-7DbrfzYrWq6L6VIdp607sboU", 
      model="davinci-002"
    )
  print(train_obj)
  #FineTuningJob(id='ftjob-l4xfUq2yiD6m3HWaWv9Ad3CH', created_at=1709647142, error=Error(code=None, message=None, param=None, error=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='davinci-002', object='fine_tuning.job', organization_id='org-d0E1PdrhxHIKNPdGeMqwWkpx', result_files=[], status='validating_files', trained_tokens=None, training_file='file-7DbrfzYrWq6L6VIdp607sboU', validation_file=None, user_provided_suffix=None)