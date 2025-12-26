# %% [markdown]
# # Pipeline di Classificazione Curriculum Vitae (Resume)
#
# Questo notebook implementa una pipeline di Machine Learning per classificare i CV in categorie.
#
# **Step:**
# 1. Caricamento e Pulizia Dati
# 2. Split del Dataset (Train / Validation / Test)
# 3. Feature Extraction (TF-IDF)
# 4. Addestramento Modello (Linear SVM)
# 5. Valutazione
# 6. Inferenza

# %%
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import seaborn as sns
import string
from wordcloud import WordCloud

# %% [markdown]
# ## 1. Caricamento e Preprocessing dei Dati

# %%
df = pd.read_csv('data/Resume.csv')

print(f"Dataset caricato con successo: {df.shape[0]} righe, {df.shape[1]} colonne")
def clean_text(text):
    s = str(text)
    tokens = s.split()
    i = 0

    # Rimozione delle parole iniziali tutte maiuscole
    while i < len(tokens):
        letters = re.sub(r'[^A-Za-z]', '', tokens[i])
        if letters and letters.isupper():
            i += 1
            continue
        break
    trimmed = ' '.join(tokens[i:]) if i < len(tokens) else s

    trimmed = trimmed.lower()
    trimmed = trimmed.translate(str.maketrans('', '', string.punctuation))
    trimmed = re.sub(r'\s+', ' ', trimmed).strip()  # Rimuove spazi extra
    return trimmed

df['cleaned_resume'] = df['Resume_str'].apply(clean_text)

# Visualizzazione delle classi
print("\nDistribuzione delle Categorie:")
print(df['Category'].value_counts().head())

# %% [markdown]
#

# %% [markdown]
# # Wordcloud

# %%
MAX_WORDS = 500
def top_words_from_series(series, n=MAX_WORDS):
    corpus = ' '.join(series.dropna().astype(str))
    tokens = re.findall(r'\b[a-z]+\b', corpus)
    tokens = [t for t in tokens if t not in ENGLISH_STOP_WORDS]
    return Counter(tokens).most_common(n)

wc = WordCloud(
    width=800, 
    height=700, 
    background_color='white',
    max_words=MAX_WORDS,
    contour_width=0,
    colormap='viridis'  # 'viridis', 'plasma', or 'inferno' work well for data
)

wc.generate_from_frequencies(dict(top_words_from_series(df['cleaned_resume'], n=MAX_WORDS)))

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off') # Remove axes for a cleaner look
plt.title("Word Cloud of Top Words", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("data/wordcloud/wordcloud_overall.png", dpi=300)
plt.close()

for category in df['Category'].unique():
    category_df = df[df['Category'] == category]
    wc.generate_from_frequencies(dict(top_words_from_series(category_df['cleaned_resume'], n=100)))
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off') # Remove axes for a cleaner look
    plt.title(f"Word Cloud for Category: {category}", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(f"data/wordcloud/wordcloud_{category}.png", dpi=300)
    plt.close()

# %%
counts = df['Category'].value_counts().reset_index()
counts.columns = ['Category','Count']
fig = px.bar(counts, x='Category', y='Count', title='Distribuzione delle Categorie', height=500 ,width=1200)
fig.show()

# %% [markdown]
# ## 2. Suddivisione del Dataset (Train + Validation + Test)
#
# Suddividiamo i dati in:
# - **Train Set (70%)**: Per addestrare il modello.
# - **Validation Set (15%)**: Per il tuning degli iperparametri (implicito in questa pipeline semplificata).
# - **Test Set (15%)**: Per la valutazione finale imparziale.

# %%
X = df['cleaned_resume']
y = df['Category']

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

print(f"Dimensioni Train: {X_train.shape[0]}")
print(f"Dimensioni Validation: {X_val.shape[0]}")
print(f"Dimensioni Test: {X_test.shape[0]}")

# %% [markdown]
# ## 3. Feature Extraction
# Utilizziamo **TF-IDF (Term Frequency - Inverse Document Frequency)**. 
# È molto efficace per il testo perché penalizza le parole troppo comuni (stop words) e valorizza quelle distintive per ogni categoria.

# %%
# Inizializzazione del vettorizzatore
# max_features=5000 limita il vocabolario alle 5000 parole più importanti per ridurre la dimensionalità
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))

# Fit solo sul training set per evitare data leakage
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(X_test)

print(f"Shape della matrice di feature (Train): {X_train_vec.shape}")

# %% [markdown]
# ## 4. Addestramento del Classificatore
# Utilizziamo una **Linear SVC (Support Vector Classifier)**, nota per essere veloce e accurata nella classificazione di testi.

# %%
model = LinearSVC(random_state=42, dual='auto')
model.fit(X_train_vec, y_train)
print("Addestramento completato.")

# %% [markdown]
# ## 5. Valutazione del Modello
# Valutiamo le performance sul **Test Set**.

# %%
y_pred = model.predict(X_test_vec)

print("--- Classification Report (Test Set) ---")
print(classification_report(y_test, y_pred))

print(f"Accuracy finale: {accuracy_score(y_test, y_pred):.4f}")

# %%
labels = sorted(y_test.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)
fig = px.imshow(cm, x=labels, y=labels, color_continuous_scale='Blues',
                labels=dict(x='Predetto', y='Reale', color='Count'),
                text_auto=True, title='Matrice di Confusione', height=800, width=800)
fig.update_layout(xaxis_title='Predetto', yaxis_title='Reale')
fig.show()

# %% [markdown]
# ## 6. Inferenza
# Utilizziamo il modello addestrato su un nuovo testo mai visto.

# %%
sample_row = df.sample(1).iloc[0]
resume_text = sample_row['cleaned_resume']
true_label = sample_row['Category']

sample_clean = clean_text(resume_text)
sample_vec = vectorizer.transform([sample_clean])

prediction = model.predict(sample_vec)[0]

print(f"Testo Input:\n{resume_text.strip()}")
print(f"\nCategoria Predetta: {prediction}")
print(f"Categoria Reale: {true_label}")
