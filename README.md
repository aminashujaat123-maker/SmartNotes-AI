# SmartNotes AI 📝🤖

SmartNotes AI is a simple note-taking web application built with Flask. It allows users to sign up, log in, and manage their personal notes through a clean, protected dashboard.

## Features

## Features

- 🔐 User authentication (Signup / Login / Logout) with hashed passwords
- 📊 Protected dashboard showing user stats and notes overview
- 📝 Full CRUD functionality for notes (create, view, edit, delete)
- 🔍 Search functionality to quickly find notes
- 🤖 AI-powered note summarization (extractive text summarization algorithm)
- 📄 Export notes as PDF
- 📱 Fully responsive design (mobile, tablet, desktop)
- 💾 SQLite database with SQLAlchemy ORM
- 🎨 Clean, modern UI built with HTML, CSS, and JavaScript

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt
- **PDF Generation:** fpdf2
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
SmartNotes-AI/
│
├── app/
│   ├── models/          # Database models (User, Note)
│   ├── routes/          # Flask blueprints (auth, main, notes)
│   ├── extensions.py    # Flask extensions setup
│   └── __init__.py      # App factory
│
├── templates/            # Jinja2 HTML templates
├── static/               # CSS, JS, images
├── instance/              # SQLite database file
├── config.py
└── app.py                # Entry point
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/<your-username>/SmartNotes-AI.git
   cd SmartNotes-AI
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application

   ```bash
   python app.py
   ```

5. Open your browser at `http://127.0.0.1:5000`

## Screenshots

<img width="1887" height="1021" alt="image" src="https://github.com/user-attachments/assets/67f79e48-e30a-4558-98af-7c2eb95ee2d7" />

## License

This project is open source and available under the [MIT License](LICENSE).
