# 🗳️ EVM Using Face Recognition

A secure **Electronic Voting Machine (EVM)** system that uses **Face Recognition** for voter authentication. This project aims to prevent unauthorized voting by ensuring that only registered and verified voters can cast their votes. The system combines **Python-based face recognition** with **Arduino-controlled hardware** to simulate a real-world electronic voting process.

---

## 📌 Project Overview

Traditional EVM systems rely on manual verification, which can lead to impersonation and fraud. This project enhances election security by integrating **biometric face recognition** to authenticate voters before allowing them to vote.

Once a voter is verified:

* The system enables voting access
* The vote is recorded securely
* Multiple voting attempts by the same person are prevented

---

## 🎯 Objectives

* Authenticate voters using face recognition
* Prevent duplicate or unauthorized voting
* Integrate software authentication with hardware control
* Demonstrate a secure and modern voting mechanism

---

## 🧠 Key Features

* ✅ Face recognition–based voter authentication
* ✅ Real-time face detection using camera input
* ✅ Arduino integration for voting control
* ✅ Secure and automated voting flow
* ✅ User-friendly and scalable design

---

## 🛠️ Technologies Used

### Software

* Python
* OpenCV
* Face Recognition Library
* NumPy

### Hardware

* Arduino
* Push buttons (for voting)
* LEDs / Indicators
* Camera (Webcam)

---

## ⚙️ System Workflow

1. Camera captures the voter's face
2. Face is detected and encoded
3. Captured face is compared with registered dataset
4. If match found:

   * Voting access is granted
   * Arduino enables voting buttons
5. Vote is recorded
6. Same voter cannot vote again

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/binisha8/EVM_using_face_recognition.git
cd EVM_using_face_recognition
```

### 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Arduino Setup

* Upload the Arduino code from `arduino_code/` to the Arduino board
* Connect buttons and LEDs as per the circuit design

---

## ▶️ How to Run the Project

```bash
python main.py
```

> Ensure the camera is connected and accessible before running the program.

---

## 🧪 Sample Logic Snippet

```python
if face_matched:
    enable_voting()
else:
    deny_access()
```

---

## 🔐 Security Advantages

* Ensures one-person-one-vote
* Improves trust in electronic voting systems

---

## 📌 Future Enhancements

* Integration with national ID database
* Cloud-based vote storage
* Improved face recognition accuracy
* GUI-based voting interface

---

⭐ If you like this project, don’t forget to star the repository!
