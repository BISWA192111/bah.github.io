from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import sqlite3
import os

app = Flask(__name__)

# Ensure the static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

# Database setup (SQLite for simplicity)
DATABASE = 'craters.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        # Save the uploaded file
        file.save("uploaded_image.jpg")
        # Process the image and get coordinates
        coords = process_image("uploaded_image.jpg")
        return jsonify(coords)

def process_image(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Preprocess image (dummy example, replace with actual crater detection logic)
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours (assuming each contour is a crater)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Dummy logic to get a centroid of the first contour as the crater's location
    if contours:
        cnt = contours[0]
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # Dummy logic to convert image coordinates to latitude and longitude
        lat, lon = convert_to_latlon(cX, cY)
        
        # Lookup database for actual coordinates (dummy example)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT latitude, longitude FROM craters WHERE image_x=? AND image_y=?", (cX, cY))
        result = cursor.fetchone()
        if result:
            return {'latitude': result[0], 'longitude': result[1]}
        else:
            return {'error': 'Crater not found in database'}

    return {'error': 'No crater detected'}

def convert_to_latlon(x, y):
    # Dummy conversion, replace with actual conversion logic
    return (x * 0.1, y * 0.1)

if __name__ == '__main__':
    app.run(debug=True)
