from flask import Flask
from flask_cors import CORS
from db import init_db
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("База данных инициализирована.")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,
    PERMANENT_SESSION_LIFETIME=86400
)

CORS(app, 
     supports_credentials=True,
     origins=["https://todo-client-seven-psi.vercel.app"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Cookie"],
     expose_headers=["Set-Cookie", "Authorization"]
)

from routes import *
