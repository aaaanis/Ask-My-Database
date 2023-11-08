from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging

from LLM_DB import ReviewDatabase

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:XXXX/review'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), default="N/A")
    rating = db.Column(db.Integer, nullable=True)
    author = db.Column(db.String(255))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/api/create_review/', methods=['POST'])
def create_review():
    data = request.json
    title = data.get('title', "N/A")
    rating = data.get('rating')
    author = data.get('author')
    content = data.get('content')
    date = data.get('date')

    if not all([author, content, date]):
        return jsonify({'error': 'Fields author, content, and date are required'}), 400

    review = Review(title=title, rating=rating, author=author, content=content, date=date)
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review created successfully'}), 201
