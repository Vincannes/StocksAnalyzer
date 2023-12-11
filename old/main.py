import json
import time
from pprint import pprint
from analyse_site import Analyse_Web
from analyse_entreprise import Analyse_Enreprise
from analyse_donne import Analyse_Donnee
from SendSheet import SendGoogleSheet


list_liens = {}
with open('files.json') as json_data:
    liens_dict = json.load(json_data)

index = 1
for enterprise, lien in liens_dict.items():
   # if enterprise == "ORANGE":
    index += 1
    donne_site = Analyse_Web(enterprise, lien[0], lien[1]).__dict__
    #pprint(donne_site)
    analyse_entreprise = Analyse_Enreprise(donne_site).__dict__
    # pprint(analyse_entreprise['data_analyse'])
    analyse = Analyse_Donnee(analyse_entreprise['data_analyse'])
    analyse['Entreprise'] = enterprise
    pprint(analyse)
    SendGoogleSheet(analyse, index)
    time.sleep(45)

"""
entreprise = "BASTID"  #VALNEVA  eiffage
site = "https://www.zonebourse.com/cours/action/BASTIDE-LE-CONFORT-MEDICA-5023/fondamentaux/"
dividende = "https://www.tradingsat.com/bastide-le-confort-FR0000035370/dividende.html"

index = 43
#entreprise = list(liens_dict.keys())[index]
#sites = list(liens_dict.values())[index]


donne_site = Analyse_Web(entreprise, site, dividende).__dict__
pprint(donne_site)
analyse_entreprise = Analyse_Enreprise(donne_site).__dict__
print(analyse_entreprise['data_analyse'])
analyse = Analyse_Donnee(analyse_entreprise['data_analyse'])
analyse['Entreprise'] = entreprise
pprint(analyse)
#SendGoogleSheet(analyse, index)
"""