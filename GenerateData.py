import random
import math
import json
import os
# from math import sqrt, log, pi, cos, sin

daysOfMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
daysOfHalfMonth = [15, 16, 15, 14, 15, 16, 15, 15, 15, 16, 15, 15, 15, 16, 15, 16, 15, 15, 15, 16, 15, 15, 15, 16]
peak_string = ["zero", "single", "double"]

# 生成符合标准正态分布的数据
def randomNormalDistribution():
    # 实现normal_box_muller方法
    u1 = random.random()
    u2 = random.random()
    r = math.sqrt(-2*math.log(u1))
    theta = 2*math.pi*u2
    return r*math.cos(theta)

# print(randomNormalDistribution())

# 生成指定方差和均值的正态分布
def getNumberInNormalDistribution(mean,std_dev):
    return round(mean+(randomNormalDistribution()*std_dev))

# value=getNumberInNormalDistribution(2000,1000)
# print(value)
# print(round(value))

def generateOriginData(peak):
    arr = []
    times = 1500
    mean = []
    std_dev = 0
    cnt = {}


    if peak==0:
        for i in range(times):
            arr.append(random.randint(0,8760))
    elif peak==1:
        mean.append(random.randint(1500,7260))
        std_dev=2000
    elif peak==2:
        mean.append(random.randint(1190,3190))
        mean.append(random.randint(5570,7570))
        std_dev=1000

    # #连续区域(如果mean为空会自动跳过)
    # for m in mean:
    #     denseMean=random.randint(m-1000,m+1000)
    #     for i in range(20):
    #         value=getNumberInNormalDistribution(denseMean,10)
    #         valWeek=math.ceil(value/24/7)
    #         cnt[valWeek]=1+cnt.get(valWeek, 0)
    #         arr.append(value)   

    #整体分布
    if peak!=0:
        time = int(times/len(mean))
        for m in mean:
            for j in range(time):
                value=getNumberInNormalDistribution(m,std_dev)
                valWeek=math.ceil(value/24/7)
                if cnt.get(valWeek,0):
                    cnt[valWeek]=cnt.get(valWeek)-1
                    if cnt[valWeek]==0:
                        del cnt[valWeek]
                else:
                    arr.append(value)

    # 为arr数组去重
    unique_set = set(arr)
    result_list = list(unique_set)

    return  result_list,mean


def generateData(peak,denseNum,emptyNum):
    arr,mean=generateOriginData(peak)

    Means=[]
    if len(mean)==0:
        Means.append(random.randint(0,8760))
        Means.append(random.randint(0,8760))
    elif len(mean)==1:
        Means.append(random.randint(mean[0]-800,mean[0]))
        Means.append(random.randint(mean[0],mean[0]+800))
    else:
        randidx=random.randint(0,1)
        Means.append(random.randint(mean[randidx]-800,mean[randidx]+800))
        Means.append(random.randint(mean[1-randidx]-800,mean[1-randidx]+800))

    for i in range(denseNum):
        denseMean=Means[0]
        del Means[0]
        print(f"dense中心是：{denseMean/24.0/30}")
        # for j in range(50):
        #     value=getNumberInNormalDistribution(denseMean,80)
        #     if value  not in arr:
        #         arr.append(value)
        #     # arr.append(value)
        for j in range(61):
            value=denseMean-90+j*3
            if value not in arr:
                arr.append(value)
    
    for i in range(emptyNum):
        temp=arr
        emptyMean=Means[0]
        del Means[0]
        print(f"empty中心是：{emptyMean/24.0/30}")
        arr=[x for x in temp if x < emptyMean-120 or x > emptyMean+120]
        num=len(temp)-len(arr)
        step=480//num
        idx=emptyMean//720*720
        for i in range(num):
            if idx+(i+1)*step<emptyMean-120:
                value=idx+(i+1)*step
                if value not in arr:
                    arr.append(value)
            else:
                now=1
                value=emptyMean+120+now*step
                now+=1
                if value not in arr:
                    arr.append(value)        



    
    # 去除超出范围的值+排序
    temp_arr=[x for x in arr if 0<=x<8760]
    result_list=sorted(temp_arr)

    return result_list
    
def generateDataFile(peak,denseNum,emptyNum):
    timeScale1=[]
    for i in range(52):
        timeScale1.append({
            "largeScale":i+1,
            "timeRange":(8 if i==51 else 7)*24,
            "time":[]
        })
    
    timeScale2=[]
    for i in range(24):
        timeScale2.append({
            "largeScale":i+1,
            "timeRange":daysOfHalfMonth[i]*24,
            "time":[]
        })

    timeScale3=[]
    for i in range(12):
        timeScale3.append({
            "largeScale":i+1,
            "timeRange":daysOfMonth[i]*24,
            "time":[]
        })
    
    arr=generateData(peak,denseNum,emptyNum)

    halfmonth=0
    month=0
    halfmonthTotal=0
    monthTotal=0

    for val in arr:
        day=int(val/24)

        # 周
        week=int(val/24/7)
        week = 51 if week==52 else week
        timeScale1[week]["time"].append(val-week*7*24)

        # 半月
        if day>=halfmonthTotal+daysOfHalfMonth[halfmonth]:
            halfmonthTotal+=daysOfHalfMonth[halfmonth]
            halfmonth+=1
        timeScale2[halfmonth]["time"].append(val-halfmonthTotal*24)

        # 月
        if day>=monthTotal+daysOfMonth[month]:
            monthTotal+=daysOfMonth[month]
            month+=1
        timeScale3[month]["time"].append(val-monthTotal*24)
    
    data={
        "timeScale1":timeScale1,
        "timeScale2":timeScale2,
        "timeScale3":timeScale3,
    }
    dataSet = {
        "data":data,
        "answer":{
            "month":3,#此处暂时写死，需要更改
            "week":12#同上
        },
        "peak":peak,
        "denseNum":denseNum,
        "emptyNum":emptyNum
    }

    # 将数据转换为 JSON 格式字符串
    json_data = json.dumps(dataSet, indent=4)
    
    # 拼接文件路径
    file_name = f"{peak_string[peak]}_{denseNum}_{emptyNum}.json"
    file_path = os.path.join("data", file_name)
    
    try:
        # 将 JSON 数据写入文件
        with open(file_path, "w") as file:
            file.write(json_data)
        print("文件写入成功")
    except Exception as e:
        print("写入出错了:", e)
    
    
#     # 指定要输出的文件路径
#     file_path = "data.json"

#     # 将数据写入 JSON 文件
#     with open(file_path, 'w') as json_file:
#         json.dump(data, json_file, indent=4)

# generateDataFile(1,1,1)



