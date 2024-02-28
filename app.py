from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,validator
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
from typing import List
class VoltageData(BaseModel):
    timestamp: datetime
    voltage: float
    amp: float

    @validator('timestamp', pre=True)
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%d-%m-%Y %H:%M')
        return value

app = FastAPI()

# เชื่อมต่อกับ MongoDB
client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.volt 
voltage_collection = db.voltage_data  

@app.post("/add_voltage_data/")
async def add_voltage_data(data: VoltageData):
    document = data.dict()
    result = await voltage_collection.insert_one(document)
    if result.inserted_id:
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=400, detail="Failed to add data.")
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_voltage_data/", response_model=List[VoltageData])
async def get_voltage_data():
    voltage_data = await voltage_collection.find().to_list(100)  # หรือจำกัดจำนวนข้อมูลที่ต้องการดึง
    return voltage_data
