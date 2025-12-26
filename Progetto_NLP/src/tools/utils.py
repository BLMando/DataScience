import re
import string
import pandas as pd
from collections import Counter

def preprocess_text(text: pd.DataFrame):
    s = str(text)
    tokens = s.split()
    starti = 0
    for i, token in enumerate(tokens):
        # Rimozione delle parole iniziali tutte maiuscole
        # nel dataset sono presenti testi che hanno un inizio composto
        # da sole lettere maiuscole che rischiano di inserire bias in quanto
        # già determinano la cetagoria del testo
        # sarebbe come barare tenerle, perciò le rimuoviamo
        if not token.isupper():
            starti = i
            break

    t = tokens[starti:]
    t = " ".join([ta.lower() for ta in t])                   # mettiamo tutto piccolo
    t = t.translate(str.maketrans('', '', string.punctuation))  # rimuoviamo segni di punteggiatura
    t = re.sub(r'\s+', ' ', t).strip()                          # Rimuove spazi extra
    return t

def unique_text(text: pd.DataFrame):
    words = set()
    for t in text:
        for w in str(t).split():
            words.add(w)
    return words


def top_in_series(series, max_words, stop_words: str):
    corpus = ' '.join(series.dropna().astype(str))
    tokens = re.findall(r'\b[a-z]+\b', corpus)
    tokens = [t for t in tokens if t not in stop_words]
    return Counter(tokens).most_common(max_words)