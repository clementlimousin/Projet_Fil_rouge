# coding: utf-8
from PIL import Image
import base64
import boto3
from flask import Flask, render_template, request,jsonify, redirect, url_for, abort, \
    send_from_directory, make_response
from werkzeug.utils import secure_filename
import control_file
import PyPDF2
import base64
from json import dumps
import csv
import os
import json

# Connection avec EC3
import boto3
import logging 
from botocore.exceptions import ClientError

BUCKET_NAME ='filrougeclement'

def save_file(filename):
    OBJECT_NAME = filename
    FILE_NAME = './fichier_json/' + filename
    session = boto3.Session(profile_name='csloginstudent')
    s3 = session.client("s3")
    try:
            response =s3.upload_file(FILE_NAME,BUCKET_NAME,OBJECT_NAME)
    except ClientError as e:
        logging.error(e)
        return 'False'
    return "Le fichier est correctement envoyé"

# PDF
def generer_json_data_pdf(filename,upload_file):
    pdf = open('./uploads/' + filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pdftext =""
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        pdftext += pageObj.extractText().replace('\n','')
    filename_json = filename.replace('.pdf','.json')
    fichier_json = json.dumps({'Nom':filename,'Metadonnees':pdfReader.getDocumentInfo(), \
        'mime_type': upload_file.mimetype, 'taille':upload_file.headers.get('Content-Length'),'Donnees':pdftext})
    with open('./fichier_json/' + filename_json, "w") as json_file:
        json.dump(fichier_json, json_file)
    save_file(filename_json)
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True))


#IMAGE
def generer_json_data_image(filename,lower_extension,upload_file):
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
        filename_json = filename.replace( i ,'json')
        if ".json" in filename_json:
            break
        session = boto3.Session()
        s3_client = session.client("rekognition")
        response = s3_client.detect_labels(
            Image={"Bytes": image_read}, MaxLabels=10, MinConfidence=95
        ) 
    Labels_result = ""
    for label in response["Labels"]:
        Labels_result += "Libellé = " + label['Name'] + ' : Confiance à ' + str(label['Confidence']) + "%" + "\n"
    fichier_json = json.dumps({'Nom':filename, 'extension':lower_extension,'mime_type': upload_file.mimetype, 'taille':upload_file.headers.get('Content-Length'),'Rekognition':Labels_result,'Donnees':json_data})
    # rename the file
    with open('./fichier_json/' + filename_json, "w") as json_file:
        json_file.write(fichier_json)
    # put the file in the good folder
    # display the file
    save_file(filename_json)
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True))
   



# TXT
def generer_json_data_txt(filename,lower_extension,upload_file):
    data_json=""
    text = open('./uploads/' + filename, "r") 
    data = text.readlines()
    for contenu in data:
        data_json += contenu
    filename_json = filename.replace('.txt','.json')
    fichier_json = json.dumps({'Nom':filename, 'extension':lower_extension,\
        'mime_type': upload_file.mimetype, 'taille':upload_file.headers.get('Content-Length'),'Donnees':data_json})
    with open('./fichier_json/' + filename_json, "w") as json_file:
        json.dump(fichier_json, json_file) 
    save_file(filename_json)
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
    save_file(filename_json)
    return make_response(send_from_directory('./fichier_json/', filename_json,as_attachment=True))
                
    #curl -i -X POST -F "file=@./fichier_test/test_pdf.pdf" http://127.0.0.1:5000/upload 
    #curl -i -X POST -u "frlaissus:sio" -F "file=@./fichier_test/test_pdf.pdf" http://127.0.0.1:5000/upload
    #curl -i -X POST -u "frlaissus:sio" -F "file=@./fichier_test/test_pdf.pdf" https://filrouge.cli.p2021.ajoga.fr/upload
    #pytest -sv test.py
