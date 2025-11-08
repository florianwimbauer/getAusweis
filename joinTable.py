#!/usr/bin/env python3

import pandas as pd
import argparse
import os

# Creates the first joint table with the getAusweis .csv and the download Data (on access Codes)
def join_getAusweis_download(getAusweis, download, output):
    # Read the getAusweis file
    getAusweisReader = pd.read_csv(getAusweis, encoding="utf-8-sig")
    downloadReader = pd.read_excel(download, usecols=["Name", "Kennwort", "Gruppe / Klasse"])
    # Creates the merge
    merger = getAusweisReader.merge(downloadReader, left_on="Zugangscode", right_on="Kennwort", how="left")
    merger = merger.drop(columns=["Kennwort"])
    # Writes it to file
    outending = output + ".csv"
    merger.to_csv(outending, index=False, encoding="utf-8-sig")
    print("Join von getAusweis und Download abgeschlossen")

# Creates the second joint table with Print Data (Birthdate, Graduation, BibID, FotoNr, ...)
def join_op1_bibData(merger, bibData, output):
    # Read both files
    mergerReader = pd.read_csv(merger)
    bibReader = pd.read_excel(bibData)
    # Create the merge
    final_merger = mergerReader.merge(bibReader, on="Name", how="left")
    final_merger = final_merger.drop(columns=["Gruppe"])
    # Writes it to file
    outending = output + ".csv"
    final_merger.to_csv(outending, index=False, encoding="utf-8-sig")

# main method
def main(getAusweis, download, bibData, output):
    # Check if paths are ok
    if not os.path.exists(getAusweis):
        print("ERR: getAusweis File existiert nicht!")
        return
    if not os.path.exists(download):
        print("ERR: download File existiert nicht!")
        return
    
    # If bibData is given, also initiate second merger
    if bibData is not None:
        # Bib Data exists
        # call first with temporary file
        join_getAusweis_download(getAusweis, download, "tmp") 
        # call second from temporary file
        join_op1_bibData("tmp.csv", bibData, output)
        # Delete temporary file
        os.remove("tmp.csv")
    else:
        # BibData is None
        join_getAusweis_download(getAusweis, download, output)
        

# Call logic for main Method, argument handler
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Joinen von getAusweis Ouput mit existierenden Schülerdaten")
    parser.add_argument("--getAusweis", "-a", required=True, help="Outputfile von getAusweis")
    parser.add_argument("--download", "-d", required=True, help="Download der Zugangsdaten als .xls von Portraitbox")
    parser.add_argument("--bibData", "-b", help="Bibliotheksdaten mit ID-Path & BibID (Name muss gemeinsam sein)")
    parser.add_argument("--output", "-o", default="printable", help="Zieldatei CSV")
    args = parser.parse_args()
    main(args.getAusweis, args.download, args.bibData, args.output)