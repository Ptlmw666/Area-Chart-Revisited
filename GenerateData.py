import random
import math
import json
import os
import numpy as np
from scipy.stats import gaussian_kde
# from math import sqrt, log, pi, cos, sin


import shortuuid
import uuid
def new_uuid(length=None):
    if length is None:
        return str(uuid.uuid1())
    else:
        return str(shortuuid.ShortUUID().random(length=length))

daysOfMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
daysOfHalfMonth = [15, 16, 14, 14, 15, 16, 15, 15, 15, 16, 15, 15, 15, 16, 15, 16, 15, 15, 15, 16, 15, 15, 15, 16]
daysOfQuarterMonth=[7,8,8,8,7,7,7,7,7,8,8,8,7,8,7,8,7,8,8,8,7,8,7,8,7,8,8,8,7,8,8,8,7,8,7,8,7,8,8,8,7,8,7,8,7,8,8,8]
peak_string = ["zero", "single", "double"]
questions = [
  'In which month does the peak occur? ',
  'In which month does the valley occur?',
  'During which periods are the observed counts dense?',
  'During which periods are few or no counts observed?'
]

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
    denseAns=[]
    emptyAns=[]
    # print(f"mean的值是：{mean}")
    # for value in mean:
    #     print(f"peak出现在第{value/24.0/30}个月")

    Means=[]
    if len(mean)==0:
        Means.append(random.randint(0,4000))
        Means.append(random.randint(4700,8760))
    elif len(mean)==1:
        Means.append(random.randint(mean[0]-800,mean[0]-400))
        Means.append(random.randint(mean[0]+400,mean[0]+800))
    else:
        randidx=random.randint(0,1)
        Means.append(random.randint(mean[randidx]-800,mean[randidx]+800))
        Means.append(random.randint(mean[1-randidx]-800,mean[1-randidx]+800))

    # if denseNum==0:
    #     idx=0
    #     for i in range(12):
    #         now=idx
    #         idx+=720+random.randint(0,1)*24
    #         temp=[x for x in arr if x>=now and x<idx]
    #         arr=[x for x in arr if x<now or x>=idx]
    #         step=(idx-now)//len(temp)
    #         for i in range(len(temp)):
    #             arr.append(now+(i+1)*step+random.randint(0,step-1))

    for i in range(denseNum):
        denseMean=Means[0]
        del Means[0]
        print(f"dense出现在第{int(denseMean/24/30+1)}个月的第{int(denseMean/24/30*4)-int(denseMean/720)*4+1}部分")
        denseAns.append(f"{int(denseMean/24/30+1)}-{int(denseMean/24/30*4)-int(denseMean/720)*4+1}")
        # for j in range(50):
        #     value=getNumberInNormalDistribution(denseMean,80)
        #     if value  not in arr:
        #         arr.append(value)
        #     # arr.append(value)
        for j in range(51):
            value=denseMean-75+j*3
            if value not in arr:
                arr.append(value)
    
    for i in range(emptyNum):
        temp=arr
        emptyMean=Means[0]
        del Means[0]
        # print(f"empty中心是：{emptyMean/24.0/30}")
        print(f"empty出现在第{int(emptyMean/24/30+1)}个月的第{int(emptyMean/24/30*4)-int(emptyMean/720)*4+1}部分")
        emptyAns.append(f"{int(emptyMean/24/30+1)}-{int(emptyMean/24/30*4)-int(emptyMean/720)*4+1}")
        arr=[x for x in temp if x < emptyMean-105 or x > emptyMean+105]
        num=(len(temp)-len(arr))
        step=510//num
        idx=emptyMean//720*720
        now=1
        for i in range(num):
            if idx+(i+1)*step<emptyMean-105:
                value=idx+(i+1)*step+random.randint(0,step)
                if value not in arr:
                    arr.append(value)
            else:
                value=emptyMean+105+now*step+random.randint(0,step)
                now+=1
                if value not in arr:
                    arr.append(value)
            
        # idx=emptyMean//720*720
        # # if emptyMean-idx<105:
        # #     emptyMean=idx+105
        # print(f"empty出现在第{int(emptyMean/24/30+1)}个月的第{int(emptyMean/24/30*4)-int(emptyMean/720)*4+1}部分")
        # arr=[x for x in temp if x < idx or x > idx+720]
        # num=len(temp)-len(arr)
        # now=1
        # step=510//num+1
        # for i in range(num):
        #     if idx+(i+1)*step<emptyMean-105:
        #         value=idx+(i+1)*step+random.randint(0,step-1)
        #         if value not in arr:
        #             arr.append(value)
        #         # arr.append(value)
        #     elif emptyMean+105+now*step<idx+720:
        #         value=emptyMean+105+now*step+random.randint(0,step-1)
        #         now+=1
        #         if value not in arr:
        #             arr.append(value)
        # # # print(list(set(arr)-set(arr1)))



    
    # 去除超出范围的值+排序
    temp_arr=[x for x in arr if 0<=x<8760]
    result_list=sorted(temp_arr)

    return result_list,mean,denseAns,emptyAns


def generateDataFile(peak,denseNum,emptyNum):
    timeScale1=[]
    for i in range(48):
        timeScale1.append({
            "largeScale":i+1,
            "timeRange":daysOfQuarterMonth[i]*24,
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
    
    arr,mean,denseAns,emptyAns=generateData(peak,denseNum,emptyNum)


    quartermonth=0
    halfmonth=0
    month=0
    quartermonthTotal=0
    halfmonthTotal=0
    monthTotal=0

    for val in arr:
        day=int(val/24)

        # 周
        if day>=quartermonthTotal+daysOfQuarterMonth[quartermonth]:
            quartermonthTotal+=daysOfQuarterMonth[quartermonth]
            quartermonth+=1
        timeScale1[quartermonth]["time"].append(val-quartermonthTotal*24)

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

    max_density=[]
    for i in range(12):
        if len(timeScale3[i]["time"])>=2:
            kde = gaussian_kde(timeScale3[i]["time"],bw_method = 24)
            temp_density = kde(np.linspace(0, timeScale3[i]["timeRange"], 2048))
            density=[x*len(timeScale3[i]["time"]) for x in temp_density]
            max_density.append({
            "max_value":np.max(density),
            "max_idx":np.argmax(density)
            })
        else:
            max_density.append({
            "max_value":0,
            "max_idx":0
            })
    max_dict = max(max_density, key=lambda x: x["max_value"])
    max_idx=max_dict["max_idx"]
    idx = max_density.index(max_dict)

    print(f"dense在{idx+1}月的{int(max_idx/2048*4)+1}部分")
    print(f"dense在{idx+1}月的{max_idx/2048*4}部分")
    
    
    # 为了找波谷，提前将每个月的总time数存储到一个数组中
    Totaltime=[]
    for i in range(12):
        Totaltime.append(len(timeScale3[i]["time"]))

    
    # peak出现的月份答案(无峰答案为-1)
    peak_months=[int(value/720+1) for value in mean]
    print(peak_months)
    peak_month=-1
    if len(mean)!=0:
        for i, month in enumerate(peak_months):
            max_len = max(len(timeScale3[month-2]["time"]), len(timeScale3[month-1]["time"]), len(timeScale3[month]["time"]))
            if max_len == len(timeScale3[month-2]["time"]):
                peak_months[i] = month - 1
            elif max_len == len(timeScale3[month-1]["time"]):
                peak_months[i] = month
            else:
                peak_months[i] = month + 1
        peak_months.sort()
        peak_month=peak_months[0]
        if len(mean)==2 and len(timeScale3[peak_months[0]-1]["time"])<len(timeScale3[peak_months[1]-1]["time"]):
            peak_month=peak_months[1]
    
    print(peak_months)
    print(Totaltime)
    # 波谷出现的月份答案（无峰跟单峰为0）
    valley_month=-1
    if len(mean)==2:
        min_value=min(Totaltime[peak_months[0]-1:peak_months[1]])
        valley_month=Totaltime.index(min_value)+1

    print(f"peak出现在第{peak_month}个月")
    print(f"valley出现在第{valley_month}个月")



    data={
        "timeScale1":timeScale1,
        "timeScale2":timeScale2,
        "timeScale3":timeScale3
    }
    
    data1={
        "timeScale1":timeScale1,
        "timeScale3":timeScale3
    }
    
    #正确答案
    questionAns=[str(peak_month),str(valley_month)]
    if denseNum==0:
        questionAns.append(f"{idx+1}-{int(max_idx/2049*4)+1}")
    elif f"{idx+1}-{int(max_idx/2049*4)+1}" in denseAns:
        questionAns.append(f"{idx+1}-{int(max_idx/2049*4)+1}")
    else:
        questionAns.append(denseAns[random.randint(0,denseNum-1)])
    if emptyNum==0:
        questionAns.append("111-111")
    else:
        questionAns.append(emptyAns[random.randint(0,emptyNum-1)])
    
    print(questionAns)
    #options包含四个问题对应的选项，每个问题的option中有六项
    options=[]
    #每个问题对应的答案的索引
    answerIdx=[]

    #前两个问题
    for i in range(2):
        option=[]
        for j in range(4):
            while True:
                random_value=random.randint(1,12)
                if str(random_value)!=questionAns[i] and str(random_value) not in option:
                    break
            option.append(str(random_value))
        option.extend(["no","not sure"])
        if int(questionAns[i])!=-1:
            option[random.randint(0,3)]=questionAns[i]
        option[:4] = sorted(option[:4], key=int)
        options.append(option)
        if int(questionAns[i])==-1:
            answerIdx.append(4)
        else:
            answerIdx.append(option.index(questionAns[i]))
    
    
    #第三个问题
    option=[]
    if denseNum!=2:
        first,last=questionAns[2].split('-')
        for j in range(4):
            while True:
                random_value1=random.randint(1,12)
                random_value2=random.randint(1,4)
                if (str(random_value1)!=first or str(random_value2)!=last) and f"{random_value1}-{random_value2}" not in option:
                    break
            option.append(f"{random_value1}-{random_value2}")
        option.extend(["no","not sure"])
        if denseNum==1:
            option[random.randint(0,3)]=questionAns[2]
    else:
        first1,last1=denseAns[0].split('-')
        first2,last2=denseAns[1].split('-')
        for j in range(4):
            while True:
                random_value1=random.randint(1,12)
                random_value2=random.randint(1,4)
                if (str(random_value1)!=first1 or str(random_value2)!=last1) and (str(random_value1)!=first2 or str(random_value2)!=last2) and f"{random_value1}-{random_value2}" not in option:
                    break
            option.append(f"{random_value1}-{random_value2}")
        option.extend(["no","not sure"])
        option[random.randint(0,3)]=questionAns[2]    
    option[:4]=sorted(option[:4], key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))
    options.append(option)
    if denseNum==0:        
        answerIdx.append(4)
    else:
        answerIdx.append(option.index(questionAns[2]))

    #第四个问题
    option=[]
    if emptyNum!=2:
        first,last=questionAns[3].split('-')
        for j in range(4):
            while True:
                random_value1=random.randint(1,12)
                random_value2=random.randint(1,4)
                if (str(random_value1)!=first or str(random_value2)!=last) and f"{random_value1}-{random_value2}" not in option:
                    break
            option.append(f"{random_value1}-{random_value2}")
        option.extend(["no","not sure"])
        if emptyNum==1:
            option[random.randint(0,3)]=questionAns[3]
    else:
        first1,last1=emptyAns[0].split('-')
        first2,last2=emptyAns[1].split('-')
        for j in range(4):
            while True:
                random_value1=random.randint(1,12)
                random_value2=random.randint(1,4)
                if (str(random_value1)!=first1 or str(random_value2)!=last1) and (str(random_value1)!=first2 or str(random_value2)!=last2) and f"{random_value1}-{random_value2}" not in option:
                    break
            option.append(f"{random_value1}-{random_value2}")
        option.extend(["no","not sure"])
        option[random.randint(0,3)]=questionAns[3]
    option[:4]=sorted(option[:4], key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))
    options.append(option)
    if emptyNum==0:        
        answerIdx.append(4)
    else:
        answerIdx.append(option.index(questionAns[3]))      


    problemId=f"{peak_string[peak]}_{denseNum}_{emptyNum}"
    originData=[]
    for i in range(4):
        originData.append({
            "data":data1,
            "Id":problemId+"_"+str(i),
            "problemId":problemId,
            "question":questions[i],
            "questionId":i,
            "options":options[i],
            # "answerIdx":answerIdx[i]
        })
    
    print(f"正确答案：{questionAns}")
    print(f"选项：{options}")
    print(f"正确索引：{answerIdx}")


    # 将数据转换为 JSON 格式字符串
    json_data = json.dumps(data, indent=4)
    
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
    

    # 将练习题以及答案记录下来
    # 将数据转换为 JSON 格式字符串
    json_originData = json.dumps(originData, indent=4)
    
    # 拼接文件路径
    file_name = f"{peak_string[peak]}_{denseNum}_{emptyNum}.json"
    file_path = os.path.join("trial_data/lab1/formal", file_name)
    
    try:
        with open(file_path, "w") as file:
            file.write(json_originData)
        print("文件写入成功")
    except Exception as e:
        print("写入出错了:", e)



    
    #存储所有试题答案
    file_name = "all_answers.json"
    file_path = os.path.join("trial_data/lab1",file_name)

    # 读取现有的 JSON 文件
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            allAns = json.load(file)
    else:
        allAns = []

    # 添加新的元素
    for i in range(4):
        allAns.append({
            "Id":problemId+"_"+str(i),
            "problemId": problemId,
            "questionId": i,
            "options":options[i],
            "answerIdx": answerIdx[i]
        })

    # 将更新后的列表写回 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(allAns, file, indent=4)

    
    # # 指定要输出的文件路径
    # file_path = "data.json"

    # # 将数据写入 JSON 文件
    # with open(file_path, 'w') as json_file:
    #     json.dump(data, json_file, indent=4)

# generateDataFile(1,1,1)

