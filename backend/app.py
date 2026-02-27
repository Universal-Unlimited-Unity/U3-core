from fastapi import FastAPI, Body
from U3Partner import U3PartnerModel
from add_partner import Add_Partner, init_db
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
