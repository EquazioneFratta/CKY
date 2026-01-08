"""
Grammatica Quenya per CKY Parser
Basata sulla morfologia e sintassi del Quenya (lingua elfica di Tolkien)

Riferimenti:
- https://eldamo.org/intro-quenya/
- http://ardalambion.immaginario.net/ardalambion/qcourse.htm
"""

from cky_parser import Grammar, CKYParser


def create_quenya_grammar():
    """
    Crea una grammatica context-free per il Quenya
    La grammatica copre costrutti base della lingua:
    - Ordine delle parole: SOV (Soggetto-Oggetto-Verbo) è comune
    - Aggettivi seguono i nomi
    - Genitivi con "o" (di)
    """
    grammar = Grammar()
    grammar.start_symbol = 'S'
    
    # === REGOLE SINTATTICHE ===
    
    # Frasi principali
    grammar.add_rule('S', ('NP', 'VP'))      # Frase con soggetto e predicato
    grammar.add_rule('S', ('NP', 'NP'))      # Frase nominale (copula implicita)
    grammar.add_rule('S', ('VP',))            # Frase senza soggetto esplicito
    
    # Sintagmi nominali
    grammar.add_rule('NP', ('N',))            # Nome semplice
    grammar.add_rule('NP', ('Det', 'N'))      # Determinante + Nome
    grammar.add_rule('NP', ('N', 'Adj'))      # Nome + Aggettivo
    grammar.add_rule('NP', ('Det', 'N'))      # Determinante + Nome + Aggettivo
    grammar.add_rule('NP', ('NAdj',))         # Nome Aggettivato
    grammar.add_rule('NP', ('Det', 'NAdj'))   # Det + Nome Aggettivato
    grammar.add_rule('NP', ('NP', 'PP'))      # NP con complemento preposizionale
    grammar.add_rule('NP', ('Pron',))         # Pronome
    
    # Nome + Aggettivo
    grammar.add_rule('NAdj', ('N', 'Adj'))
    
    # Sintagmi verbali
    grammar.add_rule('VP', ('V',))            # Verbo intransitivo
    grammar.add_rule('VP', ('NP', 'V'))       # OV (Oggetto-Verbo)
    grammar.add_rule('VP', ('V', 'NP'))       # VO (Verbo-Oggetto)
    grammar.add_rule('VP', ('VP', 'PP'))      # VP con complemento
    
    # Sintagmi preposizionali
    grammar.add_rule('PP', ('Prep', 'NP'))    # Preposizione + NP
    
    # === LESSICO QUENYA ===
    
    # Nomi (Sostantivi)
    grammar.add_lexical_rule('elda', 'N')         # elfo
    grammar.add_lexical_rule('eldar', 'N')        # elfi
    grammar.add_lexical_rule('aran', 'N')         # re
    grammar.add_lexical_rule('aranel', 'N')       # principessa
    grammar.add_lexical_rule('tári', 'N')         # regina
    grammar.add_lexical_rule('cirya', 'N')        # nave
    grammar.add_lexical_rule('ciryar', 'N')       # navi
    grammar.add_lexical_rule('elen', 'N')         # stella
    grammar.add_lexical_rule('eleni', 'N')        # stelle
    grammar.add_lexical_rule('silma', 'N')        # argento (poetico)
    grammar.add_lexical_rule('laurë', 'N')        # oro
    grammar.add_lexical_rule('macil', 'N')        # spada
    grammar.add_lexical_rule('parma', 'N')        # libro
    grammar.add_lexical_rule('parmar', 'N')       # libri
    grammar.add_lexical_rule('lómë', 'N')         # notte
    grammar.add_lexical_rule('anar', 'N')         # sole
    grammar.add_lexical_rule('isil', 'N')         # luna
    grammar.add_lexical_rule('alda', 'N')         # albero
    grammar.add_lexical_rule('aldar', 'N')        # alberi
    grammar.add_lexical_rule('ná', 'N')           # cosa
    grammar.add_lexical_rule('nér', 'N')          # uomo
    grammar.add_lexical_rule('neri', 'N')         # uomini
    grammar.add_lexical_rule('nís', 'N')          # donna
    grammar.add_lexical_rule('nissi', 'N')        # donne
    grammar.add_lexical_rule('rocco', 'N')        # cavallo
    grammar.add_lexical_rule('i', 'N')            # rocchi
    grammar.add_lexical_rule('osto', 'N')         # città
    grammar.add_lexical_rule('osteli', 'N')       # città (plurale)
    grammar.add_lexical_rule('lambë', 'N')        # lingua/linguaggio
    grammar.add_lexical_rule('quetta', 'N')       # parola
    grammar.add_lexical_rule('tengwa', 'N')       # lettera
    grammar.add_lexical_rule('ambar', 'N')        # mondo/terra
    grammar.add_lexical_rule('eä', 'N')           # universo
    
    # Aggettivi
    grammar.add_lexical_rule('vanya', 'Adj')      # bello
    grammar.add_lexical_rule('vanima', 'Adj')     # bellissimo
    grammar.add_lexical_rule('calima', 'Adj')     # luminoso
    grammar.add_lexical_rule('morna', 'Adj')      # nero/oscuro
    grammar.add_lexical_rule('carnë', 'Adj')      # rosso
    grammar.add_lexical_rule('lossë', 'Adj')      # bianco (come neve)
    grammar.add_lexical_rule('ninquë', 'Adj')     # bianco/pallido
    grammar.add_lexical_rule('laiqua', 'Adj')     # verde
    grammar.add_lexical_rule('luinë', 'Adj')      # blu
    grammar.add_lexical_rule('malta', 'Adj')      # d'oro/dorato
    grammar.add_lexical_rule('tyelpë', 'Adj')     # d'argento
    grammar.add_lexical_rule('alta', 'Adj')       # grande/alto
    grammar.add_lexical_rule('titta', 'Adj')      # piccolo
    grammar.add_lexical_rule('halla', 'Adj')      # alto
    grammar.add_lexical_rule('anda', 'Adj')       # lungo
    grammar.add_lexical_rule('mára', 'Adj')       # buono/utile
    grammar.add_lexical_rule('laurëa', 'Adj')     # d'oro/dorato
    grammar.add_lexical_rule('ilya', 'Adj')       # ogni/tutto
    
    # Verbi (forme base)
    grammar.add_lexical_rule('ná', 'V')           # è/essere
    grammar.add_lexical_rule('mar-', 'V')         # abitare
    grammar.add_lexical_rule('mat-', 'V')         # mangiare
    grammar.add_lexical_rule('tul-', 'V')         # venire
    grammar.add_lexical_rule('lir-', 'V')         # cantare
    grammar.add_lexical_rule('cen-', 'V')         # vedere
    grammar.add_lexical_rule('quet-', 'V')        # dire/parlare
    grammar.add_lexical_rule('car-', 'V')         # fare
    grammar.add_lexical_rule('tuluva', 'V')       # verrà
    grammar.add_lexical_rule('utúlië', 'V')       # è venuto
    grammar.add_lexical_rule('caluva', 'V')       # risplenderà
    grammar.add_lexical_rule('cálë', 'V')         # risplende
    grammar.add_lexical_rule('tirë', 'V')         # guarda/osserva
    grammar.add_lexical_rule('hiruva', 'V')       # troverà
    grammar.add_lexical_rule('yé', 'V')           # sarà
    grammar.add_lexical_rule('ortanë', 'V')       # ha innalzato
    
    # Pronomi
    grammar.add_lexical_rule('ni', 'Pron')        # io
    grammar.add_lexical_rule('le', 'Pron')        # tu
    grammar.add_lexical_rule('se', 'Pron')        # lui/lei
    grammar.add_lexical_rule('më', 'Pron')        # noi (esclusivo)
    grammar.add_lexical_rule('lye', 'Pron')       # voi
    grammar.add_lexical_rule('te', 'Pron')        # loro
    
    # Determinanti/Articoli
    grammar.add_lexical_rule('i', 'Det')          # il/la/i/le (articolo)
    grammar.add_lexical_rule('in', 'Det')         # il (alternativo)
    
    # Preposizioni
    grammar.add_lexical_rule('mi', 'Prep')        # in
    grammar.add_lexical_rule('nu', 'Prep')        # sotto
    grammar.add_lexical_rule('ar', 'Prep')        # e/con
    grammar.add_lexical_rule('as', 'Prep')        # con
    grammar.add_lexical_rule('na', 'Prep')        # a/verso
    grammar.add_lexical_rule('o', 'Prep')         # di (genitivo)
    grammar.add_lexical_rule('ó', 'Prep')         # da/di
    
    return grammar


def create_quenya_test_sentences():
    """
    Crea frasi di test in Quenya con traduzione
    """
    return [
        {
            'quenya': 'i elda ná vanya',
            'italiano': "l'elfo è bello",
            'note': 'Frase copulativa base'
        },
        {
            'quenya': 'i aran cálë',
            'italiano': 'il re risplende',
            'note': 'Soggetto + verbo intransitivo'
        },
        {
            'quenya': 'i aranel tirë i elen',
            'italiano': 'la principessa guarda la stella',
            'note': 'SVO - Soggetto Verbo Oggetto'
        },
        {
            'quenya': 'i cirya vanya',
            'italiano': 'la nave bella',
            'note': 'Nome + aggettivo'
        },
        {
            'quenya': 'i eldar lir-',
            'italiano': 'gli elfi cantano',
            'note': 'Soggetto plurale + verbo'
        },
        {
            'quenya': 'elen calima',
            'italiano': 'stella luminosa',
            'note': 'Nome + aggettivo senza articolo'
        },
    ]


def test_quenya_grammar():
    """Test della grammatica Quenya"""
    print("=" * 70)
    print("TEST: Grammatica Quenya (Lingua Elfica)")
    print("=" * 70)
    print()
    
    grammar = create_quenya_grammar()
    print("Grammatica Quenya caricata!")
    print(f"Regole sintattiche: {len(grammar.rules)}")
    print(f"Voci lessicali: {len(grammar.lexicon)}")
    print()
    
    parser = CKYParser(grammar)
    
    test_sentences = create_quenya_test_sentences()
    
    for test in test_sentences:
        sentence = test['quenya']
        translation = test['italiano']
        note = test['note']
        
        print(f"\n{'=' * 70}")
        print(f"Quenya:   {sentence}")
        print(f"Italiano: {translation}")
        print(f"Nota:     {note}")
        print('=' * 70)
        
        success, trees = parser.parse(sentence)
        
        words = sentence.lower().split()
        parser.print_table(words)
        
        if success:
            print(f"✓ Parsing riuscito! Trovati {len(trees)} albero/i di parsing.\n")
            for idx, tree in enumerate(trees, 1):
                print(f"--- Parse Tree {idx} ---")
                parser.print_tree(tree)
                print()
        else:
            print("✗ Parsing fallito. La frase non è generabile dalla grammatica.\n")


if __name__ == "__main__":
    test_quenya_grammar()
