from cky_parser import Grammar, CKYParser

def create_quenya_grammar():
 
    grammar = Grammar()
    grammar.start_symbol = 'S'
    
    grammar.add_rule('S', ('NP', 'VP'))
    grammar.add_rule('S', ('Aux-NP', 'VP'))
    grammar.add_rule('Aux-NP', ('Aux', 'NP'))
    
    grammar.add_rule('S', ('VP',)) 
    
    grammar.add_rule('NP', ('Pronoun',))  
    grammar.add_rule('NP', ('Proper-Noun',))
    grammar.add_rule('NP', ('Det', 'Nominal'))
    grammar.add_rule('Nominal', ('Noun',))
    grammar.add_rule('Nominal', ('Nominal', 'Noun'))
    grammar.add_rule('Nominal', ('Nominal', 'PP'))
    
    grammar.add_rule('VP', ('Verb',))
    grammar.add_rule('VP', ('Verb', 'NP'))
    grammar.add_rule('VP', ('Verb-NP', 'PP'))
    grammar.add_rule('Verb-NP', ('Verb', 'NP'))
    
    grammar.add_rule('VP', ('Verb', 'PP'))
    grammar.add_rule('VP', ('VP', 'PP'))
    grammar.add_rule('PP', ('Preposition', 'NP'))
    
    # regole lessicali 
    
    grammar.add_lexical_rule('elda', 'Noun')         # elf
    grammar.add_lexical_rule('eldar', 'Noun')        # elves
    grammar.add_lexical_rule('aran', 'Noun')         # king
    grammar.add_lexical_rule('macil', 'Noun')        # sword
    grammar.add_lexical_rule('aiwi', 'Noun')         # birds
    grammar.add_lexical_rule('atan', 'Noun')         # man
    grammar.add_lexical_rule('tecil', 'Noun')        # pen
    grammar.add_lexical_rule('hesto', 'Noun')        # captain
    
    grammar.add_lexical_rule('lumba', 'Noun')        # captain
    
    grammar.add_lexical_rule('antanë', 'Verb')       # gave
    grammar.add_lexical_rule('samë', 'Verb')         # has
    grammar.add_lexical_rule('tíra', 'Verb')         # is watching
    grammar.add_lexical_rule('nanye', 'Verb')        # I am

    grammar.add_lexical_rule('i', 'Det')             # the
    
    return grammar

def test_quenya_grammar():
    print("=" * 70)
    print("TEST: Grammatica Quenya (Lingua Elfica)")
    print("=" * 70)
    
    grammar = create_quenya_grammar()
    print("Grammatica Quenya caricata!")
    print(f"Regole sintattiche: {len(grammar.rules)}")
    print(f"Voci lessicali: {len(grammar.lexicon)}")
    
    parser = CKYParser(grammar)
    
    test_sentences = [
        "I hesto samë macil",
        "I aran tíra aiwi",
        "Nanye lumba",
        "Nálmë eldar",
        "I atan antanë i eldan tecil"
    ]
    
    for sentence in test_sentences:    
        
        print(f"\n{'=' * 70}")
        print(f"Parsing:   {sentence}")
        print('=' * 70)
        
        success, trees = parser.parse(sentence)
        
        words = sentence.lower().split()
        parser.print_table(words)
        
        if success:
            print(f"Parsing riuscito! Trovati {len(trees)} albero/i di parsing.\n")
            for idx, tree in enumerate(trees, 1):
                print(f"--- Parse Tree {idx} ---")
                parser.print_tree(tree)
                print()
        else:
            print("Parsing fallito. La frase non è generabile dalla grammatica.\n")


if __name__ == "__main__":
    test_quenya_grammar()
