import pandas as pd


df = pd.read_csv("data/chat_completions_3.csv")
print(df.head())
# pd.set_option("display.chop_threshold",10)

pd.set_option("display.max_rows", 12)
pd.set_option("display.max_columns", 12)
pd.set_option("display.width", 1000)
print(df.head())
