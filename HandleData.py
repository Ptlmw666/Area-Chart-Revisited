#%%
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
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
    'zero_0_2_peak': initial,
    'zero_0_2_valley': initial,
    'zero_0_2_dense': initial,
    'zero_0_2_empty': initial,
    'zero_1_1_peak': initial,
    'zero_1_1_valley': initial,
    'zero_1_1_dense': initial,
    'zero_1_1_empty': initial,
    'zero_2_0_peak': initial,
    'zero_2_0_valley': initial,
    'zero_2_0_dense': initial,
    'zero_2_0_empty': initial,
    'single_0_2_peak': initial,
    'single_0_2_valley': initial,
    'single_0_2_dense': initial,
    'single_0_2_empty': initial,
    'single_1_1_peak': initial,
    'single_1_1_valley': initial,
    'single_1_1_dense': initial,
    'single_1_1_empty': initial,
    'single_2_0_peak': initial,
    'single_2_0_valley': initial,
    'single_2_0_dense': initial,
    'single_2_0_empty': initial,
    'double_0_2_peak': initial,
    'double_0_2_valley': initial,
    'double_0_2_dense': initial,
    'double_0_2_empty': initial,
    'double_1_1_peak': initial,
    'double_1_1_valley': initial,
    'double_1_1_dense': initial,
    'double_1_1_empty': initial,
    'double_2_0_peak': initial,
    'double_2_0_valley': initial,
    'double_2_0_dense': initial,
    'double_2_0_empty': initial
}
question_type=["peak","valley","dense","empty"]
data_type=["zero_0_2","zero_1_1","zero_2_0","single_0_2","single_1_1","single_2_0","double_0_2","double_1_1","double_2_0"]
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

#%%
# # 查询数据
# def fetch_data():
#     global Error_Rate,Complete_Time,chart_name
#     session = SessionLocal()
#     try:
#         for i in range(3):
#             # 查询满足条件的Answer，并加载相关联的Problem
#             results = session.query(Answer).join(Problem).filter(Answer.chart_type == i).all()

#             # 处理查询结果
#             for answer in results:
#                 problem = session.query(Problem).filter(Problem.id == answer.problem_id).one()
#                 id = problem.problem_id + '_' + str(problem.question_id)
#                 if answer.answerIdx != get_answer_idx(id):
#                     Error_Rate.at[chart_name[i],id]+=1
#                 Complete_Time.at[chart_name[i],id]+=answer.spend_time/1000
        
#         TotalNum = session.query(Experiment).count()
#         Error_Rate = Error_Rate / TotalNum
#         Complete_Time = Complete_Time / TotalNum       

#         with pd.ExcelWriter('output.xlsx') as writer:
#             Error_Rate.to_excel(writer, sheet_name='Error_Rate', index=True)
#             Complete_Time.to_excel(writer, sheet_name='Complete_Time', index=True)    
#     finally:
#         # 关闭会话
#         session.close()

# # 调用函数查询数据
# fetch_data()

#%%
def getOriginData(chart_type: int):
    session = SessionLocal()
    try:
        Total_Error = []
        Total_Complete = []
        for j in range(9):
            results = session.query(Answer).join(Problem).filter(Answer.chart_type == chart_type, Problem.problem_id == data_type[j]).all()

            error_data= [[], [], [], []]
            complete_data= [[], [], [], []]           
            # peak,valley,dense,empty=[],[],[],[]
            for answer in results:
                problem = session.query(Problem).filter(Problem.id == answer.problem_id).one()
                id = problem.problem_id + '_' + str(problem.question_id)
                if answer.answerIdx != get_answer_idx(id):
                    error_data[problem.question_id].append(1)
                else:
                    error_data[problem.question_id].append(0)
                    complete_data[problem.question_id].append(answer.spend_time/1000)               
            Total_Error.extend(error_data)
            Total_Complete.extend(complete_data)
    finally:
        session.close()

    return Total_Error, Total_Complete

#%%
# #输出excel表
# def out_excel():
#     columns = [f'col_{i}' for i in range(1, 5)]  # 生成72列的列名
#     # 创建一个空的 DataFrame
#     error_df = pd.DataFrame(columns=columns, index=chart_name)
#     complete_df = pd.DataFrame(columns=columns, index=chart_name)

#     for i in range(3):
#             Total_Error, Total_Complete=getOriginData(i)
#             grouped_Error,grouped_Complete = [],[]
#             # grouped_Error = [Total_Error[i] + Total_Error[i+1] for i in range(0, len(Total_Error), 2)]
#             # grouped_Complete = [Total_Complete[i] + Total_Complete[i+1] for i in range(0, len(Total_Complete), 2)]
#             A, B, C, D = [], [], [], []
#             for j in range(0, len(Total_Error) // 2, 2):
#                 A.extend(itertools.chain(Total_Error[j*2], Total_Error[j*2 + 1]))
#                 B.extend(itertools.chain(Total_Error[(j+1)*2], Total_Error[(j+1)*2 + 1]))
#                 C.extend(itertools.chain(Total_Complete[j*2], Total_Complete[j*2 + 1]))
#                 D.extend(itertools.chain(Total_Complete[(j+1)*2], Total_Complete[(j+1)*2 + 1]))            
#             grouped_Error.extend([A,B])
#             grouped_Complete.extend([C,D])

#             idx, idx1, idx2 = 0, 0, 0
#             means = [np.mean(group) for group in grouped_Error]
#             std_devs = [np.std(group) for group in grouped_Error]
#             row=error_df.loc[chart_name[i]]
#             for col in error_df.columns:
#                 if idx%2==0:
#                     row[col]=means[idx1]
#                     idx1+=1
#                 else:
#                     row[col]=std_devs[idx2]
#                     idx2+=1
#                 idx+=1
#             error_df.loc[chart_name[i]] = row   

#             idx, idx1, idx2 = 0, 0, 0
#             means = [np.mean(group) for group in grouped_Complete]
#             std_devs = [np.std(group) for group in grouped_Complete]
#             row=complete_df.loc[chart_name[i]]
#             for col in complete_df.columns:
#                 if idx%2==0:
#                     row[col]=means[idx1]
#                     idx1+=1
#                 else:
#                     row[col]=std_devs[idx2]
#                     idx2+=1
#                 idx+=1
#             complete_df.loc[chart_name[i]] = row 
    
#     with pd.ExcelWriter('output.xlsx') as writer:
#         error_df.to_excel(writer, sheet_name='Error_Rate', index=True)
#         complete_df.to_excel(writer, sheet_name='Complete_Time', index=True)  

# out_excel()




# %%
# # 绘制每个图表的Error图和Complete图（误差棒图）
# png_ErrorIdx=0
# png_CompleteIdx=0
# Group_Type=["Error Rate","Complete Time"]
# def drawData(Group,group_type,chart_name):
#     # Total_Error, Total_Complete = getErrorData(0)
#     # print(Total_Complete)
#     means = [np.mean(group) if len(group) > 0 else -1 for group in Group]
#     std_devs = [np.std(group) if len(group) > 0 else -1 for group in Group]

#     # x 轴的位置
#     group_size = 4
#     num_groups = 9
#     spacing = 4
#     x_pos = []
            
#     for i in range(num_groups):
#         start = i * (group_size + spacing)
#         x_pos.extend([start + j for j in range(group_size)])

#     # 标签和颜色列表
#     labels = ["peak", "valley", "dense", "empty"]
#     colors = ["red", "purple", "green", "blue"]

#     # 创建图形，设置大小为12英寸宽，6英寸高
#     fig, ax = plt.subplots(figsize=(16, 4))

#     # 绘制误差棒图
#     flag=[0,0,0,0]
#     for i in range(len(means)):
#         label_index = i % group_size  # 获取标签索引
#         if means[i]!=-1:
#             ax.errorbar(x_pos[i], means[i], yerr=std_devs[i], fmt='o', 
#                         ecolor=colors[label_index], capsize=5, 
#                         label=labels[label_index] if flag[label_index]==0 else "",
#                         markerfacecolor=colors[label_index], markeredgecolor=colors[label_index])
#             flag[label_index]=1     
            

#     # 添加透明点确保图例包含所有标签
#     for label_index in range(len(labels)):
#         ax.errorbar([], [], yerr=[], fmt='o', 
#                     ecolor=colors[label_index], capsize=5, 
#                     label=labels[label_index],
#                     markerfacecolor=colors[label_index], markeredgecolor=colors[label_index], alpha=0)
                
#     # 只添加一次图例
#     handles, _ = ax.get_legend_handles_labels()
#     by_label = dict(zip(labels, handles))
#     ax.legend(by_label.values(), by_label.keys())

#     # 添加标题和标签
#     ax.set_title(chart_name)
#     ax.set_xticks([x + 1.5 for x in range(0, num_groups * (group_size + spacing), group_size + spacing)])
#     ax.set_xticklabels([data_type[i] for i in range(num_groups)])
#     # ax.set_xlabel('Data_Type')
#     ax.set_ylabel(Group_Type[group_type])

#     # 显示图形
#     plt.tight_layout()
#     plt.show()
#     if group_type==0:
#         png_ErrorIdx+=1
#         plt.savefig(f'./Result/lab1/png/A-Error-{png_ErrorIdx}.png', format='png')
#     else:
#         png_CompleteIdx+=1
#         plt.savefig(f'./Result/lab1/png/A-Complete-{png_CompleteIdx}.png', format='png')

    


# def drawAll():
#     for i in range(3):
#         Total_Error, Total_Complete = getOriginData(i)
#         drawData(Total_Error,0,chart_name[i])
#         drawData(Total_Complete,1,chart_name[i])

# drawAll()

#%%
# 绘制误差棒图
# png_ErrorIdx=0
# png_CompleteIdx=0
# Group_Type=["Error Rate","Complete Time"]
# def drawData(Group,group_type,chart_name):
#     means = [np.mean(group) if len(group) > 0 else -1 for group in Group]
#     std_devs = [np.std(group) if len(group) > 0 else -1 for group in Group]

#     # x 轴的位置
#     group_size = 2
#     num_groups = 9
#     spacing = 4
#     x_pos = []
            
#     for i in range(num_groups):
#         start = i * (group_size + spacing)
#         x_pos.extend([start + j for j in range(group_size)])

#     # 标签和颜色列表
#     labels = ["peak + valley", "dense + empty"]
#     colors = ["red","blue"]

#     # 创建图形，设置大小为12英寸宽，6英寸高
#     fig, ax = plt.subplots(figsize=(16, 4))

#     # 绘制误差棒图
#     flag=[0,0]
#     for i in range(len(means)):
#         label_index = i % group_size  # 获取标签索引
#         if means[i]!=-1:
#             ax.errorbar(x_pos[i], means[i], yerr=std_devs[i], fmt='o', 
#                         ecolor=colors[label_index], capsize=5, 
#                         label=labels[label_index] if flag[label_index]==0 else "",
#                         markerfacecolor=colors[label_index], markeredgecolor=colors[label_index])
#             flag[label_index]=1    

#     # 添加透明点确保图例包含所有标签
#     for label_index in range(len(labels)):
#         ax.errorbar([], [], yerr=[], fmt='o', 
#                     ecolor=colors[label_index], capsize=5, 
#                     label=labels[label_index],
#                     markerfacecolor=colors[label_index], markeredgecolor=colors[label_index], alpha=0)
        
#     # 只添加一次图例
#     handles, _ = ax.get_legend_handles_labels()
#     by_label = dict(zip(labels, handles))
#     ax.legend(by_label.values(), by_label.keys())

#     # 添加标题和标签
#     ax.set_title(chart_name)
#     ax.set_xticks([x + 0.5 for x in range(0, num_groups * (group_size + spacing), group_size + spacing)])
#     ax.set_xticklabels([data_type[i] for i in range(num_groups)])
#     # ax.set_xlabel('Data_Type')
#     ax.set_ylabel(Group_Type[group_type])

#     # 显示图形
#     plt.tight_layout()
#     plt.show()
    # if group_type==0:
    #     png_ErrorIdx+=1
    #     plt.savefig(f'./Result/lab1/png/B-Error-{png_ErrorIdx}.png', format='png')
    # else:
    #     png_CompleteIdx+=1
    #     plt.savefig(f'./Result/lab1/png/B-Complete-{png_CompleteIdx}.png', format='png')


# def drawAll():
#     for i in range(3):
#         Total_Error, Total_Complete = getOriginData(i)
#         grouped_Error,grouped_Complete = [],[]
#         grouped_Error = [Total_Error[i] + Total_Error[i+1] for i in range(0, len(Total_Error), 2)]
#         grouped_Complete = [Total_Complete[i] + Total_Complete[i+1] for i in range(0, len(Total_Complete), 2)]
                
#         drawData(grouped_Error,0,chart_name[i])
#         drawData(grouped_Complete,1,chart_name[i])

# drawAll()

#%%

# Group_Type=["Error Rate","Complete Time"]
# def drawData(Group,group_type):
#     means = [np.mean(group) if len(group) > 0 else -1 for group in Group]
#     std_devs = [np.std(group) if len(group) > 0 else -1 for group in Group]

#     # x 轴的位置
#     group_size = 2
#     num_groups = 3
#     spacing = 2
#     x_pos = []
            
#     for i in range(num_groups):
#         start = i * (group_size + spacing)
#         x_pos.extend([start + j for j in range(group_size)])

#     # 标签和颜色列表
#     labels = ["peak + valley", "dense + empty"]
#     colors = ["red","blue"]

#     # 创建图形，设置大小为12英寸宽，6英寸高
#     fig, ax = plt.subplots(figsize=(8, 4))

#     # 绘制误差棒图
#     flag=[0,0]
#     for i in range(len(means)):
#         label_index = i % group_size  # 获取标签索引
#         if means[i]!=-1:
#             ax.errorbar(x_pos[i], means[i], yerr=std_devs[i], fmt='o', 
#                         ecolor=colors[label_index], capsize=5, 
#                         label=labels[label_index] if flag[label_index]==0 else "",
#                         markerfacecolor=colors[label_index], markeredgecolor=colors[label_index])
#             flag[label_index]=1    

#     # 添加透明点确保图例包含所有标签
#     for label_index in range(len(labels)):
#         ax.errorbar([], [], yerr=[], fmt='o', 
#                     ecolor=colors[label_index], capsize=5, 
#                     label=labels[label_index],
#                     markerfacecolor=colors[label_index], markeredgecolor=colors[label_index], alpha=0)
                
#     # 只添加一次图例
#     handles, _ = ax.get_legend_handles_labels()
#     by_label = dict(zip(labels, handles))
#     ax.legend(by_label.values(), by_label.keys())

#     # 添加标题和标签
#     ax.set_title("three chart compare")
#     ax.set_xticks([x + 0.5 for x in range(0, num_groups * (group_size + spacing), group_size + spacing)])
#     ax.set_xticklabels([chart_name[i] for i in range(num_groups)])
#     # ax.set_xlabel('Data_Type')
#     ax.set_ylabel(Group_Type[group_type])

#     # 显示图形
#     plt.tight_layout()
#     plt.show()
#     if group_type==0:
#         png_ErrorIdx+=1
#         plt.savefig(f'./Result/lab1/png/C-Error.png', format='png')
#     else:
#         png_CompleteIdx+=1
#         plt.savefig(f'./Result/lab1/png/C-Complete.png', format='png')


# def drawAll():
#     Total_Error, Total_Complete = [], []
#     for i in range(3):
#         Error, Complete = getOriginData(i)

#         A, B, C, D = [], [], [], []
#         for i in range(0, len(Error) // 2, 2):
#             A.extend(itertools.chain(Error[i*2], Error[i*2 + 1]))
#             B.extend(itertools.chain(Error[(i+1)*2], Error[(i+1)*2 + 1]))
#             C.extend(itertools.chain(Complete[i*2], Complete[i*2 + 1]))
#             D.extend(itertools.chain(Complete[(i+1)*2], Complete[(i+1)*2 + 1]))            
#         Total_Error.extend([A,B])
#         Total_Complete.extend([C,D])
    
#     drawData(Total_Error,0)
#     drawData(Total_Complete,1)


# drawAll()