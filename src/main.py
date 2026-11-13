import os
import sqlite3
import math
from datetime import datetime # per gestire il formato della data

# Cartella del progetto, ricavata dalla posizione di questo file (src/main.py),
# così il programma trova i suoi file da qualunque cartella venga avviato
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(CARTELLA_PROGETTO, "spese.db")
SQL_FILE = os.path.join(CARTELLA_PROGETTO, "sql", "database.sql")

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
        if not math.isfinite(importo):
            print("Errore: l'importo deve essere un numero valido.")
        elif importo <= 0:
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

def definisci_budget():
    while True:
        mese = input("Mese (YYYY-MM, Invio per annullare): ").strip()
        if mese == "":
            print("Operazione annullata.")
            return
        try:
            datetime.strptime(mese, "%Y-%m")
            break
        except ValueError:
            print("Errore: il mese deve essere nel formato YYYY-MM.")

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
        if not math.isfinite(importo):
            print("Errore: l'importo deve essere un numero valido.")
        elif importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
        else:
            break

    # controllo esistenza Budget
    cursore = conn.execute(
        "SELECT id FROM budget WHERE mese = ? AND categoria_id = ?",
        (mese, categoria_id),
    )
    if cursore.fetchone() is None:
        conn.execute("INSERT INTO budget (mese, importo, categoria_id) VALUES (?, ?, ?)",(mese, importo, categoria_id),)
    else:
        conn.execute("UPDATE budget SET importo = ? WHERE mese = ? AND categoria_id = ?", (importo, mese, categoria_id))

    conn.commit()
    print("Budget mensile salvato correttamente.")

def report_totale_categorie():
    # Report della somma delle spese raggruppate per categoria
    cursore = conn.execute(
        "SELECT categorie.nome, SUM(spese.importo) "
        "FROM spese "
        "JOIN categorie ON spese.categoria_id = categorie.id "
        "GROUP BY categorie.nome "
        "ORDER BY categorie.nome"
    )
    righe = cursore.fetchall()

    if len(righe) == 0:
        print("Nessuna spesa registrata.")
        return

    print(f"{'Categoria':.<20}Totale Speso")
    for nome, totale in righe:
        print(f"{nome:.<20}{totale:.2f}")

def report_mensile_budget():
    # Report 2: per budget, totale speso nel mese e categoria
    cursore = conn.execute(
        "SELECT budget.mese, categorie.nome, budget.importo, "
        "COALESCE(SUM(spese.importo), 0) "
        "FROM budget "
        "JOIN categorie ON budget.categoria_id = categorie.id "
        "LEFT JOIN spese ON spese.categoria_id = budget.categoria_id "
        "AND substr(spese.data, 1, 7) = budget.mese "
        "GROUP BY budget.id "
        "ORDER BY budget.mese, categorie.nome"
    )
    righe = cursore.fetchall()

    if len(righe) == 0:
        print("Nessun budget definito.")
        return

    for mese, categoria, budget, speso in righe:
        # Confronto con il budget tramite if/else, come richiesto dalla traccia
        if speso > budget:
            stato = "SUPERAMENTO BUDGET"
        else:
            stato = "BUDGET RISPETTATO"

        print()
        print("Mese:", mese)
        print("Categoria:", categoria)
        print(f"Budget: {budget:.2f}")
        print(f"Speso: {speso:.2f}")
        print("Stato:", stato)

def report_elenco_spese():
    # Report 3: tutte le spese per data
    cursore = conn.execute(
        "SELECT spese.data, categorie.nome, spese.importo, spese.descrizione "
        "FROM spese "
        "JOIN categorie ON spese.categoria_id = categorie.id "
        "ORDER BY spese.data, spese.id"
    )
    righe = cursore.fetchall()

    if len(righe) == 0:
        print("Nessuna spesa registrata.")
        return

    print(f"{'Data':<12}{'Categoria':<14}{'Importo':>9}  Descrizione")
    print("-" * 50)
    for data, categoria, importo, descrizione in righe:
        if descrizione is None:
            descrizione = ""
        print(f"{data:<12}{categoria:<14}{importo:>9.2f}  {descrizione}")

def visualizza_report():
    # Sottomenu dei report
    while True:
        print("---------------------------------")
        print("REPORT")
        print("---------------------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("---------------------------------")
        scelta_report = input("Inserisci la tua scelta: ").strip()

        match scelta_report:
            case "1":
                report_totale_categorie()
            case "2":
                report_mensile_budget()
            case "3":
                report_elenco_spese()
            case "4":
                break
            case _:
                print("Scelta non valida. Riprovare.")


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
    scelta = input("Inserisci la tua scelta: ").strip()

    # Ho realizzato "switch" richiesto dalla traccia con il costrutto match-case, 
    # trovato dopo delle ricerche disponibile da Python 3.10
    match scelta:
        case "1":
            gestione_categorie()
        case "2":
            inserisci_spesa()
        case "3":
            definisci_budget()
        case "4":
            visualizza_report()
        case "5":
            print("Arrivederci!")
            conn.close()
            break
        case _:
            print("Scelta non valida. Riprovare.")

