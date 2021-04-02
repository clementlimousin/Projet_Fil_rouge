# coding: utf-8
from flask import Flask, request, abort, send_from_directory, render_template
from werkzeug.exceptions import RequestEntityTooLarge
import control_file
import convertir
from flask_swagger_ui import get_swaggerui_blueprint
import hashlib
from mdp import NOM_UTILISATEUR,MOT_DE_PASSE
# Connection avec EC3
import boto3
import logging 
from botocore.exceptions import ClientError
BUCKET_NAME ='filrougeclement'





app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
#limite la taille des fichiers à 5Mo
app.config["MAX_CONTENT_LENGTH"]=8*1024*1024

# swagger specification #
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger1.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Projet fil rouge, Clément Limousin"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# fin swagger specification ###

def authorisation_acces():
    #récupération de l'utilisateur passé en paramètre du curl
    user = request.authorization
    #hashage du nom et du mot de passe
    nom_utilisateur_hash = hashlib.sha256(user.username.encode()).hexdigest()
    mot_de_passe_hash = hashlib.sha256(user.password.encode()).hexdigest()
    #authorisation ok : retourne True
    return bool(nom_utilisateur_hash==NOM_UTILISATEUR and mot_de_passe_hash==MOT_DE_PASSE)

@app.route('/bienvenue')
def bienvenue():
    return render_template('index.html')

# Chargé un fichier dans le bucketS3
@app.route('/upload', methods=['POST'])
def upload_file():
    if authorisation_acces():   
        return control_file.aiguiller(request)
    else:
        return "Votre mot de passe ou nom d'utilisateur est incorrect"

# Liste des fichiers chargés
@app.route('/list', methods=['GET'])
def listFile():
	listeFichiers= ''
	session = boto3.Session(profile_name='csloginstudent')
	s3 = session.client("s3")
	liste = s3.list_objects(Bucket = BUCKET_NAME)
	try:
		for a in liste.get('Contents'):
			listeFichiers += a.get('Key') + '\n'
	except:
		return 'Une erreur est survenue \n'
	return(listeFichiers)

# Téléchargement d'un fichier du bucketS3
@app.route('/download/<file>', methods=['GET'])
def downloadFile(file):
	object_name = file
	liste = listFile()
	session = boto3.Session(profile_name='csloginstudent')
	s3 = session.client("s3")
	if file not in liste:
		return "Il n'y aucun fichier de ce nom \n"
	try:
		s3.download_file(BUCKET_NAME, object_name)
		uploads = os.path.join(app.config['UPLOAD_FOLDER'], file)
		file_s3 = send_file(uploads, as_attachment=True)
		os.remove(app.config['UPLOAD_FOLDER']+file)
	except: 
		return "Un problème est survenu \n"
	return file_s3

# Suppression d'un fichier dans le bucketS3
@app.route('/delete/<file>',methods=['GET'])
def deleteFile(file):
    if authorisation_acces():
        session = boto3.Session(profile_name='csloginstudent')
        s3 = session.client("s3")
        try:
            s3.delete_object(Bucket = BUCKET_NAME, Key = file)
        except ClientError as e:
            logging.error(e)
            return "Il y a eu une erreur \n"
        return 'Fichier parfaitement supprimé \n'
    else:
        return "Votre mot de passe ou nom d'utilisateur est incorrect"



    
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(413)
@app.errorhandler(500)
@app.errorhandler(RequestEntityTooLarge)
def page_erreur(error):
    return 'Vous avez rencontré une erreur {}.\n'.format(error.code), error.code