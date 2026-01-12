from cky_parser import Grammar, CKYParser

def create_quenya_grammar():
 
    grammar = Grammar()
    grammar.start_symbol = 'S'
    
    grammar.add_rule('S', ('NP', 'VP'))
    grammar.add_rule('S', ('Verb', 'Adj')) 
    grammar.add_rule('S', ('Verb', 'NP')) 
      
    grammar.add_rule('NP', ('Det', 'Noun'))  
    grammar.add_rule('NP', ('Noun',))  
    
    grammar.add_rule('VP', ('Verb', 'NP')) 
    grammar.add_rule('VP', ('Verb', 'NP-NP')) 
    grammar.add_rule('VP', ('Verb-NP', 'PP')) 
    grammar.add_rule('NP-NP', ('NP', 'NP')) 
    
    grammar.add_lexical_rule('samë', 'Verb')        # has
    grammar.add_lexical_rule('tíra', 'Verb')        # watching
    grammar.add_lexical_rule('nanye', 'Verb')       # i am not
    grammar.add_lexical_rule('nálmë', 'Verb')       # we are 
    grammar.add_lexical_rule('antanë', 'Verb')      # gave
    
    grammar.add_lexical_rule('hesto', 'Noun')       # captain
    grammar.add_lexical_rule('macil', 'Noun')       # sword
    grammar.add_lexical_rule('aran', 'Noun')        # king
    grammar.add_lexical_rule('aiwi', 'Noun')        # birds
    grammar.add_lexical_rule('eldar', 'Noun')       # elves
    grammar.add_lexical_rule('atan', 'Noun')        # man
    grammar.add_lexical_rule('eldan', 'Noun')       # elf 
    grammar.add_lexical_rule('tecil', 'Noun')       # pen
    
    grammar.add_lexical_rule('lumba', 'Adj')        # tired
    
    grammar.add_lexical_rule('i', 'Det')            # the
    return grammar

def test_quenya_grammar():
    grammar = create_quenya_grammar()
    parser = CKYParser(grammar)
    
    test_sentences = [
        "I hesto samë macil",
        "I aran tíra aiwi",
        "Nanye lumba",
        "Nálmë eldar",
        "I atan antanë i eldan tecil"
    ]
    
    for sentence in test_sentences:    
        
        print(f"Parsing:   {sentence}")
        
        success, trees = parser.parse(sentence)
        
        words = sentence.lower().split()
        parser.print_table(words)
        
        if success:
            print(f"Parsing riuscito. Trovati {len(trees)} albero/i di parsing.\n")
            for idx, tree in enumerate(trees, 1):
                print(f"--- Parse Tree {idx} ---")
                parser.print_tree(tree)
                print()
        else:
            print("Parsing fallito.\n")

if __name__ == "__main__":
    test_quenya_grammar()
