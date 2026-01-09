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
    # Remove label
    s = str(text)
    tokens = s.split()
    i = 0

    while i < len(tokens):
        letters = re.sub(r'[^A-Za-z]', '', tokens[i])
        if letters and letters.isupper():
            i += 1
            continue
        break
    
    text = ' '.join(tokens[i:]) if i < len(tokens) else s

    #  Lowercase
    text = str(text).lower()

    #  Domain-specific replacements
    replacements = {
        "c++": "cplusplus",
        "c#": "csharp",
        "f#": "fsharp",
        "node.js": "nodejs",
        "react.js": "reactjs",
        "vue.js": "vuejs",
        "three.js": "threejs",
        "socket.io": "socketio",
        "objective-c": "objectivec",
        "objective c": "objectivec",
        ".net": "dotnet",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".scss": "sass",
        ".md": "markdown",
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".rb": "ruby",
        ".rs": "rust",
        ".go": "golang",
        ".sql": "sql",
        ".php": "php",
        ".html": "html",
        ".css": "css",
        ".sh": "bash",
        ".zsh": "zsh",
        ".mk": "make",
        ".json": "json",
        ".xml": "xml",
        ".csv": "csv"
    } 

    for old, new in replacements.items():
        text = text.replace(old, new)

    #  Replace punctuation with space
    text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
    
    #  Tokenization and POS-aware Lemmatization
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
