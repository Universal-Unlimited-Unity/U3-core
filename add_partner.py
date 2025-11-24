import sqlite3
from U3Partner import U3PartnerModel

db_path = 'partner_db'

def init_db():
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  cursor.execute(""" CREATE TABLE IF NOT EXISTS partners (
    First_Name TEXT,
    Middle_Name TEXT,
    Last_Name TEXT,
    Age INTEGER,
    Gender TEXT,
    Loyalty TEXT,
    UnityId TEXT) """)

  conn.commit()
  conn.close()

def Add_Partner(p: U3PartnerModel):
  init_db()
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  cursor.execute(""" INSERT INTO partners(First_Name,
    Middle_Name,
    Last_Name,
    Age,
    Gender,
    Loyalty,
    UnityId) 
    VALUES (?, ?, ?, ?, ?, ?, ?) """, 
                 (p.FirstName,
                  p.MiddleName,
                  p.LastName,
                  p.Age,
                  p.Gender.value,
                  p.Loyalty.value,
                  p.UnityId))
  conn.commit()
  conn.close()
  
  

  
    
    
