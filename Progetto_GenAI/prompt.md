# Prompt Trivia Quiz

Agisci come un **software engineer full-stack esperto** incaricato di progettare e implementare una **web application di tipo Trivia / Quiz**. L’obiettivo è realizzare un sistema **semplice, pulito e manutenibile**, evitando soluzioni superflue o non richieste.

L’applicazione è una piattaforma web client–server in cui **utenti registrati tramite username univoco** partecipano a **sessioni di quiz a risposta multipla**. Ogni sessione è indipendente e produce un risultato finale basato su **numero di risposte corrette e tempo totale di completamento**. Non implementare ruoli amministrativi né sistemi di autenticazione avanzati.

Il **frontend** gestisce interamente il gameplay: presentazione delle domande una alla volta, raccolta delle risposte e misurazione del tempo di completamento. Il **backend** ha responsabilità limitate e ben definite: fornire le domande, valutare le risposte ricevute e persistere i risultati finali. Non deve gestire stato di gioco in tempo reale.

Il sistema deve permettere la creazione di utenti, l’avvio di nuove sessioni di quiz tramite endpoint dedicato, la selezione casuale di un numero prefissato di domande dal database e l’invio al client **senza includere le risposte corrette**. Al termine del quiz il client invia al backend le risposte selezionate e il tempo impiegato; il backend verifica la correttezza, calcola il punteggio e salva il risultato.

Ogni tentativo di quiz deve essere persistito come sessione associata all’utente, memorizzando **punteggio, numero di risposte corrette, numero totale di domande, tempo di completamento e timestamp**. Non salvare le singole risposte per domanda. L’utente deve poter avviare nuove sessioni in qualsiasi momento, senza dipendenze dalle precedenti.

Utilizza un **modello dati semplice con massimo tre entità**: user, question, attempt. Progetta **API REST chiare e coerenti**, valida gli input lato server e mantieni una netta separazione delle responsabilità tra frontend e backend. Il codice deve essere leggibile, ben strutturato ed estendibile.

Utilizza tool e tecnologie di semplici e rapido utilizzo.

## Prompt Dashboard

Agisci come un **UI engineer orientato alla data visualization**. Dallo **schema E-R del database** @database.js . Il tuo compito è generare **N dashboard statiche**, dove **N è il numero di entità**, con **una dashboard per ciascuna tabella/entità**, focalizzata sull’**analisi dei dati** e non sulla descrizione dell’entità.

Le dashboard devono essere sviluppate **esclusivamente in vanilla HTML, CSS e JavaScript**, senza framework o librerie esterne.

---

### Vincolo fondamentale

Le dashboard devono essere **semplici, coerenti e orientate agli insight**, ma **completamente non interattive**:

* nessuna operazione CRUD
* nessuna ricerca, filtro, sorting o paginazione
* nessun evento utente che modifichi lo stato
* JavaScript ammesso **solo per il rendering iniziale di dati statici** (mock)

---

### Obiettivo

Produrre un **mini-sito di dashboard analitiche read-only** che simuli ciò che un analista vedrebbe osservando le tabelle del database, utile per:

* comprendere andamenti
* individuare pattern
* valutare distribuzioni e relazioni
  senza descrivere lo schema in modo didascalico.

---

### Contenuto obbligatorio di ogni dashboard (una per entità)

Ogni dashboard deve rispondere implicitamente alla domanda:
**“Che cosa posso capire dai dati contenuti in questa tabella?”**

**1. Titolo orientato ai dati**
Nome dell’entità + focus analitico (es. “User activity overview”, “Quiz attempts performance”, “Question usage insights”).

**2. KPI principali (3–6 card)**
Metriche aggregate e plausibili derivate dai dati della tabella, ad esempio:

* conteggi totali
* medie / percentuali
* min/max
* distribuzioni per stato o categoria
* indicatori temporali (ultimi 7/30 giorni)
  Valori mock, ma **coerenti con attributi e relazioni**.

**3. Sezione Andamenti / Distribuzioni (statica)**
Visualizzazione statica di insight come:

* distribuzioni per categoria
* confronti tra sottoinsiemi
* breakdown per FK (es. tentativi per utente, record per stato)
  I grafici devono essere **simulati visivamente** (barre, progress, tabelle aggregate), non interattivi.

**4. Tabella “Snapshot dei dati”**
Tabella con 5–10 record di esempio, rappresentativi e realistici, utile solo a:

* dare contesto ai KPI
* mostrare valori tipici
  (non per descrivere lo schema).

**5. Sezione Insight testuali**
2–4 osservazioni analitiche basate sui dati, ad esempio:

* pattern evidenti
* anomalie plausibili
* metriche chiave da monitorare
* relazioni implicite con altre entità

---

### Coerenza globale

* Layout uniforme per tutte le dashboard (header, navigazione tra entità, footer).
* Design system minimale e neutro.
* Naming dei file basato sui nomi delle entità in **kebab-case**.
* Navigazione tra dashboard per passare da una vista dati all’altra.

---

### Vincoli tecnici

* Solo HTML / CSS / JS vanilla.
* Nessuna dipendenza esterna (no CDN, no Bootstrap, no chart libraries).
* JS solo per:

  * inserire dati mock
  * calcolare aggregazioni semplici
  * renderizzare il contenuto iniziale
* Nessun listener di eventi utente.

---

### Output atteso in @dashboard

1. Breve riepilogo delle entità e del **tipo di insight** atteso per ciascuna.
2. Struttura dei file e **codice completo**, preferibilmente:

   * `/index.html` (overview generale dei dati + link alle dashboard)
   * `/assets/styles.css`
   * `/assets/site.js`
   * `/dashboards/<entity>.html`
   * `/dashboards/<entity>-data.js`
3. Per ogni entità:

   * KPI coerenti con i dati
   * aggregazioni sensate
   * insight testuali realistici
4. Brevissime istruzioni di esecuzione (aprire `index.html`).

---

### Regole

* Genera **esattamente N dashboard**, una per ogni entità.
* Non usare le dashboard per spiegare lo schema o i campi, ma per **estrarre informazione dai dati**.
* Se mancano tipi o cardinalità, fai **assunzioni minimali e ragionevoli**, dichiarandole nella sezione **“Assunzioni”** dell’`index.html`.

Agisci sempre come un **data-oriented UI engineer**, privilegiando **chiarezza analitica, semplicità visiva e coerenza concettuale**.

## Secondo prompt

Nella dashboard @users.html la sezione "Registrazioni Ultimi 7 Giorni" non mostra un grafico, ci sono solo i numeri. Nella @questions.html ci sono bar chart che non hanno la linea colorata anche se il valore è maggiore di 0. in @attempts.html ci sono entambi i problemi descritti in precedenza, "Tentativi Ultimi 7 Giorni" non mostra nulla
