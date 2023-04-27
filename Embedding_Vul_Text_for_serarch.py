#!/usr/bin/env python
# coding: utf-8


# import mwclient  # for downloading example Wikipedia articles
# import mwparserfromhell  # for splitting Wikipedia articles into sections
import openai  # for generating embeddings
import pandas as pd  # for DataFrames to store article sections and embeddings
import re  # for cutting <ref> links out of Wikipedia articles
import tiktoken  # for counting tokens

openai.api_key = "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"

# clean text
def clean_section(section: tuple[list[str], str]) -> tuple[list[str], str]:
    """
    Return a cleaned up section with:
        - <ref>xyz</ref> patterns removed
        - leading/trailing whitespace removed
    """
    titles, text = section
    text = re.sub(r"<ref.*?</ref>", "", text)
    text = text.strip()
    return (titles, text)


# filter out short/blank sections
def keep_section(section: tuple[list[str], str]) -> bool:
    """Return True if the section should be kept, False otherwise."""
    titles, text = section
    if len(text) < 16:
        return False
    else:
        return True


GPT_MODEL = "gpt-3.5-turbo"  # only matters insofar as it selects which tokenizer to use


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def halved_by_delimiter(string: str, delimiter: str = "\n") -> list[str, str]:
    """Split a string in two, on a delimiter, trying to balance tokens on each side."""
    chunks = string.split(delimiter)
    if len(chunks) == 1:
        return [string, ""]  # no delimiter found
    elif len(chunks) == 2:
        return chunks  # no need to search for halfway point
    else:
        total_tokens = num_tokens(string)
        halfway = total_tokens // 2
        best_diff = halfway
        for i, chunk in enumerate(chunks):
            left = delimiter.join(chunks[: i + 1])
            left_tokens = num_tokens(left)
            diff = abs(halfway - left_tokens)
            if diff >= best_diff:
                break
            else:
                best_diff = diff
        left = delimiter.join(chunks[:i])
        right = delimiter.join(chunks[i:])
        return [left, right]


def truncated_string(
    string: str,
    model: str,
    max_tokens: int,
    print_warning: bool = True,
) -> str:
    """Truncate a string to a maximum number of tokens."""
    encoding = tiktoken.encoding_for_model(model)
    encoded_string = encoding.encode(string)
    truncated_string = encoding.decode(encoded_string[:max_tokens])
    if print_warning and len(encoded_string) > max_tokens:
        print(f"Warning: Truncated string from {len(encoded_string)} tokens to {max_tokens} tokens.")
    return truncated_string


def split_strings_from_subsection(
    subsection: tuple[list[str], str],
    max_tokens: int = 1000,
    model: str = GPT_MODEL,
    max_recursion: int = 5,
) -> list[str]:
    """
    Split a subsection into a list of subsections, each with no more than max_tokens.
    Each subsection is a tuple of parent titles [H1, H2, ...] and text (str).
    """
    titles, text = subsection
    string = "\n\n".join(titles + [text])
    num_tokens_in_string = num_tokens(string)
    # if length is fine, return string
    if num_tokens_in_string <= max_tokens:
        return [string]
    # if recursion hasn't found a split after X iterations, just truncate
    elif max_recursion == 0:
        return [truncated_string(string, model=model, max_tokens=max_tokens)]
    # otherwise, split in half and recurse
    else:
        titles, text = subsection
        for delimiter in ["\n\n", "\n", ". "]:
            left, right = halved_by_delimiter(text, delimiter=delimiter)
            if left == "" or right == "":
                # if either half is empty, retry with a more fine-grained delimiter
                continue
            else:
                # recurse on each half
                results = []
                for half in [left, right]:
                    half_subsection = (titles, half)
                    half_strings = split_strings_from_subsection(
                        half_subsection,
                        max_tokens=max_tokens,
                        model=model,
                        max_recursion=max_recursion - 1,
                    )
                    results.extend(half_strings)
                return results
    # otherwise no split was found, so just truncate (should be very rare)
    return [truncated_string(string, model=model, max_tokens=max_tokens)]

# 将section生成csv文件
def split_sections(sections, SAVE_PATH):
    MAX_TOKENS = 1600
    pdf_strings = []
    for section in sections:
        pdf_strings.extend(split_strings_from_subsection(section, max_tokens=MAX_TOKENS))

    # print(f"{len(sections)} pdf sections split into {len(pdf_strings)} strings.")

    # print example data
    # print(pdf_strings[1])

    EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
    BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

    embeddings = []
    for batch_start in range(0, len(pdf_strings), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = pdf_strings[batch_start:batch_end]
        # print(f"Batch {batch_start} to {batch_end - 1}")
        response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
        for i, be in enumerate(response["data"]):
            assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)

    df = pd.DataFrame({"text": pdf_strings, "embedding": embeddings})

    df.to_csv(SAVE_PATH, index=False)

if __name__ == "__main__":
    # split sections into chunks

    pdf_sections = [
    (["Medium Severity","[M-01]"],"If a finalAmountMin is chosen that does not closely reflect the received amount one would get at the market rate (even with just 1% slippage), this could lead to the trade being frontrun and to less tokens than with a tighter slippage amount.Balancer and Curve modules don't have any slippage protection at all which makes it easy for attackers to profit from such an attack. The min amount returned is hardcoded to 1 for both protocols. The Sushiswap/Uniswap modules are vulnerable as well, depending on the calldata that is defined by the victim trader."),
    (["High Severity","[H-01]","Front Running/Sandwich Attacks"],"Incorrectly encoded arguments to executeTrades() can allow tokens to be stolen. This finding combines a couple weaknesses into one attack. The first weakness is a lack of validation on arguments to executeTrades, the second is that a pre-existing fromToken balance can be used in a trade:\n\n1. Alice wants to convert 1000 DAI to WETH. She calls executeTrades(DAI, WETH, 1000, [], 0, alice).\n\n2. Since trades is an empty array, and finalAmountMin is 0, the result is that 100 DAI are transferred to the Slingshot contract.\n\n3. Eve (a miner or other 'front runner') may observe this, and immediately call executeTrades(DAI, WETH, 0, [\{TradeData\}], 0, eve).\n\n4. With a correctly formatted array of TradeData, Eve will receive the proceeds of converting Alice's 1000 DAI to WETH.\n\nThis issue is essentially identical to the one described in Ethereum is a Dark Forest, where locked tokens are available to anyone, and thus recovery is susceptible to front running. It also provides an unauthorized alternative to rescueTokens(), however it is still a useful function to have, as it provides a method to recover the tokens without allowing a front runner to simulate and replay it."),
    (["Medium Severity","[M-02]","Front Running/Sandwich Attacks"],"If tokens are accidently sent to Slingshot, arbitrary trades can be executed and those funds can be stolen by anyone. This vulnerability impacts the rescueToken functionality and any funds trapped in Slingshot’s contract. Tokens and/or Eth have a higher likelihood of becoming trapped in Slingshot if finalAmountMin is not utilized properly. Recommend validating parameters in the calldata passed to modules and ensuring the fromToken and amount parameter from executeTrades is equivalent to the token being swapped and amount passed to swap(). Additionally, approval values can be limited to value being traded and cleared after trades are executed."),
    (["Medium Severity","[M-03]","Infinite Approval abused by malicious admin"],"Current Slingshot contracts assume a rapid development environment so they use a proxy pattern with a trusted admin role. We do not expect any malicious behavior from admin, however we agree that in the current setup admin potentially would be able to use unlimited approvals to steal user’s funds. We consider this medium severity."),
    (["Medium Severity","[M-04]","Stuck tokens can be stolen"],"Any tokens in the Slingshot contract can be stolen by creating a fake token and a Uniswap pair for the stuck token and this fake token. Consider 10 WETH being stuck in the Slingshot contract. One can create a fake ERC20 token contract FAKE and a WETH <> FAKE Uniswap pair. The attacker provides a tiny amount of initial WETH liquidity (for example, 1 gwei) and some amount of FAKE tokens. The attacker then executes executeTrades action such that the Slingshot contract uses its Uniswap module to trade the 10 WETH into this pair."),
    (["Medium Severity","[M-05]","Admin role lockout"],"The initializeAdmin() function in Adminable.sol sets/updates admin role address in one-step. If an incorrect address (zero address or other) is mistakenly used then future administrative access or even recovering from this mistake is prevented because all onlyAdmin modifier functions (including postUpgrade() with onlyAdminIfInitialized, which ends up calling initializeAdmin()) require msg.sender to be the incorrectly used admin address (for which private keys may not be available to sign transactions). In such a case, contracts would have to be redeployed. Suggest using a two-step process where the new admin address first claims ownership in one transaction and a second transaction from the new admin address takes ownership."),
    ]


    MAX_TOKENS = 1600
    pdf_strings = []
    for section in pdf_sections:
        pdf_strings.extend(split_strings_from_subsection(section, max_tokens=MAX_TOKENS))

    print(f"{len(pdf_sections)} pdf sections split into {len(pdf_strings)} strings.")



    # print example data
    print(pdf_strings[1])


    # ## 3. Embed document chunks
    #
    # Now that we've split our library into shorter self-contained strings, we can compute embeddings for each.
    #
    # (For large embedding jobs, use a script like [api_request_parallel_processor.py](api_request_parallel_processor.py) to parallelize requests while throttling to stay under rate limits.)

    # In[12]:


    # calculate embeddings
    EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
    BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request


    embeddings = []
    for batch_start in range(0, len(pdf_strings), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = pdf_strings[batch_start:batch_end]
        print(f"Batch {batch_start} to {batch_end-1}")
        response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
        for i, be in enumerate(response["data"]):
            assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)

    df = pd.DataFrame({"text": pdf_strings, "embedding": embeddings})


    # ## 4. Store document chunks and embeddings
    #
    # Because this example only uses a few thousand strings, we'll store them in a CSV file.
    #
    # (For larger datasets, use a vector database, which will be more performant.)


    # save document chunks and embeddings

    SAVE_PATH = "./data/pdf_test.csv"

    df.to_csv(SAVE_PATH, index=False)

