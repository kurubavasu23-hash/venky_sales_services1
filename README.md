# Venky Mobiles Sales & Services

A responsive React storefront and Django REST API for Venky Mobiles, near Clock Tower, Uravakonda. The storefront remains usable with an empty catalogue; products, services and business settings can be managed in Django Admin after setup.

## Requirements

- Windows 10/11, current Node.js LTS with npm, Python 3.10–3.14, Git.
- MySQL 8 only if using MySQL; the default local configuration uses SQLite to make first startup straightforward.

## First run (Windows PowerShell)

From this repository folder:

```powershell
Copy-Item .env.example .env
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations store
python manage.py migrate
python manage.py seed_demo_products
python manage.py createsuperuser
python manage.py runserver
```

In a second PowerShell window at the repository folder:

```powershell
npm install
npm run dev
```

Open the Vite URL shown in the terminal (usually http://localhost:5173). Django Admin is at http://127.0.0.1:8000/admin/ and API endpoints are under http://127.0.0.1:8000/api/.

The initial catalogue uses clearly marked demo records with original local illustrations. The seed command is safe to re-run and never overwrites existing products. These records have no price and unknown availability; replace them with verified business details in Admin before presenting them as inventory. Django Admin supports adding, editing and deleting products, setting a verified price and availability status, and uploading product images in the product image inline. Booking and enquiry records submitted through the public forms are saved in the configured database.

## MySQL setup

Create a database and restricted application account in MySQL Workbench or the MySQL client:

```sql
CREATE DATABASE venky_mobiles CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'venky_app'@'localhost' IDENTIFIED BY 'choose-a-strong-password';
GRANT ALL PRIVILEGES ON venky_mobiles.* TO 'venky_app'@'localhost';
FLUSH PRIVILEGES;
```

Set `DB_ENGINE=django.db.backends.mysql`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, and `MYSQL_PORT` in `.env`. Re-run the migrations. Keep `.env` private and do not commit it.

## Useful commands

```powershell
# Backend, from backend/ with its venv active
python manage.py check
python manage.py makemigrations store
python manage.py migrate
python manage.py runserver

# Frontend, from repository root
npm run build
npm run preview
```

Public API: `GET /api/products/`, `GET /api/categories/`, `GET /api/brands/`, `GET /api/services/`, `GET /api/business-settings/`, `POST /api/bookings/`, `GET /api/bookings/{reference}/`, and `POST /api/enquiries/`. Staff users can manage products and services with authenticated API requests; booking, enquiry and dashboard data is staff-only at `/api/admin/bookings/`, `/api/admin/enquiries/`, and `/api/admin/dashboard/`. Django Admin at `/admin/` offers the business management interface.

## Deployment notes

Build the frontend with `npm run build` and deploy `dist/` to Vercel or another static host. Set `VITE_API_URL` at build time to the public Django API base URL. Deploy Django separately on a Python-capable host, configure MySQL, set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS`, then run migrations and collect static files. Configure HTTPS and durable media storage for uploaded product images. A Vercel frontend deployment does not deploy Django or MySQL.

Before production, review hosting-specific static/media storage, backups, monitoring, email/contact workflows, rate limits and retention practices. The sample uses Django's anonymous request throttling as a basic starting point; production should use a shared cache-backed throttle and the host's security controls.
