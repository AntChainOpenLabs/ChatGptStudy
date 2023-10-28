# datasets

s6-1 : incorrect-calculating-order

s6-1-delete-explation : incorrect-calculating-order数据中合约删除掉了对应的漏洞位置解释语句


# code

check-chat-dataset.py : 检测数据是否符合gpt3.5数据输入规范

train-GPT-3.5.py： 训练gpt3.5模型
- 需要先uploadFile上传数据后获取文件ID
- 再将trainGpt3_5传入文件ID执行训练，获取jobID
- Retrieve获取运行状态，若执行成功，会生成对应的模型iD，例如
```ft:gpt-3.5-turbo-0613:antchainopenlab::8BgMiDB9```

testFineTuneChat.py: 测试模型效果，注意测试文件格式为标准格式