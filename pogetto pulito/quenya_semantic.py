import nltk
from nltk import grammar, parse

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

def parse_with_semantics(sentence, grammar_obj):
    tokens = sentence.lower().split()
    parser = parse.FeatureEarleyChartParser(grammar_obj)
    
    results = []
    for tree in parser.parse(tokens):
        sem = tree.label()['SEM']
        results.append((tree, sem))
    
    return results


def test_quenya_semantic():    
    gram = grammar.FeatureGrammar.fromstring(QUENYA_SEMANTIC_GRAMMAR)
    
    test_sentences = [
        "I hesto samë macil",
        "I aran tíra aiwi",
        "I atan antanë i eldan tecil"
    ]
    
    for sentence in test_sentences:
        print(f"Parsing: {sentence}")

        results = parse_with_semantics(sentence, gram)
        
        if results:            
            for tree, sem in results:

                print(f"--- Parse Tree ---")
                print(tree)
                
                print(f"--- Rappresentazione Semantica ---")
                print(f"Formula: {sem}")
                
                try:
                    simplified = sem.simplify()
                    if str(simplified) != str(sem):
                        print(f"Semplificata: {simplified}")
                except:
                    pass
                
                print()
    
if __name__ == "__main__":
    test_quenya_semantic()