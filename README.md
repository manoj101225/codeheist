# 🎮 CodeHeist — GTA V-Themed DSA Learning Platform

> *"Every heist is a coding challenge. Master Data Structures and Algorithms to conquer Los Santos."*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0+-61DAFB?style=for-the-badge&logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.0+-646CFF?style=for-the-badge&logo=vite)](https://vitejs.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

---

## 🌟 Overview

**CodeHeist** transforms standard Data Structures & Algorithms (DSA) preparation into an immersive, GTA V-inspired open-world criminal career. Players progress through 14 distinct city districts—from Arrays to Dynamic Programming—pulling off coding "heists" (solving problems), earning reputation points, unlocking higher-tier districts, and climbing the underworld leaderboard.

Equipped with an adaptive **Multi-Armed Bandit (Thompson Sampling)** algorithm, CodeHeist intelligently analyzes player performance and recommends the next best mission to target weak spots and sharpen problem-solving skills.

---

## 🚀 Key Features

- 🗺️ **Interactive District Map**: Gamified progression across 14 DSA topics mapped to iconic heist territories (Array Alley, Tree Tops, DP Downtown, Graph Gangland, etc.).
- 🔫 **Mission-Based Heists**: 50+ hand-crafted coding challenges structured as high-stakes heist operations complete with briefings, starter code templates, test cases, and progressive hints.
- 💻 **Monaco Code Editor**: Fully integrated browser IDE with syntax highlighting, line numbers, and theme support for **Python**, **C++**, **Java**, and **JavaScript**.
- 🧠 **Smart Recommendation Engine**: Powered by **Thompson Sampling (Multi-Armed Bandit)** to continuously learn player weaknesses and serve optimal mission recommendations.
- ⚡ **Automated Code Judge**: Instant code execution and validation system evaluating time complexity, edge cases, and hidden test suites.
- 🏆 **Underworld Leaderboard & Profile**: Global player rankings based on Heist Reputation, completed missions, heist streak stats, and unlocked achievements.
- 🌃 **GTA V HUD Visual Aesthetics**: Custom neon dark mode, glassmorphism card layouts, HUD-style navigation bars, and responsive tactical UI design.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Database & ORM**: SQLite + [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: OAuth2 Password Flow with JWT (`python-jose`, `passlib[bcrypt]`)
- **Algorithm Engine**: SciPy / NumPy-inspired Thompson Sampling (Multi-Armed Bandit)
- **Server**: Uvicorn ASGI Server

### **Frontend**
- **Framework**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Code Editor**: [@monaco-editor/react](https://github.com/suren-atoyan/monaco-react)
- **Routing**: React Router v7
- **Styling**: Modern Vanilla CSS, Custom CSS Variables, Glassmorphism, Responsive Grid & Flexbox layout

---

## 📁 Project Structure

```text
codeheist/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI Routers (auth, districts, missions, submissions, progress, leaderboard)
│   │   ├── core/            # Security, config, judge engine & language execution harnesses
│   │   ├── models/          # SQLAlchemy Database Schema models
│   │   ├── seed/            # District & Mission syllabus data seeding
│   │   ├── services/        # Bandit algorithm recommendation engine
│   │   └── main.py          # Application entry point & startup initialization
│   └── requirements.txt     # Python backend dependencies
├── frontend/
│   ├── public/              # Static assets & SVG icons
│   ├── src/
│   │   ├── assets/          # Project visual assets & branding
│   │   ├── components/      # UI components (HUD Navbar, Map, Editor, etc.)
│   │   ├── pages/           # Application views (Auth, MapOverview, District, Mission, Leaderboard, Profile)
│   │   ├── services/        # Axios API integration client
│   │   ├── App.jsx          # React route configuration
│   │   └── main.jsx         # React application entry
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
└── README.md
```

---

## 🚦 Getting Started

### Prerequisites
- **Node.js** (v18.0.0 or higher)
- **Python** (v3.10 or higher)
- **Git**

---

### 1. Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The backend API will run at `http://localhost:8000`. You can access the interactive Swagger API documentation at `http://localhost:8000/docs`.

---

### 2. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node modules:**
   ```bash
   npm install
   ```

3. **Start the Vite dev server:**
   ```bash
   npm run dev
   ```
   The application will be accessible at `http://localhost:5173`.

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new heist player |
| `POST` | `/api/auth/token` | User login & JWT token generation |
| `GET` | `/api/districts` | Fetch all city districts and unlocked status |
| `GET` | `/api/missions/district/{slug}` | List missions within a specific district |
| `GET` | `/api/missions/{id}` | Get mission details, starter code, & test cases |
| `POST` | `/api/submissions/run` | Execute code against sample test cases |
| `POST` | `/api/submissions/submit` | Submit code for full evaluation & reputation points |
| `GET` | `/api/progress/recommendation` | Get AI Bandit recommended mission based on player skill |
| `GET` | `/api/leaderboard` | View top criminal masterminds on global leaderboard |

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new heist missions, UI improvements, or additional language support:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewHeistMission`)
3. Commit your changes (`git commit -m 'Add new Heap District heist'`)
4. Push to the branch (`git push origin feature/NewHeistMission`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
