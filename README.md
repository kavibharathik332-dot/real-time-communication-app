# 💬 Real-Time Communication App

<p align="center">
  <img src="images/banner.png" alt="Real-Time Communication App Banner" width="100%">
</p>

<p align="center">
  A simple, secure, and responsive real-time one-to-one chat application built with Flask and Flask-SocketIO.
</p>

<p align="center">
  <b>Real-Time Messaging • Secure Authentication • Online Status • Typing Indicator</b>
</p>

---

## 📌 Project Overview

The **Real-Time Communication App** is a web-based one-to-one messaging application that allows registered users to communicate instantly without requiring a phone number, OTP, or email address.

Users can create an account using a username and password, log in securely, find other registered users, and exchange messages in real time.

The application uses **Flask-SocketIO** to provide instant communication without page refreshes or continuous polling.

---

## ✨ Features

- 🔐 User registration and login
- 👤 Username and password authentication
- 🔒 Secure password hashing using Werkzeug
- 💬 Real-time one-to-one messaging
- ⚡ Instant message delivery using Socket.IO
- 🗄️ Persistent chat history using SQLite
- 🟢 Online / offline user status
- ✍️ "User is typing..." indicator
- 🕒 Message timestamps
- 🔎 User search functionality
- 🚫 Empty message validation
- 🚫 Duplicate username validation
- ❌ Invalid login validation
- 📱 Responsive design for desktop, tablet, and mobile
- 🚪 Secure logout functionality

---

## 🖥️ Application Screenshots

### 🔐 Login Page

<p align="center">
  <img src="images/login.png" alt="Login Page" width="85%">
</p>

The login page allows registered users to securely access the application using their username and password.

---

### 💬 Chat Interface

<p align="center">
  <img src="images/chat.png" alt="Chat Interface" width="85%">
</p>

The chat interface provides real-time communication between registered users with message timestamps, online status, user search, and typing indicators.

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3, Flask |
| Real-Time Communication | Flask-SocketIO |
| WebSocket | Socket.IO |
| Database | SQLite |
| Authentication | Flask Session |
| Password Security | Werkzeug |
| Production Server | Gunicorn |
| Version Control | Git & GitHub |
| Deployment | Render |

---

## 🏗️ Project Architecture

```text
User Browser
     │
     ▼
HTML / CSS / JavaScript
     │
     ▼
Socket.IO Client
     │
     ▼
Flask-SocketIO Server
     │
     ├──────────────► Authentication
     │
     ├──────────────► Real-Time Messaging
     │
     ├──────────────► Online / Offline Status
     │
     ├──────────────► Typing Indicator
     │
     ▼
SQLite Database
     │
     ├── Users
     └── Messages
```

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

## ⚡ How Real-Time Messaging Works

The application uses **Flask-SocketIO** to deliver messages instantly.

```text
User A
  │
  │ Types message
  ▼
JavaScript
  │
  │ Socket.IO
  ▼
Flask-SocketIO Server
  │
  ├── Validate message
  │
  ├── Save message to SQLite
  │
  └── Send message to User B
          │
          ▼
       User B
```

Each logged-in user is associated with a private Socket.IO room.

When a message is sent, the server delivers it directly to the receiver's room.

This allows messages to appear **without refreshing the page**.

---

## 🔐 Authentication

The application provides username and password authentication.

### Registration

Users can create an account using:

```text
Username
Password
```

No phone number, OTP, or email address is required.

### Password Security

Passwords are not stored as plain text.

The application uses **Werkzeug password hashing** to securely store user passwords.

---

## 💾 Database

The application uses **SQLite** for data storage.

The database stores information such as:

- User accounts
- Hashed passwords
- User information
- Chat messages
- Message timestamps

SQLite makes the project simple to set up because it does not require a separate database server.

---

## 🚀 Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kavibharathik332-dot/real-time-communication-app.git
```

### 2. Open the Project

```bash
cd Real_Time_Communication_App
```

### 3. Create a Virtual Environment

Windows PowerShell:

```powershell
py -m venv venv
```

### 4. Activate the Virtual Environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 6. Set the Secret Key

PowerShell:

```powershell
$env:SECRET_KEY="your-long-random-secret-key"
```

### 7. Run the Application

```powershell
python run.py
```

### 8. Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing the Application

To test real-time communication:

### Browser 1

Register:

```text
Username: kavi123
Password: ********
```

### Browser 2

Open an incognito/private window and register another user:

```text
Username: priya456
Password: ********
```

Then:

1. Login as `kavi123`
2. Select `priya456`
3. Send a message
4. Open Browser 2
5. The message should appear instantly
6. Reply from Browser 2
7. Check the message in Browser 1

You can also test:

- Online/offline status
- Typing indicator
- Logout
- Invalid login
- Empty messages
- Duplicate usernames

---

## 🌐 Deployment

The application can be deployed using **GitHub + Render**.

### Build Command

```text
pip install -r requirements.txt
```

### Start Command

```text
gunicorn --worker-class gthread --threads 100 --workers 1 --bind 0.0.0.0:$PORT run:app
```

### Environment Variable

Add the following environment variable in Render:

```text
SECRET_KEY=your-long-random-secret-key
```

After deployment, Render provides a public URL for accessing the application.

---

## ⚠️ Deployment Note

The current project uses SQLite.

SQLite is suitable for development, learning, demonstrations, and student/internship projects.

On hosting platforms with temporary filesystems, SQLite data may not survive every restart or redeployment.

For a production application, SQLite can be replaced with **PostgreSQL** or another persistent database.

---

## 🔒 Security

The application includes several basic security practices:

- Password hashing
- Session-based authentication
- Input validation
- Username validation
- Duplicate username prevention
- Protected chat functionality
- Environment variables for sensitive configuration

### Never upload

```text
.env
Real passwords
API keys
Private credentials
Production SECRET_KEY
```

These should be excluded using `.gitignore`.

---

## 🎯 Use Cases

This project can be used as:

- 🎓 College mini project
- 💼 Internship project
- 🧑‍💻 Python / Flask learning project
- 🌐 Web application development project
- ⚡ Real-time communication demonstration
- 📚 Socket.IO learning project

---

## 🔮 Future Enhancements

Possible future improvements include:

- 👥 Group chat
- 📎 File sharing
- 🖼️ Image sharing
- 🎤 Voice messaging
- 📹 Video calling
- ✓✓ Read receipts
- ❤️ Message reactions
- 🔔 Push notifications
- 🔍 Message search
- 🗃️ PostgreSQL database
- 🔐 End-to-end encryption
- 👤 Profile pictures
- 📝 Message editing and deletion

---

## 📊 Key Highlights

| Feature | Status |
|---|---|
| User Registration | ✅ |
| User Login | ✅ |
| Password Hashing | ✅ |
| One-to-One Chat | ✅ |
| Real-Time Messaging | ✅ |
| SQLite Storage | ✅ |
| Online Status | ✅ |
| Typing Indicator | ✅ |
| Search Users | ✅ |
| Responsive UI | ✅ |
| GitHub | ✅ |
| Render Deployment | ✅ |

---

## 👩‍💻 Author

**Kavi Bharathi**

Real-Time Communication App  
Built using Python, Flask, Flask-SocketIO, JavaScript, and SQLite.

---

## 📄 License

This project is created for **educational and internship purposes**.

You are welcome to study, modify, and extend the project for learning and development.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

<p align="center">
  <b>💬 Real-Time Communication App</b><br>
  Built with Flask + Socket.IO + SQLite
</p>