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