<<<<<<< HEAD
# EventBuzz – College Event Management Platform

EventBuzz is a full-stack web application for browsing, registering, and reviewing college events. Built with **Django**, **SQLite**, and **HTML/CSS/JavaScript**.

---

## Features

- **Students:** Register/Login, browse events by college and category, view event details with countdown, register for events, email confirmation, submit reviews and 5-star ratings.
- **Admins:** Add/update/delete events and colleges, view registrations and reviews, registration count per event. Event date cannot be in the past (validated in admin).
- **Event date tags:** Events show status: **Coming soon**, **Expire soon** (< 24h), **Register before time up** (< 3 days), **Expired**. Expired events are automatically excluded from the homepage.
- **UI:** Modern responsive design with gradients, glassmorphism, dark/light mode toggle, animations, and mobile-friendly layout.

---

## Tech Stack

- **Backend:** Django, SQLite, Django auth
- **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6)
- **Email:** Console backend (emails printed in terminal)

---

## Folder structure (correct layout)

**Important:** All commands below must be run from the **eventbuzz** folder (the folder that contains `manage.py`).

You can put the virtual environment (venv) **inside** eventbuzz or **outside** (in the parent folder). .env is optional and goes inside eventbuzz.

```
Aict project/
├── venv/                    ← optional: create here (env “after” / separate from app)
├── eventbuzz/               ← project root: open terminal HERE
│   ├── manage.py            ← run: python manage.py runserver
│   ├── .env                  ← optional: copy from .env.example (env vars loaded on run)
│   ├── .env.example
│   ├── .gitignore
│   ├── run.bat               ← Windows: double‑click to run server
│   ├── requirements.txt
│   ├── eventbuzz/            # Django project (settings, urls)
│   │   ├── settings.py
│   │   └── urls.py
│   ├── events/               # app (models, views, templates, static)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── templates/events/
│   │   └── static/events/
│   └── README.md
```

---

## How to run

### 1. Open terminal in the **eventbuzz** folder

```bash
cd "c:\Users\lenovo\OneDrive\Desktop\Aict project\eventbuzz"
```

(Or in File Explorer, go to the `eventbuzz` folder, then **right‑click → Open in Terminal**.)

### 2. Create virtual environment (do this once)

**Option A – venv inside eventbuzz:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Option B – venv in parent folder (env “comes after” / separate):**
```bash
cd ..
python -m venv venv
venv\Scripts\activate
cd eventbuzz
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Migrate and run

```bash
python manage.py migrate
python manage.py runserver
```

**Load sample data (recommended)** so the homepage shows colleges and events:
```bash
python manage.py seed_events
```
This creates 3 sample colleges and 6 upcoming events. Run it once; you can add more via Admin.

**Windows shortcut:** double‑click `run.bat` inside the eventbuzz folder (it will migrate and start the server; venv can be inside eventbuzz or in the parent folder).

### 5. Optional: .env file

Copy `.env.example` to `.env` if you want to override `SECRET_KEY` or `DEBUG`. The app runs without .env; settings load from .env when the app starts.

### 6. Create superuser (for admin)

In a new terminal (with venv activated and `cd eventbuzz`):

```bash
python manage.py createsuperuser
```

### 7. Open in browser

- **Site:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

Add colleges and events in the admin panel. Events with a future date/time will appear on the homepage; expired events are hidden.

---

## Security

- CSRF protection on all forms
- `@login_required` on registration and review views
- Form validation (contact number, college name, rating, password match)
- Admin: event date/time cannot be in the past

---

## Email

Registration confirmation emails are sent using Django’s **console** backend: they appear in the terminal where `runserver` is running. For production, configure a real email backend in `settings.py`.

---

## License

MIT.
=======
# eventbuzz-
college event management system
>>>>>>> 6d00e7bf3e3e32a26aa527824faf7fca3910edb9
