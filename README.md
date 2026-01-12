# Progetto CKY per il Quenya

 Tecnologie del Linguaggio Naturale - Informatica  
 2023/2024  
 Implementazione dell'algoritmo CKY con applicazione alla lingua Quenya (Elfico)

---

## Introduzione

Questo progetto implementa l'algoritmo **CKY (Cocke-Kasami-Younger)** per il parsing di grammatiche context-free e lo applica alla **lingua Quenya**

### Obiettivi del Progetto

- Parte A: Implementare CKY from scratch
- Parte B: Test su grammatica L1
- Parte C: Creare grammatica Quenya e testare con CKY
- Parte D (Bonus): Grammatica Quenya con semantica composizionale (NLTK)

---

## Utilizzo

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

### 2. `quenya_grammar.py` - Grammatica Quenya

### 3. `quenya_semantic.py` - Semantica Composizionale

**Feature-Based Grammar**

Utilizza NLTK per implementare:
- **Semantica λ-calcolo**: composizione del significato
- **Logica del primo ordine**: rappresentazione finale
---