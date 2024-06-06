from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


# # Pydantic 模型
# class AnswerModel(BaseModel):
#     answer: str
#     spendTime: int

# class ProblemModel(BaseModel):
#     questionId: int
#     problemId: str
#     answers: List[AnswerModel]

# class UserInfoModel(BaseModel):
#     name: str
#     gender: str
#     age: str
#     major: str
#     contact: str

# class DataModel(BaseModel):
#     problems: List[ProblemModel]
#     completeTime: int
#     userInfo: UserInfoModel

def saveData(data: dict,labIdx: int):
    # 数据库配置
    DATABASE_URL = f"mysql+pymysql://root:IamOP114514@8.134.215.31/AreaChartRevisited_lab{labIdx}"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    # 定义数据库模型
    class Experiment(Base):
        __tablename__ = "experiments"
        id = Column(Integer, primary_key=True, index=True)
        order = Column(String(3))
        complete_time = Column(Integer)
        #time是指现实时间 格式为年月日分秒
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
        contact = Column(String(20))

    # 创建表
    Base.metadata.create_all(bind=engine)
    # 在这里处理接收到的数据
    session = SessionLocal()
        
    # 存储用户信息
    user_info = UserInfo(
        name=data["userInfo"]["name"],
        gender=data["userInfo"]["gender"],
        age=data["userInfo"]["age"],
        major=data["userInfo"]["major"],
        contact=data["userInfo"]["contact"]
    )
    session.add(user_info)
    session.commit()
    session.refresh(user_info)

    # 存储实验信息
    experiment = Experiment(
        order=data["order"],
        complete_time=data["completeTime"],
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_id=user_info.id
    )
    session.add(experiment)
    session.commit()
    session.refresh(experiment)

    # 存储问题和答案信息
    for problem in data["problems"]:
        db_problem = Problem(
            problem_id=problem["problemId"],
            question_id=problem["questionId"],
            experiment_id=experiment.id
        )
        session.add(db_problem)
        session.commit()
        session.refresh(db_problem)
            
        for answer in problem["answers"]:
            db_answer = Answer(
                answerIdx=int(answer["answer"]),
                spend_time=answer["spendTime"],
                chart_type=answer["chart_type"],
                problem_id=db_problem.id
            )
            session.add(db_answer)
        
    session.commit()
    session.close()