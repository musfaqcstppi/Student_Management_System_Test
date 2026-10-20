from pathlib import Path
from urllib.parse import quote_plus
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session
import Model
import Service
from database import Base, engine, get_db
from schima import StudentCreate, StudentUpdate

BASE_DIR=Path(__file__).resolve().parent
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Student Management System", version="1.0.0")
app.mount("/static",StaticFiles(directory=str(BASE_DIR/"static")),name="static")
templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
DEPARTMENTS=["Computer Science and Technology","Electrical Technology","Civil Technology","Electronics Technology","Mechanical Technology","Power Technology","Other"]
SEMESTERS=["1st","2nd","3rd","4th","5th","6th","7th","8th"]
def form_error(path,message): return RedirectResponse(url=f"{path}?error={quote_plus(message)}",status_code=303)

@app.get("/",response_class=HTMLResponse)
def home(request:Request,db:Session=Depends(get_db)):
    students=Service.list_students(db)
    return templates.TemplateResponse(request=request,name="index.html",context={"total_students":len(students),"departments_count":len({s.department for s in students}),"recent_students":students[:5]})
@app.get("/students",response_class=HTMLResponse)
def students_page(request:Request,search:str="",department:str="",db:Session=Depends(get_db)):
    return templates.TemplateResponse(request=request,name="students.html",context={"students":Service.list_students(db,search,department),"search":search,"department":department,"departments":DEPARTMENTS})
@app.get("/students/new",response_class=HTMLResponse)
def create_page(request:Request):
    return templates.TemplateResponse(request=request,name="student_form.html",context={"page_title":"Add Student","student":None,"action":"/students","button_text":"Save Student","departments":DEPARTMENTS,"semesters":SEMESTERS})
@app.post("/students")
def create_student_form(roll_no:str=Form(...),name:str=Form(...),department:str=Form(...),semester:str=Form(...),email:str=Form(...),phone:str=Form(""),gender:str=Form(""),address:str=Form(""),db:Session=Depends(get_db)):
    try: data=StudentCreate(roll_no=roll_no,name=name,department=department,semester=semester,email=email,phone=phone or None,gender=gender or None,address=address or None)
    except ValidationError: return form_error("/students/new","Check required fields and enter a valid email address")
    try: Service.create_student(db,data)
    except HTTPException as exc: return form_error("/students/new",str(exc.detail))
    return RedirectResponse(url="/students?success=Student+created+successfully",status_code=303)
@app.get("/students/{student_id}/edit",response_class=HTMLResponse)
def edit_page(request:Request,student_id:int,db:Session=Depends(get_db)):
    obj=Service.find_student(db,student_id)
    return templates.TemplateResponse(request=request,name="student_form.html",context={"page_title":"Edit Student","student":obj,"action":f"/students/{student_id}/edit","button_text":"Update Student","departments":DEPARTMENTS,"semesters":SEMESTERS})
@app.post("/students/{student_id}/edit")
def update_student_form(student_id:int,roll_no:str=Form(...),name:str=Form(...),department:str=Form(...),semester:str=Form(...),email:str=Form(...),phone:str=Form(""),gender:str=Form(""),address:str=Form(""),db:Session=Depends(get_db)):
    try: data=StudentUpdate(roll_no=roll_no,name=name,department=department,semester=semester,email=email,phone=phone or None,gender=gender or None,address=address or None)
    except ValidationError: return form_error(f"/students/{student_id}/edit","Check required fields and enter a valid email address")
    try: Service.update_student(db,student_id,data)
    except HTTPException as exc: return form_error(f"/students/{student_id}/edit",str(exc.detail))
    return RedirectResponse(url=f"/students/{student_id}?success=Student+updated+successfully",status_code=303)
@app.get("/students/{student_id}",response_class=HTMLResponse)
def student_detail(request:Request,student_id:int,db:Session=Depends(get_db)):
    return templates.TemplateResponse(request=request,name="student_detail.html",context={"student":Service.find_student(db,student_id)})
@app.post("/students/{student_id}/delete")
def delete_student_form(student_id:int,db:Session=Depends(get_db)):
    Service.delete_student(db,student_id); return RedirectResponse(url="/students?success=Student+deleted+successfully",status_code=303)
@app.get("/about",response_class=HTMLResponse)
def about(request:Request): return templates.TemplateResponse(request=request,name="about.html",context={})

@app.get("/api/students")
def api_students(search:str="",department:str="",db:Session=Depends(get_db)): return Service.list_students(db,search,department)
@app.get("/api/students/{student_id}")
def api_student(student_id:int,db:Session=Depends(get_db)): return Service.find_student(db,student_id)
@app.post("/api/students",status_code=201)
def api_create(data:StudentCreate,db:Session=Depends(get_db)): return Service.create_student(db,data)
@app.put("/api/students/{student_id}")
def api_update(student_id:int,data:StudentUpdate,db:Session=Depends(get_db)): return Service.update_student(db,student_id,data)
@app.delete("/api/students/{student_id}")
def api_delete(student_id:int,db:Session=Depends(get_db)): return Service.delete_student(db,student_id)
@app.get("/health")
def health(): return {"status":"ok"}
