from flask import Flask
from flask_restful import Api, Resource, reqparse
import cv2
import urllib
import numpy as np
import urllib.request
from flask import request
import requests

url = 'http://127.0.0.1:5000/analiza-z-posta'
my_img = {'image': open('test.jpg', 'rb')}
r = requests.post(url, files=my_img)

# convert server response into JSON format.
print(r.json())
