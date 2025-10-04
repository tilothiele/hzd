import { NextRequest, NextResponse } from 'next/server';
import { getDatabaseService } from '../../../../lib/database';

export async function GET(request: NextRequest) {
  try {
    const db = getDatabaseService();

    // Alle Anwendungen abrufen für Statistiken
    const allApplications = await db.getAllApplications(1000, 0);

    // Statistiken berechnen
    const stats = {
      totalApplications: allApplications.length,
      applicationsByMonth: {} as Record<string, number>,
      applicationsByMembership: {} as Record<string, number>,
      recentApplications: allApplications.slice(0, 10).map(app => ({
        email: app.email,
        creationDate: app.creationDate,
        membership: extractMembershipFromPayload(app.payload)
      }))
    };

    // Gruppiere nach Monaten
    allApplications.forEach(app => {
      const date = new Date(app.creationDate);
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      stats.applicationsByMonth[monthKey] = (stats.applicationsByMonth[monthKey] || 0) + 1;
    });

    // Gruppiere nach Mitgliedschaftstypen
    allApplications.forEach(app => {
      const membership = extractMembershipFromPayload(app.payload);
      stats.applicationsByMembership[membership] = (stats.applicationsByMembership[membership] || 0) + 1;
    });

    return NextResponse.json({
      success: true,
      data: stats,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Fehler beim Abrufen der Datenbankstatistiken:', error);
    return NextResponse.json(
      { success: false, message: 'Interner Serverfehler' },
      { status: 500 }
    );
  }
}

function extractMembershipFromPayload(payload: string): string {
  try {
    const data = JSON.parse(payload);
    return data.mitgliedschaft || 'Unbekannt';
  } catch (error) {
    return 'Unbekannt';
  }
}
