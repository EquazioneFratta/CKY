from cky_parser import CKYParser, Grammar

# crea la grammatica L1 in CNF
def create_l1_grammar():
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
    
    grammar.add_lexical_rule('book', 'Noun')
    grammar.add_lexical_rule('flight', 'Noun')
    grammar.add_lexical_rule('meal', 'Noun')
    grammar.add_lexical_rule('morning', 'Noun')
    
    grammar.add_lexical_rule('book', 'Verb')
    grammar.add_lexical_rule('include', 'Verb')
    grammar.add_lexical_rule('prefer', 'Verb')
    
    
    grammar.add_lexical_rule('I', 'Pronoun')
    grammar.add_lexical_rule('she', 'Pronoun')
    grammar.add_lexical_rule('me', 'Pronoun')
    
    grammar.add_lexical_rule('united', 'Proper-Noun')
    grammar.add_lexical_rule('houston', 'Proper-Noun')
    
    grammar.add_lexical_rule('the', 'Det')
    grammar.add_lexical_rule('a', 'Det')

    grammar.add_lexical_rule('through', 'Preposition')

    grammar.add_lexical_rule('does', 'Aux')
    
    return grammar

def test_l1_grammar():
    grammar = create_l1_grammar()
    parser = CKYParser(grammar)
    
    test_sentences = [
        "Book the flight through Houston",
        "Does she prefer a morning flight"
    ]
    
    for sentence in test_sentences:
        print(f"Parsing: '{sentence}'")
        
        success, trees = parser.parse(sentence)
        
        words = sentence.lower().split()
        parser.print_table(words)
        
        if success:
            print(f"Parsing riuscito. Trovati {len(trees)} albero/i di parsing.\n")
            for i, tree in enumerate(trees, 1):
                print(f"--- Parse Tree {i} ---")
                parser.print_tree(tree)
        else:
            print("Parsing fallito.\n")

if __name__ == "__main__":
    test_l1_grammar()
