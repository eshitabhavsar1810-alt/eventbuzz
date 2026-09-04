# How to Run & Use the EventBuzz Admin Panel

## 1. Run the Django server

Open a terminal in the project folder and run:

```bash
cd "Aict project\eventbuzz"
python manage.py migrate
python manage.py runserver
```

Leave the server running. You should see something like: `Starting development server at http://127.0.0.1:8000/`

## 2. Open the site

In your browser go to: **http://127.0.0.1:8000/**

## 3. Open the Admin Panel

**Option A – From the navbar**  
Click **Admin** in the top menu (next to Contact). This goes to the Admin Login page.

**Option B – Direct URLs**

- Admin **login**: http://127.0.0.1:8000/admin-panel/login/
- Admin **signup** (create first admin): http://127.0.0.1:8000/admin-panel/signup/
- Admin **dashboard** (after login): http://127.0.0.1:8000/admin-panel/

## 4. First-time setup

1. Go to **http://127.0.0.1:8000/admin-panel/signup/**
2. Fill: Full Name, Email, Username, Password, Confirm Password.
3. Click **SIGN UP** → you are redirected to Admin Login.
4. Log in with that username and password.
5. You will be taken to the **Admin Dashboard**, where you can:
   - Add / Edit / Delete events
   - Set event status (Upcoming, Ongoing, Completed, Cancelled)
   - View and export registrations
   - (Users get email notifications for new/updated events and registration confirmations)

## 5. If you see “no changes” or errors

- Run migrations: `python manage.py migrate`
- Restart the server: stop it (Ctrl+C), then run `python manage.py runserver` again.
- Use **Admin** in the navbar or **http://127.0.0.1:8000/admin-panel/login/** — this is the *EventBuzz* admin, not Django’s `/admin/` site.
