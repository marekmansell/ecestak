import fitz  # this is pymupdf
import re
from os import listdir
from os.path import isfile, join
import os

IN_DIR = "in"

all_pdf_files = []

for root, dirs, files in os.walk(IN_DIR, topdown=False):
   for name in files:
      all_pdf_files.append(join(root, name))

with open("out.csv", "w") as file:

    file.write(f"\"Číslo pracovnej cesty\"; \"Meno a priezvisko\"; \"EVČ\"; \"Suma\"\n")

    for pdf_file in all_pdf_files:

        print(f"File: {pdf_file}")


        with fitz.open(pdf_file) as doc:
            text = ""
            for page in doc:
                text += page.getText()

        print(text)

        # ID
        x = re.findall("\nVyúčtovanie pracovnej cesty č. [0-9]+\n", text) 
        print(x)
        cp_id = x[0].split(" ")[-1].strip()
        print(f"ID: {cp_id}")
        file.write(f"\"{cp_id}\";")

        # Meno
        x = re.findall("\nPriezvisko, meno, titul:\n.+\n", text) 
        print(x)
        cp_name = x[0].split("\n")[-2].strip()
        print(f"Name: {cp_name}")
        file.write(f"\"{cp_name}\";")

        # EVČ
        x = re.findall("\nVozidlo:\n.* [A-Z]{2}[0-9]{3}[A-Z]{2}\n", text) 
        print(x)
        cp_evc = x[0].split("\n")[-2].strip().split(" ")[-1]
        print(f"EVČ: {cp_evc}")
        file.write(f"\"{cp_evc}\";")

        # Suma
        x = re.findall("\nSuma na vyúčtovanie:\n[0-9]+[\,\.][0-9]+ EUR\n", text) 
        print(x)
        cp_suma = x[0].split("\n")[-2].strip().split(" ")[0].replace(",", ".")
        print(f"Suma: {cp_suma}")
        file.write(f"{cp_suma};")

        file.write(f"\n")
        print("================================")
