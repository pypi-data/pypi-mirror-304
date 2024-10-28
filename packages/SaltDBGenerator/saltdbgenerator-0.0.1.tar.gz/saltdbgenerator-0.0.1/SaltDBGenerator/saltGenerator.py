import json
import random
import datetime


with open("config.json", "r") as FileJsonOpenner:
    data = json.load(FileJsonOpenner)


heure = datetime.datetime.now().strftime("%H:%M")

def generate_salt():

    maj = "ABCDEFGHIJKLMNOP"
    minu = "abcdefghijklmnop"

    all_ = maj + minu
    len_car = data["len"]

    salt = "".join(random.sample(all_, len_car))

    data["lastSalt"] = salt
    
    with open("config.json", "w+") as FileJsonWriter:
        json.dump(data, FileJsonWriter, indent=4)

        FileJsonWriter.close()
    print(salt)

    with open(data["saveFile"], "a+") as saveFileWriter:
        saveFileWriter.write(f"[DATETIME]: {heure}\n[SALT_INFO]: {salt}\n"+ "-"*9 + "\n")

def print_last_salt():    
    print(data["lastSalt"])

