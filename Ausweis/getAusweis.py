#!/usr/bin/env python3

import argparse
import os
import re
import pymupdf
from tqdm import tqdm
import pandas as pd


# Regex für die Zugangscodes
CODE_REGEX = re.compile(r"Zugangskarte: ([^\n,;]+)", re.IGNORECASE)
# Regex für das die Klasse (Anahnd Album)
CLASS_REGEX = re.compile(r"Album: ([^\s,;]+)", re.IGNORECASE)
# Das Schlagwort dass gefunden werden soll
CHECK_WORD = "Schülerausweis"

# Seitenweise Text aus dem PDF in Liste extrahieren
def extract_text_from_pdf(path):
    text_pages = []
    try:
        doc = pymupdf.open(path)
        for p in range(doc.page_count):
            page = doc.load_page(p)
            txt = page.get_text()  # plain text
            text_pages.append(txt if txt is not None else "")
        doc.close()
    except Exception as e:
        raise RuntimeError(f"Fehler beim Lesen von {path}: {e}")
    return text_pages

# Regex auf alle extrahierten strings anwenden
def find_codes_in_text(text):
    results = []
    for m in CODE_REGEX.finditer(text):
        code_chain = m.group(1).strip()
        codes = code_chain.split()
        for code in codes:
            results.append(code)
    return results

# Regex für Klasse auf alle extrahierten strings anwenden
def find_class_in_text(text):
    results = []
    for m in CLASS_REGEX.finditer(text):
        class_chain = m.group(1).strip()
        classS = class_chain.split()
        for c in classS:
            results.append(c)
    return list(set(results))

# Ein einzelnes PDF mit find_codes und extract_text verarbeiten
def process_pdf(path, withClass):
    entries = []
    text_pages = extract_text_from_pdf(path)
    joined_text = "\n".join(text_pages)
    if CHECK_WORD in joined_text:
        # Datei enthält das Stichwort -> suche nach codes (seitenweise)
        for i, page_text in enumerate(text_pages):
            found = find_codes_in_text(page_text)
            classS = find_class_in_text(joined_text)
            for code in found:
                if withClass:
                    entries.append({
                    "Re-NR": re.search(r"\d+", os.path.basename(path)).group(),
                    "Zugangscode": code,
                    "Klasse": ", ".join(classS)
                    })
                else: 
                    entries.append({
                    "Re-NR": re.search(r"\d+", os.path.basename(path)).group(),
                    "Zugangscode": code
                    })
    return entries

# Mainfunktion zum Aufruf
def main(input_dir, output_csv, recursive=False, withClass=False):
    # Sammle PDF-Dateien
    pdf_files = []
    if recursive:
        for root, dirs, files in os.walk(input_dir):
            for f in files:
                if f.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(input_dir):
            if f.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(input_dir, f))

    pdf_files.sort()
    all_entries = []
    for path in tqdm(pdf_files, desc="PDFs verarbeiten"):
        try:
            ents = process_pdf(path, withClass)
            all_entries.extend(ents)
        except Exception as e:
            print(f"[FEHLER] {path}: {e}")

    if not all_entries:
        print("Keine Codes gefunden (oder keine Dateien enthalten 'Schülerausweis').")
    else:
        # Schreibe CSV
        df = pd.DataFrame(all_entries)
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        if withClass:
            print(f"Ergebnis: {len(df)} Codes nach {output_csv} mit Klassen-Spalte extrahiert")
        else: 
            print(f"Ergebnis: {len(df)} Codes nach {output_csv} extrahiert")

    return all_entries

# Skript Logik, define main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrahiere Zugangscodes aus PDFs, falls 'Schülerausweis' enthalten ist.")
    parser.add_argument("--input", "-i", required=True, help="Ordner mit PDF-Dateien")
    parser.add_argument("--output", "-o", default="extracted_codes.csv", help="Zieldatei CSV")
    parser.add_argument("--recursive", "-r", action="store_true", help="Durchsuche Unterverzeichnisse rekursiv")
    parser.add_argument("--withClass", "-c", action="store_true", help="Klassen Spalte zur Kontrolle der Ausgabe anfügen")
    args = parser.parse_args()
    main(args.input, args.output, recursive=args.recursive, withClass=args.withClass)
