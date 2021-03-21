# coding: utf-8
from flask import Flask, request, abort, send_from_directory, render_template
from werkzeug.exceptions import RequestEntityTooLarge
import control_file
from flask_swagger_ui import get_swaggerui_blueprint
import hashlib

#Utilisateur Hashé en SHA 256 Bit
NOM_UTILISATEUR = '7a6b0e3693b34359ffdc229548e2e6b257c8ac50649ca21726d9190978ac7ebb'
#Mot de passe Hashé en SHA 256 Bit
MOT_DE_PASSE= 'b296d052a93dce8352d58dc35c94302c7255ee9c5f2b06d99d712a6c071b4a13'



app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
#limite la taille des fichiers à 5Mo
app.config["MAX_CONTENT_LENGTH"]=8*1024*1024

# swagger specification #
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
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

@app.route('/upload', methods=['POST'])
def upload_file():
    if authorisation_acces():   
        return control_file.aiguiller(request)
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