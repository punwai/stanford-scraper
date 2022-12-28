from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import openai
import time

openai.api_key = "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"


# search through the reviews for a specific product
def search_courses(df, product_description, n=3, pprint=True):
    startTime = time.time()
    embedding = get_embedding(
        product_description,
        engine="text-embedding-ada-002"
    )
    df["similarities"] = df.ada_search.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(n)
        .combined.str.replace("Title: ", "")
        .str.replace("; Content:", ": ")
    )
    if pprint:
        for r in res:
            print(r[:200])
            print()
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    return res

def main():
    input_datapath = 'complete-courses-embed.csv'  # to save space, we provide a pre-filtered dataset
    df = pd.read_csv(input_datapath)
    for i in range(len(df['ada_search'])):
        lst = ((df.at[i, 'ada_search'])[1:len(df.at[i, 'ada_search'])-1]).split(",")
        lst = [float(i) for i in lst]
        df.at[i, 'ada_search'] = lst
    query = input("Enter your search: ")
    print(search_courses(df, query, 10))



main()