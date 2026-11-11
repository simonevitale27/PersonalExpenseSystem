print("Benvenuto nel sistema di gestione delle Spese Personali!")
while True:
    print("---------------------------------")
    print("SISTEMA SPESE PERSONALI")
    print("---------------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("---------------------------------")
    scelta = input("Inserisci la tua scelta: ")

    #Ho realizzato "switch" richiesto dalla traccia con il costrutto match-case, trovato dopo delle ricerche
    match scelta:
        case "1":
            print("Hai selezionato l'opzione: Gestione Categorie")
        case "2":
            print("Hai selezionato l'opzione: Inserisci Spesa")
        case "3":
            print("Hai selezionato l'opzione: Definisci Budget Mensile")
        case "4":
            print("Hai selezionato l'opzione: Visualizza Report")
        case "5":
            print("Arrivederci!")
            break
        case _:
            print("Scelta non valida. Riprovare.")

