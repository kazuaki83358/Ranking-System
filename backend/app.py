from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes import register_routes
import os


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
    return jsonify({
        "message": "Backend Running"
    })


if __name__ == '__main__':

    port = int(
        os.environ.get('PORT', 5000)
    )

    app.run(

        host='0.0.0.0',

        port=port,

        debug=False

    )