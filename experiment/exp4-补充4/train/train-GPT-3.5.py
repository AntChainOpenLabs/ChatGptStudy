
import openai

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
        openai.FineTuningJob.create(training_file="file-BPm21guaW3YWcGxiuZiQURSL", model="gpt-3.5-turbo")
    )


def Retrieve(job):
    # Retrieve the state of a fine-tune
    print(openai.FineTuningJob.retrieve(job))
    print("#####################################")
    print(
        # List up to 10 events from a fine-tuning job
        openai.FineTuningJob.list_events(id=job, limit=10)
    )

if __name__ == "__main__":
    openai.api_key = "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"

    Retrieve("ftjob-Z981z0up1HUYWICVWX9w8FVf")




