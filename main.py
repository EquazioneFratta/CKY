"""
MAIN TEST FILE
Progetto di Tecnologie del Linguaggio Naturale
Implementazione CKY per grammatiche Context-Free con applicazione al Quenya

Autore: [Il tuo nome]
Corso: Tecnologie del Linguaggio Naturale - Informatica
Anno Accademico: 2023/2024
"""

import sys
from cky_parser import test_l1_grammar
from quenya_grammar import test_quenya_grammar
from quenya_semantic import test_quenya_semantic_grammar


def print_header():
    """Stampa l'intestazione del progetto"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  PROGETTO: Algoritmo CKY per Parsing di Grammatiche Context-Free  ".center(78) + "║")
    print("║" + "  con Applicazione alla Lingua Quenya (Elfico)  ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Tecnologie del Linguaggio Naturale - Informatica 2023/2024  ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")


def print_menu():
    """Stampa il menu di scelta"""
    print("\n" + "=" * 80)
    print("MENU - Seleziona il test da eseguire:")
    print("=" * 80)
    print("1. Test Parte A: Implementazione CKY from scratch")
    print("2. Test Parte B: CKY sulla grammatica L1 di Jurafsky & Martin")
    print("3. Test Parte C: CKY su grammatica Quenya custom")
    print("4. Test Parte D (BONUS): Grammatica Quenya con semantica NLTK")
    print("5. Esegui tutti i test")
    print("0. Esci")
    print("=" * 80)


def run_test_a():
    """Test Parte A: Implementazione CKY"""
    print("\n" + "▶" * 40)
    print("PARTE A: IMPLEMENTAZIONE CKY FROM SCRATCH")
    print("▶" * 40 + "\n")
    print("L'implementazione CKY si trova nel file: cky_parser.py")
    print("\nCaratteristiche principali:")
    print("- Algoritmo CKY completo con triplo ciclo nested")
    print("- Struttura dati: tabella triangolare superiore")
    print("- Back-pointers per ricostruzione alberi di parsing")
    print("- Supporto per grammatiche in Forma Normale di Chomsky (CNF)")
    print("- Generazione di tutti i possibili parse trees")
    print("\nPer vedere l'implementazione in azione, esegui il test B o C.")
    input("\nPremi INVIO per continuare...")


def run_test_b():
    """Test Parte B: Grammatica L1"""
    print("\n" + "▶" * 40)
    print("PARTE B: TEST SU GRAMMATICA L1 (JURAFSKY & MARTIN)")
    print("▶" * 40 + "\n")
    test_l1_grammar()
    input("\nPremi INVIO per continuare...")


def run_test_c():
    """Test Parte C: Grammatica Quenya"""
    print("\n" + "▶" * 40)
    print("PARTE C: TEST SU GRAMMATICA QUENYA")
    print("▶" * 40 + "\n")
    test_quenya_grammar()
    input("\nPremi INVIO per continuare...")


def run_test_d():
    """Test Parte D: Grammatica Quenya con semantica"""
    print("\n" + "▶" * 40)
    print("PARTE D (BONUS): GRAMMATICA QUENYA CON SEMANTICA")
    print("▶" * 40 + "\n")
    
    try:
        test_quenya_semantic_grammar()
    except ImportError:
        print("✗ NLTK non è installato. Per eseguire questa parte installare NLTK:")
        print("  pip install nltk")
    except Exception as e:
        print(f"✗ Errore durante l'esecuzione: {e}")
    
    input("\nPremi INVIO per continuare...")


def run_all_tests():
    """Esegue tutti i test in sequenza"""
    run_test_a()
    run_test_b()
    run_test_c()
    run_test_d()
    
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  TUTTI I TEST COMPLETATI!  ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    input("\nPremi INVIO per tornare al menu...")


def main():
    """Funzione principale"""
    print_header()
    
    print("Benvenuto nel progetto CKY per il Quenya!")
    print("\nQuesto progetto implementa:")
    print("  ✓ Algoritmo CKY completo from scratch")
    print("  ✓ Test sulla grammatica L1 di Jurafsky & Martin")
    print("  ✓ Grammatica custom per la lingua Quenya (Elfico di Tolkien)")
    print("  ✓ BONUS: Grammatica Quenya con rappresentazione semantica (NLTK)")
    
    while True:
        print_menu()
        
        try:
            choice = input("\nInserisci la tua scelta (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 Arrivederci! Namárië! (Addio in Quenya)")
                sys.exit(0)
            elif choice == '1':
                run_test_a()
            elif choice == '2':
                run_test_b()
            elif choice == '3':
                run_test_c()
            elif choice == '4':
                run_test_d()
            elif choice == '5':
                run_all_tests()
            else:
                print("\n✗ Scelta non valida. Riprova.")
                input("Premi INVIO per continuare...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Arrivederci! Namárië!")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Errore: {e}")
            input("Premi INVIO per continuare...")


if __name__ == "__main__":
    main()
