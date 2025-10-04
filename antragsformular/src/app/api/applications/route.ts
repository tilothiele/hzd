import { NextRequest, NextResponse } from 'next/server';
import { getApplicationService } from '../../../services/applicationService';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '100');
    const offset = parseInt(searchParams.get('offset') || '0');
    const email = searchParams.get('email');
    const uuid = searchParams.get('uuid');

    const applicationService = getApplicationService();

    if (email) {
      // Einzelne Anwendung per E-Mail abrufen
      const application = await applicationService.getApplicationByEmail(email);
      if (!application) {
        return NextResponse.json(
          { success: false, message: 'Anwendung nicht gefunden' },
          { status: 404 }
        );
      }
      return NextResponse.json({ success: true, data: application });
    }

    if (uuid) {
      // Einzelne Anwendung per UUID abrufen
      const application = await applicationService.getApplicationByUuid(uuid);
      if (!application) {
        return NextResponse.json(
          { success: false, message: 'Anwendung nicht gefunden' },
          { status: 404 }
        );
      }
      return NextResponse.json({ success: true, data: application });
    }

    // Alle Anwendungen abrufen
    const applications = await applicationService.getAllApplications(limit, offset);

    return NextResponse.json({
      success: true,
      data: applications,
      meta: {
        count: applications.length,
        limit,
        offset
      }
    });

  } catch (error) {
    console.error('Fehler beim Abrufen der Anwendungen:', error);
    return NextResponse.json(
      { success: false, message: 'Interner Serverfehler' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const email = searchParams.get('email');

    if (!email) {
      return NextResponse.json(
        { success: false, message: 'E-Mail-Parameter ist erforderlich' },
        { status: 400 }
      );
    }

    const applicationService = getApplicationService();
    const success = await applicationService.deleteApplication(email);

    if (!success) {
      return NextResponse.json(
        { success: false, message: 'Fehler beim Löschen der Anwendung' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Anwendung erfolgreich gelöscht'
    });

  } catch (error) {
    console.error('Fehler beim Löschen der Anwendung:', error);
    return NextResponse.json(
      { success: false, message: 'Interner Serverfehler' },
      { status: 500 }
    );
  }
}
