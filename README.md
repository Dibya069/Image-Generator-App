## AI Tattoo Generator

This repository contains the source code for an AI Tattoo Generator web application, designed to assist tattoo artists in creating unique and personalized tattoo designs. 

**Project Overview:**

This project utilizes OpenAI's DALL-E 3 and DALL-E 2 models for generating tattoo images based on user prompts. It offers two distinct generation modes:

1. **Text-Based Generation:** Users can input a textual prompt, select a model (DALL-E 3 or DALL-E 2), choose a style, size, and specify gender and body part. The API utilizes OpenAI's models to generate a tattoo image customized to these parameters.
2. **Image-Based Generation:** Users can upload a body part image.  Leveraging MediaPipe and DeepLabv3 models for object detection, the application identifies the body part in the image and generates a tattoo image based on the provided prompt, tattoo size, and style.

**Technical Stack:**

* **Backend:** Python Flask API
* **Frontend:** React.js
* **Database:** MongoDB

**Features:**

* **User Authentication:** Securely handles user login using email addresses.
* **Image Generation:** Offers two generation modes: text-based and image-based.
* **Customization:** Allows users to select model, style, size, gender, and body part.
* **History Management:**  Stores past generations in the database, accessible through a dedicated history feature.
* **Visual Styling:**  Includes visually appealing CSS styling.

**Project Structure:**

```
├── app.js             # React.js frontend application
├── backend
│   ├── app.py       # Flask API for backend logic
│   └── models.py    # MongoDB database models
|   |__ masked.py    # Masking the given image
└── img
    └── wizard-dark-dungeon-illustration.jpg   # Example image for the background (replace with your own)
```

**Steps are**
1. sgin Up page (mail_id should be Authenticate)

2. 