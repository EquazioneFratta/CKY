import nltk
from nltk import grammar, parse

QUENYA_SEMANTIC_GRAMMAR = r"""
% start S

# frasi base: NP + VP
S[SEM=<?subj(?vp)>] -> NP[NUM=?n,SEM=?subj] VP[NUM=?n,SEM=?vp]

# frasi solo VP
S[SEM=?vp] -> VP[SEM=?vp]

# sintagmi nominali
NP[NUM=?n,SEM=<?det(?nom)>] -> Det[NUM=?n,SEM=?det] Nom[NUM=?n,SEM=?nom]
NP[NUM=?n,SEM=?nom] -> Nom[NUM=?n,SEM=?nom]

# nominali
Nom[NUM=?n,SEM=?nom] -> N[NUM=?n,SEM=?nom]

# sintagmi verbali
# verbo transitivo: V + NP
VP[NUM=?n,SEM=<?v(?obj)>] -> TV[NUM=?n,SEM=?v] NP[SEM=?obj]

# verbo ditransitivo: V + NP + NP (oggetto indiretto + oggetto diretto)
VP[NUM=?n,SEM=<?v(?obj1,?obj2)>] -> DTV[NUM=?n,SEM=?v] NP[SEM=?obj1] NP[SEM=?obj2]

# determianti
Det[NUM=sg,SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'i'  

# nomi
N[NUM=sg,SEM=<\x.hesto(x)>] -> 'hesto'     
N[NUM=sg,SEM=<\x.macil(x)>] -> 'macil'     
N[NUM=sg,SEM=<\x.aran(x)>] -> 'aran'       
N[NUM=pl,SEM=<\x.aiwi(x)>] -> 'aiwi'       
N[NUM=sg,SEM=<\x.atan(x)>] -> 'atan'       
N[NUM=sg,SEM=<\x.elda(x)>] -> 'eldan'      
N[NUM=sg,SEM=<\x.tecil(x)>] -> 'tecil'     

# verbi transitivi 
TV[NUM=sg,SEM=<\X x.X(\y.have(x,y))>] -> 'samë'

TV[NUM=sg,SEM=<\X x.X(\y.watch(x,y))>] -> 'tíra'

# verbi distransitivi
DTV[NUM=sg,SEM=<\Y X x.X(\z.Y(\y.give(x,y,z)))>] -> 'antanë'
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