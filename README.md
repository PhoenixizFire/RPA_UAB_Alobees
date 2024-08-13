<h1>Robot Export UAB/Alobees</h1>
<i>Notice d'utilisation pour JMA</i>
<><>

<br>
<h4><b>Ce que fait le robot :</b></h4>

- Se connecte au site UAB
- Accède à la partie d'export des données
- Télécharge le fichier de données correspondant
- La même chose pour le site Alobees ensuite

<h4><b>Prérequis machine :</b></h4>

- Navigateur Google Chrome version 118.0 ou +
- Python 3.10 ou +
- Librairies python (versions utilisées lors du développement) :
    - dotenv (par défaut)
    - time (par défaut)
    - os (par défaut)
    - Selenium (4.11.2)
    - webdriver-manager (4.0.0)

<h4><b>Comment fonctionne le robot :</b></h4>

- Les paramètres du robot sont définis dans le fichier <a href="settings.env">settings.env</a>
- Le reste des actions est automatique, voici comment les scripts fonctionnent :

<h4><b><u>Script UAB</u></b></h4>

- Ouvre un navigateur Chrome, avec des paramètres spécifiques
- Accède à la page de connexion du site UAB
- Remplit les champs de connexion (username + mot de passe) et valide
- Accède à la page "Mon activité > Mes chiffres : Détail des achats"
- Accède à la sous-page dynamique dans laquelle interagir
- Remplit les champs de dates pour l'export et valide
- Ouvre le menu d'export
- Change le type de fichier en .csv puis exporte
- Le fichier se télécharge`*`, puis le navigateur se ferme

<h4><b><u>Script Alobees</u></b></h4>

- Ouvre un navigateur Chrome, avec des paramètres spécifiques
- Accède à la page de connexion du site UAB
- Remplit les champs de connexion (n° de téléphone + mot de passe) et valide
- Accède à la page "Feuille d'heures"
- Ouvre le menu d'export
- Remplit les champs de dates pour l'export et valide
- Le fichier se télécharge`*`, puis le navigateur se ferme


<h4><b>Pour démarrer le robot :</b></h4>

- Double-clic sur <a href="start.bat">start.bat</a>
- Sinon, Shift + clic droit dans la fenêtre du dossier => Ouvrir avec Powershell :
    - Saisir `python main.py` puis valider

`*` Le fichier Excel généré sera ajouté au répertoire enregistré dans le fichier <a href="settings.env">settings.env</a> à la valeur `DOWNLOAD_FOLDER`