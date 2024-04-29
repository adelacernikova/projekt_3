# projekt_3

# nejprve si v prikazove radce vytvorim vyrtualni prostredi
python -m venv projekt_3
# aktivuju si ho
projekt_3\Scripts\activate
# nainstaluju knihovny potrebne pro program - jsou vypsane v souboru reqiurements.txt
python -m pip install requests
python -m pip install beautifulsoup4

# pro vygenerovani requests
pip install pipreqs
# spustim
pipreqs


# samotny projekt spustim z prikazove radky - prvni argument je okres, pro ktery chci vysledky dotahovat, a druhy argument je nazev vystupniho csv souboru
python projekt_3.py "Prostějov" "vysledky_prostejov.csv"
