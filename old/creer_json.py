import json

liens = open("files.txt", "r")
list_liens = {}

for lien in liens:
    all_lins = lien.split('=')[1].replace('\n', '')
    all_lins = all_lins.split(" ")
    list_liens[lien.split('=')[0]] = all_lins

with open("files.json", "w") as file:
    json.dump(list_liens, file, indent=4)