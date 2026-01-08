# Progetto CKY per il Quenya

 Tecnologie del Linguaggio Naturale - Informatica  
 2023/2024  
 Implementazione dell'algoritmo CKY con applicazione alla lingua Quenya (Elfico)

---

## Indice

1. [Introduzione](#introduzione)
2. [Struttura del Progetto](#struttura-del-progetto)
3. [Installazione](#installazione)
4. [Utilizzo](#utilizzo)
5. [Descrizione delle Componenti](#descrizione-delle-componenti)
6. [Risultati](#risultati)
7. [Bibliografia](#bibliografia)

---

## Introduzione

Questo progetto implementa l'algoritmo **CKY (Cocke-Kasami-Younger)** per il parsing di grammatiche context-free e lo applica alla **lingua Quenya**, una delle lingue elfiche create da J.R.R. Tolkien.

### Obiettivi del Progetto

- Parte A: Implementare CKY from scratch
- Parte B: Testare su grammatica L1 di Jurafsky & Martin
- Parte C: Creare grammatica Quenya e testare con CKY
- Parte D (Bonus): Grammatica Quenya con semantica composizionale (NLTK)

---

## Struttura del Progetto

```
progetto-cky-quenya/
│
├── main.py                  # File principale con menu interattivo
├── cky_parser.py           # Implementazione algoritmo CKY
├── quenya_grammar.py       # Grammatica Quenya per CKY
├── quenya_semantic.py      # Grammatica Quenya con semantica (NLTK)
├── README.md               # Questo file
├── RELAZIONE.md           # Relazione dettagliata del progetto
└── requirements.txt        # Dipendenze Python
```

---

## Installazione

### Prerequisiti

- Python 3.7 o superiore
- pip (package manager Python)

### Installazione Dipendenze

```bash
# Dipendenze base (solo per Parte A, B, C)
# Non richiede installazioni aggiuntive - usa solo libreria standard Python

# Per Parte D (Bonus) - Semantica NLTK
pip install nltk
```

### Setup Completo

```bash
# 1. Clona/scarica il progetto
cd progetto-cky-quenya

# 2. (Opzionale) Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# 3. Installa dipendenze per il bonus
pip install nltk

# 4. Esegui il progetto
python main.py
```

---

## Utilizzo

### Esecuzione Interattiva

```bash
python main.py
```

Il programma presenterà un menu interattivo con le seguenti opzioni:

1. **Test Implementazione CKY** - Visualizza dettagli implementazione
2. **Test Grammatica L1** - Parsing frasi inglesi con grammatica Jurafsky
3. **Test Grammatica Quenya** - Parsing frasi elfiche
4. **Test Semantica Quenya (Bonus)** - Parsing con rappresentazione logica
5. **Esegui Tutti i Test** - Esecuzione completa
0. **Esci**

### Esecuzione Singoli Moduli

```bash
# Test grammatica L1
python cky_parser.py

# Test grammatica Quenya
python quenya_grammar.py

# Test semantica Quenya (richiede NLTK)
python quenya_semantic.py
```

---

## Descrizione delle Componenti

### 1. `cky_parser.py` - Algoritmo CKY

**Classe `Grammar`**
- Rappresenta una grammatica context-free
- Supporta regole sintattiche: `A → B C`
- Supporta regole lessicali: `POS → word`
- Metodi per validazione CNF (Chomsky Normal Form)

**Classe `CKYParser`**
- Implementazione completa dell'algoritmo CKY
- Struttura dati: tabella triangolare superiore `n×n`
- Back-pointers per ricostruzione parse trees
- Genera tutti i possibili parse trees

**Algoritmo CKY - Pseudocodice**

```
CKY(words, grammar):
    n = len(words)
    table = [[[]] for i,j in 0..n]
    
    # Fase 1: Riempi diagonale (parole)
    for i = 0 to n-1:
        for each POS that can generate words[i]:
            table[i][i].add(POS)
    
    # Fase 2: Bottom-up filling
    for length = 2 to n:
        for i = 0 to n-length:
            j = i + length - 1
            for k = i to j-1:
                for B in table[i][k]:
                    for C in table[k+1][j]:
                        for each rule A → B C:
                            table[i][j].add(A)
    
    return START_SYMBOL in table[0][n-1]
```

**Complessità**
- Tempo: O(n³ × |G|) dove n = lunghezza frase, |G| = dimensione grammatica
- Spazio: O(n²)

### 2. `quenya_grammar.py` - Grammatica Quenya

**Caratteristiche della Grammatica**

- **80+ voci lessicali** coprendo:
  - Nomi (elda, aran, cirya, elen, ...)
  - Aggettivi (vanya, calima, morna, ...)
  - Verbi (cálë, tirë, lírë, ...)
  - Pronomi e determinanti
  - Preposizioni

- **Regole sintattiche** che rispecchiano:
  - Ordine SOV (Soggetto-Oggetto-Verbo) del Quenya
  - Aggettivi postnominali (dopo il nome)
  - Costruzioni genitive

**Frasi di Test**

```quenya
i elda ná vanya          → "l'elfo è bello"
i aran cálë              → "il re risplende"
i aranel tirë i elen     → "la principessa guarda la stella"
```

### 3. `quenya_semantic.py` - Semantica Composizionale

**Feature-Based Grammar**

Utilizza NLTK per implementare:
- **Features sintattiche**: NUM (numero grammaticale)
- **Semantica λ-calcolo**: composizione del significato
- **Logica del primo ordine**: rappresentazione finale

**Esempio di Derivazione Semantica**

```
Frase: "i elda cálë" (l'elfo risplende)

1. i     → λP.λQ.∃x.(P(x) ∧ Q(x))    [determinante]
2. elda  → λx.elda(x)                 [nome]
3. cálë  → λx.cale(x)                 [verbo]

Composizione:
NP = [Det Nom] → ∃x.elda(x) ∧ ...
S  = [NP VP]   → ∃x.(elda(x) ∧ cale(x))

Significato: "Esiste un x tale che x è un elfo e x risplende"
```

---

## Risultati

### Grammatica L1 (Jurafsky)

**Frasi parsificate con successo:**
-  "book the flight through Houston"
-  "does she prefer a morning flight"

**Statistiche:**
- Tempo di parsing: < 1ms per frase
- Parse trees generati: 1-2 per frase (ambiguità strutturale)

### Grammatica Quenya

**Frasi parsificate con successo:**
- "i elda ná vanya" (l'elfo è bello)
- "i aran cálë" (il re risplende)
- "i aranel tirë i elen" (la principessa guarda la stella)
- "i cirya vanya" (la nave bella)
- "i eldar lir-" (gli elfi cantano)
- "elen calima" (stella luminosa)

**Coverage lessicale:**
- 80+ parole Quenya
- 15+ regole sintattiche
- 6 frasi di test validate

### Grammatica Semantica (Bonus)

**Frasi con rappresentazione logica:**
- "i elda cálë" → `∃x.(elda(x) ∧ cale(x))`
- "i aran tirë i elen" → `∃x.∃y.(aran(x) ∧ elen(y) ∧ tire(x,y))`
- "galadriel lírë" → `lire(galadriel)`

---

## Bibliografia

### Libri di Riferimento

1. **Jurafsky, D., & Martin, J. H.** (2023). *Speech and Language Processing* (3rd ed.)
   - Capitolo 18: Context-Free Grammars and Parsing
   - Figura 18.10: Grammatica L1

2. **Tolkien, J.R.R.** (1955-2007). *The Lord of the Rings*, appendici linguistiche

### Risorse Online

1. **Eldamo - Quenya Grammar**
   - https://eldamo.org/intro-quenya/eldamo-intro-quenya-01.html
   - https://eldamo.org/intro-quenya/eldamo-intro-quenya-12.html

2. **Ardalambion - Quenya Course**
   - http://ardalambion.immaginario.net/ardalambion/qcourse.htm

3. **Wikipedia - Quenya**
   - https://it.wikipedia.org/wiki/Quenya
   - https://it.wikipedia.org/wiki/Grammatica_della_lingua_quenya

4. **Neo-Quenya Translator**
   - https://pcknot.fit.vutbr.cz/elvish/

5. **NLTK Documentation**
   - https://www.nltk.org/
   - Feature-based grammars: https://www.nltk.org/book/ch09.html

---

## Note Aggiuntive

### Differenze tra Inglese e Quenya

| Aspetto | Inglese | Quenya |
|---------|---------|--------|
| Ordine base | SVO | SOV (flessibile) |
| Aggettivi | Pre-nominali | Post-nominali |
| Articoli | the, a/an | i, in |
| Caso grammaticale | Limitato | Ricco (10 casi) |

### Limitazioni Attuali

- La grammatica Quenya copre solo costrutti base
- Non implementati tutti i casi grammaticali
- Manca il sistema verbale completo (tempi, modi)
- Lessico limitato a ~80 parole

### Possibili Estensioni

1. **Grammatica più completa**
   - Implementare i 10 casi Quenya
   - Aggiungere sistema verbale completo
   - Espandere lessico (500+ parole)

2. **Features linguistiche**
   - Agreement numero/persona
   - Gestione dei casi
   - Subordinate e coordinate

3. **Parsing avanzato**
   - Probabilistic CKY
   - Dependency parsing
   - Neural parsing

---