from U3Partner import U3PartnerModel
from sqlalchemy import Table, MetaData, Column, create_engine,String, Enum, Integer, select, insert,delete

db = 'postgresql+psycopg://postgres:adamaakif@db:5432/u3'
eng = create_engine(db)
metadata = MetaData()
partners = Table(
    "partners",
    metadata,
    Column("UnityId", String, primary_key=True),
    Column("FirstName", String),
    Column("MiddleName", String),
    Column("LastName", String),
    Column("Gender", Enum('M', 'F', name='gender')),
    Column("Age", Integer),
    Column("Loyalty", Enum('Universel', 'Unlimited', 'Limited', name='U3Rank'))
  )
def init_db():
  metadata.create_all(eng, checkfirst=True)

def UnityId_Used(UnityId: str) -> bool:
  with eng.connect() as conn:
    stmt = select(partners).where(partners.c.UnityId == UnityId)
    res = conn.execute(stmt).fetchone()
    if res is None:
       return False
    return True  
    
def Update_UnityId(p: U3PartnerModel):
    Edit = 0
    UnityId_OG = p.UnityId
    while UnityId_Used(p.UnityId):
      Edit = Edit + 85
      NewUnityId = UnityId_OG + str(Edit)
      p.UnityId = NewUnityId
    
def Add_Partner(p: U3PartnerModel):
  # check if unityId is unique, if not generate a new one.

  if (UnityId_Used(p.UnityId)):
    Update_UnityId(p)
    
  #Insert new partner

  with eng.connect() as conn:
    stmt = insert(partners).values(UnityId=p.UnityId, FirstName=p.FirstName, MiddleName=p.MiddleName,LastName=p.LastName,Gender=p.Gender.value,Age=p.Age, Loyalty=p.Loyalty.value)
    conn.execute(stmt)
    conn.commit()
def Search(UnityId: str):
    with eng.connect() as conn:
        if UnityId.lower() != "all":
          search = select(partners).where(partners.c.UnityId == UnityId)
          exist = conn.execute(search).fetchone()
          return exist
        else:
          search = select(partners)
          exist = conn.execute(search).fetchall()
          return exist
    
def Remove_Partner(UnityId: str):
    if Search(UnityId):
        with eng.connect() as conn:
            with conn.begin():
              stmt = delete(partners).where(partners.c.UnityId == UnityId)
              conn.execute(stmt)
            return 0
    return 1

      


  