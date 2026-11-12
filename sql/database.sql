CREATE TABLE categorie (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE COLLATE NOCASE
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


-- DATI DI ESEMPIO

-- Categorie
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Svago');
INSERT INTO categorie (nome) VALUES ('Bollette');

-- Spese di gennaio 2026
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-01-03', 50.00, 'Abbonamento bus', 2);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-01-05', 120.50, 'Spesa supermercato', 1);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-01-12', 85.00, 'Spesa settimanale', 1);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-01-15', 25.00, 'Pranzo', 1);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-01-20', 70.00, 'Benzina', 2);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-01-26', 90.00, 'Spesa mensile', 1);

-- Spese di febbraio 2026  
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-02-04', 95.40, 'Spesa supermercato', 1);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-02-08', 15.00, NULL, 2);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-02-10', 45.00, 'Concerto', 3);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-02-15', 80.00, 'Bolletta luce', 4);
INSERT INTO spese (data, importo, descrizione, categoria_id) VALUES ('2026-02-22', 30.00, 'Cinema', 3);

-- Budget mensili
INSERT INTO budget (mese, importo, categoria_id) VALUES ('2026-01', 300, 1);
INSERT INTO budget (mese, importo, categoria_id) VALUES ('2026-01', 150, 2);
INSERT INTO budget (mese, importo, categoria_id) VALUES ('2026-02', 300, 1);
INSERT INTO budget (mese, importo, categoria_id) VALUES ('2026-02', 60, 3);