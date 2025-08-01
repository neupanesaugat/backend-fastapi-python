# test_db.py
from app.database import SessionLocal
from sqlalchemy import text  

try:
    db = SessionLocal()
    db.execute(text("SELECT 1"))  
    print("Database connected successfully!")
except Exception as e:
    print(" Failed to connect to the database:")
    print(e)
finally:
    db.close()
