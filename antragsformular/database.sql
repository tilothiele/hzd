-- SQLite Database Schema für HZD Antragsformular
-- Erstellt die Tabelle für Anträge

CREATE TABLE IF NOT EXISTS applications (
    email VARCHAR(100) PRIMARY KEY,
    creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    uuid VARCHAR(20) NOT NULL,
    payload TEXT NOT NULL
);

-- Index für bessere Performance
CREATE INDEX IF NOT EXISTS idx_applications_creation_date ON applications(creationDate);
CREATE INDEX IF NOT EXISTS idx_applications_uuid ON applications(uuid);
