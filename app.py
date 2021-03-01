
from flask import Flask, request, abort, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
import control_file

app = Flask(__name__)
#limite la taille des fichiers à 5Mo
app.config["MAX_CONTENT_LENGTH"]=8*1024*1024


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