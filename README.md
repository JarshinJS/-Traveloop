# 🌍 Traveloop

**Traveloop** is a modern, full-stack AI-powered travel planning web application built with **Django 5.2**. It enables users to plan multi-city trips, manage detailed itineraries, track budgets, maintain packing checklists, write travel journals, and get intelligent recommendations — all within a clean, responsive Bootstrap 5 UI that supports both light and dark mode.

---

## ✨ Features

### 🗺️ Trip Planning
- **Multi-City Itinerary Builder** — Drag-and-drop stop ordering across multiple destinations
- **Itinerary Timeline & List View** — View your full plan as an elegant timeline or compact table
- **Trip Detail Hub** — Centralized overview with tabs for Itinerary, Budget, Packing, and Notes
- **Trip Sharing** — Generate a unique public link; viewers can clone the trip into their own account

### 🤖 AI Assistant — "Trave"
- **Floating AI Chatbot** available on every page — ask about features, navigation, or travel tips
- **Google Gemini powered** when an API key is provided; smart rule-based fallback always works
- **Contextual navigation** — Trave knows all app URLs and guides users with clickable links
- **Conversation memory** — maintains chat history for multi-turn, contextual conversations

### 🧠 Smart Suggestions Engine
- **Hybrid algorithm** — combines database-driven filtering with optional Gemini AI ranking
- **Budget-aware** — suggests activities priced within the trip's daily budget range
- **Region-intelligent** — prioritises cities in the same region as existing stops, then diversifies
- **Category diversity** — avoids repeating activity types already added to the itinerary
- **Live AI tip** — when Gemini is active, generates a personalised travel insight for your route

### 💰 Budget Management
- Set a total trip budget and track estimated costs per stop
- Interactive **doughnut chart** (cost by category) and **bar chart** (cost by destination)
- Over-budget alert with a red progress bar indicator
- Avg. daily cost and budget utilisation percentage at a glance

### 📦 Packing Checklist
- Add items with category grouping (Clothing, Documents, Electronics, etc.)
- Two-column responsive grid grouped by category
- Progress bar tracks packing completion percentage
- One-click reset to unpack all items

### 📓 Journey Journal (Notes)
- Two-panel layout: notes list + composer side by side
- Link notes to specific trip stops
- Auto-resize textarea for comfortable writing

### 🏙️ Destination Explorer
- Browse and filter all cities by region and name
- City cards with hero images, cost index, and popularity rating
- "Add to Journey" modal to assign a city directly to any existing trip

### 🎯 Activity Catalogue
- Filter by city, category, and maximum cost
- Category chip filters for one-click browsing
- Popular activity badges and detailed cost/duration info

### 🔐 Accounts & Profile
- User registration and login with secure authentication
- Profile page with avatar upload, name/email editing
- Account deletion with confirmation modal

### 📊 Admin Dashboard
- Staff-only analytics: user growth, popular cities, platform-wide usage statistics

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2, Python 3.11+ |
| **AI / ML** | Google Gemini (`google-generativeai` 0.8.6) |
| **Database** | PostgreSQL (production) / SQLite (development) |
| **Frontend** | Django Templates, Bootstrap 5.3.3, Bootstrap Icons |
| **Reactivity** | Alpine.js 3.x |
| **Charts** | Chart.js |
| **Auth** | Django built-in auth + session management |
| **Config** | python-decouple |
| **Images** | Pillow |

---

## ⚙️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/JarshinJS/-Traveloop.git
cd -Traveloop
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy the example file and fill in your values:
```bash
cp .env.example .env
```

Key variables in `.env`:

| Variable | Description |
|---|---|
| `SECRET_KEY` | A long, random Django secret key |
| `DEBUG` | `True` for local dev, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list (e.g. `127.0.0.1,localhost`) |
| `GEMINI_API_KEY` | *(Optional)* Google Gemini API key for AI features |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (default `127.0.0.1`) |
| `DB_PORT` | Database port (default `5432`) |

> **Getting a Gemini API Key (free):** Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) to generate a key. Without it, the chatbot and suggestions still work via the built-in rule-based fallback.

> **SQLite for local dev:** Update the `DATABASES` dict in `traveloop_project/settings.py` if you prefer SQLite over PostgreSQL.

### 5. Run database migrations
```bash
python manage.py migrate
```

### 6. Seed the database *(recommended)*
Populate your local database with sample cities and activities:
```bash
python manage.py seed_cities
python manage.py seed_activities
```

### 7. Create a superuser
```bash
python manage.py createsuperuser
```

### 8. Start the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.
The admin panel is at **/admin/**, and the staff analytics dashboard is at **/admin-dashboard/**.

---

## 🔑 AI Features Setup

The AI chatbot ("Trave") and Smart Suggestions work in two modes:

| Mode | Requires | Capabilities |
|---|---|---|
| **Rule-based** (default) | Nothing extra | Keyword navigation, feature guidance, app links |
| **Gemini-powered** | `GEMINI_API_KEY` in `.env` | Full conversation, contextual travel advice, AI-ranked suggestions |

To enable full AI mode, add your key to `.env`:
```env
GEMINI_API_KEY=your-key-here
```

---

## 🗂️ Project Structure

```
Traveloop/
├── accounts/           # Auth, registration, profile management
├── activities/         # Activity catalogue — search, detail views
├── ai_assistant/       # Trave chatbot + smart suggestions engine
│   ├── views.py        # /api/ai/chat/ and /api/ai/suggestions/<id>/
│   └── urls.py
├── budget/             # Budget app models (if separated)
├── cities/             # City explorer — search, detail views
├── trips/              # Core: trips, stops, itinerary, notes, packing
├── admin_dashboard/    # Staff analytics dashboard
├── templates/          # All Django HTML templates
│   ├── base.html       # Global layout + Trave chatbot widget
│   ├── accounts/
│   ├── activities/
│   ├── cities/
│   └── trips/
├── static/
│   ├── css/custom.css  # Bootstrap overrides & design tokens
│   └── js/
│       ├── theme.js    # Light/dark mode toggle
│       └── app.js      # Global JS utilities
├── traveloop_project/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── .env.example
```

---

## 🔒 Security

- All credentials and API keys are stored in `.env`, excluded from version control via `.gitignore`
- Django's built-in **CSRF protection** is enforced on all state-changing requests
- Logout uses a secure **POST request** (no GET-based logout exposure)
- Authentication-required views are protected with `@login_required`

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
