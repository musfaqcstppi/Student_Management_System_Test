from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import repository
from schima import StudentCreate, StudentUpdate

def list_students(db: Session, search="", department=""): return repository.get_students(db, search, department)
def total_students(db: Session): return repository.count_students(db)
def find_student(db: Session, student_id: int):
    obj=repository.get_student(db, student_id)
    if obj is None: raise HTTPException(status_code=404, detail="Student not found")
    return obj

def create_student(db: Session, data: StudentCreate):
    if repository.get_by_roll(db, data.roll_no): raise HTTPException(status_code=409, detail="Roll number already exists")
    if repository.get_by_email(db, str(data.email).lower()): raise HTTPException(status_code=409, detail="Email already exists")
    try: return repository.create_student(db, data)
    except IntegrityError:
        db.rollback(); raise HTTPException(status_code=409, detail="Roll number or email already exists")

def update_student(db: Session, student_id: int, data: StudentUpdate):
    obj=find_student(db, student_id); by_roll=repository.get_by_roll(db,data.roll_no); by_email=repository.get_by_email(db,str(data.email).lower())
    if by_roll and by_roll.id != student_id: raise HTTPException(status_code=409, detail="Roll number is used by another student")
    if by_email and by_email.id != student_id: raise HTTPException(status_code=409, detail="Email is used by another student")
    try: return repository.update_student(db,obj,data)
    except IntegrityError:
        db.rollback(); raise HTTPException(status_code=409, detail="Could not update student; check roll number and email")

def delete_student(db: Session, student_id: int):
    obj=find_student(db,student_id); repository.delete_student(db,obj); return {"message":"Student deleted successfully"}
