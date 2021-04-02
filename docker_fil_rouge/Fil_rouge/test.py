import unittest
import io
from requests.auth import _basic_auth_str
from app import app


class TestFilRouge(unittest.TestCase):
    def test_uploadCSV(self):
            print('\n |---------------Upload un fichier CSV---------------|')
            with app.test_client() as client:
                username = 'laissus'
                password = 'sio'
                with open('./fichier_test/test_csv.csv','rb') as fichier:
                    fichierIO = io.BytesIO(fichier.read())
                maData = {'monFichier': (fichierIO, 'test_csv.csv')}
                maReponse = client.post('/upload', headers={'Authorization': _basic_auth_str(username, password)}, \
                        data=maData, content_type='multipart/form-data')
                print("Aboutissement de la requête (200 si ok):", maReponse.status_code)
                assert maReponse.status_code == 200
    def test_uploadPNG(self):
            print('\n |---------------Upload un fichier PNG---------------|')
            with app.test_client() as client:
                username = 'laissus'
                password = 'sio'
                with open('./fichier_test/test_png.png','rb') as fichier:
                    fichierIO = io.BytesIO(fichier.read())
                maData = {'monFichier': (fichierIO, 'test_png.png')}
                maReponse = client.post('/upload', headers={'Authorization': _basic_auth_str(username, password)}, \
                        data=maData, content_type='multipart/form-data')
                print("Aboutissement de la requête (200 si ok):", maReponse.status_code)
                assert maReponse.status_code == 200
    def test_uploadJPG(self):
            print('\n |---------------Upload un fichier JPG---------------|')
            with app.test_client() as client:
                username = 'laissus'
                password = 'sio'
                with open('./fichier_test/test_jpg.jpg','rb') as fichier:
                    fichierIO = io.BytesIO(fichier.read())
                maData = {'monFichier': (fichierIO, 'test_jpg.jpg')}
                maReponse = client.post('/upload', headers={'Authorization': _basic_auth_str(username, password)}, \
                        data=maData, content_type='multipart/form-data')
                print("Aboutissement de la requête (200 si ok):", maReponse.status_code)
                assert maReponse.status_code == 200
    def test_uploadGIF(self):
            print('\n |---------------Upload un fichier GIF---------------|')
            with app.test_client() as client:
                username = 'laissus'
                password = 'sio'
                with open('./fichier_test/test_gif.gif','rb') as fichier:
                    fichierIO = io.BytesIO(fichier.read())
                maData = {'monFichier': (fichierIO, 'test_gif.gif')}
                maReponse = client.post('/upload', headers={'Authorization': _basic_auth_str(username, password)}, \
                        data=maData, content_type='multipart/form-data')
                print("Aboutissement de la requête (200 si ok):", maReponse.status_code)
                assert maReponse.status_code == 200
    def test_uploadPDF(self):
            print('\n |---------------Upload un fichier PDF---------------|')
            with app.test_client() as client:
                username = 'laissus'
                password = 'sio'
                with open('./fichier_test/test_pdf.pdf','rb') as fichier:
                    fichierIO = io.BytesIO(fichier.read())
                maData = {'monFichier': (fichierIO, 'test_pdf.pdf')}
                maReponse = client.post('/upload', headers={'Authorization': _basic_auth_str(username, password)}, \
                        data=maData, content_type='multipart/form-data')
                print("Aboutissement de la requête (200 si ok):", maReponse.status_code)
                assert maReponse.status_code == 200
    def test_uploadTXT(self):
            print('\n |---------------Upload un fichier TXT---------------|')
            with app.test_client() as client:
                username = 'laissus'
                password = 'sio'
                with open('./fichier_test/test_txt.txt','rb') as fichier:
                    fichierIO = io.BytesIO(fichier.read())
                maData = {'monFichier': (fichierIO, 'test_txt.txt')}
                maReponse = client.post('/upload', headers={'Authorization': _basic_auth_str(username, password)}, \
                        data=maData, content_type='multipart/form-data')
                print("Aboutissement de la requête (200 si ok):", maReponse.status_code)
                assert maReponse.status_code == 200         
               