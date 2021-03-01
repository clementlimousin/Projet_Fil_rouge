from PIL import Image
import base64
import boto3
from flask import Flask, render_template, request,jsonify, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import control_file
import PyPDF2
import base64
from json import dumps
import csv
import os
import json


def generer_json_data_pdf(filename):
                pdf = open('./uploads/' + filename, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdf)
                pdftext =""
                for page in range(pdfReader.numPages):
                    pageObj = pdfReader.getPage(page)
                    pdftext += pageObj.extractText().replace('\n','')
                metadata = pdfReader.documentInfo
                filename_json = filename.replace('.pdf','.json')
                with open('./fichier_json/' + filename_json, "w") as json_file:
                    json.dump(pdftext, json_file)
                with open("./fichier_metadata/metadata_" + filename_json, "w") as metadata_json_file:
                    json.dump(metadata, metadata_json_file)
                #os.rename('./' + filename_json, './fichier_json/' + filename_json)
                return send_from_directory('./fichier_json/', filename_json)
            #IMAGE
def generer_json_data_image(filename):
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
                    print(filename_json)
                    if ".json" in filename_json:
                        break
                    print(filename_json)
                # rename the file
                with open('./fichier_json/' + filename_json, "w") as json_file:
                    json_file.write(json_data)
                # put the file in the good folder
                # display the file
                return send_from_directory('./fichier_json/', filename_json)
                #return image_encoding
            # TXT
def generer_json_data_txt(filename):
                data_json=""
                text = open('./uploads/' + filename, "r") 
                data = text.readlines()
                for contenu in data:
                    data_json += contenu
                filename_json = filename.replace('.txt','.json')
                with open('./fichier_json/' + filename_json, "w") as json_file:
                    json.dump(data_json, json_file) 
                return send_from_directory('./fichier_json/', filename_json)  
            # CSV
def generer_json_data_csv(filename):
                data ={}
                with open('./uploads/' + filename, encoding='utf-8') as csvf:
                    csvReader= csv.DictReader(csvf)
                    for row in csvReader:
                        print(csvReader.line_num)
                        print(len(row))
                        data[csvReader.line_num] = row
                filename_json = filename.replace('.csv','.json')  
                with open('./fichier_json/' + filename_json, "w") as f:
                    f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))) #for pretty   
                return send_from_directory('./fichier_json/', filename_json) 
