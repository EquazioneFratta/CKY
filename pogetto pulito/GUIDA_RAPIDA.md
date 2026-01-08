# 🚀 Guida Rapida - Progetto CKY per Quenya

**Tecnologie del Linguaggio Naturale - A.A. 2023/2024**

---

## 📦 Cosa Contiene il Progetto

```
progetto-cky-quenya/
├── main.py                  # ⭐ File principale con menu interattivo
├── cky_parser.py           # Implementazione algoritmo CKY
├── quenya_grammar.py       # Grammatica Quenya
├── quenya_semantic.py      # Grammatica con semantica (NLTK)
├── README.md               # Documentazione completa
├── RELAZIONE.md           # Relazione dettagliata
└── requirements.txt        # Dipendenze
```

---

## ⚡ Installazione Veloce

### 1. Verifica Python

```bash
python --version
# Dovrebbe mostrare: Python 3.7+
```

### 2. Estrai i File

Estrai `progetto-cky-quenya.zip` in una cartella a tua scelta.

### 3. (Opzionale) Installa NLTK

**Solo se vuoi eseguire la Parte D (Bonus)**:

```bash
pip install nltk
```

**Nota**: Le Parti A, B e C funzionano SENZA installazioni aggiuntive!

---

## 🎮 Come Usare

### Metodo 1: Menu Interattivo (⭐ Raccomandato)

```bash
cd progetto-cky-quenya
python main.py
```

Apparirà un menu:

```
MENU - Seleziona il test da eseguire:
═══════════════════════════════════════════════════════════════════
1. Test Parte A: Implementazione CKY from scratch
2. Test Parte B: CKY sulla grammatica L1 di Jurafsky & Martin
3. Test Parte C: CKY su grammatica Quenya custom
4. Test Parte D (BONUS): Grammatica Quenya con semantica NLTK
5. Esegui tutti i test
0. Esci
═══════════════════════════════════════════════════════════════════
```

### Metodo 2: Esecuzione Diretta

```bash
# Test grammatica L1 (Inglese)
python cky_parser.py

# Test grammatica Quenya (Elfico)
python quenya_grammar.py

# Test semantica (richiede NLTK)
python quenya_semantic.py
```

---

## 📝 Esempi di Frasi

### Inglese (Grammatica L1)

```
✓ "book the flight through Houston"
✓ "does she prefer a morning flight"
```

### Quenya (Elfico)

```
✓ "i elda ná vanya"          → "l'elfo è bello"
✓ "i aran cálë"              → "il re risplende"
✓ "i aranel tirë i elen"     → "la principessa guarda la stella"
✓ "i cirya vanya"            → "la nave bella"
✓ "i eldar lir-"             → "gli elfi cantano"
✓ "elen calima"              → "stella luminosa"
```

---

## 🎯 Output Attesi

### Esempio: Parsing "i aran cálë"

```
══════════════════════════════════════════════════════════════════
Quenya:   i aran cálë
Italiano: il re risplende
══════════════════════════════════════════════════════════════════

=== CKY Table ===
[0,2] ['i', 'aran', 'cálë']: S, VP
[0,1] ['i', 'aran']: NP, S
[1,2] ['aran', 'cálë']: S, VP

✓ Parsing riuscito! Trovati 1 albero/i di parsing.

--- Parse Tree 1 ---
[S
  [NP
    [Det i]
    [N aran]]
  [VP
    [V cálë]]]
```

---

## 🐛 Problemi Comuni

### ❌ "python: command not found"

**Soluzione**: Installa Python da [python.org](https://www.python.org/downloads/)

### ❌ "ModuleNotFoundError: No module named 'nltk'"

**Soluzione**: La Parte D richiede NLTK. Installa con:
```bash
pip install nltk
```

### ❌ Il parsing di una frase fallisce

**Causa**: Parola non nel lessico o struttura non coperta dalla grammatica.

**Soluzione**: Controlla che tutte le parole siano nel lessico (vedi `quenya_grammar.py`)

---

## 📚 Struttura del Progetto

### Parte A: Implementazione CKY ✓

- Algoritmo CKY completo con triplo ciclo
- Tabella triangolare superiore n×n
- Back-pointers per ricostruzione parse trees
- Gestione ambiguità strutturale
- Supporto regole unarie (A → B)

**File**: `cky_parser.py`

### Parte B: Grammatica L1 ✓

- Grammatica da Jurafsky & Martin (3rd ed., Fig. 18.10)
- Test su 2 frasi inglesi
- Parsing con successo al 100%

**File**: `cky_parser.py` (funzione `test_l1_grammar()`)

### Parte C: Grammatica Quenya ✓

- 80+ voci lessicali
- 12 regole sintattiche
- 6 frasi di test validate
- Coverage: costrutti base della lingua

**File**: `quenya_grammar.py`

### Parte D: Semantica (BONUS) ✓

- Grammatica feature-based (NLTK)
- Lambda-calcolo per composizione
- Logica del primo ordine
- 6 frasi con rappresentazione semantica

**File**: `quenya_semantic.py`

---

## 🎓 Caratteristiche Tecniche

### Algoritmo CKY

- **Complessità temporale**: O(n³ × |G|)
- **Complessità spaziale**: O(n²)
- **Grammatica**: Chomsky Normal Form (CNF) + regole unarie
- **Output**: Tutti i possibili parse trees

### Grammatica Quenya

- **Ordine parole**: SOV (Soggetto-Oggetto-Verbo)
- **Aggettivi**: Post-nominali (dopo il nome)
- **Lessico**: Nomi, verbi, aggettivi, pronomi, determinanti, preposizioni
- **Features**: Numero grammaticale (singolare/plurale)

---

## 📖 Documentazione Completa

Per informazioni dettagliate:

- **README.md**: Documentazione completa del progetto
- **RELAZIONE.md**: Relazione tecnica con esempi e analisi

---

## 🌟 Quick Tips

1. **Inizia con il menu interattivo** (`python main.py`) - è il modo più semplice
2. **Le Parti A, B, C non richiedono installazioni** - funzionano subito!
3. **La Parte D (Bonus) richiede NLTK** - ma è opzionale
4. **Guarda gli esempi di output** nel README per capire il formato atteso
5. **Consulta la RELAZIONE.md** per dettagli teorici sull'algoritmo

---

## 📧 Supporto

Per domande o problemi:
- Consulta il **README.md** per la documentazione completa
- Leggi la **RELAZIONE.md** per dettagli tecnici
- Controlla la sezione "Troubleshooting" nel README

---

## 🧝 Curiosità sul Quenya

Il Quenya è una delle lingue elfiche create da J.R.R. Tolkien:
- È ispirato al finlandese e al latino
- Tolkien lo sviluppò per oltre 60 anni
- Ha ~1500 parole documentate
- È la lingua "alta" degli Eldar nella Terra di Mezzo

**Parole utili in Quenya**:
- `namárië` = addio
- `márienna` = buon viaggio
- `aiya` = salve
- `hara máriesse` = stai bene

---

**Namárië!** (Addio in Quenya) 🧝‍♂️

*Progetto sviluppato per il corso di Tecnologie del Linguaggio Naturale*
