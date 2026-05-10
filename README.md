# 🌍 Traveloop

Traveloop is a modern, full-stack travel planning web application built with **Django**. It enables users to seamlessly plan multi-city trips, manage complex itineraries, track their travel budget, create packing checklists, and share their planned trips publicly with friends.

## 🚀 Features

- **Multi-City Itinerary Builder**: Plan comprehensive trips across multiple cities. Drag-and-drop your stops to reorder them easily.
- **Activity Scheduling**: Add specific activities and attractions to each stop, complete with cost estimates and duration tracking.
- **Budget Management**: Track your estimated costs against your set budget. Visual charts (powered by Chart.js) provide a clear breakdown of expenses per city and per category.
- **Packing Checklist**: A built-in checklist to keep track of items you need to pack for your journey.
- **Trip Notes**: Jot down important information, reservations, or ideas linked to specific stops.
- **Public Sharing**: Generate a unique public link to share your itinerary with others. Users can even clone public trips into their own accounts!
- **Admin Dashboard**: A customized analytics dashboard for staff members to monitor user growth, popular cities, and platform usage.

## 🛠️ Technology Stack

- **Backend**: Django 5.2, Python 3.11+
- **Database**: PostgreSQL (Production) / SQLite (Development fallback)
- **Frontend**: Django Templates, Tailwind CSS (Design System), Alpine.js (Reactivity)
- **Data Visualization**: Chart.js
- **Environment Management**: Python Decouple

## ⚙️ Local Development Setup

Follow these steps to run Traveloop locally:

### 1. Clone the repository
```bash
git clone https://github.com/JarshinJS/-Traveloop.git
cd -Traveloop
```

### 2. Set up a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# MacOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
The project uses `python-decouple` for secure credential management.
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and set up your variables.
   - **Important:** Ensure you set a secure, random string for `SECRET_KEY`.
   - Configure your database credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, etc.). By default, the `settings.py` is configured to use **PostgreSQL**. If you prefer to use SQLite locally, you must update the `DATABASES` dictionary in `traveloop_project/settings.py`.

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Seed the Database (Optional but recommended)
Populate your local database with sample cities and activities:
```bash
python manage.py seed_cities
python manage.py seed_activities
```

### 7. Create a Superuser
```bash
python manage.py createsuperuser
```

### 8. Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser. You can access the admin panel at `/admin/`.

## 🔒 Security
- All sensitive credentials and API keys are stored in the `.env` file, which is excluded from version control via `.gitignore`.
- Django's built-in CSRF protection is enabled for all state-changing requests.

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
