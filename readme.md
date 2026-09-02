# 🛒 Grocery Store Management System — Backend API

A REST API backend for managing a grocery store's products, inventory, and customer orders, built with **FastAPI** and **MySQL**. Secured with **JWT authentication**, containerized with **Docker**, and deployed live on **Railway**.

## 🔗 Live Demo

**API Docs (Swagger UI):**
https://grocery-store-application-production.up.railway.app/docs

Try the endpoints directly in your browser — no setup required.

> Note: the free-tier deployment may take 10–30 seconds to respond on the first request after a period of inactivity. This is normal behavior for free-tier hosting.

## 📌 What This Project Does

This is a **backend-only** API (no frontend UI) that lets a grocery store:
- Register and authenticate users with **JWT tokens**
- Manage products — add, view, and soft-delete products, each with a unit of measure (UOM) and price
- Create customer orders containing multiple products, and view full order history
- Protect all product/order routes behind authentication — only logged-in users can manage store data

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Python) |
| Database | MySQL |
| Authentication | JWT (python-jose) + bcrypt password hashing |
| Containerization | Docker + Docker Compose |
| Deployment | Railway |

## 🏗️ Architecture

The backend follows a **layered architecture** for separation of concerns:

```
Backend/
├── app/
│   ├── main.py                  # App creation, middleware, router registration
│   ├── api/routes/               # Thin route handlers (HTTP layer)
│   │   ├── auth.py               # /register, /login
│   │   ├── products.py           # /getProducts, /getUOM, /insertProduct, /deleteProduct
│   │   └── orders.py             # /getAllOrders
│   ├── core/                     # Shared infrastructure
│   │   ├── database.py           # DB connection instance
│   │   ├── sql_connection.py     # PyMySQL connection setup
│   │   ├── security.py           # JWT creation/verification, password hashing
│   │   └── init_db.py            # Auto-creates tables + seed data on startup
│   └── dao/                      # Data Access layer — raw SQL queries only
│       ├── user_dao.py
│       ├── product_dao.py
│       ├── order_dao.py
│       └── uom_dao.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

**Why this structure:** routes stay thin and only handle HTTP concerns; all database logic is isolated in the DAO layer; shared infrastructure like auth and DB connections live in `core/`. This keeps each file focused on a single responsibility and makes the codebase easy to navigate and extend.

## 📡 API Endpoints

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| POST | `/register` | No | Create a new user account |
| POST | `/login` | No | Log in, returns a JWT access token |
| GET | `/getUOM` | Yes | List all units of measure |
| GET | `/getProducts` | Yes | List all active products |
| POST | `/insertProduct` | Yes | Add a new product |
| POST | `/deleteProduct` | Yes | Soft-delete a product |
| GET | `/getAllOrders` | Yes | List all orders with their line items |

Full interactive documentation with request/response schemas is available at `/docs`.

## 🚀 Running Locally

### Option A — With Docker (recommended)

```bash
cd Backend
docker compose up --build
```

This starts the API and a local MySQL container together. Visit:
```
http://localhost:8000/docs
```

To stop:
```bash
docker compose down
```

### Option B — Without Docker

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure a MySQL instance is running and accessible, and set the following environment variables (in a `.env` file):
   ```
   DB_HOST=localhost
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=grocery_db
   SECRET_KEY=your_secret_key
   ```
4. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Visit:
   ```
   http://localhost:8000/docs
   ```

## ☁️ Deployment

Deployed on **Railway**:
- The FastAPI app runs from the `Dockerfile` in `Backend/`
- A managed MySQL database is provisioned alongside the app, connected via environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`)
- On startup, `app/core/init_db.py` automatically creates any missing tables (`CREATE TABLE IF NOT EXISTS`) and seeds default units of measure — so the database schema is set up with zero manual steps after deployment

## 🔐 Authentication Flow

1. A user registers via `/register` — their password is hashed with bcrypt before being stored
2. A user logs in via `/login` — on success, the API returns a signed JWT access token
3. The token is sent in the `Authorization: Bearer <token>` header for all protected routes
4. `get_current_user` (in `app/core/security.py`) decodes and validates the token on every protected request

## 📈 Possible Next Steps

- Add a `services/` layer to separate business logic (e.g. ownership checks, validation) from the DAO layer
- Add role-based access control (e.g. admin vs staff)
- Add pagination and search/filtering to `/getProducts`
- Add automated tests (pytest + FastAPI's TestClient)
