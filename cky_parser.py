from collections import defaultdict
from typing import List, Tuple

#grammatica context-free in forma normale di Chomsky (CNF)
class Grammar:
    
    def __init__(self):
        self.rules = defaultdict(list)  # regola di produzione, es. NP -> [(Det, Nominal), ...] 
        self.lexicon = defaultdict(list)  # produzione lessicale, es. dog -> [N]
        self.start_symbol = 'S'
        
    def add_rule(self, head: str, body: Tuple):
        self.rules[head].append(body)
        
    def add_lexical_rule(self, word: str, pos: str):
        if pos not in self.lexicon[word]:
            self.lexicon[word].append(pos)
    
    def get_pos_for_word(self, word: str) -> List[str]:
        return self.lexicon.get(word.lower(), [])
    
    def get_rules_by_body(self, body: Tuple) -> List[str]:
        result = []
        for head, rules in self.rules.items():
            if body in rules:
                result.append(head)
        return result
    
    def is_cnf(self) -> bool:
        for _, rules_list in self.rules.items():
            for body in rules_list:
                if len(body) > 2:
                    return False
                if len(body) == 2:
                    # deve essere A -> B C (due non-terminali)<
                    if not all(symbol[0].isupper() for symbol in body):
                        return False
        return True
class CKYParser:
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = None
        self.back_pointers = None
        
    def parse(self, sentence: str):
        words = sentence.lower().split()
        n = len(words)
        
        # table[i][j] contiene i non-terminali che possono generare words[i:j+1]
        self.table = [[set() for _ in range(n+1)] for _ in range(n+1)]
        # inizializza i puntatori per ricostruire l'albero di parsing
        self.back_pointers = [[defaultdict(list) for _ in range(n+1)] for _ in range(n+1)]
        
        # cicla sulle colonne
        for j in range(1, n + 1):
            word = words[j-1]
            
            # riempie la diagonale
            for A in self.grammar.get_pos_for_word(word):
                self.table[j-1][j].add(A)
                self.back_pointers[j-1][j][A].append(('terminal', word))
            
            self.add_unary_closure(j-1, j)
            
            #j: numero di parole considerate
            #i: punto da cui parte [0, 1, ...]
            
            # riempie la riga i nella colonna j 
            for i in range(j - 2, -1, -1): 
                
                # cicla sui possibili punti di split
                for k in range(i + 1, j):
                    
                    for B in self.table[i][k]:
                        for C in self.table[k][j]:
                            lhs_list = self.grammar.get_rules_by_body((B, C))
                            
                            for A in lhs_list:
                                self.table[i][j].add(A)
                                # Salvataggio back-pointer coerente con gli indici
                                self.back_pointers[i][j][A].append(('binary', k, B, C))
                
                self.add_unary_closure(i, j)
        
        success = self.grammar.start_symbol in self.table[0][n]
        
        if success:
            trees = self.build_trees(0, n, self.grammar.start_symbol, words)
            return True, trees
        else:
            return False, None
        
    # gestisce regole come: NP → Pronoun, Nominal → Noun, etc.
    def add_unary_closure(self, i: int, j: int):
        added = True
        while added:
            added = False
            current_symbols = list(self.table[i][j])
            
            for B in current_symbols:
                # cerca regole unarie A → B
                unary_rules = self.grammar.get_rules_by_body((B,))
                
                for A in unary_rules:
                    if A not in self.table[i][j]:
                        self.table[i][j].add(A)
                        self.back_pointers[i][j][A].append(('unary', B))
                        added = True
    
    def build_trees(self, i: int, j: int, symbol: str, words: List[str]) -> List:
        trees = []
        
        if j - i == 1:
            # caso base: foglia (terminale)
            for bp_info in self.back_pointers[i][j][symbol]:
                if bp_info[0] == 'terminal':
                    _, word = bp_info
                    trees.append([symbol, word])
                elif bp_info[0] == 'unary':
                    _, B = bp_info
                    subtrees = self.build_trees(i, j, B, words)
                    for subtree in subtrees:
                        trees.append([symbol, subtree])
        else:
            # caso ricorsivo: nodo interno
            for bp_info in self.back_pointers[i][j][symbol]:
                if bp_info[0] == 'binary':
                    _, k, B, C = bp_info
                    
                    left_trees = self.build_trees(i, k, B, words)
                    right_trees = self.build_trees(k, j, C, words)
                    
                    for left_tree in left_trees:
                        for right_tree in right_trees:
                            trees.append([symbol, left_tree, right_tree])
                
                elif bp_info[0] == 'unary':
                    _, B = bp_info
                    subtrees = self.build_trees(i, j, B, words)
                    for subtree in subtrees:
                        trees.append([symbol, subtree])
        
        return trees
    
    def print_table(self, words: List[str]):
        n = len(words)
        print("\nTabella CKY")
        print(f"parole: {words}\n")
        
        for length in range(n, 0, -1):
            for i in range(n - length + 1):
                j = i + length
                span = f"[{i},{j}]"
                symbols = ', '.join(sorted(self.table[i][j])) if self.table[i][j] else '∅'
                print(f"{span:8s} {words[i:j]}: {symbols}")
            print()
    
    def print_tree(self, tree, indent=0):
        if isinstance(tree, list):
            if len(tree) == 2 and isinstance(tree[1], str):
                # Foglia
                print("  " * indent + f"[{tree[0]} {tree[1]}]")
            else:
                # Nodo interno
                print("  " * indent + f"[{tree[0]}")
                for subtree in tree[1:]:
                    self.print_tree(subtree, indent + 1)
                print("  " * indent + "]")
        else:
            print("  " * indent + str(tree))
            
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
