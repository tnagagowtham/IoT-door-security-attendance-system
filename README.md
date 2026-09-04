# 🔐 IoT-Based Door Security & Attendance Sys

A real-time facial recognition system that verifies registered users and
automatically unlocks a servo-motor-controlled door via Arduino, with
automated WhatsApp alerts to the admin for every entry and new registration.

## 🎬 Demo Video
https://github.com/user-attachments/assets/2d0a395b-3047-4403-b960-a6eac602214e

## 🚀 Overview
This system uses a webcam + face recognition to check who is at the door.
If the face is recognized, the door opens automatically and the admin gets
a WhatsApp attendance alert. If the face is unknown, the system asks for a
secret code word — if correct, the new face is saved for future recognition
and the admin is notified of the new registration.

## 🛠️ Tech Stack
- **Python** — core application logic
- **Flask** — web server & API backend
- **face_recognition** — face detection and matching
- **OpenCV** — webcam capture and image processing
- **PyWhatKit** — automated WhatsApp alerts
- **pyserial** — serial communication with Arduino
- **Arduino Uno + Servo Motor** — physical door control

## ✨ Key Features
- Real-time face detection and recognition via webcam
- Auto-unlocks door (servo motor via Arduino) for registered users
- WhatsApp attendance alert sent to admin on every entry
- Fallback registration flow for unknown faces (code-word verified)
- New face images saved to database automatically
- WhatsApp alert sent to admin for every new registration
- Clean web dashboard (served via Flask)

## 🔌 How It Works

```
Camera captures frame
        ↓
Face detected? ── No ──→ "No face detected"
        ↓ Yes
Compare against registered database
        ↓
   Known face?
   ↙         ↘
  Yes          No
   ↓            ↓
Open door    Ask for code word
Send alert      ↓
             Correct code word?
             ↙         ↘
            Yes          No
             ↓            ↓
         Save face    "Access denied"
         Send alert
```

## ⚙️ Setup & Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Add registered face images**
- Place `.jpg` photos of authorized users inside the `known_faces/` folder
- Name each file after the person: `Gowtham.jpg`, `Priya.jpg`, etc.

**3. Configure your settings** (in `app.py`)
```python
ARDUINO_PORT    = 'COM7'           # Your Arduino COM port
WHATSAPP_NUMBER = '+91XXXXXXXXXX'  # Admin WhatsApp number
CODE_WORD       = 'your_secret'    # Code word for new registrations
```

**4. Connect Arduino**
- Upload a simple servo sketch to your Arduino (servo on pin 9)
- Listens for `'o'` (open) and `'c'` (close) commands via Serial

**5. Run the app**
```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

## 📁 Project Structure
```
door-security-system/
├── app.py              ← Flask backend + face recognition logic
├── requirements.txt    ← Python dependencies
├── known_faces/        ← Registered face images (add your own)
│   └── Person_Name.jpg
└── templates/
    └── index.html      ← Web dashboard frontend
```

## 📈 Future Improvements
- Add liveness detection (prevent spoofing with a printed photo)
- Web dashboard to view attendance logs and registered users
- Multi-door support with a centralized database
- Mobile app for remote admin control

## 📌 Status
Core recognition, door control (Arduino servo), and WhatsApp alerts
working end-to-end. See demo video above for proof of working system.
