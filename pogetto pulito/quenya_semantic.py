"""
Grammatica Quenya con Semantica (Bonus Track)
Implementazione di una grammatica feature-based per il Quenya con rappresentazione semantica
ispirata a simple-sem.fcfg di NLTK
"""

import nltk
from nltk import grammar, parse
from nltk.sem import logic
from io import StringIO


# Grammatica Quenya con features e semantica in formato NLTK
QUENYA_SEMANTIC_GRAMMAR = r"""
% start S

# ==================
# REGOLE SINTATTICHE CON SEMANTICA
# ==================

# Frasi
S[SEM=<?subj(?vp)>] -> NP[NUM=?n,SEM=?subj] VP[NUM=?n,SEM=?vp]
S[SEM=<?vp>] -> VP[SEM=?vp]

# Sintagmi nominali
NP[NUM=?n,SEM=<?det(?nom)>] -> Det[NUM=?n,SEM=?det] Nom[NUM=?n,SEM=?nom]
NP[NUM=?n,SEM=?nom] -> Nom[NUM=?n,SEM=?nom]
NP[NUM=?n,SEM=?pron] -> PropN[NUM=?n,SEM=?pron]

# Nominali
Nom[NUM=?n,SEM=?noun] -> N[NUM=?n,SEM=?noun]
Nom[NUM=?n,SEM=<?adj(?nom)>] -> N[NUM=?n,SEM=?nom] Adj[SEM=?adj]

# Sintagmi verbali
VP[NUM=?n,SEM=?v] -> IV[NUM=?n,SEM=?v]
VP[NUM=?n,SEM=<?v(?obj)>] -> TV[NUM=?n,SEM=?v] NP[SEM=?obj]

# ==================
# LESSICO CON SEMANTICA
# ==================

# Determinanti
Det[NUM=sg,SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'i'

# Nomi
N[NUM=sg,SEM=<\x.elda(x)>] -> 'elda'
N[NUM=pl,SEM=<\x.elda(x)>] -> 'eldar'
N[NUM=sg,SEM=<\x.aran(x)>] -> 'aran'
N[NUM=sg,SEM=<\x.tari(x)>] -> 'tári'
N[NUM=sg,SEM=<\x.aranel(x)>] -> 'aranel'
N[NUM=sg,SEM=<\x.cirya(x)>] -> 'cirya'
N[NUM=pl,SEM=<\x.cirya(x)>] -> 'ciryar'
N[NUM=sg,SEM=<\x.elen(x)>] -> 'elen'
N[NUM=pl,SEM=<\x.elen(x)>] -> 'eleni'
N[NUM=sg,SEM=<\x.parma(x)>] -> 'parma'
N[NUM=pl,SEM=<\x.parma(x)>] -> 'parmar'
N[NUM=sg,SEM=<\x.macil(x)>] -> 'macil'
N[NUM=sg,SEM=<\x.alda(x)>] -> 'alda'
N[NUM=pl,SEM=<\x.alda(x)>] -> 'aldar'

# Nomi propri
PropN[NUM=sg,SEM=<\P.P(galadriel)>] -> 'galadriel'
PropN[NUM=sg,SEM=<\P.P(elendil)>] -> 'elendil'
PropN[NUM=sg,SEM=<\P.P(finrod)>] -> 'finrod'

# Aggettivi
Adj[SEM=<\P x.(P(x) & vanya(x))>] -> 'vanya'
Adj[SEM=<\P x.(P(x) & vanima(x))>] -> 'vanima'
Adj[SEM=<\P x.(P(x) & calima(x))>] -> 'calima'
Adj[SEM=<\P x.(P(x) & morna(x))>] -> 'morna'
Adj[SEM=<\P x.(P(x) & alta(x))>] -> 'alta'
Adj[SEM=<\P x.(P(x) & mara(x))>] -> 'mára'

# Verbi intransitivi
IV[NUM=sg,SEM=<\x.cale(x)>] -> 'cálë'
IV[NUM=pl,SEM=<\x.cale(x)>] -> 'calar'
IV[NUM=sg,SEM=<\x.lire(x)>] -> 'lírë'
IV[NUM=pl,SEM=<\x.lire(x)>] -> 'lírer'
IV[NUM=sg,SEM=<\x.tule(x)>] -> 'tulë'
IV[NUM=pl,SEM=<\x.tule(x)>] -> 'tuler'

# Verbi transitivi
TV[NUM=sg,SEM=<\X x.X(\y.tire(x,y))>] -> 'tirë'
TV[NUM=pl,SEM=<\X x.X(\y.tire(x,y))>] -> 'tirer'
TV[NUM=sg,SEM=<\X x.X(\y.cene(x,y))>] -> 'cenë'
TV[NUM=pl,SEM=<\X x.X(\y.cene(x,y))>] -> 'cener'
TV[NUM=sg,SEM=<\X x.X(\y.hire(x,y))>] -> 'hirë'
TV[NUM=pl,SEM=<\X x.X(\y.hire(x,y))>] -> 'hirer'
"""


def load_quenya_semantic_grammar():
    """Carica la grammatica semantica Quenya"""
    return grammar.FeatureGrammar.fromstring(QUENYA_SEMANTIC_GRAMMAR)


def parse_with_semantics(sentence, grammar_obj):
    """
    Esegue il parsing di una frase e estrae la rappresentazione semantica
    
    Args:
        sentence: Frase in Quenya da analizzare
        grammar_obj: Grammatica feature-based
        
    Returns:
        Lista di tuple (tree, semantics)
    """
    tokens = sentence.split()
    
    # Crea il parser
    parser = parse.FeatureEarleyChartParser(grammar_obj)
    
    results = []
    for tree in parser.parse(tokens):
        sem = tree.label()['SEM']
        results.append((tree, sem))
    
    return results


def test_quenya_semantic_grammar():
    """Test della grammatica semantica Quenya"""
    print("=" * 80)
    print("TEST: Grammatica Quenya con Semantica (BONUS TRACK)")
    print("=" * 80)
    print()
    
    # Carica la grammatica
    try:
        gram = load_quenya_semantic_grammar()
        print("✓ Grammatica semantica caricata con successo!")
        print()
    except Exception as e:
        print(f"✗ Errore nel caricamento della grammatica: {e}")
        return
    
    # Frasi di test
    test_sentences = [
        {
            'quenya': 'i elda cálë',
            'italiano': "l'elfo risplende",
            'note': 'Determinante + Nome + Verbo intransitivo'
        },
        {
            'quenya': 'i aran tirë i elen',
            'italiano': 'il re guarda la stella',
            'note': 'Soggetto + Verbo transitivo + Oggetto'
        },
        {
            'quenya': 'i aranel tirë i cirya vanya',
            'italiano': 'la principessa guarda la bella nave',
            'note': 'Frase con aggettivo'
        },
        {
            'quenya': 'galadriel lírë',
            'italiano': 'Galadriel canta',
            'note': 'Nome proprio + verbo'
        },
        {
            'quenya': 'elendil cenë i alda alta',
            'italiano': 'Elendil vede il grande albero',
            'note': 'Nome proprio + TV + NP complesso'
        },
        {
            'quenya': 'finrod hirë i macil',
            'italiano': 'Finrod trova la spada',
            'note': 'Nome proprio + TV + NP'
        },
    ]
    
    for test in test_sentences:
        sentence = test['quenya']
        translation = test['italiano']
        note = test['note']
        
        print("=" * 80)
        print(f"Quenya:   {sentence}")
        print(f"Italiano: {translation}")
        print(f"Nota:     {note}")
        print("-" * 80)
        
        try:
            results = parse_with_semantics(sentence, gram)
            
            if results:
                print(f"✓ Parsing riuscito! Trovati {len(results)} parse tree(s).\n")
                
                for idx, (tree, sem) in enumerate(results, 1):
                    print(f"--- Parse Tree {idx} ---")
                    print(tree)
                    print()
                    
                    print(f"--- Rappresentazione Semantica {idx} ---")
                    print(f"Formula logica: {sem}")
                    
                    # Semplifica la formula se possibile
                    try:
                        simplified = sem.simplify()
                        if str(simplified) != str(sem):
                            print(f"Semplificata:   {simplified}")
                    except:
                        pass
                    
                    print()
            else:
                print("✗ Parsing fallito. La frase non è generabile dalla grammatica.\n")
                
        except Exception as e:
            print(f"✗ Errore durante il parsing: {e}\n")
        
        print()


def create_grammar_explanation():
    """
    Crea un documento esplicativo sulla grammatica semantica
    """
    explanation = """
# Grammatica Quenya con Semantica - Spiegazione

## Struttura della Grammatica

La grammatica implementata segue il modello della semantica composizionale,
dove il significato di un'espressione complessa è derivato dal significato
delle sue parti e dal modo in cui queste sono combinate.

### Features Sintattiche

- **NUM**: Numero grammaticale (sg = singolare, pl = plurale)
- **SEM**: Rappresentazione semantica (formula logica)

### Rappresentazione Semantica

La semantica è espressa usando la logica del primo ordine con lambda-calcolo:

1. **Nomi**: λx.P(x) - predicati unari
   - Esempio: 'elda' → λx.elda(x) 
   - "x è un elfo"

2. **Aggettivi**: λP.λx.(P(x) & Q(x)) - modificatori
   - Esempio: 'vanya' → λP.λx.(P(x) & vanya(x))
   - "x ha la proprietà P ed è bello"

3. **Determinanti**: Quantificatori
   - Esempio: 'i' (il/la) → λP.λQ.∃x.(P(x) & Q(x))
   - "esiste un x tale che P(x) e Q(x)"

4. **Verbi Intransitivi**: λx.P(x)
   - Esempio: 'cálë' → λx.cale(x)
   - "x risplende"

5. **Verbi Transitivi**: λX.λx.X(λy.R(x,y))
   - Esempio: 'tirë' → λX.λx.X(λy.tire(x,y))
   - "x guarda y"

### Esempi di Derivazione

#### Frase: "i elda cálë" (l'elfo risplende)

1. 'i' → λP.λQ.∃x.(P(x) & Q(x))
2. 'elda' → λx.elda(x)
3. 'cálë' → λx.cale(x)
4. NP = Det + N → ∃x.elda(x) & ...
5. S = NP + VP → ∃x.(elda(x) & cale(x))

Significato: "Esiste un x tale che x è un elfo e x risplende"

#### Frase: "i aran tirë i elen" (il re guarda la stella)

1. Soggetto: ∃x.aran(x) & ... 
2. Oggetto: ∃y.elen(y)
3. Verbo: tire(x,y)
4. Risultato: ∃x.∃y.(aran(x) & elen(y) & tire(x,y))

Significato: "Esiste un x (re) ed esiste un y (stella) tale che x guarda y"

## Connessione con NLTK

Questa grammatica è ispirata a `simple-sem.fcfg` di NLTK e utilizza:
- Feature structures per agreement
- Lambda calculus per composizione semantica
- Logica del primo ordine per rappresentazione del significato

## Estensioni Possibili

1. Aggiungere casi grammaticali Quenya (nominativo, genitivo, dativo, ecc.)
2. Implementare accordo di numero tra soggetto e verbo
3. Aggiungere preposizioni e sintagmi preposizionali
4. Includere la negazione
5. Gestire frasi coordinate e subordinate
"""
    return explanation


if __name__ == "__main__":
    test_quenya_semantic_grammar()
    
    print("\n" + "=" * 80)
    print("SPIEGAZIONE DELLA GRAMMATICA SEMANTICA")
    print("=" * 80)
    print(create_grammar_explanation())
