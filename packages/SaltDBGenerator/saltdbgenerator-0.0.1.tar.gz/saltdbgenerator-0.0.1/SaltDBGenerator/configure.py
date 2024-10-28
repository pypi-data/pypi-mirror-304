import json 

def change_len():
    len_salt = int(input('Entrer le nombre de caractère pour le salt : '))

    data["len"] = len_salt

    with open("config.json", "w+") as FileJsonWriter:
        json.dump(data, FileJsonWriter, indent=4)

def change_saveFile():
    filename = str(input("Entrer le nom avec l'extention du fichier de sauvegarde : "))

    data["saveFile"] = filename

    with open("config.json", "w+") as FileJsonWriter:
        json.dump(data, FileJsonWriter, indent=4)

with open("config.json", "r") as FileJsonOpenner:
    data = json.load(FileJsonOpenner)
