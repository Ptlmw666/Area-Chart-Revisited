from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
import json

with open('./trial_data/lab1/all_answers.json','r') as file:
    all_answers = json.load(file)

all_answers = pd.DataFrame(all_answers)

def get_answer_idx(Id):
    # 查找匹配的行
    row = all_answers[(all_answers['Id'] == Id)]
    
    # 如果找到匹配的行，则返回 answerIdx
    if not row.empty:
        return row.iloc[0]['answerIdx']
    else:
        return None
    

#设置表格
initial=[0.0,0.0,0.0]
data = {
    'zero_0_2_0': initial,
    'zero_0_2_1': initial,
    'zero_0_2_2': initial,
    'zero_0_2_3': initial,
    'zero_1_1_0': initial,
    'zero_1_1_1': initial,
    'zero_1_1_2': initial,
    'zero_1_1_3': initial,
    'zero_2_0_0': initial,
    'zero_2_0_1': initial,
    'zero_2_0_2': initial,
    'zero_2_0_3': initial,
    'single_0_2_0': initial,
    'single_0_2_1': initial,
    'single_0_2_2': initial,
    'single_0_2_3': initial,
    'single_1_1_0': initial,
    'single_1_1_1': initial,
    'single_1_1_2': initial,
    'single_1_1_3': initial,
    'single_2_0_0': initial,
    'single_2_0_1': initial,
    'single_2_0_2': initial,
    'single_2_0_3': initial,
    'double_0_2_0': initial,
    'double_0_2_1': initial,
    'double_0_2_2': initial,
    'double_0_2_3': initial,
    'double_1_1_0': initial,
    'double_1_1_1': initial,
    'double_1_1_2': initial,
    'double_1_1_3': initial,
    'double_2_0_0': initial,
    'double_2_0_1': initial,
    'double_2_0_2': initial,
    'double_2_0_3': initial
}
chart_name=['Small-box-BarChart', 'Big-box-BarChart', 'Compressed-Small-box-BarChart']
Error_Rate = pd.DataFrame(data, index=chart_name)
Complete_Time = pd.DataFrame(data, index=chart_name)





# 数据库配置
DATABASE_URL = "mysql+pymysql://root:IamOP114514@8.134.215.31/AreaChartRevisited_lab1"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

# 定义数据库模型
class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    order = Column(String(3))
    complete_time = Column(Integer)
    time = Column(String(50))
    user_id = Column(Integer, ForeignKey('user_info.id'))

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    problem_id = Column(String(50))
    experiment_id = Column(Integer, ForeignKey('experiments.id'))

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    answerIdx = Column(Integer)
    spend_time = Column(Integer)
    chart_type = Column(Integer)
    problem_id = Column(Integer, ForeignKey('problems.id'))

class UserInfo(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    gender = Column(String(10))
    age = Column(String(3))
    major = Column(String(50))
    familiarity = Column(String(50))
    contact = Column(String(20))


# 查询数据
def fetch_data():
    global Error_Rate,Complete_Time,chart_name
    session = SessionLocal()
    try:
        for i in range(3):
            # 查询满足条件的Answer，并加载相关联的Problem
            results = session.query(Answer).join(Problem).filter(Answer.chart_type == i).all()

            # 处理查询结果
            for answer in results:
                problem = session.query(Problem).filter(Problem.id == answer.problem_id).one()
                id = problem.problem_id + '_' + str(problem.question_id)
                if answer.answerIdx != get_answer_idx(id):
                    Error_Rate.at[chart_name[i],id]+=1
                Complete_Time.at[chart_name[i],id]+=answer.spend_time/1000
        
        TotalNum = session.query(Experiment).count()
        Error_Rate = Error_Rate / TotalNum
        Complete_Time = Complete_Time / TotalNum       

        with pd.ExcelWriter('output.xlsx') as writer:
            Error_Rate.to_excel(writer, sheet_name='Error_Rate', index=True)
            Complete_Time.to_excel(writer, sheet_name='Complete_Time', index=True)    
    finally:
        # 关闭会话
        session.close()

# 调用函数查询数据
fetch_data()


