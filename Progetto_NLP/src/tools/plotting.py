import matplotlib.pyplot as plt
from wordcloud import WordCloud as wc
from tools import utils as u


def wordcloud(wc, df, MAX_WORDS, STOP_WORDS, title="Word Cloud of Top Words"):

    wc.generate_from_frequencies(dict(u.top_in_series(df, MAX_WORDS, STOP_WORDS)))

    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off') # Remove axes for a cleaner look
    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()
    plt.close()
    return fig
