# Sistema di Gestione delle Spese Personali e del Budget

Programma per tenere sotto controllo le proprie spese. Permette di creare
le categorie di spesa, registrare le spese di ogni giorno, fissare un budget mensile
per ogni categoria e vedere dei report che mostrano quanto si è speso e se il budget
è stato rispettato.

Progetto finale di Fondamenti di Informatica, Vitale Simone

## Requisiti

- Python 3.10 o superiore (per il costrutto `match`/`case`)
- Nessuna libreria esterna: solo moduli della libreria standard di Python
  - `sqlite3` – database relazionale SQL
  - `os` – costruisce i percorsi dei file e controlla se il database esiste già
  - `datetime` – verifica che date e mesi inseriti siano validi
  - `math` – controlla che l'importo sia un numero finito

## Installazione

Non è richiesta compilazione: Python è un linguaggio interpretato.

[Link al repository GitHub: lo aggiungiamo dopo la pubblicazione.]

## Avvio

Dalla cartella principale del progetto, eseguire:

```bash
python3 src/main.py
```

Su Windows: `python src/main.py`

Al primo avvio il programma crea il database `spese.db` eseguendo
`sql/database.sql` (tabelle, vincoli e dati di esempio). Dagli avvii successivi
riutilizza lo stesso database, quindi i dati inseriti restano salvati.

## Struttura del progetto

```
PersonalExpenseSystem/
├── src/main.py          – programma principale
├── sql/database.sql     – script SQL di creazione e dati di esempio
├── demo/                – video dimostrativo
└── README.md
```

## Note sulle scelte di implementazione

- **Lo switch richiesto dalla traccia.** Python non ha lo switch del C/C++: al suo
  posto ho usato match/case, disponibile da Python 3.10, che funziona allo stesso
  modo. Il caso "case _"fa da "default" e gestisce le scelte non valide. Allo stesso
  modo, cout e cin sono sostituiti da print() e input().
- **La validazione degli input.** Ogni dato viene controllato appena l'utente lo
  inserisce, se è sbagliato il programma mostra un messaggio di errore
  e lo richiede, senza bloccarsi. Premendo Invio senza scrivere nulla si annulla
  l'operazione e si torna al menu.
- **Doppio controllo sui dati.** Oltre ai controlli in Python, il database ha i suoi
  vincoli (PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK), quindi un
  dato non valido viene rifiutato anche se arrivasse senza passare dal programma.
- **Categorie senza doppioni.** I nomi delle categorie non distinguono maiuscole e
  minuscole (COLLATE NOCASE): "Casa" e "casa" sono la stessa categoria.
- **Budget inserito o aggiornato.** Se per una categoria e un mese esiste già un
  budget, il programma lo aggiorna invece di crearne un secondo.
