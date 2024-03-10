from fastapi import FastAPI
import os
import json
from GenerateData import generateDataFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

peak_string = ["zero", "single", "double"]

@app.get('/data/get')
async def get_data(peak: int, dense: int, empty: int):
    try:
        file_path = os.path.join(os.path.dirname(__file__), f"data/{peak_string[peak]}_{dense}_{empty}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return {"peak": peak, "dense": dense, "empty": empty, "data": data}
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
async def generate_and_send_data(peak: int, dense: int, empty: int):
    try:
        generated_data = generateDataFile(peak, dense, empty)
        return {"message": "Successfully generated data", "generated_data": generated_data}
    except Exception as e:
        return {"error": f"Failed to generate data: {str(e)}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)