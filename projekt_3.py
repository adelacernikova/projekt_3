"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Adéla Černíková
email: adela.cernikova@seznam.cz
discord: adelacernikova_89606
"""


import sys # spousteni s argumentama
import csv

import requests
from bs4 import BeautifulSoup



# Získání argumentů z příkazové řádky
okres = sys.argv[1] # napr. "Prostějov"
vystupni_soubor = sys.argv[2] # napr. "vysledky_prostejov.csv"


# Pokud uživatel nezadá oba argumenty program jej upozorní a nepokračuje.
if not okres or not vystupni_soubor:
    print("Chybí zadání územního celku nebo jména výstupního souboru")
    # jednička představuje obecně jakoukoliv chybu
    sys.exit(1)
else:
    print("Program pokračuje..")


def najdi_okres(okres: str):
    """
    vyhledava vstupni argument mezi okresama na strance s vysledkama voleb
    pro dany okres ziska url adresu s obcemi v danem okresu
    """
    url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    # Stahování HTML stránky
    odpoved_serveru = requests.get(url)
    rozdeleny_text = BeautifulSoup(odpoved_serveru.content, 'html.parser')

    # Najít všechny řádky (tr) s okresama
    radky = rozdeleny_text.find_all('tr')
    # Projít všechny řádky a najít ten, který obsahuje zadany okres
    for radek in radky:
        cells = radek.find_all('td')
        if cells != []:
            nazev_okres = cells[1].text.strip()
            if nazev_okres == okres:
                odkaz_cast = cells[3].find('a')['href']
                url_okres = (f" https://volby.cz/pls/ps2017nss/{odkaz_cast}")
                #requests.get(f" https://volby.cz/pls/ps2017nss/{odkaz_cast}"
                najdi_obce(url_okres)
                break
            else:
                print("Okres nenalezen")


def najdi_obce(url_okres: str):
    """
    najde vsechny obce v danem okresu a pro kazdou obec dohleda url adresu stranky, na ktere jsou vysledky za danou obec
    """
    obce = []

    # Vytvoření objektu BeautifulSoup
    odpoved_serveru = requests.get(url_okres)
    rozdeleny_text = BeautifulSoup(odpoved_serveru.content, 'html.parser')

    # Najít všechny řádky (tr) s obcemi
    radky = rozdeleny_text.find_all('tr')
    # Projít všechny řádky a ulozit si nazvy obci, jejich cisla a url
    for radek in radky:
        nazev_obec_td = radek.find("td", {"class": "overflow_name"})
        if nazev_obec_td != None:
            cislo_obec = radek.find("td", {"class": "cislo"}).get_text()
            nazev_obec = nazev_obec_td.get_text()
            odkaz_obec_cast = radek.find('a')['href']
            url_obec = (f" https://volby.cz/pls/ps2017nss/{odkaz_obec_cast}")
            obec = [cislo_obec, nazev_obec, url_obec]
            obce.append(obec)

    # pripravim vystupni soubor CSV
    vystupni_csv(obce)


def vystupni_csv(obce: list):
    """
    vytvori nove CSV s hlavickama. Nazev CSV zadal uzivatel pri sousteni programu
    """
    # vytvorim si vystupni CSV soubor
    prvni_obec = True
    for obec in obce:
        url_obec = obec[2]
        odpoved_serveru = requests.get(url_obec)
        rozdeleny_text = BeautifulSoup(odpoved_serveru.content, 'html.parser')

        # v prvnim behu pripravi vystupni CSV soubor
        if prvni_obec:
            hlavicka = ["code", "location", "registered","envelopes","valid"]
            radky = rozdeleny_text.find_all('tr')
            for radek in radky:
                strana = radek.find("td", {"class": "overflow_name"})
                if strana != None:
                    nazev_strany = strana.get_text()
                    hlavicka.append(nazev_strany)

            # vytvorim nove CSV s hlavickou
            nove_csv = open(vystupni_soubor, mode="w", newline="")
            zapisovac = csv.writer(nove_csv, delimiter=";")
            zapisovac.writerow(hlavicka)
            nove_csv.close()

            prvni_obec = False # nastavim na False, aby se pri pristim behu znovu nevytvarel CSV soubor

        # pro kazdou obec dotahnu vysledky a pridam je do CSV souboru
        vysledky_voleb_obec(rozdeleny_text, obec)


def vysledky_voleb_obec(rozdeleny_text: BeautifulSoup, obec: str):
    """
    pro zadanou obec dohledam vysledky voleb a nahraju do pripraveneho CSV souboru
    """
    # celkove o´pocty za obec
    registered = rozdeleny_text.find("td", {"class": "cislo", "headers": "sa2", "data-rel": "L1"}).text
    envelopes = rozdeleny_text.find("td", {"class": "cislo", "headers": "sa3", "data-rel": "L1"}).text
    valid = rozdeleny_text.find("td", {"class": "cislo", "headers": "sa6", "data-rel": "L1"}).text

    # pripravim si zactek radku pro vkladani do CSV
    radek_csv = [obec[0], obec[1], registered,envelopes,valid]

    # pocty hlasu pro jednotlive strany
    radky = rozdeleny_text.find_all('tr')
    for radek in radky:
        strana = radek.find("td", {"class": "overflow_name"})
        if strana != None:
            cells = radek.find_all('td')
            pocet_hlasu = cells[2].get_text()
            radek_csv.append(pocet_hlasu) # pridavam do CSV radku

    # zapisu novy radek do CSV
    nove_csv = open(vystupni_soubor, mode="a", newline="")
    zapisovac = csv.writer(nove_csv, delimiter=";")
    zapisovac.writerow(radek_csv)
    nove_csv.close()




# ************************** spousteni ***********************************************
najdi_okres(okres)