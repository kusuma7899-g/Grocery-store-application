# 🛒 Grocery Store Management System

A full-stack web application to manage grocery store products and orders.

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| Database | MySQL |
| Authentication | JWT Tokens |
| Frontend | HTML, Bootstrap, jQuery |

## ✨ Features

- User Login and Registration with JWT Authentication
- Manage Products (Add, View, Delete)
- Create Customer Orders with multiple products
- View all Order History
- Protected API routes

## 📁 Project Structure
Grocery-store-application/
├── Backend/
│   ├── server.py        → All API routes
│   ├── auth.py          → JWT authentication
│   ├── product_dao.py   → Product database operations
│   ├── order_dao.py     → Order database operations
│   ├── user_dao.py      → User database operations
│   └── sql_connection.py→ MySQL connection
├── UI/
│   ├── login.html       → Login page
│   ├── index.html       → Dashboard
│   ├── manage-product.html → Product management
│   ├── order.html       → Create new order
│   └── js/custom/       → JavaScript files
└── .gitignore

## 🚀 How to Run

### Backend
```bash
# Install packages
pip install fastapi uvicorn pymysql python-dotenv python-jose[cryptography] passlib bcrypt==4.0.1 python-multipart

# Create .env file in Backend folder
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=grocery_db
SECRET_KEY=yoursecretkey

# Start server
cd Backend
uvicorn server:app --reload
```

### Frontend
- Open `UI/login.html` with Live Server in VS Code
- Go to `http://127.0.0.1:5500/UI/login.html`

## 🔐 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /register | No | Create new user |
| POST | /login | No | Login and get token |
| GET | /getProducts | Yes | Get all products |
| POST | /insertProduct | Yes | Add new product |
| POST | /deleteProduct | Yes | Delete product |
| GET | /getUOM | Yes | Get units of measurement |
| GET | /getAllOrders | Yes | Get all orders |
| POST | /insertOrder | Yes | Create new order |

## 🔒 Authentication Flow
Register → Login → Get JWT Token
↓
Send token with every API call
↓
Token expires in 30 minutes
↓
Login again

## 💻 Database Tables

- **users** - stores login credentials
- **uom** - units of measurement (kg, litre etc)
- **products** - grocery products
- **orders** - customer orders
- **orders_details** - individual items in each order

## 👩‍💻 Author

Kusuma — Fresher Full Stack Developer