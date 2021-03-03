
import convertir
import imghdr
import os
from flask import Flask, render_template, request,jsonify, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2
import base64
from PIL import Image
import json
from json import dumps
import csv



CONTROL_CSV = ['csv']
CONTROL_TXT = ['txt']
CONTROL_PDF = ['pdf']
CONTROL_IMAGE= ['gif','jpeg','jpg','png']
CONTROL_EXTENSIONS = ['csv','gif','jpeg','jpg','md','pdf','png','txt']
CONTROL_IMAGES = ['jpg','jpeg','png']
UPLOAD_PATH = './uploads/'
UPLOAD_PATH_JSON = './uploads/fichier_json/'
UPLOAD_PATH_METADATA = './uploads/fichier_metadata/'



def aiguiller(request):
    upload_file = request.files['file']
    filename = secure_filename(upload_file.filename)
    upload_file.save(os.path.join('./uploads/', filename))
    lower_extension = filename.rsplit('.', 1)[1].lower()
    filename = filename.replace( filename.rsplit('.', 1)[1] ,lower_extension)
    if upload_file:
        if lower_extension in CONTROL_EXTENSIONS:
            if lower_extension in CONTROL_TXT:
                return convertir.generer_json_data_txt(filename)
            elif lower_extension in CONTROL_CSV:
                return convertir.generer_json_data_csv(filename)
            elif lower_extension in CONTROL_PDF:
                return convertir.generer_json_data_pdf(filename)    
            elif lower_extension in CONTROL_IMAGE:
                return convertir.generer_json_data_image(filename)
            else:
                return convertir.generer_json_vierge(request)
        else:
            return 'Accès autorisé mais le fichier ne porte pas une extension autorisée !\n'
    else:
        return 'Accès autorisé mais vous avez oublié le fichier en paramètre !\n'