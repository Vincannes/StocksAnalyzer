import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

class Analyse_Web:
    def __init__(self, entreprise, zoneb, bfmb):
        self.entreprise = entreprise
        self.bfmb = bfmb
        self.zoneb = zoneb
        self.data_site = {}
        self.scrap_site_zoneb()

    def scrap_data(self, dico_data, ind_name, elements):
        element = []
        for el in elements:
            element.append(el.text)
        dico_data[ind_name] = element
        return dico_data

    def scrap_site_zoneb(self):
        response = requests.get(self.zoneb)
        soup = BeautifulSoup(response.text)
        annee = soup.findAll("td", {"class": "bc2Y"})
        indicator = soup.findAll("td", {"class": "bc2T"})
        values = soup.findAll("td", {"class": "bc2V"})

        # Prix
        prix = soup.find(id='zbjsfv_dr').text
        self.data_site['prix'] = prix
        # Année
        self.scrap_data(self.data_site, "Année", annee[0:6])
        # Capitalisation
        self.scrap_data(self.data_site, indicator[0].text[:-1], values[0:6])
        # PER
        self.scrap_data(self.data_site, indicator[2].text, values[12:18])
        # Rendement
        self.scrap_data(self.data_site, indicator[3].text, values[18:24])
        # BNA
        self.scrap_data(self.data_site, indicator[18].text[:-1], values[108:114])
        # Chiffre d'affaire
        self.scrap_data(self.data_site, indicator[11].text[:-1], values[66:72])
        # EBITDA
        self.scrap_data(self.data_site, indicator[12].text[:-1], values[72:78])
        # EBIT Résultat d'exploitation
        self.scrap_data(self.data_site, indicator[13].text[:-8], values[78:84])
        # EBT Résultat Net avant Impot
        self.scrap_data(self.data_site, indicator[15].text[:-7], values[90:96])
        # Résultat Net
        self.scrap_data(self.data_site, indicator[16].text[:-1], values[96:102])
        # Marge Nette
        self.scrap_data(self.data_site, indicator[17].text, values[102:108])
        # Dividende / Action
        self.scrap_data(self.data_site, indicator[19].text[:-1], values[114:120])
        # Dette Nette
        self.scrap_data(self.data_site, "Dette Nette", values[126:132])
        # Leverage (Dette/EBITDA)
        self.scrap_data(self.data_site, indicator[23].text[:8], values[138:144])
        # Trésorie Nette
        self.scrap_data(self.data_site, "Tresorie", values[132:138])
        # Free ClashFlow
        self.scrap_data(self.data_site, indicator[24].text[:-1], values[144:150])
        # ROE
        self.scrap_data(self.data_site, indicator[25].text[:3], values[150:156])
        # ROA
        self.scrap_data(self.data_site, indicator[27].text[:3], values[162:168])
        # Capitaux Propres
        self.scrap_data(self.data_site, indicator[26].text[:-1], values[156:162])
        # Totals Actifs
        self.scrap_data(self.data_site, indicator[28].text[:-1], values[168:174])
        # BVPS
        self.scrap_data(self.data_site, indicator[29].text[:4], values[174:180])
        # CPS (CashFlow par Action)
        self.scrap_data(self.data_site, indicator[30].text[:3], values[180:186])

        # Nombre d'employé
        employe = soup.findAll("div", {"class": "fCCR"})
        nombre = 0
        for i in employe:
            if i.text.startswith("Nombre d'employés"):
                nombre = " ".join(re.findall('\d+', i.text))

        self.data_site["Nombre d'employés"] = nombre

        self.data_site["Dividende"] = self.scrap_site_bfmb()
        return self.data_site

    def scrap_site_bfmb(self):
        response = requests.get(self.bfmb)
        soup = BeautifulSoup(response.text)
        test = soup.findAll("tr")#, {"class": "even"})
        div_dic = {}
        try:
            for i in test[1:8]:
                if i.text.split('\n')[-2].endswith('€'):
                    if i.text.split('\n')[1] .isdigit():
                        year = i.text.split('\n')[1]
                        price = i.text.split('\n')[-2]
                        div_dic[year] = price
        except:
            try:
                for i in test[1:3]:
                    if i.text.split('\n')[-2].endswith('€'):
                        if i.text.split('\n')[1] .isdigit():
                            year = i.text.split('\n')[1]
                            price = i.text.split('\n')[-2]
                            div_dic[year] = price
            except:
                div_dic['year'] = "Aucune donnée"
        return div_dic