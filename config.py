import os

SECRET_KEY = 'daniel'
MONGO_URI = "mongodb://localhost:27017/jogoteca"
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'