import { NextRequest, NextResponse } from 'next/server';
import jsPDF from 'jspdf';
import fs from 'fs';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { formData } = body;

    // PDF erstellen
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 20;
    const contentWidth = pageWidth - 2 * margin;
    let yPosition = margin;

    // Adresse (links)
    pdf.setFontSize(8);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(0, 0, 0);
    const addressLines = [
      'HZD Ortsgruppe Hamburg u.U.',
      'Tilo Thiele',
      'Geschäftsstelle',
      'Anne-Becker-Ring 8',
      '21031 Hamburg'
    ];
    addressLines.forEach((line, index) => {
      pdf.text(line, margin, yPosition + (index * 4));
    });

    // Logo (oben rechts)
    try {
      // Logo als Base64 laden

      // Absoluten Pfad zum Logo erstellen
      const absoluteLogoPath = path.join(process.cwd(), 'public', 'logo.png');

      if (fs.existsSync(absoluteLogoPath)) {
        const logoBuffer = fs.readFileSync(absoluteLogoPath);
        const logoBase64 = logoBuffer.toString('base64');

        // Logo in PDF einbetten (20x20mm)
        const logoWidth = 20;
        const logoHeight = 20;
        const logoX = pageWidth - margin - logoWidth;
        const logoY = yPosition - 15;

        pdf.addImage(`data:image/png;base64,${logoBase64}`, 'PNG', logoX, logoY, logoWidth, logoHeight);
      } else {
        // Fallback: Hund-Emoji wenn Logo nicht gefunden
        pdf.setFontSize(24);
        pdf.setTextColor(59, 130, 246); // Blue-600
        const logoX = pageWidth - margin - 10;
        pdf.text('🐕', logoX, yPosition);
      }
    } catch (error) {
      console.error('Fehler beim Laden des Logos:', error);
      // Fallback: Hund-Emoji
      pdf.setFontSize(24);
      pdf.setTextColor(59, 130, 246); // Blue-600
      const logoX = pageWidth - margin - 10;
      pdf.text('🐕', logoX, yPosition);
    }

    yPosition += 25;

    // Titel
    pdf.setFontSize(20);
    pdf.setTextColor(0, 0, 0);
    pdf.setFont('helvetica', 'bold');
    pdf.text('HZD Ortsgruppen-Aufnahmeantrag', pageWidth / 2, yPosition, { align: 'center' });
    yPosition += 10;

    pdf.setFontSize(16);
    pdf.setFont('helvetica', 'normal');
    pdf.text('OG Hamburg und Umgebung', pageWidth / 2, yPosition, { align: 'center' });
    yPosition += 20;

    // Funktion zum Formatieren des Datums
    const formatDate = (dateString: string) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString;
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    };

    // Funktion zum Hinzufügen von Text mit Zeilenumbruch
    const addWrappedText = (text: string, fontSize: number, y: number, maxWidth: number) => {
      pdf.setFontSize(fontSize);
      const lines = pdf.splitTextToSize(text, maxWidth);
      pdf.text(lines, margin, y);
      return y + (lines.length * fontSize * 0.4);
    };

    // Funktion zum Hinzufügen eines Abschnitts
    const addSection = (title: string, data: Record<string, string>, loremText: string, useTable: boolean = false) => {
      // Abschnittstitel
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(59, 130, 246); // Blue-600
      pdf.text(title, margin, yPosition);
      yPosition += 8;

      // Lorem Ipsum Text
      yPosition = addWrappedText(loremText, 10, yPosition, contentWidth);
      yPosition += 5;

      // Formulardaten
      pdf.setFontSize(10);
      pdf.setFont('helvetica', 'normal');
      pdf.setTextColor(0, 0, 0);

      if (useTable) {
        // Tabellarische Darstellung (zweispaltig)
        const entries = Object.entries(data).filter(([, value]) => value && value.trim());
        const halfLength = Math.ceil(entries.length / 2);
        const leftColumn = entries.slice(0, halfLength);
        const rightColumn = entries.slice(halfLength);

        const columnWidth = contentWidth / 2 - 10;
        const leftX = margin;
        const rightX = margin + contentWidth / 2 + 10;

        // Linke Spalte
        leftColumn.forEach(([key, value]) => {
          const label = key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1');
          pdf.setFont('helvetica', 'bold');
          pdf.text(`${label}:`, leftX, yPosition);
          pdf.setFont('helvetica', 'normal');
          const valueLines = pdf.splitTextToSize(value, columnWidth - 30);
          pdf.text(valueLines, leftX + 30, yPosition);
          yPosition += Math.max(valueLines.length * 4, 6);
        });

        // Rechte Spalte (neue Y-Position für rechte Spalte)
        let rightYPosition = yPosition - (leftColumn.length * 6);
        rightColumn.forEach(([key, value]) => {
          const label = key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1');
          pdf.setFont('helvetica', 'bold');
          pdf.text(`${label}:`, rightX, rightYPosition);
          pdf.setFont('helvetica', 'normal');
          const valueLines = pdf.splitTextToSize(value, columnWidth - 30);
          pdf.text(valueLines, rightX + 30, rightYPosition);
          rightYPosition += Math.max(valueLines.length * 4, 6);
        });

        // Verwende die höhere Y-Position
        yPosition = Math.max(yPosition, rightYPosition);
      } else {
        // Normale Darstellung (einspaltig)
        Object.entries(data).forEach(([key, value]) => {
          if (value && value.trim()) {
            const label = key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1');
            const text = `${label}: ${value}`;
            yPosition = addWrappedText(text, 10, yPosition, contentWidth);
            yPosition += 2;
          }
        });
      }

      yPosition += 10;
    };

    // Prüfe ob neue Seite nötig
    const checkNewPage = () => {
      if (yPosition > pageHeight - 50) {
        pdf.addPage();
        yPosition = margin;
      }
    };

    // Abschnitt 1: Antragsteller
    checkNewPage();
    addSection(
      '1. Antragsteller',
      {
        'Vorname': formData.vorname,
        'Nachname': formData.name,
        'Geburtsdatum': formatDate(formData.geburtsdatum),
        'Straße': formData.strasse,
        'PLZ': formData.plz,
        'Ort': formData.ort,
        'Telefon': formData.telefon,
        'E-Mail': formData.email
      },
      'Hiermit beantrage ich in Anerkennung der Satzung, Ordnungen und Beschlüsse der HZD die Mitgliedschaft in der Ortsgruppe Hamburg u.U. der Hovawart '
      +'Zuchtgemeinschaft Deutschland e.V.. Ich gehöre keinem kynologischen Verein außerhalb des Verbandes für das Deutsche Hundewesen '
      +'(VDH) bzw. außerhalb der Fédération Cynologique Internationale (FCI) an. Ich bestätige, dass ich aus keinem anderen VDH-Verein '
      +'ausgeschlossen wurde und dass gegen mich kein Ausschlussverfahren läuft. Ich bin weder gewerbsmäßiger Hundehändler/-züchter noch '
      +'Hundeverkaufsvermittler.',
      true // Tabellarische Darstellung
    );

    // VDH Mitgliedschaften über gesamte Breite
    if (formData.mitgliedschaftVDH && formData.mitgliedschaftVDH.trim()) {
      yPosition += 5;
      pdf.setFontSize(10);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(0, 0, 0);
      pdf.text('Ich bin/war bereits Mitglied in folgenden kynologischen Verbänden oder Vereinen des VDH:', margin, yPosition);
      yPosition += 5;

      pdf.setFont('helvetica', 'normal');
      const vdhLines = pdf.splitTextToSize(formData.mitgliedschaftVDH, contentWidth);
      pdf.text(vdhLines, margin, yPosition);
      yPosition += vdhLines.length * 4 + 5;
    }

    // Abschnitt 2: Hund
    checkNewPage();
    addSection(
      '2. Hund',
      {
        'Name': formData.hundName,
        'Zwinger': formData.hundZwinger,
        'Zuchtbuchnummer': formData.hundZuchtbuch,
        'Chip-Nr.': formData.hundChip,
        'Wurfdatum': formatDate(formData.hundWurfdatum),
        'Rasse': formData.hundRasse,
        'Geschlecht': formData.hundGeschlecht,
        'Haftpflichtvers.': formData.hundVersicherung,
        'Vers.nr.': formData.hundVersNr
      },
      'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      true // Tabellarische Darstellung
    );

    // Datum und Unterschrift nach Abschnitt 2
    yPosition += 5;
    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(0, 0, 0);

    // Abschnitt 3: Mitgliedschaft
    checkNewPage();
    addSection(
      '3. Mitgliedschaft',
      {
        'Gewählte Mitgliedschaft': formData.mitgliedschaft.join(', '),
        'Kurzzeit von': formData.kurzzeitVon,
        'Kurzzeit bis': formData.kurzzeitBis
      },
      'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.'
    );

    // Datum und Unterschrift nach Abschnitt 3 (nur Labels)
    yPosition += 5;
    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(0, 0, 0);

    yPosition = addWrappedText('Datum: _________________', 10, yPosition, contentWidth);
    yPosition += 5;
    yPosition = addWrappedText('Unterschrift: _________________', 10, yPosition, contentWidth);
    yPosition += 5;

    // Abschnitt 4: SEPA
    checkNewPage();
    addSection(
      '4. SEPA-Lastschriftmandat',
      {
        'Kontoinhaber': formData.kontoinhaber,
        'Kreditinstitut': formData.sepaKreditinstitut,
        'IBAN': formData.sepaIban,
        'BIC': formData.sepaBic
      },
      'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.'
    );

    // Datum und Unterschrift nach Abschnitt 4 (nur Labels)
    yPosition += 5;
    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(0, 0, 0);

    yPosition = addWrappedText('Datum: _________________', 10, yPosition, contentWidth);
    yPosition += 5;
    yPosition = addWrappedText('Unterschrift: _________________', 10, yPosition, contentWidth);
    yPosition += 5;

    // Weitere Mitteilungen (nur wenn ausgefüllt)
    if (formData.weitereMitteilungen && formData.weitereMitteilungen.trim()) {
      checkNewPage();
      yPosition += 10;
      pdf.setFontSize(12);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(0, 0, 0);
      yPosition = addWrappedText('Weitere Mitteilungen:', 10, yPosition, contentWidth);
      yPosition += 5;

      pdf.setFont('helvetica', 'normal');
      pdf.setFontSize(10);
      const mitteilungenLines = pdf.splitTextToSize(formData.weitereMitteilungen, contentWidth);
      pdf.text(mitteilungenLines, margin, yPosition);
      yPosition += mitteilungenLines.length * 4 + 10;
    }

    // PDF als Buffer zurückgeben
    const pdfBuffer = pdf.output('arraybuffer');

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="HZD-Aufnahmeantrag.pdf"'
      }
    });

  } catch (error) {
    console.error('Error generating PDF:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
