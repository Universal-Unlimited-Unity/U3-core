from fastapi import FastAPI
from U3Partner import U3PartnerModel
from add_partner import Add_Partner

app = FastAPI()

@app.post("/partners")
async def create_partner(p: U3PartnerModel):
  Add_Partner(p)
  return {"status": "success", "partner": p.model_dump()}
