# This Script takes protraitbox.com downloads and prints them directly via a brother .lbx file
# Made to run on Windows 10 with python and brother b-pac
# Uses the individual .pdf invoices Download
# by F. Wimbauer, 2026

from pathlib import Path
import re
import shutil
import sys
import pymupdf
import pandas as pd
import win32com.client

print("Hello")

# Paths
input_path = Path(r"C:\Users\accou\OneDrive\Desktop\Print")
final_destination = Path(r"C:\Users\accou\OneDrive\Desktop\Print\Finished")

# Filed Names in the .lbx Template
template = Path(r"C:\Users\accou\OneDrive\Desktop\Etiketten\Kombietikett.lbx")
adress_field = "Adresse"
invoice_field = "Bestellnr"
class_field = "Klasse"
code_field = "Code"

# Regex for Address
CODE_REGEX = re.compile(r"Zugangskarte: ([^\n,;]+)", re.IGNORECASE)
CLASS_REGEX = re.compile(r"Album: ([^\s,;]+)", re.IGNORECASE)
ADDRESS_CROP_BOX = pymupdf.Rect(30, 80, 300, 220)

# Helper to work with PDF
def extract_pdf_data(pdf_path):
    entries = []
    try:
        doc = pymupdf.open(pdf_path)
        if len(doc) == 0:
            return entries
        
        first_page = doc[0]
        raw_address = first_page.get_text("text", clip=ADDRESS_CROP_BOX)
        
        lines = [line.strip() for line in raw_address.splitlines() if line.strip()]

        # Remove "Fotostduio F. Wimbauer" and Country
        if lines:
            lines.pop(0)
            lines.pop(-1)

        address_clean = "\r\n".join(lines)

        # Build Whole Text
        text_pages = [page.get_text() or "" for page in doc]
        doc.close()

    except Exception as e:
        print(f"Fehler beim Lesen von {pdf_path.name}: {e}")
        return entries

    joined_text = "\n".join(text_pages)

    # Extract R-Nr.
    match = re.search(r"\d+", pdf_path.name)
    re_nr = match.group() if match else pdf_path.stem

    # Extract Class
    classes = []
    for m in CLASS_REGEX.finditer(joined_text):
        classes.extend(m.group(1).strip().split())
    klasse_str = ", ".join(sorted(list(set(classes))))

    # Find Code
    for page_text in text_pages:
        for m in CODE_REGEX.finditer(page_text):
            codes = m.group(1).strip().split()
            for code in codes:
                entries.append({
                    "Re-NR": re_nr,
                    "Adresse": address_clean,
                    "Zugangscode": code,
                    "Klasse": klasse_str
                })

    return entries


pdf_files = sorted(list(input_path.glob("*.pdf")))

if not pdf_files:
    print("Keine PDF-Dateien gefunden.")
    input("\nEnter zum Beenden")
    sys.exit()

# Process PDFs and collect data
all_entries = []
processed_files = []

for pdf_file in pdf_files:
    entries = extract_pdf_data(pdf_file)
    if entries:
        all_entries.extend(entries)
        processed_files.append(pdf_file)

if not all_entries:
    print("Keine Zugangscodes in den PDF-Dateien gefunden.")
    input("\nEnter zum Beenden")
    sys.exit()

data = pd.DataFrame(all_entries)

print()
print("========================================")
print("          ETIKETTENDRUCK")
print("========================================")
print()
print(f"PDF-Dateien: {len(pdf_files)}")
print(f"Etiketten:   {len(data)}")
print()
print("Druck starten?")
print()

antwort = input("Drucken? [J/N]: ")

if antwort.lower() not in ("j", "ja"):
    print("\nAbgebrochen.")
    input("Enter zum Beenden...")
    sys.exit()

# Init printer
try:
    handle = win32com.client.Dispatch("bpac.Document")

    if not handle.Open(str(template)):
        print("Vorlage konnte nicht geöffnet werden")
        input("\nEnter zum Beenden")
        sys.exit()

    handle.SetPrinter(handle.GetPrinterName, True)

except Exception as e:
    print(f"\nFehler beim Initialisieren von b-PAC: {e}")
    input("\nEnter zum Beenden...")
    sys.exit()

# Start printing
try:
    handle.StartPrint("Etikettendruck", 1)

    for index, line in data.iterrows():
        invoice = str(line["Re-NR"]).strip()
        code = str(line["Zugangscode"]).strip()
        klasse = str(line["Klasse"]).strip()
        adresse = str(line["Adresse"]).strip()

        print(f"Drucke Etikett {index + 1}/{len(data)}: Re-Nr: {invoice} | Code: {code} | Klasse: {klasse}")

        # Write the information
        handle.GetObject(adress_field).Text = adresse
        handle.GetObject(invoice_field).Text = invoice
        handle.GetObject(class_field).Text = klasse
        handle.GetObject(code_field).Text = code

        handle.PrintOut(1, 1)

    handle.Close(str(template))

except Exception as e:
    pass

# Move files into finished folder
final_destination.mkdir(parents=True, exist_ok=True)

for file in processed_files:
    loc = final_destination / file.name

    # If same file already exists
    if loc.exists():
        loc.unlink()

    shutil.move(str(file), str(loc))

print()
print("========================================")
print("              FERTIG")
print("========================================")
input("Enter zum Beenden")