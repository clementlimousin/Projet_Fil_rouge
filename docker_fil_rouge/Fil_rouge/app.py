# coding: utf-8
from flask import Flask, request, abort, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
import control_file
from flask_swagger_ui import get_swaggerui_blueprint

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

@app.route('/bienvenue')
def bienvenue():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
   
    return control_file.aiguiller(request)
    
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(413)
@app.errorhandler(500)
@app.errorhandler(RequestEntityTooLarge)
def page_erreur(error):
    return 'Vous avez rencontré une erreur {}.\n'.format(error.code), error.code