import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



# DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/students"
DATABASE_URL = "postgresql+psycopg2://training_jls0_user:h3daqQFGBaycKf2aK9n9iL5SaFIPJiA6@dpg-dbbfgmeq1p3s73cefugg-a.oregon-postgres.render.com/training_jls0"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()






# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")



# connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
# engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
