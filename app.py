from flask import Flask, render_template, jsonify, request 
import cv2
import face_recognition
import numpy as np
import os
import serial
import time
import webbrowser
import pyautogui
import pywhatkit
from flask_cors import CORS

KNOWN_FACES_DIR = 'known_faces'
ARDUINO_PORT = 'COM7'
WHATSAPP_NUMBER = '+91xxxxxxxxxx'
CODE_WORD = "****"

app = Flask(__name__)
CORS(app)

try:
    arduino = serial.Serial(ARDUINO_PORT, 9600)
    time.sleep(2)
except:
    arduino = None
    print(f"[WARNING] Could not connect to Arduino on {ARDUINO_PORT}")

known_face_encodings = []
known_face_names = []

if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

for filename in os.listdir(KNOWN_FACES_DIR):
    img_path = os.path.join(KNOWN_FACES_DIR, filename)
    img = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(img)
    if encodings:
        known_face_encodings.append(encodings[0])
        known_face_names.append(os.path.splitext(filename)[0])

def send_whatsapp_message(number, message):
    try:
        pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
        print(f"[INFO] WhatsApp message sent to {number}")
    except Exception as e:
        print(f"[ERROR] Failed to send WhatsApp message: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recognition', methods=['GET'])
def start_recognition():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return jsonify({"status": "failure", "message": "Failed to capture video"})

    ret, frame = cap.read()
    if not ret:
        cap.release()
        return jsonify({"status": "failure", "message": "Failed to capture frame"})

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    result = {"status": "failure", "message": "Unknown face"}

    for encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, encoding)

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        if name != "Unknown":
            result = {"status": "success", "message": f"Hello, {name}! Door is opening."}
            send_whatsapp_message(WHATSAPP_NUMBER, f"Present: {name}")
            if arduino:
                arduino.write(b'o')
                time.sleep(5)
                arduino.write(b'c')
            result["reload"] = True
            break
        else:
            result = {"status": "ask_code_word", "message": "Unknown face. Please enter code word."}
            code_word = request.args.get('code_word', default="")
            if code_word == CODE_WORD:
                name = request.args.get('name', default="Unknown")
                img_path = os.path.join(KNOWN_FACES_DIR, name + ".jpg")
                cv2.imwrite(img_path, frame)
                known_face_encodings.append(encoding)
                known_face_names.append(name)
                result = {"status": "success", "message": f"Face saved as {name}."}
                send_whatsapp_message(WHATSAPP_NUMBER, f"New face added: {name}")
                result["reload"] = True
                break

    cap.release()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)