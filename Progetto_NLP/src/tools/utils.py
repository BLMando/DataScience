import re
import string
import pandas as pd
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download necessary NLTK resources
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    """Map NLTK POS tag to WordNet POS tag."""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def preprocess_text(text):
    """
    Robust text preprocessing for Resume classification.
    - Lowercase
    - Preserve technical keywords (C++, C#, .NET)
    - Replace punctuation with spaces
    - POS-aware Lemmatization
    """
    # 1. Lowercase
    text = str(text).lower()
    
    # 2. Domain-specific replacements
    text = text.replace("c++", "cplusplus")
    text = text.replace("c#", "csharp")
    text = text.replace(".net", "dotnet")
    
    # 3. Replace punctuation with space
    text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
    
    # 4. Tokenization and POS-aware Lemmatization
    tokens = text.split()
    if not tokens:
        return ""
        
    tagged = nltk.pos_tag(tokens)
    lemmatized_tokens = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag)) 
        for word, tag in tagged
    ]
    
    return ' '.join(lemmatized_tokens)

def unique_text(text: pd.DataFrame):
    words = set()
    for t in text:
        for w in str(t).split():
            words.add(w)
    return words

def top_in_series(series, max_words, stop_words):
    corpus = ' '.join(series.dropna().astype(str))
    tokens = re.findall(r'\b[a-z]+\b', corpus)
    tokens = [t for t in tokens if t not in stop_words]
    return Counter(tokens).most_common(max_words)
