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
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from wordcloud import WordCloud
from tools import utils as u
from tools import plotting as p

# %% [markdown]
# ## 1. Caricamento e Preprocessing dei Dati

# %%
df = pd.read_csv('data/Resume.csv')

print(f"Dataset caricato con successo: {df.shape[0]} righe, {df.shape[1]} colonne")

df['cleaned_resume'] = df['Resume_str'].apply(u.preprocess_text)

# Visualizzazione delle classi
print("\nDistribuzione delle Categorie:")
print(df['Category'].value_counts().head())

# %% [markdown]
#

# %% [markdown]
# # Wordcloud

# %%
# Definizione Custom Stop Words per rimuovere termini generici da CV (come suggerito dal report)
custom_stop_words = list(ENGLISH_STOP_WORDS) + ['experience', 'skills', 'worked', 'team', 'responsible']

MAX_WORDS = 500
wc_obj = WordCloud(
    width=800, 
    height=700, 
    background_color='white',
    max_words=MAX_WORDS,
    contour_width=0,
    colormap='viridis'
)

# Overall WordCloud
fig = p.wordcloud(wc_obj, df['cleaned_resume'], MAX_WORDS, custom_stop_words, "Word Cloud of Top Words")
fig.savefig("data/wordcloud/wordcloud_overall.png", dpi=300)

for category in df['Category'].unique():
    category_df = df[df['Category'] == category]
    fig = p.wordcloud(wc_obj, category_df['cleaned_resume'], 100, custom_stop_words, f"Word Cloud for Category: {category}")
    fig.savefig(f"data/wordcloud/wordcloud_{category}.png", dpi=300)

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
# Utilizziamo le custom_stop_words definite precedentemente
# Aumentiamo max_features (o rimuoviamo il limite) per catturare la coda lunga dei termini tecnici
vectorizer = TfidfVectorizer(stop_words=custom_stop_words, max_features=20000, ngram_range=(1, 2))

# Fit solo sul training set per evitare data leakage
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(X_test)

print(f"Shape della matrice di feature (Train): {X_train_vec.shape}")

# %% [markdown]
# ## 4. Addestramento del Classificatore
# Utilizziamo una **Linear SVC (Support Vector Classifier)**, nota per essere veloce e accurata nella classificazione di testi.

# %%
# Utilizziamo class_weight='balanced' per gestire lo sbilanciamento delle classi
# E CalibratedClassifierCV per ottenere probabilità (confidence scores)
base_svc = LinearSVC(random_state=42, dual='auto', class_weight='balanced')
model = CalibratedClassifierCV(base_svc)
model.fit(X_train_vec, y_train)
print("Addestramento completato (con calibrazione probabilità).")

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

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title('Matrice di Confusione')
plt.ylabel('Reale')
plt.xlabel('Predetto')
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('data/confusion_matrix.png', dpi=300)
print("Matrice di confusione salvata in data/confusion_matrix.png")
# fig = px.imshow(cm, x=labels, y=labels, color_continuous_scale='Blues',
#                 labels=dict(x='Predetto', y='Reale', color='Count'),
#                 text_auto=True, title='Matrice di Confusione', height=800, width=800)
# fig.update_layout(xaxis_title='Predetto', yaxis_title='Reale')
# fig.show()

# %% [markdown]
# ## 6. Inferenza
# Utilizziamo il modello addestrato su un nuovo testo mai visto.

# %%
sample_row = df.sample(1).iloc[0]
resume_text = sample_row['Resume_str'] # Use the raw text to test full pipeline
true_label = sample_row['Category']

sample_clean = u.preprocess_text(resume_text)
sample_vec = vectorizer.transform([sample_clean])

prediction = model.predict(sample_vec)[0]
proba = model.predict_proba(sample_vec)[0]
confidence = np.max(proba)

print(f"Testo Input:\n{resume_text.strip()}")
print(f"\nCategoria Predetta: {prediction}")
print(f"Confidence: {confidence:.2f}")
print(f"Categoria Reale: {true_label}")
