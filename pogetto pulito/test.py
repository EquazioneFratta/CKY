import nltk
from nltk import grammar, parse
from nltk.sem import logic

QUENYA_SEMANTIC_GRAMMAR = r"""
% start S

# Frasi base: NP + VP
S[SEM=<?subj(?vp)>] -> NP[NUM=?n,SEM=?subj] VP[NUM=?n,SEM=?vp]

# Frasi con verbo flesso (pronome incorporato): solo VP
S[SEM=?vp] -> VP[SEM=?vp]

# Sintagmi nominali
NP[NUM=?n,SEM=<?det(?nom)>] -> Det[NUM=?n,SEM=?det] Nom[NUM=?n,SEM=?nom]
NP[NUM=?n,SEM=?nom] -> Nom[NUM=?n,SEM=?nom]

# Nominali
Nom[NUM=?n,SEM=?nom] -> N[NUM=?n,SEM=?nom]

# Sintagmi verbali
# Verbo transitivo: V + NP (oggetto)
VP[NUM=?n,SEM=<?v(?obj)>] -> TV[NUM=?n,SEM=?v] NP[SEM=?obj]

# Verbo ditransitivo: V + NP + NP (oggetto indiretto + oggetto diretto)
# In Quenya: antanë + i eldan (dativo) + tecil
VP[NUM=?n,SEM=<?v(?obj1,?obj2)>] -> DTV[NUM=?n,SEM=?v] NP[SEM=?obj1] NP[SEM=?obj2]

# Copula + Aggettivo predicativo (per "Nanye lumba" = I am tired)
VP[SEM=<?cop(?adj)>] -> Cop[SEM=?cop] Adj[SEM=?adj]

# Copula + Nome predicativo (per "Nálmë eldar" = we are elves)  
VP[SEM=<?cop(?np)>] -> Cop[SEM=?cop] NP[SEM=?np]

############################
# Lexical Rules
############################

# DETERMINANTI
Det[NUM=sg,SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'i'  
Det[NUM=pl,SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'i'  

# NOMI
N[NUM=sg,SEM=<\x.hesto(x)>] -> 'hesto'     
N[NUM=sg,SEM=<\x.macil(x)>] -> 'macil'     
N[NUM=sg,SEM=<\x.aran(x)>] -> 'aran'       
N[NUM=pl,SEM=<\x.aiwi(x)>] -> 'aiwi'       
N[NUM=pl,SEM=<\x.elda(x)>] -> 'eldar'      
N[NUM=sg,SEM=<\x.atan(x)>] -> 'atan'       
N[NUM=sg,SEM=<\x.elda(x)>] -> 'eldan'      
N[NUM=sg,SEM=<\x.tecil(x)>] -> 'tecil'     

# AGGETTIVI
Adj[SEM=<\x.lumba(x)>] -> 'lumba'          

# VERBI TRANSITIVI (TV)
# samë = has/have
TV[NUM=sg,SEM=<\X x.X(\y.have(x,y))>] -> 'samë'
TV[NUM=pl,SEM=<\X x.X(\y.have(x,y))>] -> 'samë'

# tíra = is watching / watches
TV[NUM=sg,SEM=<\X x.X(\y.watch(x,y))>] -> 'tíra'
TV[NUM=pl,SEM=<\X x.X(\y.watch(x,y))>] -> 'tíra'

# VERBI DITRANSITIVI (DTV)
# antanë = gave
DTV[NUM=sg,SEM=<\Y X x.X(\z.Y(\y.give(x,y,z)))>] -> 'antanë'
DTV[NUM=pl,SEM=<\Y X x.X(\z.Y(\y.give(x,y,z)))>] -> 'antanë'

# COPULA (verbi essere con pronomi incorporati)
# nanye = I am (ná + -nye)
Cop[SEM=<\P.P(speaker)>] -> 'nanye'        

# nálmë = we are (ná + -lmë)  
Cop[SEM=<\P.all x.(we(x) -> P(x))>] -> 'nálmë' 
"""


def load_quenya_semantic_grammar():
    try:
        return grammar.FeatureGrammar.fromstring(QUENYA_SEMANTIC_GRAMMAR)
    except Exception as e:
        print(f"Errore nel caricamento della grammatica: {e}")
        raise


def parse_with_semantics(sentence, grammar_obj):
    """
    Esegue il parsing di una frase Quenya e estrae la rappresentazione semantica
    
    Args:
        sentence: Frase in Quenya
        grammar_obj: Grammatica feature-based NLTK
        
    Returns:
        Lista di tuple (tree, semantics)
    """
    tokens = sentence.lower().split()
    parser = parse.FeatureEarleyChartParser(grammar_obj)
    
    results = []
    for tree in parser.parse(tokens):
        sem = tree.label()['SEM']
        results.append((tree, sem))
    
    return results


def test_quenya_semantic():    
    try:
        gram = load_quenya_semantic_grammar()
        print()
    except Exception as e:
        print(f"✗ Errore: {e}")
        return
    
    # Le 5 frasi richieste
    test_sentences = [
        "I hesto samë macil",
        "I aran tíra aiwi",
        "Nanye lumba",
        "Nálmë eldar",
        "I atan antanë i eldan tecil"
    ]
    
    successful = 0
    failed = 0
    
    for idx, sentence in enumerate(test_sentences, 1):
        print(f"Frase {idx}/5")
        print(f"{sentence}")

        try:
            results = parse_with_semantics(sentence, gram)
            
            if results:
                print(f"Parsing riuscito. Trovati {len(results)} parse tree(s).\n")
                successful += 1
                
                for parse_idx, (tree, sem) in enumerate(results, 1):
                    print(f"--- Parse Tree {parse_idx} ---")
                    print(tree)
                    print()
                    
                    print(f"--- Rappresentazione Semantica {parse_idx} ---")
                    print(f"Formula: {sem}")
                    
                    # Semplifica la formula
                    try:
                        simplified = sem.simplify()
                        if str(simplified) != str(sem):
                            print(f"Semplificata: {simplified}")
                    except:
                        pass
                    
                    print()
            else:
                print("Parsing fallito.\n")
                failed += 1
                
        except Exception as e:
            print(f"Errore: {e}\n")
            failed += 1
        
        print()
    
    # Risultati finali
    print("=" * 80)
    print("RISULTATI FINALI")
    print("=" * 80)
    print(f"Frasi parsate con successo: {successful}/5")
    print(f"Frasi fallite: {failed}/5")
    print()
    
    if successful >= 3:
        print("✓ Requisito bonus soddisfatto (3+ frasi con semantica)!")
    
    if successful == 5:
        print("🎉 Perfetto! Tutte le 5 frasi hanno semantica!")


def create_semantic_explanation():
    """Crea documentazione sulla semantica implementata"""
    explanation = r"""
# Semantica Quenya - Spiegazione

## Rappresentazione Semantica

La grammatica usa logica del primo ordine con lambda-calcolo per rappresentare
il significato delle frasi, seguendo l'approccio di sem3.fcfg di NLTK.

### 1. Verbi Transitivi (TV)

**Esempio: "samë" (has)**
```
SEM = <\X x.X(\y.have(x,y))>
```

Significato: prende un NP oggetto (X) e un soggetto (x), 
applicando X alla relazione have(x,y).

**Frase: "I hesto samë macil"**
- Soggetto: ∃x.(hesto(x) & ...)
- Oggetto: ∃y.macil(y)
- Risultato: ∃x.∃y.(hesto(x) & macil(y) & have(x,y))
- Traduzione: "Esiste un capitano x ed esiste una spada y tale che x ha y"

### 2. Verbi Ditransitivi (DTV)

**Esempio: "antanë" (gave)**
```
SEM = <\Y X x.X(\z.Y(\y.give(x,y,z)))>
```

Prende due oggetti (indiretto Y e diretto X) e un soggetto (x).

**Frase: "I atan antanë i eldan tecil"**
- Soggetto: ∃x.atan(x)
- Oggetto indiretto: ∃y.elda(y)
- Oggetto diretto: ∃z.tecil(z)
- Risultato: ∃x.∃y.∃z.(atan(x) & elda(y) & tecil(z) & give(x,y,z))
- Traduzione: "Esiste un uomo x, un elfo y e una penna z tali che x dà z a y"

### 3. Copula + Aggettivo

**Esempio: "Nanye lumba" (I am tired)**
```
Cop[SEM=<\P.P(speaker)>] -> 'nanye'
Adj[SEM=<\x.lumba(x)>] -> 'lumba'
```

- Risultato: lumba(speaker)
- Traduzione: "Il parlante è stanco"

### 4. Copula + Nome Predicativo

**Esempio: "Nálmë eldar" (we are elves)**
```
Cop[SEM=<\P.all x.(we(x) -> P(x))>] -> 'nálmë'
NP[SEM=<\x.elda(x)>] -> 'eldar'
```

- Risultato: ∀x.(we(x) → elda(x))
- Traduzione: "Per ogni x, se x è noi, allora x è un elfo"

### 5. Determinanti

**"i" (il/la/i/le)**
```
Det[SEM=<\P Q.exists x.(P(x) & Q(x))>]
```

Quantificatore esistenziale: combina due predicati P e Q.

## Confronto con sem3.fcfg

| Caratteristica | sem3.fcfg (Inglese) | Quenya Grammar |
|----------------|---------------------|----------------|
| Verbi transitivi | TV: sees, chases | TV: samë, tíra |
| Verbi ditransitivi | DTV: gives | DTV: antanë |
| Pronomi | PropN: Angus, Cyril | Incorporati in verbi |
| Copula | Implicita | Esplicita: nanye, nálmë |
| Determinanti | a, every, some | i |

## Differenze Principali

1. **Pronomi Incorporati**: In Quenya, pronomi come "I" e "we" sono suffissati 
   ai verbi (nanye = I am, nálmë = we are), non esistono come parole separate.

2. **Casi Nominali**: "eldan" (dativo) vs "elda" (nominativo) - gestito come
   parole diverse nel lessico.

3. **Ordine Parole**: Quenya è più flessibile grazie ai casi, ma la grammatica
   usa l'ordine SVO base per semplicità.

## Feature Syntattiche

- **NUM**: Numero (sg/pl) - per accordo soggetto-verbo
- **SEM**: Rappresentazione semantica in lambda calculus
"""
    return explanation


if __name__ == "__main__":
    # Test principale
    test_quenya_semantic()
    
    # Spiegazione
    print("\n" + "=" * 80)
    print("SPIEGAZIONE DELLA SEMANTICA")
    print("=" * 80)
    print(create_semantic_explanation())