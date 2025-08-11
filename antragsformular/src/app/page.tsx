"use client"

import { useState, ChangeEvent, FormEvent, useRef, useEffect } from "react";
import { v4 as uuidv4 } from 'uuid';

interface FormData {
  name: string;
  vorname: string;
  geburtsdatum: string;
  strasse: string;
  plz: string;
  ort: string;
  email: string;
  telefon: string;
  mitgliedschaftVDH: string;
  hundName: string;
  hundZwinger: string;
  hundZuchtbuch: string;
  hundChip: string;
  hundWurfdatum: string;
  hundRasse: string;
  hundGeschlecht: string;
  hundVersicherung: string;
  hundVersNr: string;
  mitgliedschaft: string[];
  kurzzeitVon: string;
  kurzzeitBis: string;
  sepaName: string;
  sepaIban: string;
  sepaBic: string;
  sepaKreditinstitut: string;
}

export default function AntragForm() {
  const formRef = useRef<HTMLFormElement>(null);
  const [requestId, setRequestId] = useState<string>('');
  const [showSuccessDialog, setShowSuccessDialog] = useState<boolean>(false);
  
  // Debug: Log requestId when it changes
  useEffect(() => {
    if (requestId) {
      console.log('Request ID set:', requestId);
    }
  }, [requestId]);
  const [formData, setFormData] = useState<FormData>({
    name: "",
    vorname: "",
    geburtsdatum: "",
    strasse: "",
    plz: "",
    ort: "",
    email: "",
    telefon: "",
    mitgliedschaftVDH: "",
    hundName: "",
    hundZwinger: "",
    hundZuchtbuch: "",
    hundChip: "",
    hundWurfdatum: "",
    hundRasse: "",
    hundGeschlecht: "",
    hundVersicherung: "",
    hundVersNr: "",
    mitgliedschaft: [],
    kurzzeitVon: "",
    kurzzeitBis: "",
    sepaName: "",
    sepaIban: "",
    sepaBic: "",
    sepaKreditinstitut: "",

  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isFormValid, setIsFormValid] = useState(false);
  const [savedFormData, setSavedFormData] = useState<FormData | null>(null);

  // Initiale Validierung beim Laden der Komponente
  useEffect(() => {
    const validationResult = validateFormWithData(formData);
    setIsFormValid(validationResult.isValid);
  }, [formData]);

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;

    let updatedFormData;
    if (type === "radio") {
      updatedFormData = { ...formData, mitgliedschaft: [value] };
    } else {
      updatedFormData = { ...formData, [name]: value };
    }

    setFormData(updatedFormData);

    // Validiere das Formular mit den aktualisierten Daten
    setTimeout(() => {
      const validationResult = validateFormWithData(updatedFormData);
      console.log('Updated form data:', updatedFormData);
      console.log('Validation result:', validationResult);
      console.log('Form valid:', validationResult.isValid);
      console.log('Error count:', Object.keys(validationResult.errors).length);
      console.log('Errors:', validationResult.errors);
      setIsFormValid(validationResult.isValid);
    }, 100);
  };

  const validateFormWithData = (data: FormData): { isValid: boolean; errors: Record<string, string> } => {
    const newErrors: Record<string, string> = {};

    console.log('Validating form data:', data);

    // Vereinfachte Validierung - nur die wichtigsten Felder
    if (!data.vorname || !data.vorname.trim()) {
      newErrors.vorname = "Vorname ist erforderlich";
      console.log('Vorname missing or empty');
    }
    if (!data.name || !data.name.trim()) {
      newErrors.name = "Nachname ist erforderlich";
      console.log('Name missing or empty');
    }
    if (!data.email || !data.email.trim()) {
      newErrors.email = "E-Mail ist erforderlich";
      console.log('Email missing or empty');
    }
    if (!data.hundName || !data.hundName.trim()) {
      newErrors.hundName = "Name des Hundes ist erforderlich";
      console.log('Hund name missing or empty');
    }
    if (!data.mitgliedschaft || data.mitgliedschaft.length === 0) {
      newErrors.mitgliedschaft = "Bitte wählen Sie eine Mitgliedschaftsart";
      console.log('Mitgliedschaft not selected');
    }

    console.log('Validation errors found:', Object.keys(newErrors).length);
    console.log('Errors:', newErrors);

    return { isValid: Object.keys(newErrors).length === 0, errors: newErrors };
  };

  const validateForm = (): { isValid: boolean; errors: Record<string, string> } => {
    return validateFormWithData(formData);
  };



  const generatePDF = async () => {
    // Verwende die gespeicherten Daten für die PDF-Generierung
    const dataToUse = savedFormData || formData;
    console.log('Generating PDF with data:', dataToUse);

    try {
      // Serverseitige PDF-Generierung
      const response = await fetch('/api/generate-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          formData: dataToUse
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // PDF als Blob herunterladen
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'HZD-Aufnahmeantrag.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error('Fehler beim Generieren des PDFs:', error);
      alert('Fehler beim Generieren des PDFs. Bitte versuchen Sie es erneut.');
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const validationResult = validateForm();
    if (!validationResult.isValid) {
      // Set errors immediately so they show up in the UI
      setErrors(validationResult.errors);
      setIsFormValid(false);

      // Wait for React to update the DOM with errors
      setTimeout(() => {
        // Scroll to first error in the correct order
        const errorFields = [
          'vorname', 'name', 'geburtsdatum', 'strasse', 'plz', 'ort', 'telefon', 'email',
          'hundName', 'hundChip', 'hundWurfdatum', 'hundRasse', 'hundGeschlecht', 'hundVersicherung', 'hundVersNr',
          'sepaName', 'sepaKreditinstitut', 'sepaIban', 'sepaBic',
          'mitgliedschaft', 'kurzzeitVon', 'kurzzeitBis'
        ];

        for (const fieldName of errorFields) {
          if (validationResult.errors[fieldName]) {
            const errorField = document.querySelector(`[name="${fieldName}"]`);
            if (errorField) {
              console.log('Scrolling to field:', fieldName); // Debug log
              errorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
              break;
            }
          }
        }
      }, 100);
      return;
    }

    setIsSubmitting(true);

    // Generiere UUID für diesen Request
    const currentRequestId = uuidv4();
    setRequestId(currentRequestId);

    try {
      // REST-Endpoint aufrufen
      const response = await fetch('/api/submit-application', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Request-ID': currentRequestId
        },
        body: JSON.stringify({
          requestId: currentRequestId,
          timestamp: new Date().toISOString(),
          formData: formData
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Formular erfolgreich gesendet:", result);
      
      // Speichere die Daten für die PDF-Generierung
      setSavedFormData({ ...formData });
      setShowSuccessDialog(true);

      // Reset form
      setFormData({
        name: "",
        vorname: "",
        geburtsdatum: "",
        strasse: "",
        plz: "",
        ort: "",
        email: "",
        telefon: "",
        mitgliedschaftVDH: "",
        hundName: "",
        hundZwinger: "",
        hundZuchtbuch: "",
        hundChip: "",
        hundWurfdatum: "",
        hundRasse: "",
        hundGeschlecht: "",
        hundVersicherung: "",
        hundVersNr: "",
        mitgliedschaft: [],
        kurzzeitVon: "",
        kurzzeitBis: "",
        sepaName: "",
        sepaIban: "",
        sepaBic: "",
        sepaKreditinstitut: "",

      });
      setErrors({});
      setIsFormValid(false); // Button nach Reset deaktivieren
      setRequestId(''); // Reset Request ID after successful submission
    } catch (error) {
      console.error("Fehler beim Senden:", error);
      alert("Es gab einen Fehler beim Senden des Antrags. Bitte versuchen Sie es erneut.");
      setRequestId(''); // Reset Request ID on error
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4" style={{ backgroundColor: '#f8f8f8' }}>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            {/* Logo */}
            <div className="flex justify-center mb-6">
              <img
                src="/logo.png"
                alt="HZD Logo"
                className="w-24 h-24 object-contain"
              />
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              HZD Ortsgruppen-Aufnahmeantrag
            </h1>
            <p className="text-xl text-blue-600 font-semibold">
              OG Hamburg und Umgebung
            </p>
            <p className="text-l text-blue-600">
              Mittlerer Landweg 74a, 21033 Hamburg
            </p>
            <div className="w-24 h-1 bg-blue-600 mx-auto mt-4 rounded-full"></div>
          </div>
        </div>

        {/* Main Form */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <form ref={formRef} onSubmit={handleSubmit} className="p-8 space-y-12">

            {/* Antragsteller Section */}
            <div className="border-b border-gray-200 pb-8">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  1
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Antragsteller</h2>
              </div>

              <div className="mb-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  Hiermit beantrage ich in Anerkennung der Satzung, Ordnungen und Beschlüsse der HZD die Mitgliedschaft in der
                  Ortsgruppe Hamburg u.U. der Hovawart
                  Zuchtgemeinschaft Deutschland e.V.. Ich gehöre keinem kynologischen Verein außerhalb des Verbandes für das Deutsche Hundewesen
                  (VDH) bzw. außerhalb der Fédération Cynologique Internationale (FCI) an. Ich bestätige, dass ich aus keinem anderen VDH-Verein
                  ausgeschlossen wurde und dass gegen mich kein Ausschlussverfahren läuft. Ich bin weder gewerbsmäßiger Hundehändler/-züchter noch
                  Hundeverkaufsvermittler.
                </p>
              </div>

              <div className="space-y-8">
                {/* 1. Zeile: Vorname, Nachname, Geburtsdatum */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">Vorname *</label>
                    <input
                      name="vorname"
                      value={formData.vorname}
                      placeholder="Ihr Vorname"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.vorname ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.vorname}
                    />
                    {errors.vorname && (
                      <p className="text-sm text-red-600 mt-1">{errors.vorname}</p>
                    )}
                  </div>

                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">Nachname *</label>
                    <input
                      name="name"
                      value={formData.name}
                      placeholder="Ihr Nachname"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.name ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.name}
                    />
                    {errors.name && (
                      <p className="text-sm text-red-600 mt-1">{errors.name}</p>
                    )}
                  </div>

                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">Geburtsdatum *</label>
                    <input
                      name="geburtsdatum"
                      type="date"
                      value={formData.geburtsdatum}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.geburtsdatum ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.geburtsdatum}
                    />
                    {errors.geburtsdatum && (
                      <p className="text-sm text-red-600 mt-1">{errors.geburtsdatum}</p>
                    )}
                  </div>
                </div>

                {/* 2. Zeile: Straße, PLZ, Ort */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">Straße *</label>
                    <input
                      name="strasse"
                      value={formData.strasse}
                      placeholder="Musterstraße 123"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.strasse ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.strasse}
                    />
                    {errors.strasse && (
                      <p className="text-sm text-red-600 mt-1">{errors.strasse}</p>
                    )}
                  </div>

                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">PLZ *</label>
                    <input
                      name="plz"
                      value={formData.plz}
                      placeholder="20095"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.plz ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.plz}
                    />
                    {errors.plz && (
                      <p className="text-sm text-red-600 mt-1">{errors.plz}</p>
                    )}
                  </div>

                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">Ort *</label>
                    <input
                      name="ort"
                      value={formData.ort}
                      placeholder="Hamburg"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.ort ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.ort}
                    />
                    {errors.ort && (
                      <p className="text-sm text-red-600 mt-1">{errors.ort}</p>
                    )}
                  </div>
                </div>

                {/* 3. Zeile: Telefon, E-Mail */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">Telefon *</label>
                    <input
                      name="telefon"
                      value={formData.telefon}
                      placeholder="+49 40 12345678"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.telefon ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.telefon}
                    />
                    {errors.telefon && (
                      <p className="text-sm text-red-600 mt-1">{errors.telefon}</p>
                    )}
                  </div>

                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700">E-Mail *</label>
                    <input
                      name="email"
                      type="email"
                      value={formData.email}
                      placeholder="ihre.email@beispiel.de"
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.email ? 'border-red-500' : 'border-gray-300'
                      }`}
                      data-error={!!errors.email}
                    />
                    {errors.email && (
                      <p className="text-sm text-red-600 mt-1">{errors.email}</p>
                    )}
                  </div>
                </div>
              </div>

              {/* 4. Zeile: VDH Mitgliedschaften (vollbreite) */}
              <div className="mt-8">
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">VDH Mitgliedschaften</label>
                  <input
                    value={formData.mitgliedschaftVDH}
                    name="mitgliedschaftVDH"
                    placeholder="Bestehende VDH Mitgliedschaften"
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  />
                </div>
              </div>
            </div>

            {/* Hund Section */}
            <div className="border-b border-gray-200 pb-8">
              <div className="flex items-center mb-8">
                <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  2
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Hund</h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Name *</label>
                  <input
                    name="hundName"
                    value={formData.hundName}
                    placeholder="Name des Hundes"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundName ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundName}
                  />
                  {errors.hundName && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundName}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Zwinger</label>
                  <input
                    name="hundZwinger"
                    value={formData.hundZwinger}
                    placeholder="Zwingername"
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                  />
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Zuchtbuchnummer</label>
                  <input
                    value={formData.hundZuchtbuch}
                    name="hundZuchtbuch"
                    placeholder="Zuchtbuchnummer"
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                  />
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Chip-Nr. *</label>
                  <input
                    value={formData.hundChip}
                    name="hundChip"
                    placeholder="Chip-Nummer"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundChip ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundChip}
                  />
                  {errors.hundChip && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundChip}</p>
                  )}
                </div>



                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Wurfdatum *</label>
                  <input
                    value={formData.hundWurfdatum}
                    name="hundWurfdatum"
                    type="date"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundWurfdatum ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundWurfdatum}
                  />
                  {errors.hundWurfdatum && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundWurfdatum}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Rasse *</label>
                  <input
                    value={formData.hundRasse}
                    name="hundRasse"
                    placeholder="Hunderasse"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundRasse ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundRasse}
                  />
                  {errors.hundRasse && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundRasse}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Geschlecht *</label>
                  <select
                    value={formData.hundGeschlecht}
                    name="hundGeschlecht"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundGeschlecht ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundGeschlecht}
                  >
                    <option value="">Bitte wählen</option>
                    <option value="Rüde">Rüde</option>
                    <option value="Hündin">Hündin</option>
                  </select>
                  {errors.hundGeschlecht && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundGeschlecht}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Haftpflichtversicherung *</label>
                  <input
                    value={formData.hundVersicherung}
                    name="hundVersicherung"
                    placeholder="Versicherungsgesellschaft"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundVersicherung ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundVersicherung}
                  />
                  {errors.hundVersicherung && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundVersicherung}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Versicherungsnummer *</label>
                  <input
                    value={formData.hundVersNr}
                    name="hundVersNr"
                    placeholder="Versicherungsnummer"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 ${
                      errors.hundVersNr ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.hundVersNr}
                  />
                  {errors.hundVersNr && (
                    <p className="text-sm text-red-600 mt-1">{errors.hundVersNr}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Mitgliedschaft Section */}
            <div className="border-b border-gray-200 pb-8">
              <div className="flex items-center mb-8">
                <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  3
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Mitgliedschaft</h2>
              </div>

              <div className="space-y-6">
                {errors.mitgliedschaft && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-600">{errors.mitgliedschaft}</p>
                  </div>
                )}
                <div className="flex items-start space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="mitgliedschaft"
                    value="HZD Vollmitgliedschaft"
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <div>
                    <label className="text-sm font-medium text-gray-900">HZD Vollmitgliedschaft</label>
                    <p className="text-sm text-gray-600">35 € jährlich</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="mitgliedschaft"
                    value="HZD Familienmitglied"
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <div>
                    <label className="text-sm font-medium text-gray-900">HZD Familienmitglied</label>
                    <p className="text-sm text-gray-600">16 € jährlich</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="mitgliedschaft"
                    value="Ortsgruppenmitglied"
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <div>
                    <label className="text-sm font-medium text-gray-900">Ortsgruppenmitglied</label>
                    <p className="text-sm text-gray-600">138 € jährlich</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="mitgliedschaft"
                    value="OG Familienmitglied"
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <div>
                    <label className="text-sm font-medium text-gray-900">OG Familienmitglied</label>
                    <p className="text-sm text-gray-600">16 € jährlich</p>
                  </div>
                </div>



                <div className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <input
                      type="radio"
                      name="mitgliedschaft"
                      value="Kurzzeitmitglied"
                      onChange={handleChange}
                      className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                    />
                    <div className="flex-1">
                      <label className="text-sm font-medium text-gray-900">Kurzzeitmitglied</label>
                      <p className="text-sm text-gray-600">11,50 € pro Monat</p>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                        <div className="space-y-1">
                          <label className="block text-xs text-gray-600">Von (Jahr/Monat)</label>
                          <input
                            type="month"
                            name="kurzzeitVon"
                            onChange={handleChange}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-transparent ${
                              errors.kurzzeitVon ? 'border-red-500' : 'border-gray-300'
                            }`}
                            data-error={!!errors.kurzzeitVon}
                          />
                          {errors.kurzzeitVon && (
                            <p className="text-xs text-red-600 mt-1">{errors.kurzzeitVon}</p>
                          )}
                        </div>
                        <div className="space-y-1">
                          <label className="block text-xs text-gray-600">Bis (Jahr/Monat)</label>
                          <input
                            type="month"
                            name="kurzzeitBis"
                            onChange={handleChange}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                              errors.kurzzeitBis ? 'border-red-500' : 'border-gray-300'
                            }`}
                            data-error={!!errors.kurzzeitBis}
                          />
                          {errors.kurzzeitBis && (
                            <p className="text-xs text-red-600 mt-1">{errors.kurzzeitBis}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* SEPA Section */}
            <div className="border-b border-gray-200 pb-8">
              <div className="flex items-center mb-8">
                <div className="w-10 h-10 bg-orange-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  4
                </div>
                <h2 className="text-2xl font-bold text-gray-900">SEPA-Lastschriftmandat</h2>
              </div>

              <div className="grid grid-cols-1">
                <div className="space-y-3 mb-4">
                  <p className="text-sm text-gray-600">
                    Ich ermächtige die Hovawart Zuchtgemeinschaft Deutschland, den Mitgliedsbeitrag mittels Lastschrift einzuziehen. Zugleich weise ich
                    mein Kreditinstitut an, die von der Hovawart Zuchtgemeinschaft auf mein Konto gezogenen Lastschriften einzulösen.
                    <br />
                    Hinweis: Ich kann innerhalb von acht Wochen, beginnend mit dem Belastungsdatum, die Erstattung des belasteten Betrages verlangen.
                    <br />
                    Es gelten dabei die mit meinem Kreditinstitut vereinbarten Bedingungen.
                    <br />
                    Gläubiger-Identifikationsnummer: DE79 ZZZ0 0000 5154 60. Mandatsreferenz ist die Mitgliedsnummer (wird separat mitgeteilt).
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Kontoinhaber *</label>
                  <input
                    name="sepaName"
                    value={formData.sepaName}
                    placeholder="Name des Kontoinhabers"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 ${
                      errors.sepaName ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.sepaName}
                  />
                  {errors.sepaName && (
                    <p className="text-sm text-red-600 mt-1">{errors.sepaName}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">Kreditinstitut *</label>
                  <input
                    name="sepaKreditinstitut"
                    value={formData.sepaKreditinstitut}
                    placeholder="Name der Bank"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 ${
                      errors.sepaKreditinstitut ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.sepaKreditinstitut}
                  />
                  {errors.sepaKreditinstitut && (
                    <p className="text-sm text-red-600 mt-1">{errors.sepaKreditinstitut}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">IBAN *</label>
                  <input
                    name="sepaIban"
                    value={formData.sepaIban}
                    placeholder="DE89 3704 0044 0532 0130 00"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 font-mono ${
                      errors.sepaIban ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.sepaIban}
                  />
                  {errors.sepaIban && (
                    <p className="text-sm text-red-600 mt-1">{errors.sepaIban}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">BIC *</label>
                  <input
                    name="sepaBic"
                    value={formData.sepaBic}
                    placeholder="COBADEFFXXX"
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 font-mono ${
                      errors.sepaBic ? 'border-red-500' : 'border-gray-300'
                    }`}
                    data-error={!!errors.sepaBic}
                  />
                  {errors.sepaBic && (
                    <p className="text-sm text-red-600 mt-1">{errors.sepaBic}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Abschluss Section */}
            <div className="pb-8">
              <div className="flex items-center mb-8">
                <div className="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  5
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Abschluss</h2>
              </div>

              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">
                  <strong>Hinweis:</strong> Die Daten werden elektronisch an die Geschäftsstelle der HZD OG Hamburg Billwerder übermittelt.
                    Der Antrag wird erst gültig, wenn er in Papierform und unterschrieben vorliegt. Sie können ihren unterschriebenen per Post an die o.a. Adresse schicken.
                    Alternativ können Sie zur Unterschrift bei nächster Gelegenheit im Vereinshaus in Hamburg-Billwerder vorbeikommen.
                </p>
              </div>
            </div>

            {/* Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">


              <button
                type="submit"
                disabled={!isFormValid || isSubmitting}
                className={`px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 shadow-lg ${
                  !isFormValid || isSubmitting
                    ? 'bg-gray-400 cursor-not-allowed opacity-50'
                    : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 transform hover:scale-105 hover:shadow-xl'
                }`}
                onClick={() => console.log('Button clicked, isFormValid:', isFormValid, 'isSubmitting:', isSubmitting)}
              >
                {isSubmitting ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Wird gesendet...</span>
                  </div>
                ) : (
                  'Weiter'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Success Dialog */}
      {showSuccessDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md mx-4">
            <div className="text-center">
              {/* Success Icon */}
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>

              {/* Title */}
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Antrag erfolgreich eingereicht!
              </h3>

              {/* Lorem Ipsum Message */}
              <div className="text-sm text-gray-600 mb-6 space-y-3">
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                  Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </p>
                <p>
                  Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                  Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
                <p>
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                </p>
              </div>

              {/* PDF Download Button */}
              <div className="mb-4">
                <button
                  onClick={generatePDF}
                  className="w-full px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors duration-200 mb-3"
                >
                  PDF herunterladen
                </button>
              </div>

              {/* Close Button */}
              <button
                onClick={() => setShowSuccessDialog(false)}
                className="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors duration-200"
              >
                Schließen
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
