TABLE = {
    'BRACELET':  {'trigram': 'bra', 'trigram_group': 'bra'},
    'BOITIER':   {'trigram': 'boi', 'trigram_group': 'boi'},
    'REMONTOIR': {'trigram': 'cap', 'trigram_group': 'boi'},
    'LUNETTE':   {'trigram': 'lte', 'trigram_group': 'boi'},
    'CYCLOPE':   {'trigram': 'cyc', 'trigram_group': 'cdm'},
    'AIGUILLES': {'trigram': 'aig', 'trigram_group': 'cdm'},
    'REHAUT':    {'trigram': 'jnt', 'trigram_group': 'cdm'},
    'DECALQUE':  {'trigram': 'deq', 'trigram_group': 'cdm'},
    'APPLIQUES': {'trigram': 'apl', 'trigram_group': 'bra'},
    'CADRAN':    {'trigram': 'cdm', 'trigram_group': 'cdm'},
}
trigram = 'bra'
for i, n in TABLE.items():
    for group, value in n.items():
        if group != "trigram":
            continue
        if value == trigram:
            print(i)