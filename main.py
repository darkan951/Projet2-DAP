####################################################################
# Description : programme permettant de scraper un site de vente   #
#               de livre d'occasion                                #
# Date : ??/??/2021                                                #
# Version : 0.1                                                    #
# Rédacteur : Franck HEBERT                                        #
####################################################################

#!/usr/bin/env python3

# Bibliothèque à importer
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/category/books/"
fin_url = "/index.html"

# Récupération des catégories
requete_init = requests.get('http://books.toscrape.com/index.html')
soup = BeautifulSoup(requete_init.content, 'html.parser')
liste_categories = soup.select('ul')[2]
categories = liste_categories.find_all('li')

test = open("test.txt", 'a')

# Parcours des catégories
cpt=2
for cat in categories:
    categorie = cat.text.strip().lower().replace(' ', '-')
    lien = base_url + categorie + '_' + str(cpt) + fin_url
    print(lien)
    test.write(lien + ' :\n')
    requete_categorie = requests.get(lien)
    contenue_categorie = BeautifulSoup(requete_categorie.content, 'html.parser')
    all_books = contenue_categorie.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    
    nb_livre = len(all_books)
    num_page = 2

    for x in all_books:
        print(x.h3.a.get('href'))
        test.write(x.h3.a.get('href') + '\n')
    
    while nb_livre % 20 == 0:
        lien_new = base_url + categorie + '_' + str(cpt) + '/page-' + str(num_page) + '.html'
        new_requete_categorie = requests.get(lien_new)
        contenue_categorie_suite = BeautifulSoup(new_requete_categorie.content, 'html.parser')
        all_books_new = contenue_categorie_suite.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        nb_livre = len(all_books_new)
        test.write(lien_new + ' :\n')
        for x in all_books_new:
            print(x.h3.a.get('href'))
            test.write(x.h3.a.get('href') + '\n')
        num_page = num_page + 1
    cpt+=1