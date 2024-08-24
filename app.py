from fastapi import FastAPI, HTTPException
import os
import json
from GenerateData import generateDataFile
from SaveData import saveData
from fastapi.middleware.cors import CORSMiddleware
from sskernel import sskernel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

peak_string = ["zero", "single", "double"]

#前端中生成数据请求响应
@app.get('/data/generate')
async def generate_and_send_data(peak: int, dense: int, empty: int):
    try:
        generated_data = generateDataFile(peak, dense, empty)
        return {"message": "Successfully generated data", "generated_data": generated_data}
    except Exception as e:
        return {"error": f"Failed to generate data: {str(e)}"}

#前端的数据请求响应
@app.get('/data/get')
async def get_data(peak: int, dense: int, empty: int):
    try:
        file_path = os.path.join(os.path.dirname(__file__), f"data/{peak_string[peak]}_{dense}_{empty}.json")
        # file_path = os.path.join(os.path.dirname(__file__), f"trial_data/lab1/exercise/{peak_string[peak]}_{dense}_{empty}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return {"peak": peak, "dense": dense, "empty": empty, "data": data}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

#前端中样本数据的请求响应
@app.get('/sample/get')
async def get_sample_data(name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), f"data/{name}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return {"data": data}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

    

#前端中实验数据的请求响应
@app.get('/experiment/get')
async def generate_trail_problem(labIdx: int,type: int):
    try:
        doc=["exercise","formal"]
        if type==0:
            file_path = os.path.join(os.path.dirname(__file__), f"trial_data/lab1/{doc[type]}/double_1_1.json")
            # file_path = os.path.join(os.path.dirname(__file__), f"trial_data/lab{labIdx}/{doc[type]}/double_1_1.json")
            with open(file_path, "r") as file:
                originData = json.load(file)
            return {"data": originData}
        # if type==0:
        #     originData=[]
        #     folder_path = f"trial_data/lab{labIdx}/{doc[type]}"
        #     for filename in os.listdir(folder_path):
        #         file_path = os.path.join(folder_path,filename)
        #         with open(file_path, "r") as file:
        #             data = json.load(file)
        #         originData.extend(data)
        #     return {"data": originData}
        if type==1:
            originData=[]
            folder_path = f"trial_data/lab{labIdx}/{doc[type]}"
            # folder_path = f"trial_data/lab1/{doc[type]}"
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as file:
                    data = json.load(file)
                originData.extend(data)
            return {"data": originData}                
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}
    
#接收前端的实验结果并处理
@app.post('/experiment/submit')
async def receive_experiment_data(data: dict):
    try:
        print(data)
        # 在这里处理接收到的数据
        labIdx=data["labIdx"]+1
        saveData(data,labIdx)
        return {"message": "Data received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process data: {str(e)}")

#自适应带宽核密度估计 根据前端请求的数组生成核密度估计值返回
@app.post('/kde/get')
async def adaptive_bandwidth_kde(data:dict):
    x = data["x"]
    bins_num = data["binsNum"]
    nbs = 1000
    W = None
    increment = (8760 /(bins_num * 12))
    tin = [i * increment for i in range(int(8760 / increment) + 1)]

    result  =  sskernel(np.array(x), tin, W, nbs);

    try:
        y = result[0].tolist() if hasattr(result[0], 'tolist') else result[0]
        t = result[1].tolist() if hasattr(result[1], 'tolist') else result[1]

        combined_list = [{"x": t_val, "y": y_val} for t_val, y_val in zip(t, y)]

        return {
            "density": combined_list,
            "optw": float(result[2]) if isinstance(result[2], (int, float)) else result[2],
            # "W": result[3].tolist() if hasattr(result[3], 'tolist') else result[3],
            # "C": result[4].tolist() if hasattr(result[4], 'tolist') else result[4],
            # "confb95": result[5].tolist() if hasattr(result[5], 'tolist') else result[5],
            # "yb": result[6].tolist() if hasattr(result[6], 'tolist') else result[6]
        }
    except Exception as e:
        print(f"Error during serialization: {e}")
        raise
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)