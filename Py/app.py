from flask import Flask
from ports.api_routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000 ,debug=True)
