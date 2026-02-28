from fastapi import FastAPI, Body, Path, HTTPException
from U3Partner import U3PartnerModel
from CRUD import Add_Partner, init_db, Remove_Partner, Search
from contextlib import asynccontextmanager
from typing import Annotated
@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  print("Table Created!")
  yield
  print("Shutting Down...")
app = FastAPI(lifespan=lifespan)
@app.post("/partners")
async def create_partner(p: Annotated[U3PartnerModel, Body()]):
  Add_Partner(p)
  return {"status": "success", "partner": p.model_dump(mode="json")}

@app.delete("/partners/{UnityId}")
async def delete_partner(UnityId: Annotated[str, Path()]):
  return Remove_Partner(UnityId)

@app.get("/partners/{UnityId}", response_model=list[U3PartnerModel] | U3PartnerModel)
def get_partner(UnityId: Annotated[str, Path()]):
  p = Search(UnityId)
  if not p:
    raise HTTPException(status_code=404)
  return p

  
