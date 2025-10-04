-- SQLite Database Schema für HZD Antragsformular
-- Erstellt die Tabelle für Anträge

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) NOT NULL,
    creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    uuid VARCHAR(20) NULL,
    payload TEXT NULL
);

-- Index für bessere Performance
CREATE INDEX IF NOT EXISTS idx_applications_email ON applications(email);
CREATE INDEX IF NOT EXISTS idx_applications_creation_date ON applications(creationDate);
CREATE INDEX IF NOT EXISTS idx_applications_uuid ON applications(uuid);
