import os
import sqlite3
from datetime import datetime # per gestire il formato della data

DB_FILE = "spese.db"
SQL_FILE = "sql/database.sql"

# creazione al primo avvio del database
primo_avvio = not os.path.exists(DB_FILE)

# Apro la connessione al database (se non esiste viene creato vuoto)
conn = sqlite3.connect(DB_FILE)
# Attivo i controlli sulle chiavi esterne
conn.execute("PRAGMA foreign_keys = ON")

# Al primo avvio creo le tabelle e inserisco i dati di esempio da database.sql
if primo_avvio:
    with open(SQL_FILE, encoding="utf-8") as file:
        conn.executescript(file.read())
    conn.commit()

def gestione_categorie():
    nome = input("Nome della categoria: ").strip()

    if nome == "":
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    cursore = conn.execute("SELECT id FROM categorie WHERE nome = ?", (nome,))
    if cursore.fetchone() is not None:
        print("La categoria esiste già.")
        return

    conn.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
    conn.commit()
    print("Categoria inserita correttamente.")

def inserisci_spesa():
    # Funzione per inserire una spesa nel database
    # Data: la richiedo finché non è valida (Invio vuoto = annulla)
    while True:
        data = input("Data (YYYY-MM-DD, Invio per annullare): ").strip()
        if data == "":
            print("Operazione annullata.")
            return
        try:
            datetime.strptime(data, "%Y-%m-%d")
            break
        except ValueError:
            print("Errore: la data deve essere nel formato YYYY-MM-DD.")

    while True:
        testo_importo = input("Importo (Invio per annullare): ").strip().replace(",", ".")
        if testo_importo == "":
            print("Operazione annullata.")
            return
        try:
            importo = float(testo_importo)

        except ValueError:
            print("Errore: l'importo deve essere un numero valido.")
            continue
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
        else:
            break

    while True:
        nome_categoria = input("Categoria (Invio per annullare): ").strip()
        if nome_categoria == "":
            print("Operazione annullata.")
            return
        cursore = conn.execute("SELECT id FROM categorie WHERE nome = ?", (nome_categoria,))
        riga = cursore.fetchone()
        if riga is None:
            print("Errore: la categoria non esiste.")
        else:
            categoria_id = riga[0]
            break

    # Descrizione facoltativa
    descrizione = input("Descrizione (facoltativa): ").strip()
    if descrizione == "":
        descrizione = None

    # Inserimento della spesa con la chiave esterna categoria_id
    conn.execute("INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES (?, ?, ?, ?)",(data, importo, descrizione, categoria_id),)
    conn.commit()
    print("Spesa inserita correttamente.")

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
            gestione_categorie()
        case "2":
            inserisci_spesa()
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

