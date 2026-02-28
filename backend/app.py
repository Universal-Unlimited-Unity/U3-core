from fastapi import FastAPI, Body, Path, HTTPException
from U3Partner import U3PartnerModel, U3Update_PartnerModel
from CRUD import Add_Partner, init_db, Remove_Partner, Search, Update_Partner, Search_No_All
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

@app.patch("/partners/{UnityId}", response_model=U3Update_PartnerModel)
def update_partner(UnityId: Annotated[str, Path()], u: Annotated[U3Update_PartnerModel, Body()]):
  if Search_No_All(UnityId):
    Update_Partner(UnityId, u)
    return Search_No_All(UnityId)
  raise HTTPException(status_code=404)
