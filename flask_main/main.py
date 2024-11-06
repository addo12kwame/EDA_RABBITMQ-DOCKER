from dataclasses import dataclass

import requests,os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint, Column, Integer, String
from sqlalchemy.exc import IntegrityError
from producer import publish
from dotenv import load_dotenv

load_dotenv(".env")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    image = Column(String(200))

@dataclass
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,nullable=False)
    product_id = Column(Integer,nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='uix_user_product'),)

@app.route("/api/products")
def index():
    return jsonify(Product.query.all())

@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id):
    req = requests.get("http://docker.for.mac.localhost:8000/api/user/")

    json = req.json()

    try:
        product_user = ProductUser(user_id=json["id"], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish("product_liked", id)
    except IntegrityError:
        db.session.rollback()
        abort(400, "You already liked this product")
    except Exception as e:
        abort(500, f"An unexpected error occurred: {str(e)}")
    return jsonify({
        "message": "Success"
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
