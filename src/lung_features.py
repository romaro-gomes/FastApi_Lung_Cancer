from pydantic import BaseModel
from enum import Enum

class LungFeatures(BaseModel):
    gender: str
    age:int
    smoking:str
    yellow_fingers:str
    anxiety:str
    peer_pressure:str
    chronic_disease:str
    fatigue:str
    allergy:str
    wheezing:str
    alcohol_consuming:str
    coughing:str
    shortness_of_breath:str
    swallowing_difficulty:str
    chest_pain:str