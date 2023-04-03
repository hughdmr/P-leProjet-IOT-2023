import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spacy
import re

df = pd.read_csv("df30.csv")
A = df['Info']
L = A[1:]


# Charger le modèle de langue de votre choix
nlp = spacy.load("en_core_web_sm")
nlp2 = spacy.load("fr_core_news_md")

# Liste de mots à comparer
liste_mots = ["light", "brightness", "lux"]
liste_mots2 = ["luminosité", "lux", "ampoule", "électricité"]


# Chaîne de caractères à analyser
chaine = str({"00212EFFFF0820B0": {"attr": {"id": "2", "lastannounced": "2022-05-19T11: 58: 48Z", "lastseen": "2022-05-27T11: 23Z", "manufacturername": "LUMI", "modelid": "lumi.plug.maeu01", "name": "Smart plug 2",
             "swversion": "09-22-2020", "type": "Smart plug", "uniqueid": "54: ef: 44: 10: 00: 3a: 65: d6-01"}, "e": "changed", "id": "2", "r": "lumière7", "t": "event", "uniqueid": "54: ef: 44: 10: 00: 3a: 65: d6-01"}})
# chaine = re.sub(r"[^a-zA-Z]", "", chaine)
# print(chaine)
# Analyser la chaîne de caractères avec spaCy
doc = nlp(chaine)
doc2 = nlp2(chaine)


# Pour chaque mot dans la chaîne de caractères, calculer la similarité avec chaque mot de la liste donnée
for token in doc:
    token = ''.join(filter(str.isalpha, token.text))
    print(token)
    for mot in liste_mots:
        sim = token.similarity(nlp(mot))
        if sim > 0.8:  # Choisir un seuil de similarité approprié
            print("The word '{}' dans la chaîne de caractères est similaire au mot '{}' dans la liste de mots.".format(
                token.text, mot))

for token in doc2:
    for mot in liste_mots2:
        sim = token.similarity(nlp2(mot))
        if sim > 0.5:  # Choisir un seuil de similarité approprié
            print("Le mot '{}' dans la chaîne de caractères est similaire au mot '{}' dans la liste de mots.".format(
                token.text, mot))
