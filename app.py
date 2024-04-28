from typing import List
from fastapi import FastAPI
import os
import json
from GenerateData import generateDataFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BasicInfo(BaseModel):
    name: str
    gender: str
    age: int
    major: str
    contact: str
class TimeScale(BaseModel):
    largeScale:int
    timeRange:int
    time:List[int]
class DataSet(BaseModel):
    timeScale1:TimeScale
    timeScale2:TimeScale
    timeScale3:TimeScale
class Problem(BaseModel):
    # data: DataSet
    question: str
    label: str
    questionId:int
    rightAnswer:str
    answer:str
    spendTime:int
    peak:int
    dense:int
    empty:int
class ProblemInfo(BaseModel):
    session:int
    problems:List[Problem]
class OneInfo(BaseModel):
    problemInfo:List[ProblemInfo]
    info: BasicInfo
    completeTime: int

peak_string = ["zero", "single", "double"]

@app.get('/data/get')
async def get_data(peak: int, dense: int, empty: int):
    try:
        file_path = os.path.join(os.path.dirname(__file__), f"data/{peak_string[peak]}_{dense}_{empty}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return {"data": data}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

@app.get('/sample/get')
async def get_sample_data(name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), f"data/{name}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return {"data": data}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

@app.get('/data/generate')
async def generate_and_send_data(peak: int, dense: int, empty: int, answer: int):
    try:
        generated_data = generateDataFile(peak, dense, empty)
        file_path = os.path.join(os.path.dirname(__file__), f"data/{peak_string[peak]}_{dense}_{empty}.json")
        with open(file_path, "r") as file:
            newData = json.load(file)
        if answer==0:
            newData["answer"]=[]
        return {"message": "Successfully generated data", 
                "generated_data": newData}

    except Exception as e:
        return {"error": f"Failed to generate data: {str(e)}"}

@app.post('/experiment/submit')
async def save_experiment_data(info: OneInfo):
    try:
        print(info)
        return {"message": "Successfully saved experiment data"}
    except Exception as e:
        return {"error": f"Failed to save experiment data: {str(e)}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)