import { PrismaClient } from '@prisma/client';

// Singleton pattern for Prisma client
let prisma: PrismaClient | null = null;

export function getPrismaClient(): PrismaClient {
  if (!prisma) {
    prisma = new PrismaClient();
  }
  return prisma;
}

export interface ApplicationRecord {
  id: number;
  creationDate: Date;
  email: string;
  uuid: string | null;
  payload: string | null;
}

export class DatabaseService {
  private prisma: PrismaClient;

  constructor() {
    this.prisma = getPrismaClient();
  }

  /**
   * Initialisiert die Datenbank und erstellt Tabellen falls notwendig
   */
  async initializeDatabase(): Promise<void> {
    try {
      // Prisma erstellt die Tabellen automatisch basierend auf dem Schema
      await this.prisma.$connect();
      console.log('Datenbank erfolgreich initialisiert');
    } catch (error) {
      console.error('Fehler beim Initialisieren der Datenbank:', error);
      throw error;
    }
  }

  /**
   * Fügt eine neue Antragsanmeldung hinzu
   */
  async insertApplication(data: {
    email: string;
    uuid: string;
    payload: string;
  }): Promise<number> {
    try {
      const result = await this.prisma.application.create({
        data: {
          email: data.email,
          uuid: data.uuid,
          payload: data.payload,
          creationDate: new Date(),
        },
      });
      return result.id;
    } catch (error) {
      console.error('Fehler beim Einfügen der Antragsanmeldung:', error);
      throw error;
    }
  }

  /**
   * Ruft eine Antragsanmeldung anhand der E-Mail-Adresse ab
   */
  async getApplicationByEmail(email: string): Promise<ApplicationRecord | null> {
    try {
      const record = await this.prisma.application.findUnique({
        where: { email },
      });
      return record;
    } catch (error) {
      console.error('Fehler beim Abrufen der Antragsanmeldung:', error);
      return null;
    }
  }

  /**
   * Ruft eine Antragsanmeldung anhand der UUID ab
   */
  async getApplicationByUuid(uuid: string): Promise<ApplicationRecord | null> {
    try {
      const record = await this.prisma.application.findFirst({
        where: { uuid },
      });
      return record;
    } catch (error) {
      console.error('Fehler beim Abrufen der Antragsanmeldung:', error);
      return null;
    }
  }

  /**
   * Ruft alle Antragsanmeldungen ab (mit Pagination)
   */
  async getAllApplications(limit: number = 100, offset: number = 0): Promise<ApplicationRecord[]> {
    try {
      const records = await this.prisma.application.findMany({
        take: limit,
        skip: offset,
        orderBy: { creationDate: 'desc' },
      });
      return records;
    } catch (error) {
      console.error('Fehler beim Abrufen aller Antragsanmeldungen:', error);
      return [];
    }
  }

  /**
   * Löscht eine Antragsanmeldung anhand der ID
   */
  async deleteApplicationById(id: number): Promise<boolean> {
    try {
      await this.prisma.application.delete({
        where: { id },
      });
      return true;
    } catch (error) {
      console.error('Fehler beim Löschen der Antragsanmeldung:', error);
      return false;
    }
  }

  /**
   * Löscht eine Antragsanmeldung anhand der E-Mail-Adresse
   */
  async deleteApplication(email: string): Promise<boolean> {
    try {
      await this.prisma.application.delete({
        where: { email },
      });
      return true;
    } catch (error) {
      console.error('Fehler beim Löschen der Antragsanmeldung:', error);
      return false;
    }
  }

  /**
   * Prüft, ob eine Antragsanmeldung mit der E-Mail existiert
   */
  async applicationExists(email: string): Promise<boolean> {
    try {
      const record = await this.prisma.application.findUnique({
        where: { email },
        select: { id: true },
      });
      return record !== null;
    } catch (error) {
      console.error('Fehler beim Prüfen der Antragsanmeldung:', error);
      return false;
    }
  }

  /**
   * Schließt die Datenbankverbindung
   */
  async close(): Promise<void> {
    await this.prisma.$disconnect();
  }
}