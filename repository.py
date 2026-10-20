from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from Model import Student
from schima import StudentCreate, StudentUpdate

def get_students(db: Session, search: str = "", department: str = ""):
    stmt = select(Student).order_by(Student.id.desc())
    if search.strip():
        term = f"%{search.strip()}%"
        stmt = stmt.where(or_(Student.name.ilike(term), Student.roll_no.ilike(term), Student.email.ilike(term)))
    if department.strip(): stmt = stmt.where(Student.department == department.strip())
    return list(db.scalars(stmt).all())

def count_students(db: Session): return len(db.scalars(select(Student.id)).all())
def get_student(db: Session, student_id: int): return db.get(Student, student_id)
def get_by_roll(db: Session, roll_no: str): return db.query(Student).filter(Student.roll_no == roll_no.strip()).first()
def get_by_email(db: Session, email: str): return db.query(Student).filter(Student.email == str(email).lower()).first()

def create_student(db: Session, data: StudentCreate):
    obj = Student(roll_no=data.roll_no.strip(), name=data.name.strip(), department=data.department.strip(), semester=data.semester.strip(), email=str(data.email).lower(), phone=data.phone.strip() if data.phone else None, gender=data.gender or None, address=data.address.strip() if data.address else None)
    db.add(obj); db.commit(); db.refresh(obj); return obj

def update_student(db: Session, obj: Student, data: StudentUpdate):
    obj.roll_no=data.roll_no.strip(); obj.name=data.name.strip(); obj.department=data.department.strip(); obj.semester=data.semester.strip(); obj.email=str(data.email).lower(); obj.phone=data.phone.strip() if data.phone else None; obj.gender=data.gender or None; obj.address=data.address.strip() if data.address else None
    db.commit(); db.refresh(obj); return obj

def delete_student(db: Session, obj: Student): db.delete(obj); db.commit()
