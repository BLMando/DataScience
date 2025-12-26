# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: src
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# %% [markdown]
# The three nltk.download() lines ensure that necessary datasets like the tokenizer models (punkt) and stopword list are downloaded and available

# %%
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")

# %%
df = pd.read_csv("./data/Resume.csv")
df.dropna(inplace=True)

print(df.head())

# %%
type(df.sample(1)['Resume_str'].values[0])

# %%
tts = train_test_split(df, test_size=0.2, random_state=42)

# %%
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower
    tokens = word_tokenize(str(text))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)

df['clean_text'] = df['Resume_str'].apply(preprocess)
print(df[['Resume_str', 'clean_text']].head())

# %%
