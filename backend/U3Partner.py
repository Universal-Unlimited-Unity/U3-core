from pydantic import BaseModel, field_validator, model_validator, Field
from enum import Enum

class U3Gender(str, Enum):
  Male = 'M'
  Female = 'F'
class U3Rank(str,Enum):
  Universel = 'Universel'
  Unlimited = 'Unlimited'
  Limited = 'Limited'
class U3PartnerModel(BaseModel):
  Gender: U3Gender 
  Loyalty: U3Rank
  FirstName: str
  MiddleName: str | None = None
  LastName: str
  Age: int = Field(ge=18)
  UnityId: str | None = None
  @model_validator(mode='after')
  def Generate_Unityid(self):
    if self.UnityId is None:
      self.UnityId = f"U{self.LastName[-1]}{self.FirstName[-1]}{self.Loyalty.value}"
    return self

class U3Update_PartnerModel(BaseModel):
  Gender: U3Gender | None = None
  Loyalty: U3Rank | None = None
  FirstName: str | None = None
  MiddleName: str | None = None
  LastName: str | None = None
  Age: int | None = Field(ge=18, default=None)
