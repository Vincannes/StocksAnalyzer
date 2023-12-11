from pprint import pprint

class Analyse_Enreprise:
    def __init__(self, entreprise=None):
        if entreprise is None:
            entreprise = {}
        self.nom_entreprise = entreprise['entreprise']
        self.data = entreprise['data_site']
        self.prix = self.data['prix']
        self.annee_en_cour = 3
        self.annee_prec = 2
        self.data_analyse = {}
        self.data_analyse['Tresorie'] = self.data['Tresorie']
        self.launcher()

    def launcher(self):
        # pprint(self.data)
        self.BVPS()
        self.PER()
        self.Dette()
        self.Capitalisaton()
        self.ChiffreAffaire()
        self.BNA()
        self.Dividende()
        self.TauxDistri()
        self.ROE()
        self.ROA()

    def croissance(self, ls_check):
        ls_croi = []
        el_prec = ls_check[0]
        for element in ls_check:
            if el_prec < element:
                ls_croi.append(True)
            else:
                ls_croi.append(False)
            el_prec = element
        decroi = ls_croi.count(False)
        croi = ls_croi.count(True)
        return croi, decroi

    def BVPS(self):
        bvps = self.data['BVPS'][self.annee_prec].replace(',', '.')
        analyse = ""
        print(bvps, self.prix)
        if float(bvps) < float(self.prix):
            analyse = "SUR"
        elif float(bvps) > float(self.prix):
            analyse = "SOUS"
        bvps_ = [bvps, analyse]
        self.data_analyse['PRIX'] = self.prix
        self.data_analyse['BVPS'] = bvps_
        print(bvps_)

    def PER(self):
        per = float(self.data['PER'][self.annee_prec][:-1].replace(",", "."))
        analyse = ""
        if per <= 0:
            analyse = per #"PER : {} négatif".format(per)
        elif per >= 17:
            analyse = per#"PER : {} SUR-évalué".format(per)
        elif 10 <= per < 17:
            analyse  = per #"PER : {} Normal".format(per)
        elif per < 10:
            analyse = per #"PER : {} SOUS-évalué".format(per)
        self.data_analyse['PER'] = analyse

    def _refacto_dette(self, dette_toref, leverage_toref):
        dette = []
        leverage = []
        for dett in dette_toref:
            if dett == "-":
                dette.append(0)
            else:
                dette.append(dett)
        for lev in leverage_toref:
            try:
                leverage.append(float(lev[:-1].replace(',', '.')))
            except:
                leverage.append(lev)
        return dette, leverage

    def Dette(self):
        dette = self.data["Dette Nette"]
        leverage = self.data["Leverage"]
        analyse = ""
        anal_leverage = []
        dette, leverage = self._refacto_dette(dette, leverage)
        for i in leverage[:3]:
            try:
                if 0 < i <= 2:
                    anal_leverage.append('Controle')
                elif i <= 0:
                    anal_leverage.append('Aucune')
                elif i > 2:
                    anal_leverage.append('Eleve')
            except:
                anal_leverage.append('Pas de Dette')
        count_ana = {'controle': anal_leverage.count("Controle"),
                     'aucun': anal_leverage.count("Aucune"),
                     'eleve': anal_leverage.count("Eleve")}
        for i, cout in count_ana.items():
            if cout == max(count_ana.values()):
                if i == "aucun":
                    analyse = "Aucune Dette"
                elif i == "controle":
                    analyse = "Dette Controle"
                elif i == "eleve":
                    analyse = "Sur-Endette"
        leverage = leverage[:3]
        leverage.append(analyse)
        self.data_analyse['Dette'] = leverage

    def Capitalisaton(self):
        capitalisation = self.data['Capitalisation'][self.annee_prec]
        self.data_analyse['Capitalisation'] = capitalisation

    def ChiffreAffaire(self):
        chiffreA = self.data["Chiffre d'affaires"][:3]
        chiffre = []
        for i in chiffreA:
            chiffre.append(i.replace(' ', ''))
        croi, decroi = self.croissance(chiffre)
        if croi > decroi:
            analyse = "Chiffre d'affaire en croissance sur les 3 dernieres années."
        elif croi < decroi and chiffre[-1] > chiffre[1]:
            analyse = "Chiffre d'affaire en décroissance mais Chiffre d'affaire en hausse la derniere année."
        else:
            analyse = "Chiffre d'affaire en décroissance sur les 3 dernieres années."
        chiffreA.append(analyse)
        self.data_analyse['Chiffre Affaire'] = chiffreA

    def BNA(self):
        bna = self.data['BNA'][:3]
        crois, decrois = self.croissance(bna)
        if crois > decrois:
            analyse = "BNA en croissance sur les 3 dernieres années."
        elif crois < decrois and bna[-1] > bna[1]:
            analyse = "BNA en décroissance mais Chiffre d'affaire en hausse la derniere année."
        else:
            analyse = "BNA en décroissance sur les 3 dernieres années."
        bna.append(analyse)
        self.data_analyse['BNA'] = bna

    def Dividende(self):
        year = self.data['Année'][:3]
        dividende = self.data['Dividende']
        data_div = {}
        for annee, div in dividende.items():
            if annee in year:
                data_div[annee] = div
            else:
                for ye in year:
                    if ye not in dividende.keys():
                        data_div[ye] = "0€"
        all_div = []
        for div in data_div.values():
            div_ = float(div[:-1])
            all_div.append(div_)
        croi, decroi = self.croissance(all_div)
        if croi > decroi:
            analyse = "Dividende en croissance."
        else:
            analyse = "Dividende en décroissances."
        data_div['analyse'] = analyse
        self.data_analyse['Dividende'] = data_div

    def TauxDistri(self):
        year = self.data['Année'][:3]
        bna = self.data['BNA'][:3]
        dividende = self.data_analyse['Dividende']
        dividend_ = []
        bna_ = []
        for anne, div in dividende.items():
            if anne not in year:
                continue
            dividend_.append(float(div[:-1].replace(',', '.')))
        for bn in bna:
            bna_.append(float(bn.replace(',', '.')))

        tauxdistri = []
        zip_object = zip(dividend_, bna_)
        for list1_i, list2_i in zip_object:
            tauxdistri.append("%.2f" % ((list1_i / list2_i)*100))

        croi, decroi = self.croissance(tauxdistri)
        if croi > decroi:
            analyse = "Croissance"
        else:
            analyse = "Decroissance"
        tauxdistri.append(analyse)
        self.data_analyse["Taux distribution"] = tauxdistri

    def ROE(self):
        roe = self.data['ROE']
        roe_ = []
        for r in roe:
            r = r.replace(',', '.')[:-1]
            roe_.append(r)
        try:
            if float(roe_[2]) < 10:
                analyse = 'Resultat Mediocre'
            else:
                analyse = 'Resultat Acceptable'
            roe.append(analyse)
            self.data_analyse['ROE'] = roe
        except:
            self.data_analyse['ROE'] = "Pas de donnée"

    def ROA(self):
        roa = self.data['ROA']
        roa_ = []
        for r in roa:
            r = r.replace(',', '.')[:-1]
            roa_.append(r)
        try:
            if float(roa_[2]) < 10:
                analyse = 'Mauvaise rentabilite'
            else:
                analyse = 'Bonne rentabilite'
            roa.append(analyse)
            self.data_analyse['ROA'] = roa
        except:
            self.data_analyse['ROA'] = "Pas de donnée"