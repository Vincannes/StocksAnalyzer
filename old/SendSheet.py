import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SendGoogleSheet:
    def __init__(self, entreprise, index):
        self.data = entreprise
        scope = ['https://spreadsheets.google.com/feeds' + ' ' + 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('./json_api/client_secret.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open("Analyse Cac40").sheet1

        roe = "{} : {}".format(self.data['ROE'][-1], self.data['ROE'][2])
        roa = "{} : {}".format(self.data['ROA'][-1], self.data['ROA'][2])

        row = index
        # print(self.data['Chiffre Affaire'][:3])
        sheet.update_cell(row, 1, self.data['Entreprise'])
        sheet.update_cell(row, 2, self.data['Prix'])
        sheet.update_cell(row, 3, self.data['BVPS'][0])
        sheet.update_cell(row, 4, self.data['BVPS'][-1])
        sheet.update_cell(row, 5, self.data['PER'])
        sheet.update_cell(row, 6, " , ".join(self.data['Chiffre Affaire'][:3]))
        sheet.update_cell(row, 7, str(self.data['Chiffre Affaire'][-1]))
        sheet.update_cell(row, 8, self.data['Capitalisation'])
        sheet.update_cell(row, 9, self.data['Dette'])
        sheet.update_cell(row, 10, self.data['BNA'][-1])
        sheet.update_cell(row, 11, " , ".join(self.data['Dividende']))
        sheet.update_cell(row, 12, self.data['BNA Dividende'])
        sheet.update_cell(row, 13, " , ".join(self.data['Taux distribution']))
        sheet.update_cell(row, 14, self.data['Tresorie'][2])
        sheet.update_cell(row, 15, roe)
        sheet.update_cell(row, 16, roa)

        # list_of_hashes = sheet.get_all_records()
