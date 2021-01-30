####################################################################
# Description : programme permettant de scraper un site de vente   #
#               de livre d'occasion                                #
# Date : 29/01/2021                                                #
# Version : 1.0                                                    #
# Rédacteur : Franck HEBERT                                        #
####################################################################

#!/usr/bin/env python3

# Bibliothèque à importer
import requests
from bs4 import BeautifulSoup
import csv
import os

# Initialisation de l'adresse initiale où attaquer le site web
base_url = 'http://books.toscrape.com/catalogue/category/books/'
fin_url = '/index.html'


# Création de l'arborescence de fichier pour stocket les images et les csv
if os.path.exists('./CSV') == False :
    os.mkdir('./CSV')
if os.path.exists('./Images') == False :
    os.mkdir('./Images')

# Récupération des catégories
requete_init = requests.get('http://books.toscrape.com/catalogue/category/books/travel_2/index.html')
soup = BeautifulSoup(requete_init.content, 'html.parser')
liste_categories = soup.select('ul')[2]
categories = liste_categories.find_all('li')

# Parcours des catégories
cpt=2
for cat in categories:
    # initialisation du dictionnaire pour remplir le CSV
    all_info = []

    # Création de la sous arborescence du dossier image pour les ranger par catégories
    img_dir = './Images/' + cat.text.strip().replace(' ', '_')
    if os.path.exists(img_dir) == False :
        os.mkdir(img_dir)

    categorie_script = cat.text.strip().lower().replace(' ', '-')
    lien = base_url + categorie_script + '_' + str(cpt) + fin_url

    requete_categorie = requests.get(lien.strip())
    contenue_categorie = BeautifulSoup(requete_categorie.content, 'html.parser')
    all_books = contenue_categorie.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    
    # Calcul du nombre de livre dans sur la page
    nb_livre = len(all_books)

    # Initialisation de la variable servant au parcour des pages supplémentaire
    num_page = 2

    # Parcours des livres de la premiere page
    for x in all_books:
        # Initialisation de l'adresse des livres
        lien_livre = 'http://books.toscrape.com/catalogue/' + x.h3.a.get('href').split(sep='/')[3] + '/' + x.h3.a.get('href').split(sep='/')[4]

        # Requete sur la page du livre et initialisation de la Soup
        livre_req = requests.get(lien_livre.strip())
        livre_soup = BeautifulSoup(livre_req.content, 'html.parser')

        # Récupération des différentes informations de chaque livres
        titre = livre_soup.select('h1')[0].text.strip()
        lien_image = livre_soup.select('img')[0].get('src')
        url_image =  lien_image.replace('../../', 'http://books.toscrape.com/')
        categorie = livre_soup.select('li')[2].text.strip()
        description = livre_soup.select('p')[3].text.strip()
        nb_dispo = livre_soup.select('p')[1].text.strip()
        upc = livre_soup.select('td')[0].text.strip()
        prix_HT = livre_soup.select('td')[2].text.strip()
        prix_TTC = livre_soup.select('td')[3].text.strip()
        nb_star = livre_soup.select('p')[2].get('class')
        rating = nb_star[1] + " stars"

        # Enregistrement de l'image du livre
        image_data = requests.get(url_image).content
        titre_clean = titre.translate({ord(c): "" for c in "!@#$%^&*()[]{\r};:,./<>?\\|`~-=_+\"\'"})
        img_name = img_dir + '/' + titre_clean.replace(" ","_") + '.jpg'
        with open(img_name, 'wb') as img:
            img.write(image_data)

        # Stockage des informations dans un dictionnaire
        all_info.append({
            "product_page_url": lien_livre,
            "universal_ product_code": upc,
            "title": titre,
            "price_including_tax": prix_TTC,
            "price_excluding_tax": prix_HT,
            "number_available": nb_dispo,
            "product_description": description,
            "category": categorie,
            "review_rating": rating,
            "image_url": url_image,
        })
    
    # Parcours des différentes pages
    while nb_livre % 20 == 0:
        lien_new = base_url + categorie_script + '_' + str(cpt) + '/page-' + str(num_page) + '.html'
        new_requete_categorie = requests.get(lien_new.strip())

        if new_requete_categorie.status_code == 200 :
            contenue_categorie_suite = BeautifulSoup(new_requete_categorie.content, 'html.parser')
            all_books_new = contenue_categorie_suite.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

            # Parcours des livres des différentes pages
            for x in all_books_new:
                lien_livre = 'http://books.toscrape.com/catalogue/' + x.h3.a.get('href').split(sep='/')[3] + '/' + x.h3.a.get('href').split(sep='/')[4]

                # Requete sur la page du livre et initialisation de la Soup
                livre_req = requests.get(lien_livre.strip())
                livre_soup = BeautifulSoup(livre_req.content, 'html.parser')

                # Récupération des différentes informations de chaque livres
                titre = livre_soup.select('h1')[0].text.strip()
                lien_image = livre_soup.select('img')[0].get('src')
                url_image =  lien_image.replace('../../', 'http://books.toscrape.com/')
                categorie = livre_soup.select('li')[2].text.strip()
                description = livre_soup.select('p')[3].text.strip()
                nb_dispo = livre_soup.select('p')[1].text.strip()
                upc = livre_soup.select('td')[0].text.strip()
                prix_HT = livre_soup.select('td')[2].text.strip()
                prix_TTC = livre_soup.select('td')[3].text.strip()
                nb_star = livre_soup.select('p')[2].get('class')
                rating = nb_star[1] + " stars"

                # Enregistrement de l'image du livre
                image_data = requests.get(url_image).content
                titre_clean = titre.translate({ord(c): "" for c in "!@#$%^&*()[]{\r};:,./<>?\\|`~-=_+\"\'"})
                img_name = img_dir + '/' + titre_clean.replace(" ","_") + '.jpg'
                with open(img_name, 'wb') as img:
                    img.write(image_data)

                # Stockage des informations dans un dictionnaire
                all_info.append({
                    "product_page_url": lien_livre,
                    "universal_ product_code": upc,
                    "title": titre,
                    "price_including_tax": prix_TTC,
                    "price_excluding_tax": prix_HT,
                    "number_available": nb_dispo,
                    "product_description": description,
                    "category": categorie,
                    "review_rating": rating,
                    "image_url": url_image,
                })

            nb_livre = len(all_books_new)

            # Incrémentation du numéro de la page du livre
            num_page = num_page + 1
        else:
            break
    
    # Stockage des clés du dictionnaire
    keys = all_info[0].keys()

    # Création du CSV avec les clés du dictionnaire comme nom de colonne
    with open('./CSV/liste_livre_' + cat.text.strip() + '.csv', 'w', newline='', encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_info)
    
    # Incrémentation du compteur pour le passage à la catégorie suivante
    cpt+=1