
import openai


# s6_1_file = "file-BPm21guaW3YWcGxiuZiQURSL"
# s6_1_2_file = "file-1FmfKfPbT3EXASuruS9QeSx9" # 删除解释性语言的
# s6_1_2_2_file = "file-Q46Tihzpmsk3iT6f7Zvh9g3j" # 删除注释+提示
s6_1_2_davinci_file = "file-QEITlorURto5m0qOIjj3Lypk"

# s6_1_job = "ftjob-Z981z0up1HUYWICVWX9w8FVf"
# s6_1_2_job = "ftjob-Hf9vem4gpm4aPmXh0ffvY5P2"
# s6_1_2_2_job = "ftjob-lIjtxl9n1woqdU3whWqpYzpB"
s6_1_2_davinci_job = "ftjob-0nsLNlB8ZH8RBlo81UTd30IS"

def uploadFile(filename):
    # 上传文件
    # filename = "train/gpt3.5/train_chat_Incorrect_calculating_order.jsonl"
    print(
        openai.File.create(
            file=open(filename, "rb"),
            purpose='fine-tune'
        )
    )

def trainGpt3_5(training_file):
    # 创建gpt-3.5-turbo微调模型
    print(
        openai.FineTuningJob.create(training_file=training_file, model="gpt-3.5-turbo")
    )


def Retrieve(job):
    # Retrieve the state of a fine-tune
    print(openai.FineTuningJob.retrieve(job))
    print("#####################################")
    print(
        # List up to 10 events from a fine-tuning job
        openai.FineTuningJob.list_events(id=job, limit=30)
    )

if __name__ == "__main__":
    openai.api_key = "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"

    # Retrieve("") # s6-1

    # uploadFile("gpt3.5/train_chat_Incorrect_calculating_order_delete_explation_2.jsonl")
    # trainGpt3_5(s6_1_2_2_file)
    # #
    # Retrieve(s6_1_2_2_job)

    # uploadFile("davinci/train_prompt_Incorrect_calculating_order_delete_explation_2_prepared.jsonl")
    # print(
    #     openai.FineTuningJob.create(training_file=s6_1_2_davinci_file, model="davinci-002")
    # )
    Retrieve(s6_1_2_davinci_job)



