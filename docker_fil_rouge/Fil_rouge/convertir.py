# coding: utf-8
from PIL import Image
import base64
import boto3
from flask import Flask, render_template, request,jsonify, redirect, url_for, abort, \
    send_from_directory, make_response
from werkzeug.utils import secure_filename
from datetime import datetime
import control_file
import PyPDF2
import base64
from json import dumps
import csv
import os
import json
import boto3

#BUCKET='filrougeclement'


def generer_json_data_pdf(filename):
    pdf = open('./uploads/' + filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pdftext =""
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        pdftext += pageObj.extractText().replace('\n','')
    filename_json = filename.replace('.pdf','.json')
    fichier_json = json.dumps({'Nom':filename,'Metadonnees':pdfReader.getDocumentInfo(),'Donnees':pdftext})
    with open('./fichier_json/' + filename_json, "w") as json_file:
        json.dump(fichier_json, json_file)
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True))



#IMAGE
def generer_json_data_image(filename,lower_extension):
    # reading the binary stuff
    img = open('./uploads/' + filename, 'rb')
    image_read = img.read()
    # base64 encode read data
    encoded_string = base64.b64encode(image_read)
    # decode these bytes to text
    image_encoding = encoded_string.decode('utf-8')
    # doing stuff with the data
    raw_data = {filename: image_encoding}
    # encoding the data to json
    json_data = dumps(raw_data, indent=2)
    # writing the json string to disk
    for i in ['gif','jpeg','jpg','png'] :
        filename_json = filename.replace( i ,'.json')
        if ".json" in filename_json:
            break
    fichier_json = json.dumps({'Nom':filename, 'extension':lower_extension,'Donnees':json_data})
    # rename the file
    with open('./fichier_json/' + filename_json, "w") as json_file:
        json_file.write(fichier_json)
    # put the file in the good folder
    # display the file
    #enregistrer_fichier(filename)
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True))
    #return image_encoding



            # TXT
def generer_json_data_txt(filename,lower_extension):
    data_json=""
    text = open('./uploads/' + filename, "r") 
    data = text.readlines()
    for contenu in data:
        data_json += contenu
    filename_json = filename.replace('.txt','.json')
    fichier_json = json.dumps({'Nom':filename, 'extension':lower_extension,'Donnees':data_json})
    with open('./fichier_json/' + filename_json, "w") as json_file:
        json.dump(fichier_json, json_file) 
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True)) 



            # CSV
def generer_json_data_csv(filename):
    data ={}
    with open('./uploads/' + filename, encoding='utf-8') as csvf:
        csvReader= csv.DictReader(csvf)
        for row in csvReader:
            data[csvReader.line_num] = row
        #json_data = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
    filename_json = filename.replace('.csv','.json')  
    #fichier_json = json.dumps({'Nom':filename, 'extension':lower_extension,'Donnees':json_data})
    with open('./fichier_json/' + filename_json, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))) #for pretty   
    #enregistrer_fichier(filename)
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True))


#def enregistrer_fichier(filename):
#    now = datetime.now()
#    now_string = now.strftime("%Y%m%d%H%M%S")
#    nom_fichier = secure_filename(request.files['file'].filename)
#    cle = now_string + "_" + nom_fichier
#    s3 = boto3.resource('s3')
#    s3.Bucket(BUCKET).put_object(Key=cle, Body=request.files['file'])

                
    #curl -i -X POST -F "file=@./fichier_test/test_pdf.pdf" https://127.0.0.1/upload 

