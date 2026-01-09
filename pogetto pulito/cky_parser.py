from collections import defaultdict
from typing import List, Tuple, Optional

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
    
    # def __str__(self):
    #     lines = ["regole"]
    #     for head, rules_list in sorted(self.rules.items()):
    #         for body in rules_list:
    #             lines.append(f"{head} -> {' '.join(body)}")
        
    #     lines.append("\nlessico")
    #     for word, pos_list in sorted(self.lexicon.items()):
    #         for pos in pos_list:
    #             lines.append(f"{pos} -> {word}")
        
    #     return "\n".join(lines)

class CKYParser:
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = None
        self.back_pointers = None
        
    # -> Tuple[bool, Optional[List]]
    def parse(self, sentence: str):
        words = sentence.lower().split()
        n = len(words)
        
        # Inizializza la tabella CKY (triangolare superiore)
        # table[i][j] contiene i non-terminali che possono generare words[i:j+1]
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        
        # Inizializza i back-pointers per ricostruire l'albero di parsing
        self.back_pointers = [[defaultdict(list) for _ in range(n)] for _ in range(n)]
        
        # FASE 1: Riempi la diagonale (parole singole)
        for i in range(n):
            word = words[i]
            pos_tags = self.grammar.get_pos_for_word(word)
            
            if not pos_tags:
                print(f"Attenzione: parola '{word}' non trovata nel lessico")
                return False, None
            
            for pos in pos_tags:
                self.table[i][i].add(pos)
                self.back_pointers[i][i][pos].append(('terminal', word))
            
            # Aggiungi chiusura di regole unarie (A → B)
            self._add_unary_closure(i, i)
        
        # FASE 2: Riempi la tabella bottom-up
        # l è la lunghezza dello span (distanza tra i e j)
        for length in range(2, n + 1):  # lunghezza dello span
            for i in range(n - length + 1):  # inizio dello span
                j = i + length - 1  # fine dello span
                
                # Prova tutte le possibili divisioni dello span [i, j]
                for k in range(i, j):  # punto di divisione
                    # Cerca combinazioni B ∈ table[i][k] e C ∈ table[k+1][j]
                    # che possano essere generate da A -> B C
                    
                    for B in self.table[i][k]:
                        for C in self.table[k+1][j]:
                            # Cerca regole A -> B C
                            head_list = self.grammar.get_rules_by_body((B, C))
                            
                            for A in head_list:
                                if A not in self.table[i][j]:
                                    self.table[i][j].add(A)
                                    # Salva il back-pointer per ricostruire l'albero
                                    self.back_pointers[i][j][A].append(('binary', k, B, C))
                
                # Aggiungi chiusura di regole unarie dopo ogni cella
                self._add_unary_closure(i, j)
        
        # FASE 3: Verifica se il simbolo iniziale è nella cella [0][n-1]
        success = self.grammar.start_symbol in self.table[0][n-1]
        
        if success:
            trees = self._build_trees(0, n-1, self.grammar.start_symbol, words)
            return True, trees
        else:
            return False, None
    
    def _add_unary_closure(self, i: int, j: int):
        """
        Aggiunge la chiusura transitiva delle regole unarie (A → B) alla cella [i,j]
        Questo gestisce regole come: NP → Pronoun, Nominal → Noun, etc.
        """
        added = True
        while added:
            added = False
            # Copia per evitare modifiche durante iterazione
            current_symbols = list(self.table[i][j])
            
            for B in current_symbols:
                # Cerca regole unarie A → B
                unary_rules = self.grammar.get_rules_by_body((B,))
                
                for A in unary_rules:
                    if A not in self.table[i][j]:
                        self.table[i][j].add(A)
                        self.back_pointers[i][j][A].append(('unary', B))
                        added = True
    
    def _build_trees(self, i: int, j: int, symbol: str, words: List[str]) -> List:
        """
        Ricostruisce ricorsivamente gli alberi di parsing usando i back-pointers
        
        Args:
            i, j: Indici dello span
            symbol: Simbolo non-terminale da espandere
            words: Lista delle parole della frase
            
        Returns:
            Lista di alberi di parsing (come liste nested)
        """
        trees = []
        
        if i == j:
            # Caso base: foglia (terminale)
            for bp_info in self.back_pointers[i][j][symbol]:
                if bp_info[0] == 'terminal':
                    _, word = bp_info
                    trees.append([symbol, word])
                elif bp_info[0] == 'unary':
                    # Regola unaria: A → B
                    _, B = bp_info
                    subtrees = self._build_trees(i, j, B, words)
                    for subtree in subtrees:
                        trees.append([symbol, subtree])
        else:
            # Caso ricorsivo: nodo interno
            for bp_info in self.back_pointers[i][j][symbol]:
                if bp_info[0] == 'binary':
                    _, k, B, C = bp_info
                    
                    # Ottieni tutti i sottoalberi per B e C
                    left_trees = self._build_trees(i, k, B, words)
                    right_trees = self._build_trees(k+1, j, C, words)
                    
                    # Combina tutti i sottoalberi possibili
                    for left_tree in left_trees:
                        for right_tree in right_trees:
                            trees.append([symbol, left_tree, right_tree])
                
                elif bp_info[0] == 'unary':
                    # Regola unaria: A → B
                    _, B = bp_info
                    subtrees = self._build_trees(i, j, B, words)
                    for subtree in subtrees:
                        trees.append([symbol, subtree])
        
        return trees
    
    def print_table(self, words: List[str]):
        """Stampa la tabella CKY in formato leggibile"""
        n = len(words)
        print("\n=== CKY Table ===")
        print(f"Words: {words}\n")
        
        # Stampa la tabella dall'alto verso il basso
        for length in range(n, 0, -1):
            for i in range(n - length + 1):
                j = i + length - 1
                span = f"[{i},{j}]"
                symbols = ', '.join(sorted(self.table[i][j])) if self.table[i][j] else '∅'
                print(f"{span:8s} {words[i:j+1]}: {symbols}")
            print()
    
    def print_tree(self, tree, indent=0):
        """Stampa un albero di parsing in formato leggibile"""
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
    
    # regole lessicali 
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
    
    grammar.add_lexical_rule('United', 'Proper-Noun')
    grammar.add_lexical_rule('Houston', 'Proper-Noun')
    
    grammar.add_lexical_rule('the', 'Det')
    grammar.add_lexical_rule('a', 'Det')

    grammar.add_lexical_rule('through', 'Preposition')

    grammar.add_lexical_rule('does', 'Aux')
    
    return grammar

def test_l1_grammar():
    
    grammar = create_l1_grammar()
    print(grammar)
    
    parser = CKYParser(grammar)
    
    test_sentences = [
        "book the flight through Houston",
        "does she prefer a morning flight"
    ]
    
    for sentence in test_sentences:
        print(f"Parsing: '{sentence}'")
        
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
    test_l1_grammar()
