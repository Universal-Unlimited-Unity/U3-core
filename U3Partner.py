from pydantic import BaseModel, field_validator, model_validator, Field
from enum import Enum

PATH = 'U3Partners.csv'
class U3Gender(str, Enum):
  Male = 'M'
  Female = 'F'
class U3Rank(str,Enum):
  Universel = 'Universel'
  Unlimited = 'Unlimited'
  Limited = 'Limited'
class U3Partner(BaseModel):
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