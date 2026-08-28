# 💬 Real-Time Communication App

<p align="center">
  <img src="images/banner.png" alt="Real-Time Communication App Banner" width="100%">
</p>

<p align="center">
  <strong>A real-time one-to-one chat application built for fast and seamless communication.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.x-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Socket.IO-Real--Time-purple?logo=socketdotio" alt="Socket.IO">
  <img src="https://img.shields.io/badge/Database-SQLite-blue" alt="SQLite">
  <img src="https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render" alt="Render">
</p>

---

## 📌 Project Overview

**Real-Time Communication App** is a web-based one-to-one messaging application developed using **Python Flask and Flask-SocketIO**.

The application allows registered users to communicate with each other through real-time messaging without refreshing the webpage.

Users can create an account using only a **username and password**. After logging in, users can view other registered users, select a user, and exchange messages instantly.

The application demonstrates how **WebSocket-based real-time communication** works in a modern web application.

---

## ✨ Features

- 🔐 User registration and login
- 👤 Username and password authentication
- 🔒 Secure password hashing
- 💬 One-to-one real-time messaging
- ⚡ Instant message delivery using Socket.IO
- 🟢 Online / offline user status
- ✍️ Typing indicator
- 🕐 Message timestamps
- 🔎 User search functionality
- 💾 Persistent chat history using SQLite
- 📱 Responsive user interface
- 🚪 Secure logout
- ✅ Input validation
- ❌ Duplicate username prevention
- 🔑 Invalid login validation
- 🌐 Free deployment support using Render

---

## 🖥️ Application Screenshots

### 🔐 Login Page

<p align="center">
  <img src="images/login.png" alt="Login Page" width="850">
</p>

The login page allows registered users to securely access the application using their username and password.

---

### 💬 Chat Interface

<p align="center">
  <img src="images/chat.png" alt="Chat Interface" width="850">
</p>

The chat interface allows users to select another registered user and communicate through real-time messages.

---

## ⚙️ How the Application Works

The basic communication flow is:

```text
User A
   │
   │ Types Message
   ▼
JavaScript Client
   │
   │ Socket.IO
   ▼
Flask-SocketIO Server
   │
   ├── Validate Message
   │
   ├── Save Message
   │
   └── Find Receiver
   │
   ▼
Receiver's Socket.IO Room
   │
   ▼
User B
   │
   ▼
Message Appears Instantly
```

### 🔄 Real-Time Communication

The application uses **Flask-SocketIO** to establish a real-time connection between the browser and the server.

When a user sends a message:

1. The sender types a message.
2. JavaScript captures the message.
3. Socket.IO sends the message to the Flask server.
4. The server identifies the receiver.
5. The message is stored in SQLite.
6. The server sends the message to the receiver's Socket.IO room.
7. The receiver gets the message instantly.
8. No page refresh is required.

---

## 🧑‍💻 Authentication

The application does **not require a phone number, OTP, or email address**.

Registration requires:

```text
Username
Password
```

Passwords are securely hashed using Werkzeug before being stored in the database.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SocketIO | Real-time communication |
| Socket.IO | WebSocket-based messaging |
| HTML5 | Page structure |
| CSS3 | User interface styling |
| JavaScript | Client-side functionality |
| SQLite | Database |
| Werkzeug | Password hashing |
| Gunicorn | Production server |
| Render | Free deployment |
| GitHub | Source code management |

---

## 📂 Project Structure

```text
Real_Time_Communication_App/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── routes.py
│   └── socket_events.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── chat.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── images/
│   ├── banner.png
│   ├── login.png
│   └── chat.png
│
├── instance/
│   └── chat.db
│
├── run.py
├── requirements.txt
├── Procfile
├── .gitignore
├── .env.example
└── README.md
```

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project folder:

```bash
cd Real_Time_Communication_App
```

---

### 2. Create a Virtual Environment

For Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

The main dependencies include:

```text
Flask
Flask-SocketIO
python-socketio
python-engineio
simple-websocket
Werkzeug
Gunicorn
```

---

### 4. Configure Secret Key

For local development, set the environment variable.

PowerShell:

```powershell
$env:SECRET_KEY="your-long-random-secret-key"
```

Or use the `.env` configuration supported by your application if implemented.

**Do not upload real secret keys to GitHub.**

---

### 5. Run the Application

```bash
python run.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

## 🧪 Testing Real-Time Chat

To test communication between two users:

### Browser 1

Register:

```text
Username: kavi123
Password: ********
```

### Browser 2

Open an incognito/private window and register another account:

```text
Username: priya456
Password: ********
```

Then:

1. Login as `kavi123`.
2. Select `priya456`.
3. Send a message.
4. Open the second browser.
5. The message should appear instantly.
6. Reply from the second browser.
7. Check the first browser.

The message exchange happens without manually refreshing the page.

---

## 🌐 Free Deployment on Render

This project can be deployed using **GitHub + Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn --worker-class gthread --threads 100 --workers 1 --bind 0.0.0.0:$PORT run:app
```

### Environment Variable

Add:

```text
SECRET_KEY = your-long-random-secret-key
```

After deployment, Render provides a public URL similar to:

```text
https://your-app-name.onrender.com
```

### ⚠️ SQLite Deployment Note

The application uses SQLite for simplicity and for demonstrating database functionality.

On free hosting, local SQLite storage may not be permanently preserved across certain service restarts, redeployments, or filesystem changes.

For a production-scale application, SQLite can later be replaced with PostgreSQL or another managed database.

---

## 🎥 Demo Video

The complete working demonstration of the project is available here:

**[▶️ Watch Project Demo Video](https://drive.google.com/file/d/1ISdbT1CZq4YhkeQuFd1n3uglDrUFVLGg/view?usp=sharing)**

> Replace `YOUR_GOOGLE_DRIVE_VIDEO_LINK` with your Google Drive video sharing link.

Make sure the Google Drive sharing permission allows viewers to access the video.

---

## 🔐 Security

The application includes basic security practices such as:

- Password hashing using Werkzeug
- Session-based authentication
- Input validation
- Duplicate username validation
- Invalid login handling
- Environment variables for secret configuration
- `.gitignore` protection for sensitive files

### Important

Never commit:

```text
.env
Passwords
API keys
Secret keys
Private credentials
```

to a public GitHub repository.

---

## 📡 Real-Time Architecture

```text
┌──────────────────────┐
│      User A          │
│      Browser         │
└──────────┬───────────┘
           │
           │ Socket.IO
           ▼
┌──────────────────────┐
│   Flask-SocketIO     │
│       Server         │
└──────────┬───────────┘
           │
           ├──────────────► SQLite Database
           │
           │
           ▼
┌──────────────────────┐
│  Receiver's Room     │
│      user_<id>       │
└──────────┬───────────┘
           │
           │ Socket.IO
           ▼
┌──────────────────────┐
│      User B          │
│      Browser         │
└──────────────────────┘
```

---

## 🎯 Project Objectives

The main objectives of this project are:

1. To develop a real-time communication system.
2. To implement one-to-one messaging.
3. To understand WebSocket communication.
4. To implement user authentication.
5. To store chat messages in a database.
6. To provide a responsive web interface.
7. To understand client-server communication.
8. To deploy a web application using free hosting services.

---

## 📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

- Python web development
- Flask application development
- REST and web routing concepts
- WebSocket communication
- Socket.IO events
- User authentication
- Password hashing
- Session management
- SQLite database operations
- Frontend JavaScript
- Git and GitHub
- Cloud deployment
- Production server configuration

---

## 🔮 Future Enhancements

The application can be extended with:

- 👥 Group chat
- 📎 File sharing
- 🖼️ Image sharing
- 😊 Message reactions
- ✔️ Read receipts
- 🔔 Notifications
- 🔍 Message search
- 🎙️ Voice communication
- 📹 Video communication
- 🗄️ PostgreSQL database
- 🔐 End-to-end encryption
- 📱 Progressive Web App support

---

## 👩‍💻 Project Information

**Project Name:** Real-Time Communication App

**Project Type:** Internship Project

**Application Type:** Web Application

**Communication:** Real-Time One-to-One Messaging

**Backend:** Python Flask

**Real-Time Engine:** Flask-SocketIO

**Database:** SQLite

**Deployment:** Render

**Source Control:** GitHub

---

## 📄 License

This project is developed for educational and internship purposes.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

<p align="center">
  <strong>Built with Python, Flask and Socket.IO ❤️</strong>
</p>