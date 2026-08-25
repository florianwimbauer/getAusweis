# This Script takes protraitbox.com downloads and prints them directly via a brother .lbx file
# Made to run on Windows 10 with python and brother b-pac
# by F. Wimbauer, 2026

from pathlib import Path
import shutil
import sys

import pandas as pd
import win32com.client

print("Hello")

# Customer Data
input_path = Path(r"C:\Users\accou\OneDrive\Desktop\Print")
final_destination = Path(r"C:\Users\accou\OneDrive\Desktop\Print\Finished")

# .lbx Data
template = Path(r"C:\Users\accou\OneDrive\Desktop\Etiketten\Kombietikett.lbx")
adress_field = "Adresse"
invoice_field = "Bestellnr"

# Work with Excel

data = list(input_path.glob("*.xlsx"))

if not data:
    print("Keine Excel-Datei gefunden.")
    input("\nEnter zum Beenden")
    sys.exit()

file = max(data, key=lambda d: d.stat().st_mtime)

try:
    data = pd.read_excel(file)
except Exception as e:
    print(f"Excel-Datei nicht lesbar: \n{e}")
    input("\nEnter zum Beenden")
    sys.exit()

expected_columns = [
    "Vorname",
    "Nachname",
    "Straße",
    "PLZ",
    "Ort",
    "Bestell-Nr."
] 

if not all(actual_data in data.columns for actual_data in expected_columns):
    print("Excel-Datei hat unzulässiges Format. Erwartete Spalten wurden nicht gefunden")
    input("\nEnter zum Beenden")
    sys.exit()

# We expect that the file is fine now
print()
print("========================================")
print("          ETIKETTENDRUCK")
print("========================================")
print()
print(f"Datei:       {file.name}")
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
        # Prepare Data-Regex
        adress = (
            f"{str(line['Vorname']).strip()} {str(line['Nachname']).strip()}\r\n"
            f"{str(line['Straße']).strip()}\r\n"
            f"{str(line['PLZ']).strip()} {str(line['Ort']).strip()}"
        )
        invoice = str(line["Bestell-Nr."]).strip()

        print(f"Drucke Etikett {index +1}/{len(data)}: {invoice}")

        # Write the information
        handle.GetObject(adress_field).Text = adress
        handle.GetObject(invoice_field).Text = invoice

        handle.PrintOut(1, 1)

    print("success 1")
    handle.Close(str(template))
    print("success 2")

except Exception as e:
    pass

# Move file into finished folder
final_destination.mkdir(parents=True, exist_ok=True)

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