import { getServerDatabaseService, generateServerUuid, serverLog } from '../lib/server-only';
import { FormData } from '../types/formData';
import { ApplicationSubmissionRequest, ApplicationSubmissionResponse } from '../types/api';

class ApplicationService {
  private db = getServerDatabaseService();

  /**
   * Speichert eine neue Antragsanmeldung in der Datenbank
   */
  async submitApplication(request: ApplicationSubmissionRequest): Promise<ApplicationSubmissionResponse> {
    try {
      const { formData, uuid } = request;

      // Validierung
      if (!formData.email || !formData.email.trim()) {
        return {
          success: false,
          message: 'E-Mail-Adresse ist erforderlich'
        };
      }

      if (!uuid || !uuid.trim()) {
        return {
          success: false,
          message: 'UUID ist erforderlich'
        };
      }

      // Prüfe ob bereits eine Anwendung mit dieser E-Mail existiert
      const existingApplication = await this.db.getApplicationByEmail(formData.email);
      if (existingApplication) {
        return {
          success: false,
          message: 'Eine Anmeldung mit dieser E-Mail-Adresse existiert bereits'
        };
      }

      // Prüfe ob bereits eine Anwendung mit dieser UUID existiert
      const existingByUuid = await this.db.getApplicationByUuid(uuid);
      if (existingByUuid) {
        return {
          success: false,
          message: 'Diese Anfrage wurde bereits verarbeitet'
        };
      }

      // FormData als JSON-String speichern
      const payload = JSON.stringify(formData);

      // In Datenbank speichern
      await this.db.insertApplication(formData.email, uuid, payload);

      serverLog(`Neue Antragsanmeldung gespeichert: ${formData.email} (UUID: ${uuid})`);

      return {
        success: true,
        message: 'Antragsanmeldung erfolgreich gespeichert',
        uuid,
        email: formData.email
      };

    } catch (error) {
      console.error('Fehler beim Speichern der Antragsanmeldung:', error);
      return {
        success: false,
        message: 'Interner Serverfehler beim Speichern der Antragsanmeldung'
      };
    }
  }

  /**
   * Ruft eine Antragsanmeldung anhand der E-Mail-Adresse ab
   */
  async getApplicationByEmail(email: string): Promise<FormData | null> {
    try {
      const record = await this.db.getApplicationByEmail(email);
      if (!record) {
        return null;
      }

      return JSON.parse(record.payload);
    } catch (error) {
      console.error('Fehler beim Abrufen der Antragsanmeldung:', error);
      return null;
    }
  }

  /**
   * Ruft eine Antragsanmeldung anhand der UUID ab
   */
  async getApplicationByUuid(uuid: string): Promise<FormData | null> {
    try {
      const record = await this.db.getApplicationByUuid(uuid);
      if (!record) {
        return null;
      }

      return JSON.parse(record.payload);
    } catch (error) {
      console.error('Fehler beim Abrufen der Antragsanmeldung:', error);
      return null;
    }
  }

  /**
   * Ruft alle Antragsanmeldungen ab (mit Pagination)
   */
  async getAllApplications(limit: number = 100, offset: number = 0): Promise<FormData[]> {
    try {
      const records = await this.db.getAllApplications(limit, offset);
      return records.map(record => JSON.parse(record.payload));
    } catch (error) {
      console.error('Fehler beim Abrufen aller Antragsanmeldungen:', error);
      return [];
    }
  }

  /**
   * Löscht eine Antragsanmeldung anhand der E-Mail-Adresse
   */
  async deleteApplication(email: string): Promise<boolean> {
    try {
      await this.db.deleteApplication(email);
      return true;
    } catch (error) {
      console.error('Fehler beim Löschen der Antragsanmeldung:', error);
      return false;
    }
  }

  /**
   * Prüft ob eine Antragsanmeldung mit der gegebenen E-Mail existiert
   */
  async applicationExists(email: string): Promise<boolean> {
    try {
      return await this.db.applicationExists(email);
    } catch (error) {
      console.error('Fehler beim Prüfen der Antragsanmeldung:', error);
      return false;
    }
  }

  /**
   * Generiert eine neue UUID für eine Antragsanmeldung
   * Verwendet crypto.randomUUID() als Node.js native Lösung
   */
  generateUuid(): string {
    return generateServerUuid();
  }

  /**
   * Validiert die FormData vor dem Speichern
   */
  validateFormData(formData: FormData): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Erforderliche Felder prüfen
    const requiredFields = [
      'vorname', 'name', 'email', 'strasse', 'plz', 'ort',
      'hundName', 'mitgliedschaft', 'sepaIban', 'sepaBic', 'sepaKreditinstitut'
    ];

    for (const field of requiredFields) {
      const value = (formData as unknown as Record<string, unknown>)[field];
      if (!value || !value.toString().trim()) {
        errors.push(`Feld '${field}' ist erforderlich`);
      }
    }

    // E-Mail-Format prüfen
    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.push('Ungültige E-Mail-Adresse');
    }

    // PLZ prüfen (5-stellig)
    if (formData.plz && !/^\d{5}$/.test(formData.plz)) {
      errors.push('PLZ muss 5-stellig sein');
    }

    // IBAN prüfen (vereinfacht)
    if (formData.sepaIban && !/^[A-Z]{2}\d{2}[A-Z0-9]+$/.test(formData.sepaIban.replace(/\s/g, ''))) {
      errors.push('Ungültige IBAN');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

// Singleton-Instanz
let applicationService: ApplicationService | null = null;

export function getApplicationService(): ApplicationService {
  if (!applicationService) {
    applicationService = new ApplicationService();
  }
  return applicationService;
}
