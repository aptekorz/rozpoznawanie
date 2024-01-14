from flask import Flask
from flask_restful import Api, Resource, reqparse
import cv2
import urllib
import numpy as np
import urllib.request
from flask import request
from PIL import ImageTk, Image
import os

try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode


app = Flask(__name__)
api = Api(app)

# Parser argumentów
parser = reqparse.RequestParser()
parser.add_argument('url', type=str, help='Adres URL obrazu do analizy')

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


class AnalizaLiczbyOsob(Resource):
    def get(self):
        try:
            url = request.args.get('url')
            if url:
                req = urllib.request.urlopen(url)
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                image = cv2.imdecode(arr, -1) 
                if image is not None:
                    image = cv2.resize(image, (700, 400))
                    # detect people in the image
                    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
                    # draw the bounding boxes
                    for (x, y, w, h) in rects:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # Liczenie liczby znalezionych twarzy
                    liczba_osob = len(rects)
                    return {"liczba_osob": liczba_osob}, 200
                else:
                    return {"Błąd": "Nie można wczytać obrazu z podanego adresu URL."}, 400
            else:
                return {"Błąd": "Brak adresu URL obrazu w danych wejściowych."}, 400
        except Exception as e:
            return {"Błąd": str(e)}, 500

class AnalizaLiczbyOsobZPliku(Resource):
    def get(self):
        try:
            #url to z pliku 
            url = request.args.get('url')
            if url:
                image = cv2.imread(url)
                if image is not None:
                    image = cv2.resize(image, (700, 400))
                    # detect people in the image
                    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
                    # draw the bounding boxes
                    for (x, y, w, h) in rects:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # Liczenie liczby znalezionych twarzy
                    liczba_osob = len(rects)
                    return {"liczba_osob": liczba_osob}, 200
                else:
                    return {"Błąd": "Nie można wczytać obrazu z podanego adresu URL."}, 400
            else:
                return {"Błąd": "Brak adresu URL obrazu w danych wejściowych."}, 400
        except Exception as e:
            return {"Błąd": str(e)}, 500

class AnalizaLiczbyOsobZPOSTA(Resource):
    def post(self):
        try:
            file = request.files['image'][0]
            print(file)
            image = Image.open(file.stream)
            #file.save('/home/parallels/Desktop/rozpoznawanie/im-received.jpg')
            #image = cv2.imread('/home/parallels/Desktop/rozpoznawanie/im-received.jpg')

            if image:
                
                if image is not None:
                    image = cv2.resize(image, (700, 400))
                    # detect people in the image
                    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
                    # draw the bounding boxes
                    for (x, y, w, h) in rects:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    liczba_osob = len(rects)

                    return {"liczba_osob": liczba_osob}, 200
                else:
                    return {"Błąd": "Nie można wczytać obrazu z podanego adresu URL."}, 400
            else:
                return {"Błąd": "Brak adresu URL obrazu w danych wejściowych."}, 400
        except Exception as e:
            return {"Błąd": str(e)}, 500


api.add_resource(AnalizaLiczbyOsobZPOSTA, '/analiza-z-posta')
api.add_resource(AnalizaLiczbyOsobZPliku, '/analiza-z-pliku')
api.add_resource(AnalizaLiczbyOsob, '/analiza-z-url')

if __name__ == '__main__':
    app.run(debug=True)
