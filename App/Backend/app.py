from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import requests
from pymongo import MongoClient
from flask_pymongo import PyMongo
import os, re
from openai import OpenAI
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

MONGO_URI = "mongodb+srv://dibya069:dibya069@cluster0.bn7rr30.mongodb.net/"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['user_database']
users_collection = db['users']

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

@app.route('/')
def index():
    return 'Welcome to my Flask App!'

@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.json
    email = data.get('email')

    if not email or not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400

    existing_user = users_collection.find_one({'email': email})
    if not existing_user:
        users_collection.insert_one({'email': email, 'history': []})

    return jsonify({'message': 'Sign in successful'}), 200

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    email = data.get('email')
    prompt = data.get('prompt')
    model = data.get("model")
    style = data.get("style")
    size = data.get("size")
    sex = data.get("sex")
    body = data.get("body")

    if not email or not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    f_prompt = (
        f"{prompt} as a tattoo design that fits perfectly on a {sex}'s **{body}** part. "
        "Ensure there is no extra background space beyond the shape of the body. "
        "Use a white background for any empty space."
        f"generate {style} style image"
    )

    response = client.images.generate(
        model=model,
        prompt=f_prompt,
        size=size,
        quality="standard",
        n=1
    )

    image_url = response.data[0].url

    # Save generation details to user's history
    generation_details = {
        'prompt': prompt,
        'model': model,
        'style': style,
        'size': size,
        'sex': sex,
        'body': body,
        'timestamp': datetime.utcnow()
    }

    users_collection.update_one(
        {'email': email},
        {'$push': {'history': generation_details}}
    )

    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')