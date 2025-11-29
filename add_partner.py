import sqlite3
from U3Partner import U3PartnerModel

db_path = 'partner_db'

def init_db():
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  cursor.execute(""" CREATE TABLE IF NOT EXISTS partners (
    First_Name TEXT UNIQUE,
    Middle_Name TEXT,
    Last_Name TEXT,
    Age INTEGER,
    Gender TEXT,
    Loyalty TEXT,
    UnityId TEXT) """)

  conn.commit()
  conn.close()

def UnityId_Used(p: U3PartnerModel) -> bool:
  init_db()
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute(""" SELECT * FROM partners
                    WHERE UnityId = ? """, (p.UnityId,))
  result = cursor.fetchone()
  conn.close()
  return result is not None
  
def Update_UnityId(p: U3PartnerModel):
  Edit = 0
  UnityId_OG = p.UnityId
  while UnityId_Used(p):
    Edit = Edit + sum(list(map(ord, p.FirstName+p.LastName))) // 85
    NewUnityId = UnityId_OG + str(Edit + sum(list(map(ord, p.FirstName+p.LastName))) // 85)
    p.UnityId = NewUnityId
  
def Add_Partner(p: U3PartnerModel):
  init_db()
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  # check if unityId is unique, if not generate a new one.

  if (UnityId_Used(p)):
    Update_UnityId(p)

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
  
  

  
    
    
