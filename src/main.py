import os
import sqlite3

DB_FILE = "spese.db"
SQL_FILE = "sql/database.sql"

# creazione al primo avvio del database
primo_avvio = not os.path.exists(DB_FILE)

conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA foreign_keys = ON")

if primo_avvio:
    with open(SQL_FILE, encoding="utf-8") as file:
        conn.executescript(file.read())
    conn.commit()

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

    # Ho realizzato "switch" richiesto dalla traccia con il costrutto match-case, 
    # trovato dopo delle ricerche disponibile da Python 3.10
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
            conn.close()
            break
        case _:
            print("Scelta non valida. Riprovare.")

