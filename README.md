# FastAPI Student Management System

## Six pages
1. Home `/`
2. Student list/search/filter `/students`
3. Add student `/students/new`
4. Student details `/students/{student_id}`
5. Edit student `/students/{student_id}/edit`
6. About `/about`

## Backend files
- `database.py`: SQLAlchemy engine/session; SQLite by default
- `repository.py`: database CRUD operations
- `Main.py`: FastAPI routes and app
- `Service.py`: business logic and duplicate validation
- `schima.py`: Pydantic schemas (filename kept as requested)
- `Model.py`: SQLAlchemy Student model

Frontend files are in `templates/`, `static/css/style.css`, and `static/js/app.js`.

## Run on Windows / VS Code
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn Main:app --reload
```
Open `http://127.0.0.1:8000/`; Swagger docs: `http://127.0.0.1:8000/docs`. The SQLite database `students.db` is created automatically.

## JSON API
- `GET /api/students?search=&department=`
- `GET /api/students/{student_id}`
- `POST /api/students`
- `PUT /api/students/{student_id}`
- `DELETE /api/students/{student_id}`

Example JSON: `{"roll_no":"CST-23001","name":"Rahim Uddin","department":"Computer Science and Technology","semester":"3rd","email":"rahim@example.com","phone":"01700000000","gender":"Male","address":"Pabna, Bangladesh"}`

## Optional PostgreSQL
Create the database first, install `psycopg2-binary`, then set `DATABASE_URL` to `postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/student_db`. Do not use the database name as a schema.

This is a learning project. Add authentication, CSRF protection, tests, migrations, and production hardening before using it for sensitive real student data.
