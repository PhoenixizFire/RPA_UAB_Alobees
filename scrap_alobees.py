# Imports
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv
import time
import datetime
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

# Page de connexion du site Alobees
def log_alobees(driver):
    # Champ n de téléphone
    username = driver.find_elements(By.ID,"phoneNumber")
    env_user = os.environ.get("USER_ALOBEES")
    if len(username)==1:
        username[0].send_keys(env_user)
    time.sleep(2)
    
    # Champ mot de passe
    password = driver.find_elements(By.ID,"password")
    env_password = os.environ.get("PASSWORD_ALOBEES")
    if len(password)==1:
        password[0].send_keys(env_password)
    time.sleep(2)
    
    # Bouton connexion
    nextButton = driver.find_elements(By.XPATH,"//button[contains(text(),'Connexion')]")
    if len(nextButton)==1:
        nextButton[0].click()
    time.sleep(5)

# Routine de connexion
def start():
    # Récupération du chemin de téléchargement dans "settings.env"
    download_path = os.environ.get("DOWNLOAD_FOLDER")
    # Démarrage du webdriver avec le paramètre ci-dessus
    driver = setup(download_path)

    # Lancement de la page de connexion Alobees
    alobees_url = "https://app.alobees.com/login"
    driver.get(alobees_url)
    time.sleep(5)
    
    # Appel de la procédure de connexion
    log_alobees(driver)
    time.sleep(3)
    return driver

# Procédure de récupération des données
def procedure(driver):
    # Accès à la page cible
    alobees_first_dest = "https://app.alobees.com/timesheets"
    driver.get(alobees_first_dest)
    time.sleep(7)

    # Bouton du menu Export
    boutonExport = driver.find_elements(By.XPATH,"//button[contains(text(),'Exporter')]")
    if len(boutonExport)==1:
        boutonExport[0].click()
    else:
        print("len(boutonExport) : "+str(len(boutonExport)))

    # Définition des dates de début et de fin
    use_custom_dates = os.environ.get("USE_CUSTOM_DATES")
    # Si on utilise les dates personnalisés du fichier "settings.env"
    if eval(use_custom_dates)==True:
        start_date = os.environ.get("START_DATE_ALOBEES")
        end_date = os.environ.get("END_DATE_ALOBEES")
    # ou si on utilise le système préconfiguré défini à j-1 et j
    else:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        start_date = yesterday.strftime("%d/%m/%Y")
        end_date = today.strftime("%d/%m/%Y")

    # Saisie des dates de début et de fin
    champFin = driver.find_elements(By.XPATH,"//input[contains(@placeholder,'--/--/----')]")
    if len(champFin)==2:
        champFin[0].clear()
        champFin[0].send_keys(start_date)
        
        champFin[1].clear()
        champFin[1].send_keys(end_date)
    else:
        print("len(champFin) : "+str(len(champFin)))
    
    # Validation de l'export
    boutonExporter = driver.find_elements(By.XPATH,"//button[contains(text(),'Exporter')]")
    if len(boutonExporter)==2:
        boutonExporter[1].click()
    else:
        print("len(boutonExporter) : "+str(len(boutonExporter)))
    time.sleep(5)

# Fonction principale du script appelant les précédentes fonctions
def main():
    init_dotenv()
    driver = start()
    log_alobees(driver)
    procedure(driver)

if __name__=="__main__":
    # Ici, c'est les fonction appelées lorsque le script est executé
    main()