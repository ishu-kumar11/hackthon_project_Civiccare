# CivicCare – Citizen Issue Reporting System

CivicCare is a simple Django-based web application where citizens can report local civic problems such as road issues, water leakage, sanitation problems, and electricity faults.

The purpose of this project is to provide a basic online platform where issues can be submitted, viewed publicly, and tracked for transparency.

This project was created as part of a hackathon and is focused on solving real-life civic problems using web technology.

## Features

- Citizens can report civic issues
- Issues can be categorized (Road, Water, Electricity, Sanitation, etc.)
- Public list of reported issues
- Issue status tracking (Pending, In Progress, Resolved)
- Simple and clean user interface
- Multi-language support
- Secure backend using Django


---

## Project Structure

Website For Hackathon/
│
├── civiccare/ # Main Django project settings (settings, urls, wsgi)
├── core/ # Main Django app (views, models, forms)
├── templates/ # HTML template files
├── static/ # CSS, JavaScript, and images
├── locale/ # Language translation files
├── media/ # Uploaded files (ignored in GitHub)
├── manage.py # Django project entry file
├── .gitignore # Files ignored by Git
└── README.md # Project description


---

## Technology Used

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite (for development)








# 🪟 CivicCare – Installation Guide (Windows Only)

Follow these steps to run the CivicCare project on a Windows system.

---

## 1. Install Required Software

Make sure these are installed:

* **Python 3.9 or higher** → https://www.python.org/downloads/
* **Git** → https://git-scm.com/download/win

While installing Python, ✔ check **"Add Python to PATH"**

---

## 2. Clone the Project

Open **Command Prompt** or **PowerShell** and run:

git clone https://github.com/ishu-kumar11/hackthon_project_Civiccare.git
cd hackthon_project_Civiccare
```

---

## 3. Create Virtual Environment

python -m venv venv
```

Activate it:

venv\Scripts\activate
```

You should see `(venv)` in the terminal.

---

## 4. Install Dependencies

requirements.txt` exists:

pip install -r requirements.txt
```

```

---

## 5. Apply Database Migrations

```bash
python manage.py migrate
```

---

## 6. Create Admin User (Superuser)

```bash
python manage.py createsuperuser
```

Enter:

* Username
* Email
* Password

---

## 7. Run the Project

```bash
python manage.py runserver
```

Open browser and go to:

**Main Website**

```
http://127.0.0.1:8000/
```

**Admin Panel**

```
http://127.0.0.1:8000/admin/
```

---

## 8. Stop the Server

Press:

```
CTRL + C
```

---

## Notes

* Always activate virtual environment before running project:

  ```bash
  venv\Scripts\activate
  ```
* Default database is SQLite (no setup needed)
* Do not delete `venv` or project files

---



