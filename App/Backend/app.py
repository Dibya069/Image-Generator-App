from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import requests
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')  # Add a route for the root path
def index():
    return 'Welcome to my Flask App!'

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')