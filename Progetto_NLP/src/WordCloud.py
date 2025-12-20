# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] id="RQHtyjv6z6Jv"
# # **WordCloud**
#
# Creazione di word cloud basate sulla frequenza delle parole.

# %% colab={"base_uri": "https://localhost:8080/"} id="MSEe0WohgnIN" executionInfo={"status": "ok", "timestamp": 1733396971908, "user_tz": -60, "elapsed": 17790, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}} outputId="76493578-edfd-4845-9b7f-b5faeeea68a9"
from google.colab import drive
drive.mount('/content/drive')

# %% id="8pERrMDt1Zyr"
csv_file = '/content/drive/MyDrive/Didattica/Seminario NLP/sts_gold_tweet.csv'
txt_file = '/content/drive/MyDrive/Didattica/Seminario NLP/Chapter4.txt'

df_tweets = pd.read_csv(csv_file, delimiter= ";")
file = open(txt_file, mode= "r",encoding="utf8")
ch4_raw = file.read()
file.close()

# %% colab={"base_uri": "https://localhost:8080/", "height": 206} id="6_4MVYU82MdY" outputId="77924095-e204-4e6f-a0c4-6e7169f178a4" executionInfo={"status": "ok", "timestamp": 1733397169817, "user_tz": -60, "elapsed": 239, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
df_tweets.head()

# %% colab={"base_uri": "https://localhost:8080/"} id="kz_J2gEl2SA1" outputId="dddbc9c9-3094-44fa-beeb-e8eb0cb4650e" executionInfo={"status": "ok", "timestamp": 1733397185844, "user_tz": -60, "elapsed": 202, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
df_tweets.shape

# %% id="AmeXzVRs3dpJ"
# Twitter data is quite large so for this example we will consider only 200-300 tweets.

df_tweets = df_tweets.iloc[1750:]

# %% colab={"base_uri": "https://localhost:8080/"} id="07k_4mhY3j3d" outputId="f0f12fc6-ac27-4e8f-8b6c-291c8cd3a9dc" executionInfo={"status": "ok", "timestamp": 1733397197201, "user_tz": -60, "elapsed": 196, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
df_tweets.shape

# %% id="m-jwK38M3kqv"
# Adding the 284 tweets into a list.

corpus_split = list(df_tweets['tweet'])


# %% id="Vu9ji6h2VHuj"
# Helper function which concatenates all the data into a single corpus.

def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result


# %% colab={"base_uri": "https://localhost:8080/", "height": 140} id="rLx5s_o2PP8n" outputId="bc37f058-adc0-4ce0-a05c-83155144faf0" executionInfo={"status": "ok", "timestamp": 1733397215635, "user_tz": -60, "elapsed": 366, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
corpus_twitter = concatenate_list_data(corpus_split)
corpus_twitter[:10000]

# %% colab={"base_uri": "https://localhost:8080/", "height": 1000} id="sNo6TT1FS9qc" outputId="a0e314b4-ea0d-49f1-aa54-54ccf350fd96" executionInfo={"status": "ok", "timestamp": 1733397236045, "user_tz": -60, "elapsed": 5676, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
# load text.
# Split into words by white space.

ch4_raw = ch4_raw.split()
corpus_twitter = corpus_twitter.split()

# Remove punctuation from each word.

import string
table = str.maketrans('', '', string.punctuation)
stripped_ch4 = [w.translate(table) for w in ch4_raw]
stripped_twitter = [w.translate(table) for w in corpus_twitter]

# Detokenizing all the words

from nltk.tokenize.treebank import TreebankWordDetokenizer
TreebankWordDetokenizer().detokenize(stripped_ch4)
TreebankWordDetokenizer().detokenize(stripped_twitter)


# %% id="oDl427bxBcLP"
# Appending all the data in the list to a string.

string_ch4=' '
string_twitter=' '
string_ch4 = string_ch4.join(stripped_ch4)
string_twitter = string_twitter.join(stripped_twitter)

# %% colab={"base_uri": "https://localhost:8080/"} id="SJbmmdP73uCY" outputId="d25c5406-21ce-4940-ac27-c32cd43cc9f1" executionInfo={"status": "ok", "timestamp": 1733397488427, "user_tz": -60, "elapsed": 661, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
# Importing necessary NLTK packages.

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

# Setting stopwords to english.

stop_words = set(stopwords.words('english'))

# Tokenizing the string
word_tokens_ch4 = word_tokenize(string_ch4, language='english', preserve_line=True)
word_tokens_twitter = word_tokenize(string_twitter, language='english', preserve_line=True)

# %% id="NSr_Ar8ZVpXv"
# Removing all the stop words.

filtered_corpus_ch4 = [w for w in word_tokens_ch4 if not w in stop_words]
filtered_corpus_twitter = [w for w in word_tokens_twitter if not w in stop_words]

# %% id="Ls2S6u72Io-F"
# Calculating the frequency of each word.

wordfreq_ch4=[filtered_corpus_ch4.count(p) for p in filtered_corpus_ch4]
result_ch4 = dict(zip(filtered_corpus_ch4,wordfreq_ch4))
wordfreq_twitter=[filtered_corpus_twitter.count(p) for p in filtered_corpus_twitter]
result_twitter = dict(zip(filtered_corpus_twitter,wordfreq_twitter))

# %% colab={"base_uri": "https://localhost:8080/", "height": 1000} id="hpNuVZoNWD2Q" outputId="0111f14b-86e6-4ad4-c0f6-142fc45cb44b" executionInfo={"status": "ok", "timestamp": 1733397514933, "user_tz": -60, "elapsed": 8132, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
# Finally lets plot the wordcloud.

# !pip install wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(width = 1200, height = 1200, background_color="white",min_font_size =10).generate_from_frequencies(result_twitter)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout()

plt.show()

# %% colab={"base_uri": "https://localhost:8080/", "height": 1000} id="DHoJamr9zOLE" outputId="faa26fcf-25cf-4bc5-d077-1d5f1bdbf714" executionInfo={"status": "ok", "timestamp": 1733397537339, "user_tz": -60, "elapsed": 6320, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
from wordcloud import WordCloud
import matplotlib.pyplot as plt


wordcloud = WordCloud(width = 1200, height = 1200, min_font_size =10).generate_from_frequencies(result_ch4)

plt.figure(figsize = (10, 10), facecolor = None)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()

plt.show()

# %% colab={"base_uri": "https://localhost:8080/", "height": 1000} id="IoD_HmMmtmmp" outputId="6686b0ee-c659-4150-9535-c44f64ca48f0" executionInfo={"status": "ok", "timestamp": 1733397558071, "user_tz": -60, "elapsed": 8948, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
from wordcloud import WordCloud
import matplotlib.pyplot as plt


wordcloud = WordCloud(width = 1200, height = 1200,background_color="white", min_font_size =10).generate_from_frequencies(result_ch4)

plt.figure(figsize = (10, 10), facecolor = None)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()

plt.show()

# %% [markdown] id="sbvGX9IgSreV"
# ### Custom Shaped Word Clouds
# We need to create a mask for our custom image. We use the python [pillow](https://pillow.readthedocs.io/en/stable/) library for this.

# %% id="CTW9CxWhF1Hf"
# Custom word cloud.

from PIL import Image
import numpy as np
import urllib
import requests

def generate_wordcloud(words, mask):
    wordcloud = WordCloud(width = 1200, height = 1200,background_color="white", min_font_size =10,mask=mask).generate_from_frequencies(words)
    plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='blue')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()


# %% [markdown] id="eSTrHyA0DKLK"
# #### Recreate the same word clouds in various shapes

# %% colab={"base_uri": "https://localhost:8080/", "height": 836} id="OfQZL2db83KJ" outputId="6a7c3a9f-189c-40ed-8c3c-0db6389ea0cb" executionInfo={"status": "ok", "timestamp": 1733397587085, "user_tz": -60, "elapsed": 2119, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
mask_house = np.array(Image.open(requests.get('http://www.clker.com/cliparts/O/i/x/Y/q/P/yellow-house-hi.png', stream=True).raw))
generate_wordcloud(result_ch4, mask_house)

# %% colab={"base_uri": "https://localhost:8080/", "height": 836} id="bX8p8QgZ97GX" outputId="2e944871-1dac-4710-f226-d7f43756b44c" executionInfo={"status": "ok", "timestamp": 1733397594895, "user_tz": -60, "elapsed": 4043, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
mask_circle = np.array(Image.open(requests.get('https://res.cloudinary.com/dk-find-out/image/upload/q_80,w_960,f_auto/DCTM_Penguin_UK_DK_AL526630_wkmzns.jpg', stream=True).raw))
generate_wordcloud(result_ch4, mask_circle)

# %% colab={"base_uri": "https://localhost:8080/", "height": 836} id="p7hMmnUH-sFq" outputId="078adb90-f719-458a-da4c-e6fe7ff07c86" executionInfo={"status": "ok", "timestamp": 1733397617814, "user_tz": -60, "elapsed": 4590, "user": {"displayName": "Chris Bura", "userId": "09629359015337873880"}}
mask_p = np.array(Image.open(requests.get('https://previews.123rf.com/images/frescomovie/frescomovie1201/frescomovie120100042/11918955-letter-p-made-from-red-blood-cells-isolated-on-a-white-.jpg', stream=True).raw))
generate_wordcloud(result_ch4, mask_p)


# %% colab={"base_uri": "https://localhost:8080/", "height": 856} id="j4PlZln91AcG" outputId="5ab2aa40-8ea8-4f60-ea81-de550be82e92"
mask_hea = np.array(Image.open(requests.get('https://www.shutterstock.com/image-vector/heart-love-romance-valentines-day-600nw-2516011563.jpg', stream=True).raw))
generate_wordcloud(result_ch4, mask_p)

# %% id="ABkdcBZc1KqU"
