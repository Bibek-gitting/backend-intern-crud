# Backend Intern CRUD API

A FastAPI-based backend that implements authentication, blog posts, comments, and likes.  
This project is built as part of an assignment to demonstrate CRUD operations, JWT authentication, and relational database handling.

---

## 🚀 Features
- User registration & login (JWT authentication)
- Create, read, update, delete (CRUD) blog posts
- Comment & like functionality
- Protected routes with access tokens
- Swagger UI & Postman collection for testing

---

## 🛠️ Tech Stack
- **Python** (FastAPI, SQLAlchemy, Pydantic)
- **PostgreSQL** (via psycopg2)
- **Alembic** (database migrations)
- **JWT** (authentication)
- **Uvicorn** (server)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Bibek-gitting/backend-intern-crud.git
cd backend-intern-crud
```
---

### 2. **Create virtual environment & install dependencies**
```bash
python -m venv venv
source venv/bin/activate # Linux / macOS
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

### 3. **Setup PostgreSQL Database**
 ```bash
CREATE DATABASE backend_crud;
```
Create `.env` file in the project root:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/backend_crud
SECRET_KEY=your_secret_key
```

### 4. **Run migrations**
```bash
alembic upgrade head
```

### 5. **Start the FastAPI server**
```bash
uvicorn app.main:app --reload
```

Now visit:
- API root → http://127.0.0.1:8000
- Swagger UI → http://127.0.0.1:8000/docs

---

## Testing with Postman
- Import `postman_collection.json`
- Demonstrates authorized vs unauthorized requests
- CRUD operations
- Like & comment workflows

---

## Example API Flow
1. Register → `/auth/register`
2. Login → `/auth/login` (get JWT access token)
3. Use token in Authorization header:
   - Create Post → `/posts`
   - Update/Delete Post → `/posts/{id}`
   - Add Comment → `/comments`
   - Like Post → `/likes`

---

