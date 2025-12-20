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
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## 1. Caricamento e Preprocessing dei Dati

# %%
# Caricamento del dataset
try:
    df = pd.read_csv('data/Resume.csv')
    print(f"Dataset caricato con successo: {df.shape[0]} righe, {df.shape[1]} colonne")
except FileNotFoundError:
    print("Errore: Il file 'data/Resume.csv' non è stato trovato.")
    # Creazione dati dummy per permettere l'esecuzione se il file non esiste
    data = {
        'Resume_str': ['Java developer with sql experience', 'HR manager with recruitment skills', 'Designer with photoshop skills'] * 50,
        'Category': ['Engineering', 'HR', 'Arts'] * 50
    }
    df = pd.DataFrame(data)

# Pulizia basilare del testo
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text) # Rimuove punteggiatura
    text = re.sub(r'\s+', ' ', text).strip() # Rimuove spazi extra
    return text

df['cleaned_resume'] = df['Resume_str'].apply(clean_text)

# Visualizzazione delle classi
print("\nDistribuzione delle Categorie:")
print(df['Category'].value_counts().head())

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

# Primo split: Train (70%) vs Temp (30%)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Secondo split: Temp in Validation (15% orig) e Test (15% orig)
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

# %% [markdown]
# ## 6. Inferenza
# Utilizziamo il modello addestrato su un nuovo testo mai visto.

# %%
sample_resume = """
Experienced Data Scientist with strong skills in Python, Machine Learning, and Deep Learning. 
Proficient in TensorFlow, PyTorch, and Scikit-Learn. 
History of working in the finance industry analyzing large datasets.
"""

# Preprocessing e Vettorizzazione del singolo campione
sample_clean = clean_text(sample_resume)
sample_vec = vectorizer.transform([sample_clean])

# Predizione
prediction = model.predict(sample_vec)[0]

print(f"Testo Input:\n{sample_resume.strip()}")
print(f"\nCategoria Predetta: {prediction}")