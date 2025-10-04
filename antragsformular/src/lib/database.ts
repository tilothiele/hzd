import sqlite3 from 'sqlite3';
import path from 'path';

// Datenbankpfad
const DB_PATH = path.join(process.cwd(), 'data', 'applications.db');

export interface ApplicationRecord {
  email: string;
  creationDate: string;
  uuid: string;
  payload: string;
}

class DatabaseService {
  private db: sqlite3.Database | null = null;

  constructor() {
    this.initializeDatabase();
  }

  private async initializeDatabase(): Promise<void> {
    return new Promise((resolve, reject) => {
      // Erstelle das data Verzeichnis falls es nicht existiert
      import('fs').then(fs => {
        const dataDir = path.dirname(DB_PATH);
        if (!fs.existsSync(dataDir)) {
          fs.mkdirSync(dataDir, { recursive: true });
        }

        this.db = new sqlite3.Database(DB_PATH, (err) => {
          if (err) {
            console.error('Fehler beim Öffnen der Datenbank:', err);
            reject(err);
            return;
          }
          console.log('SQLite Datenbank verbunden:', DB_PATH);
          this.createTables().then(resolve).catch(reject);
        });
      }).catch(reject);
    });
  }

  private async createTables(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Datenbank nicht initialisiert'));
        return;
      }

      const createTableSQL = `
        CREATE TABLE IF NOT EXISTS applications (
          email VARCHAR(100) PRIMARY KEY,
          creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
          uuid VARCHAR(20) NOT NULL,
          payload TEXT NOT NULL
        );
      `;

      const createIndexSQL = `
        CREATE INDEX IF NOT EXISTS idx_applications_creation_date ON applications(creationDate);
        CREATE INDEX IF NOT EXISTS idx_applications_uuid ON applications(uuid);
      `;

      this.db.exec(createTableSQL, (err) => {
        if (err) {
          console.error('Fehler beim Erstellen der Tabelle:', err);
          reject(err);
          return;
        }

        this.db!.exec(createIndexSQL, (err) => {
          if (err) {
            console.error('Fehler beim Erstellen der Indizes:', err);
            reject(err);
            return;
          }
          console.log('Datenbanktabellen erstellt');
          resolve();
        });
      });
    });
  }

  async insertApplication(email: string, uuid: string, payload: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Datenbank nicht initialisiert'));
        return;
      }

      const sql = `
        INSERT OR REPLACE INTO applications (email, uuid, payload, creationDate)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
      `;

      this.db.run(sql, [email, uuid, payload], function(err) {
        if (err) {
          console.error('Fehler beim Einfügen der Anwendung:', err);
          reject(err);
          return;
        }
        console.log(`Anwendung eingefügt: ${email} (ID: ${this.lastID})`);
        resolve();
      });
    });
  }

  async getApplicationByEmail(email: string): Promise<ApplicationRecord | null> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Datenbank nicht initialisiert'));
        return;
      }

      const sql = 'SELECT * FROM applications WHERE email = ?';

      this.db.get(sql, [email], (err, row: ApplicationRecord | undefined) => {
        if (err) {
          console.error('Fehler beim Abrufen der Anwendung:', err);
          reject(err);
          return;
        }
        resolve(row || null);
      });
    });
  }

  async getApplicationByUuid(uuid: string): Promise<ApplicationRecord | null> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Datenbank nicht initialisiert'));
        return;
      }

      const sql = 'SELECT * FROM applications WHERE uuid = ?';

      this.db.get(sql, [uuid], (err, row: ApplicationRecord | undefined) => {
        if (err) {
          console.error('Fehler beim Abrufen der Anwendung:', err);
          reject(err);
          return;
        }
        resolve(row || null);
      });
    });
  }

  async getAllApplications(limit: number = 100, offset: number = 0): Promise<ApplicationRecord[]> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Datenbank nicht initialisiert'));
        return;
      }

      const sql = `
        SELECT * FROM applications 
        ORDER BY creationDate DESC 
        LIMIT ? OFFSET ?
      `;

      this.db.all(sql, [limit, offset], (err, rows: ApplicationRecord[]) => {
        if (err) {
          console.error('Fehler beim Abrufen aller Anwendungen:', err);
          reject(err);
          return;
        }
        resolve(rows || []);
      });
    });
  }

  async deleteApplication(email: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Datenbank nicht initialisiert'));
        return;
      }

      const sql = 'DELETE FROM applications WHERE email = ?';

      this.db.run(sql, [email], function(err) {
        if (err) {
          console.error('Fehler beim Löschen der Anwendung:', err);
          reject(err);
          return;
        }
        console.log(`Anwendung gelöscht: ${email} (${this.changes} Zeilen betroffen)`);
        resolve();
      });
    });
  }

  async applicationExists(email: string): Promise<boolean> {
    const application = await this.getApplicationByEmail(email);
    return application !== null;
  }

  async close(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        resolve();
        return;
      }

      this.db.close((err) => {
        if (err) {
          console.error('Fehler beim Schließen der Datenbank:', err);
          reject(err);
          return;
        }
        console.log('Datenbankverbindung geschlossen');
        this.db = null;
        resolve();
      });
    });
  }
}

// Singleton-Instanz
let databaseService: DatabaseService | null = null;

export function getDatabaseService(): DatabaseService {
  if (!databaseService) {
    databaseService = new DatabaseService();
  }
  return databaseService;
}

// Graceful shutdown
process.on('SIGINT', async () => {
  if (databaseService) {
    await databaseService.close();
  }
  process.exit(0);
});

process.on('SIGTERM', async () => {
  if (databaseService) {
    await databaseService.close();
  }
  process.exit(0);
});
