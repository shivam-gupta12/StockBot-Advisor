from flask import Flask
from flask_socketio import SocketIO
from .routes import init_routes


socketio = SocketIO(async_mode='eventlet')  

def create_app():
    app = Flask(__name__)
    
    # Set a secret key for the application
    app.secret_key = 'woinfj902hrf98whb'

    socketio.init_app(app)
    
    init_routes(app, socketio)
    return app
