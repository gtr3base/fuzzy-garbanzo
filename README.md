# 🐍 SK Python Project

Welcome to the **SK Python Project**, a Django-based web app for managing personal learning topics, sharing ideas, and engaging with a community through comments, likes, and real-time notifications.

![Django](https://img.shields.io/badge/Powered%20By-Django-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Contributions Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

---

## 🚀 Features

- 📝 **Create & Manage Topics**  
  Organize your learning thoughts in public or private topics.

- 💬 **Add Entries & Comments**  
  Share ideas and let others comment to spark discussions.

- 👍👎 **Like / Dislike System**  
  Support or critique topics with a simple click.

- 🔔 **Real-Time Notifications**  
  Stay updated when someone interacts with your topics.

- 🧑‍💻 **User Profiles**  
  Update your username and password right from your profile page.

- 🔍 **Search Functionality**  
  Easily search through public or personal topics.

---

## 🛠️ Tech Stack

- **Backend:** Django, Django Channels (WebSockets)
- **Frontend:** HTML, CSS (custom templates)
- **Database:** SQLite (default, can be changed to PostgreSQL/MySQL)
- **Real-Time:** Django Channels + Redis (for production)

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/gtr3base/fuzzy-garbanzo.git
cd sk-python-project
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
🤝 Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.

Want to Contribute?
🍴 Fork the repo

👯 Clone your fork

✅ Create a new branch

🛠️ Make your changes

🚀 Push and create a PR

Made with 🧠, ☕, and 💻 by [gtr3base]
