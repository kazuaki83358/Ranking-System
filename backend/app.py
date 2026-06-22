from flask import Flask
from models import db
from routes import register_routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
register_routes(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return {
        "message": "Backend Running"
    }


if __name__ == '__main__':
    app.run(debug=True)