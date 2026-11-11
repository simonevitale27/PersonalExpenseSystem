CREATE TABLE categorie (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE spese(
    id INTEGER PRIMARY KEY,
    data TEXT NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    descrizione TEXT,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

CREATE TABLE budget(
    id INTEGER PRIMARY KEY,
    mese TEXT NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    categoria_id INTEGER NOT NULL,
    UNIQUE (mese, categoria_id),
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);