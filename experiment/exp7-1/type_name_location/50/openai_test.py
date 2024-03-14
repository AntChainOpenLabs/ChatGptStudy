from openai import OpenAI
import os
os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
print(os.environ['http_proxy'])
print(os.environ['https_proxy'])
client = OpenAI()



file_obj = client.files.create(
  file=open("/home/yyq/桌面/project/chatgpt_Antchain/3_5De/type_name_location/50/err_price_ben.jsonl", "rb"),
  purpose="fine-tune"
)

print(file_obj.id)



train_obj=client.fine_tuning.jobs.create(
    training_file=file_obj.id, 
    model="davinci-002"
  )
print(train_obj)
#file-BEFfp8rdLCqi56UZ97hKRQHt
#FineTuningJob(id='ftjob-D9f8DMyTwqmn6VZzMg3obvqd', created_at=1709712663, error=Error(code=None, message=None, param=None, error=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='davinci-002', object='fine_tuning.job', organization_id='org-d0E1PdrhxHIKNPdGeMqwWkpx', result_files=[], status='validating_files', trained_tokens=None, training_file='file-BEFfp8rdLCqi56UZ97hKRQHt', validation_file=None, user_provided_suffix=None)