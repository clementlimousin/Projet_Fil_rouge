# Description

Cette application est le projet FIL ROUGE fait dans le cadre de mon mastère SIO 2021 à centrale supélec .Il a pour but de construire une API qui renvoie un fichier en format JSON ainsi que les metadatas associés. L'application doit être capable de convetir des fichiers image, PDF, txt et csv.

# Utilisation

## Local

### Installation de git
- FreeBSD : 
``` 
sudo pkg install git
``` 
- Ubuntu
``` 
sudo apt install git-all
``` 
### Importer le répertoire sur votre ordinateur

Dans une console, placer vous dans votre répertoire de travail et récupérer le projet avec la commande :
```
git clone https://github.com/clementlimousin/Projet_Fil_rouge.git
```
### Installation des requirements
1) Installer python
``` 
 sudo pkg install python
 ``` 
2) Installer pip
``` 
 sudo pkg install py37-pip
 ``` 
3) Installer les packages requis
``` 
Exemple : pip install -r requirements.txt
``` 
## Lancement du serveur 
Windows :
``` 
set FLASK_APP=app.py
``` 
ou linux :
``` 
export FLASK_APP=app.py
``` 
puis lancer le serveur flask
``` 
flask run
```
## A distance

L'application sera disponible à l'url suivante: 
https://filrouge.cli.p2021.ajoga.fr/

# Fonctionnalité

## /bienvenue

Une page de bienvenue est renvoyée.

```
curl https://filrouge.cli.p2021.ajoga.fr/bienvenue
```

## /upload

Cette fonctionnalité permet d'envoyer un fichier dans les formats suivant: .txt , .pdf , .csv, .jpg , . png , .gif
L'API stocke et renvoie un fichier sous format JSON avec ses métadata.
Pour les formats images, rekognition est associé à cette API.

exemple de commande:
```
curl -i -X POST -u "frlaissus:sio" -F "file=@./fichier_test/test_pdf.pdf" https://filrouge.cli.p2021.ajoga.fr/upload
```

## /list

La liste des fichiers chargés est renvoyée.

```
curl https://filrouge.cli.p2021.ajoga.fr/list
```

## /delete/{fichier}

Permet de supprimer un fichier chargé.

exemple de commande:
```
curl -i -X POST -u "frlaissus:sio" https://filrouge.cli.p2021.ajoga.fr/delete/test_pdf.pdf
```

## /download/{fichier}

Permet de téléchargé un fichier préalablement chargé.

exemple de commande:
```
curl -i -X POST -u "frlaissus:sio" https://filrouge.cli.p2021.ajoga.fr/download/test_pdf.pdf
```

# Documentation

L'application est documenté à l'adresse :

à distance :
https://filerouge.cli.p2021.ajoga.fr/swagger

en local : http://127.0.0.1:5000/swagger

# TEST

Pour faire les tests unitaires, Il faut se placer dans le dossier du projet fil rouge et utiliser la commande suivante :

``` 
pytest -sv test.py
```

