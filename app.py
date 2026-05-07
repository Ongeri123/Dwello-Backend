from flask import Flask
from flask_cors import CORS

from routes.upload import upload_bp
from routes.auth import auth_bp
from routes.requests import requests_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(requests_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5001)