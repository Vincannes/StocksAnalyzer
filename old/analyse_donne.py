def Analyse_Donnee(data):
    global prix_achat
    analyse_data = {}
    prix = data['PRIX']
    bvps = data['BVPS']
    per = data['PER']
    dette = data['Dette']
    CA = data['Chiffre Affaire']
    bna = data['BNA']
    capitalisation = data['Capitalisation']
    dividende = data['Dividende']
    tauxdistribution =  data['Taux distribution']

    # analyse_data['Prix'] =  prix
    # BVPS
    analyse_bvps = ""
    bvps_ = []
    try:
        if bvps[1] == "SUR":
            analyse_bvps = "Prix SUR-COTE à sa valeur intrasèque : {} €.".format(bvps[0])
        elif bvps[1] == "SOUS":
            analyse_bvps = "Prix SOUS-COTE à sa valeur intrasèque : {}€".format(bvps[0])
        try:
            prix_achat = "%.2f" % (float(bvps[0]) * 0.7)
        except:
            prix_achat = "%.2f" % (float(bvps[0].replace(',', '.')) * 0.7)
        bvps_.append(analyse_bvps)
        bvps_.append("{} €".format(prix_achat))
        analyse_data['BVPS'] = bvps_
    except:
        analyse_data['BVPS'] = "Pas de Données"

    # PER
    analyse_per = ""
    if float(per) <= 10:
        analyse_per = "PER %s < 10, Entreprise SOUS-COTE." % per
    elif 10 < float(per) <= 17:
        analyse_per = "PER %s Normal , Entreprise OK." % per
    elif float(per) > 17 :
        analyse_per = "PER %s eleve , Entreprise SUR-COTE." % per
    analyse_data['PER'] = analyse_per

    # Verifier sante entreprise
    #if  bvps[1] == "SOUS-COTE" and float( per) < 10:

    # Dette
    analyse_dette = ""
    dette_ = " , ".join(str(s) + "%" for s in dette[:-1])
    if  dette[-1] == "Aucune Dette":
        analyse_dette = "Aucune Dette : {}".format(dette_)
    elif  dette[-1] == "Dette Controle":
        analyse_dette = "Dette Controle : {}".format(dette_)
    elif dette[-1] == "Sur-Endette":
        analyse_dette = "Sur-Dette : {}".format(dette_)
    analyse_data['Dette'] = analyse_dette

    # Capitalisation
    if int( capitalisation.replace(' ', '')) > 100:
        analyse_capit = "Grosse Entreprise {} M €".format( capitalisation)
    else:
        analyse_capit = "Petite Entreprise {} M €".format( capitalisation)
    analyse_data['Capitalisation'] = analyse_capit

    # Chiffre Affaire
    if CA[3].split(' ')[3] == 'croissance':
        analyse_ca = "Chiffre d'Affaire en croissance"
    else:
        analyse_ca = "Chiffre d'Affaire en décroissance"
    CA = [s + "M €" for s in CA[:-1]]
    CA.append(analyse_ca)
    analyse_data['Chiffre Affaire'] = CA

    # BNA Dividende
    if  bna[3].split(' ')[2] == "croissance" and  dividende['analyse'][2] == "croissance":
        analyse = "BNA et Dividende en croissance "
    elif  bna[3].split(' ')[2] == "décroissances" and  dividende['analyse'][2] == "croissance":
        analyse = "BNA en décroissance mais Dividende en croissance"
    else:
        analyse = "BNA et Dividende en décroissance"
    div = []
    for annee, prix in  dividende.items():
        div.append(prix)

    analyse_data['BNA'] = [s + " €" for s in bna[:-1]]
    analyse_data['Dividende'] = div[:-1]
    analyse_data['BNA Dividende'] = analyse
    analyse_data['Tresorie'] = [s + "M €" for s in data['Tresorie']]

    # Taux Distribution
    if tauxdistribution[-1] == "Croissance":
        analyse = 'Part de Dividende en croissance'
    else:
        analyse = 'Part de Dividende en decroissance'
    tauxdis = []
    for taux in tauxdistribution[:-1]:
        if taux == "-0.00":
            taux = '0'
        tauxdis.append(str(taux) + "%")
    tauxdis.append(analyse)
    analyse_data['Taux distribution'] = tauxdis

    analyse_data['ROA'] = data['ROA']
    analyse_data['ROE'] = data['ROE']
    analyse_data['Prix'] = str(data['PRIX']) + "€"

    return analyse_data
