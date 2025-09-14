import { NextRequest, NextResponse } from 'next/server';

// In-Memory storage for processed request IDs (in production, use a database)
const processedRequests = new Set<string>();

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { requestId, timestamp, formData } = body;
    const requestIdHeader = request.headers.get('X-Request-ID');

    // Validierung der UUID
    if (!requestId || !requestIdHeader || requestId !== requestIdHeader) {
      return NextResponse.json(
        { error: 'Invalid or missing request ID' },
        { status: 400 }
      );
    }

    // Prüfe auf Doppelrequests
    if (processedRequests.has(requestId)) {
      return NextResponse.json(
        { error: 'Duplicate request detected', requestId },
        { status: 409 }
      );
    }

    // Markiere Request als verarbeitet
    processedRequests.add(requestId);

    // Hier würde die eigentliche Verarbeitung der Formulardaten stattfinden
    // z.B. Speicherung in Datenbank, E-Mail-Versand, etc.
    console.log('Processing application:', {
      requestId,
      timestamp,
      formData
    });

    // Simuliere Verarbeitungszeit
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Erfolgreiche Antwort
    return NextResponse.json({
      success: true,
      requestId,
      message: 'Application submitted successfully',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error processing application:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

