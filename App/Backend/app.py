from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import requests
from io import BytesIO
from pymongo import MongoClient
from flask_pymongo import PyMongo
import os, re
from PIL import Image
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

@app.route('/generate-image-sec', methods=['POST'])
def generate_image_sec():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    email = request.form.get('email')
    prompt = request.form.get('prompt')
    model = request.form.get('model')
    style = request.form.get('style')

    if not email or not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Open the uploaded image using Pillow
    image = Image.open(file)
    image = image.convert('RGBA')
    width, height = 256, 256
    image = image.resize((width, height))

    # Convert the image to a BytesIO object
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()

    f_prompt = (
        f"Generate a {prompt} tattoo on the body part of the image is given. "
        f"Generate {style} style image."
    )

    response = client.images.edit(
        model=model,
        image=byte_array,
        prompt=f_prompt,
        n=1,
        size="1024x1024"  # Adjust the size as needed
    )

    image_url = response.data[0].url

    # Save generation details to user's history
    generation_details = {
        'prompt': f_prompt,
        'model': model,
        'style': style,
        'image': file.filename,
        'timestamp': datetime.utcnow()
    }

    users_collection.update_one(
        {'email': email},
        {'$push': {'history': generation_details}}
    )

    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')