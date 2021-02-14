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


# Définition du format des images
app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.gif','.png','.jpg', '.pdf','.txt', '.csv']
format_img = ['.gif','.jpg','.png']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_PATH_JSON'] = 'fichier_json'
app.config['UPLOAD_PATH_METADATA'] = 'fichier _metadata'
# Validation de l'image
def validate_image(stream):
     header = stream.read(512)  
     stream.seek(0)  
     format = imghdr.what(None, header)
     if not format:
        return None
     return '.' + (format if format != 'jpeg' else 'jpg')


# Affichage de la page web
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html')

# Chargement de l'image dans le dossier uploads
@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        #PDF
        if file_ext in ['.pdf']:
            pdf = open("./uploads/" + filename, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdf)
            pdftext =""
            for page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page)
                pdftext += pageObj.extractText().replace('\n','')
            metadata = pdfReader.documentInfo
            filename_json = filename.replace('.pdf','.json')
            with open(filename_json, "w") as json_file:
                json.dump(pdftext, json_file)
            with open("metadata_" + filename_json, "w") as metadata_json_file:
                json.dump(metadata, metadata_json_file)
            os.rename('./' + filename_json, './fichier_json/' + filename_json)
            return send_from_directory(app.config['UPLOAD_PATH_JSON'], filename_json)
        #IMAGE
        elif file_ext in format_img:
            # reading the binary stuff
            img = open("./uploads/" + filename, 'rb')
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
            for i in format_img :
                filename_json = filename.replace( i ,'.json')
                print(filename_json)
                if ".json" in filename_json:
                    break
                print(filename_json)
            # rename the file
            with open(filename_json, "w") as json_file:
                json_file.write(json_data)
            # put the file in the good folder
            os.rename('./' + filename_json, './fichier_json/' + filename_json)    
            # display the file
            return send_from_directory(app.config['UPLOAD_PATH_JSON'], filename_json)
            #return image_encoding
        # TXT
        elif file_ext in '.txt':
            data_json=""
            text = open("./uploads/" + filename, "r") 
            data = text.readlines()
            for contenu in data:
                data_json += contenu
            filename_json = filename.replace('.txt','.json')
            with open(filename_json, "w") as json_file:
                json.dump(data_json, json_file)
            os.rename('./' + filename_json, './fichier_json/' + filename_json)   
            return send_from_directory(app.config['UPLOAD_PATH_JSON'], filename_json)  
        # CSV
        elif file_ext in '.csv':
            data ={}
            with open("./uploads/" + filename, encoding='utf-8') as csvf:
                csvReader= csv.DictReader(csvf)
                for row in csvReader:
                    print(csvReader.line_num)
                    print(len(row))
                    data[csvReader.line_num] = row
            filename_json = filename.replace('.csv','.json')  
            with open(filename_json, "w") as f:
                f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))) #for pretty    
            os.rename('./' + filename_json, './fichier_json/' + filename_json)   
            return send_from_directory(app.config['UPLOAD_PATH_JSON'], filename_json)  
            
       
            



    #uploaded_file.save(secure_filename(uploaded_file.filename))
    #with open(uploaded_file, "rb") as image_file:
    #    encoded_string = base64.b64encode(image_file.read())
    #return encoded_string


    

# Affiche les metadata de l'image choisi
 #@app.route('/<filename>/metadata')
#def metadata(filename):
#    im = Image.open("./uploads/"+  filename)
 #   metadata = {"size": im.size, "format" : im.format, "mode" : im.mode, "filename" : im.filename, "info" : im.info}
 #   return metadata

# Affiche l'image choisi
#@app.route('/<filename>')
#def upload(filename):
 #   return send_from_directory(app.config['UPLOAD_PATH'], filename)