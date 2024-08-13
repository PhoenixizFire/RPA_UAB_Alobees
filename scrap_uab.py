# Imports
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv
import datetime
import time
import os
from os.path import join,dirname

# Code

# Importe les données du fichier "settings.env". A n'appeler qu'une seule foise
def init_dotenv():
    # Chemin du fichier "settings.env"
    dotenv_path = join(dirname(__file__),"settings.env")
    # Chargement des données de "settings.env" dans la mémoire du script
    load_dotenv(dotenv_path)
    # Définition de la variable globale CUSTOM_DATES (bool)
    global CUSTOM_DATES
    # Booléen si utilisation des dates pour une période personnalisée ou non. Par défaut, Date début = J-1 ; Date fin = J
    CUSTOM_DATES = os.environ.get("USE_CUSTOM_DATES")

# Paramétrage du webdriver sous Selenium
def setup(down_path):
    # Création de l'objet ChromeOptions() pour paramétrer le navigateur automatisé
    chromeOptions = webdriver.ChromeOptions()
    # Paramètre pour désactiver l'écran de choix du navigateur intempestif
    chromeOptions.add_argument("--disable-search-engine-choice-screen")
    # Paramètres pour toujours récupérer un fichier .pdf au lieu de l'ouvrir + définir le chemin de téléchargement du fichier
    chromeOptions.add_experimental_option('prefs', {"plugins.always_open_pdf_externally": True,'download.default_directory':down_path});
    # Création de l'objet webdriver sous Chrome, en incluant les paramètres définis ci-dessus
    driver = webdriver.Chrome(service=Service(),options=chromeOptions)
    # Fenêtre du navigateur agrandie
    driver.maximize_window()
    # Récupération du webdriver pour utilisation ultérieure
    return driver

# Page de connexion du site UAB
def log_uab(driver):
    # Champ username
    username = driver.find_elements(By.ID,"login_identifiant")
    env_user = os.environ.get("USER_UAB")
    if len(username)==1:
        username[0].send_keys(env_user)
    time.sleep(2)
    
    # Champ mot de passe
    password = driver.find_elements(By.ID,"login_password")
    env_password = os.environ.get("PASSWORD_UAB")
    if len(password)==1:
        password[0].send_keys(env_password)
    time.sleep(2)
    
    # Bouton valider
    nextButton = driver.find_elements(By.XPATH,"//button[contains(@type,'submit')]")
    if len(nextButton)==1:
        nextButton[0].click()
    time.sleep(5)

# Routine de connexion
def start():
    # Récupération du chemin de téléchargement dans "settings.env"
    download_path = os.environ.get("DOWNLOAD_FOLDER")
    # Démarrage du webdriver avec le paramètre ci-dessus
    driver = setup(download_path)

    # Lancement de la page de connexion UAB
    uab_url = "https://b2b.uab-adherents.fr/pa10/page-d-authentification"
    driver.get(uab_url)
    time.sleep(5)
    
    # Appel de la procédure de connexion
    log_uab(driver)
    time.sleep(3)
    return driver

# Procédure de récupération des données
def procedure(driver):
    # Liens des pages à accéder
    uab_first_dest = "https://b2b.uab-adherents.fr/pa6140/mes-chiffres-detail-des-achats"
    uab_second_dest = "https://passerelle.uab-adherents.fr/webapp/STATS_CR_visu_achats.aspx"
    # Chargement de la première page pour le cookie de connexion
    driver.get(uab_first_dest)
    time.sleep(7)
    # Chargement de la deuxième page (page interne à la première) afin de naviguer dedans librement
    driver.get(uab_second_dest)
    time.sleep(5)

    # Définition des dates de début et de fin
    use_custom_dates = os.environ.get("USE_CUSTOM_DATES")
    # Si on utilise les dates personnalisés du fichier "settings.env"
    if eval(use_custom_dates)==True:
        start_date = os.environ.get("START_DATE_UAB")
        end_date = os.environ.get("END_DATE_UAB")
    # ou si on utilise le système préconfiguré défini à j-1 et j
    else:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        start_date = yesterday.strftime("%d/%m/%Y")
        end_date = today.strftime("%d/%m/%Y")

    # Saisie de la date de début de période
    champDebut = driver.find_elements(By.XPATH,"//input[contains(@name,'ReportUsageDetailByArea_p0DiscreteValue')]")
    if len(champDebut)==1:
        champDebut[0].clear()
        champDebut[0].send_keys(start_date)
    else:
        print("len(champDebut) : "+str(len(champDebut)))

    # Saisie de la date de fin de période
    champFin = driver.find_elements(By.XPATH,"//input[contains(@name,'ReportUsageDetailByArea_p1DiscreteValue')]")
    if len(champFin)==1:
        champFin[0].clear()
        champFin[0].send_keys(end_date)
    else:
        print("len(champFin) : "+str(len(champFin)))

    # Validation des dates
    time.sleep(1)
    boutonOk = driver.find_elements(By.ID,"ReportUsageDetailByArea_submitButton")
    if len(boutonOk)==1:
        boutonOk[0].click()
    else:
        print("len(boutonOk) : "+str(len(boutonOk)))
    time.sleep(5)

    # Bouton pour ouvrir le menu d'Export
    boutonExport = driver.find_elements(By.ID,"ReportUsageDetailByArea_toptoolbar_export")
    if len(boutonExport)==1:
        boutonExport[0].click()
    else:
        print("len(boutonExport) : "+str(len(boutonExport)))
    time.sleep(2)

    # Clic sur le menu déroulant pour l'option du format d'export
    boutonFormat = driver.find_elements(By.XPATH,"//table[contains(@title,'Format de fichier :')]")
    if len(boutonFormat)>1:
        boutonFormat[0].click()
    else:
        print("len(boutonFormat) : "+str(len(boutonFormat)))
    time.sleep(1)

    # Sélection de la valeur CSV pour l'export
    boutonCsv = driver.find_elements(By.XPATH,"//span[contains(@title,'Format délimité par des caractères (CSV)')]")
    if len(boutonCsv)==1:
        boutonCsv[0].click()
    else:
        print("len(boutonCsv) : "+str(len(boutonCsv)))
    time.sleep(1)

    # Le bouton Exporter final
    boutonExporter = driver.find_elements(By.XPATH,"//a[contains(text(),'Exporter')]") #TODO ISSUE
    if len(boutonExporter)==1:
        boutonExporter[0].click()
    else:
        print("len(boutonExporter) : "+str(len(boutonExporter)))
    time.sleep(5)

# Fonction principale du script appelant les précédentes fonctions
def main():
    init_dotenv()
    driver = start()
    log_uab(driver)
    procedure(driver)

if __name__=="__main__":
    # Ici, c'est les fonction appelées lorsque le script est executé
    main()