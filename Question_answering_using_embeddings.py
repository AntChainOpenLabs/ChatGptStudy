#!/usr/bin/env python
# coding: utf-8


# imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = "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"



# ## 2. Search
# 
# Now we'll define a search function that:
# - Takes a user query and a dataframe with text & embedding columns
# - Embeds the user query with the OpenAI API
# - Uses distance between query embedding and text embeddings to rank the texts
# - Returns two lists:
#     - The top N texts, ranked by relevance
#     - Their corresponding relevance scores

# In[7]:


# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


# ## 3. Ask
# 
# With the search function above, we can now automatically retrieve relevant knowledge and insert it into messages to GPT.
# 
# Below, we define a function `ask` that:
# - Takes a user query
# - Searches for text relevant to the query
# - Stuffs that text into a mesage for GPT
# - Sends the message to GPT
# - Returns GPT's answer

# In[9]:


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    # introduction = 'Use the below articles on the 2022 Winter Olympics to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
    introduction = ''
    question = f"\n\nQuestion: {query}"
    messages = []
    message = ""
    index = 0
    while index < len(strings):
        while index < len(strings):
            string = strings[index]
            next_article = f'\n\narticle section:\n"""\n{string}\n"""'
            if (
                    num_tokens(message + next_article + question, model=model)
                    > token_budget
            ):
                if message != "":
                    messages += [message + question]
                    message = ""
                    break
                else:
                    # 如果message 为空则证明单个article + question超过了token的数量，跳过
                    index += 1
                    print("单个article + question超过了token的数量 : \n{} \n".format(next_article))
            else:
                message += next_article
                index += 1
                # 处理结尾
                if index == len(strings):
                    messages += [message + question]



    return messages


def ask(
    query: str,
    df: pd.DataFrame,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    response_message = ""
    for msg in message:
        messages = [
            {"role": "system", "content": "You answer questions about the smart contract vulnerability report."},
            {"role": "user", "content": msg},
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0
        )
        response_message += response["choices"][0]["message"]["content"]  + "\n\n"
    return response_message


def get_section_json(embeddings_path):
    df = pd.read_csv(embeddings_path)

    df['embedding'] = df['embedding'].apply(ast.literal_eval)

    # answer = ask(
    #     'Point out the vulnerability type, vulnerability location, repair method, and vulnerability information mentioned in the above text. Output if present, empty string if absent. Use the json format required as follows: {"Vulnerability Type": "", "Vulnerability Location": "", "Repair Method": " ", "Vulnerability Information": "" }',
    #     df,print_message=True)
    answer  = ask('Point out the vulnerability type, vulnerability location, repair method, and vulnerability information mentioned in the above text. Output if present, empty string if absent. Use the json format required as follows and escape all values in json : {"Vulnerability Type": "", "Vulnerability Location": "", "Repair Method": " ", "Vulnerability Information": ""}.For example text:[H-100] fake notification .fake notification occurs in the erc20 contract. If the erc20 contract only releases standard events without changing contract variables, it is considered that a fake notification has occurred. The way to fix it is to only release the standard event when the contract variable is changed, and the value represented by the event is equal to the value of the variable change",json: {"Vulnerability Type": "fake notification", "Vulnerability Location": "function () external payable {\n emit Transfer(msg.sender, owner, msg.value);\n }", "Repair Method": "When releasing a standard event, check whether the account balance has been modified accordingly", "Vulnerability Information": "fake notification occurs in the erc20 contract. If the erc20 contract only releases standard events without changing contract variables, it is considered that a fake notification has occurred."}',df,print_message=False)
    # print(answer)
    return answer


if __name__ == "__main__":


    # embeddings_path = "./data/pdf_test.csv"
    embeddings_path =  r"json/code4rena2/2021-08-gravitybridge-findings.csv"
    df = pd.read_csv(embeddings_path)

    # In[5]:

    # convert embeddings from CSV str type back to list type
    df['embedding'] = df['embedding'].apply(ast.literal_eval)

    # In[6]:

    # the dataframe has two columns: "text" and "embedding"

    print(ask(
        'Point out the vulnerability type, vulnerability location, repair method, and vulnerability information mentioned in the above text. Output if present, empty string if absent. Use the json format required as follows: {"Vulnerability Type": "", "Vulnerability Location": "", "Repair Method": " ", "Vulnerability Information": "" }',df))