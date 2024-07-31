import getOriginData as god
from sklearn.utils import resample
from scipy.stats import norm
import numpy as np

#   1:Coarse-Grained Bar Chart   2:Fine-Grained Bar Chart   0:Expanded Fine-Grained Bar Chart
chart_name=['Expanded Fine-Grained BarChart','Coarse-Grained BarChart', 'Fine-Grained BarChart']
e_4name = ["peak_e", "valley_e", "dense_e", "sparse_e"]
c_4name = ["peak_c", "valley_c", "dense_c", "sparse_c"]


def bootstrap_bca(data, alpha=0.05, n_iterations=10000):
    n = len(data)
    stat_original = np.mean(data)
    bootstrapped_stats = []

    # 引导抽样
    for _ in range(n_iterations):
        sample = resample(data)
        bootstrapped_stats.append(np.mean(sample))

    # 计算偏差校正和加速校正
    bootstrapped_stats = np.array(bootstrapped_stats)
    z0 = norm.ppf(np.mean(bootstrapped_stats < stat_original))
    jacks = np.array([np.mean(np.delete(data, i)) for i in range(n)])
    j_mean = np.mean(jacks)
    a = np.sum((j_mean - jacks) ** 3) / (6.0 * np.sum((j_mean - jacks) ** 2) ** 1.5)

    # 计算 BCa 置信区间
    lower_percentile = norm.cdf(z0 + (z0 + norm.ppf(alpha / 2)) / (1 - a * (z0 + norm.ppf(alpha / 2))))
    upper_percentile = norm.cdf(z0 + (z0 + norm.ppf(1 - alpha / 2)) / (1 - a * (z0 + norm.ppf(1 - alpha / 2))))
    lower_bound = np.percentile(bootstrapped_stats, 100 * lower_percentile)
    upper_bound = np.percentile(bootstrapped_stats, 100 * upper_percentile)
    
    return stat_original, lower_bound, upper_bound

def do_bca():
    for i in range(3):
        print(f"{chart_name[i]}:")
        Total_Error, Total_Complete = god.getOriginData(i)

        peak_e, valley_e, dense_e, sparse_e = [], [], [], []
        peak_c, valley_c, dense_c, sparse_c = [], [], [], []   
 
        for j in range(0, len(Total_Error) // 4):
            peak_e.append(Total_Error[j*4])
            valley_e.append(Total_Error[j*4+1])
            dense_e.append(Total_Error[j*4+2])
            sparse_e.append(Total_Error[j*4+3])
        e_4=[]
        e_4.extend([peak_e, valley_e, dense_e, sparse_e])

        for j in range(4):
            # 计算 95% 置信区间
            mean, lower, upper = bootstrap_bca(e_4[j])
            print(f"{e_4name[j]}的 95% 置信区间: [{lower:.4f}, {upper:.4f}],  均值 = {mean:.4f}")

        for j in range(0, len(Total_Complete) // 4):
            peak_c.extend(Total_Complete[j*4])
            valley_c.extend(Total_Complete[j*4+1])
            dense_c.extend(Total_Complete[j*4+2])
            sparse_c.extend(Total_Complete[j*4+3])
        c_4=[]
        c_4.extend([peak_c, valley_c, dense_c, sparse_c])

        for j in range(4):
            # 计算 95% 置信区间
            mean, lower, upper = bootstrap_bca(c_4[j])
            print(f"{c_4name[j]}的 95% 置信区间: [{lower:.4f}, {upper:.4f}],  均值 = {mean:.4f}")

        print("=============================================================")
        print("=============================================================")


from scipy.stats import friedmanchisquare
import scikit_posthocs as sp
def friedman_test():  
        Total_Error, Total_Complete = god.getOriginData(1)
        peak_e1, valley_e1, dense_e1, sparse_e1 = [], [], [], []
        peak_c1, valley_c1, dense_c1, sparse_c1 = [], [], [], []
        for j in range(0, len(Total_Error) // 4):
            peak_e1.append(Total_Error[j*4])
            valley_e1.append(Total_Error[j*4+1])
            dense_e1.append(Total_Error[j*4+2])
            sparse_e1.append(Total_Error[j*4+3])
        # for j in range(0, len(Total_Complete) // 4):
        #     peak_c1.extend(Total_Complete[j*4])
        #     valley_c1.extend(Total_Complete[j*4+1])
        #     dense_c1.extend(Total_Complete[j*4+2])
        #     sparse_c1.extend(Total_Complete[j*4+3])


        Total_Error, Total_Complete = god.getOriginData(2)
        peak_e2, valley_e2, dense_e2, sparse_e2 = [], [], [], []
        peak_c2, valley_c2, dense_c2, sparse_c2 = [], [], [], []   
        for j in range(0, len(Total_Error) // 4):
            peak_e2.append(Total_Error[j*4])
            valley_e2.append(Total_Error[j*4+1])
            dense_e2.append(Total_Error[j*4+2])
            sparse_e2.append(Total_Error[j*4+3])
        # for j in range(0, len(Total_Complete) // 4):
        #     peak_c2.extend(Total_Complete[j*4])
        #     valley_c2.extend(Total_Complete[j*4+1])
        #     dense_c2.extend(Total_Complete[j*4+2])
        #     sparse_c2.extend(Total_Complete[j*4+3])

        
        Total_Error, Total_Complete = god.getOriginData(0)
        peak_e3, valley_e3, dense_e3, sparse_e3 = [], [], [], []
        peak_c3, valley_c3, dense_c3, sparse_c3 = [], [], [], []   
        for j in range(0, len(Total_Error) // 4):
            peak_e3.append(Total_Error[j*4])
            valley_e3.append(Total_Error[j*4+1])
            dense_e3.append(Total_Error[j*4+2])
            sparse_e3.append(Total_Error[j*4+3])
        # for j in range(0, len(Total_Complete) // 4):
        #     peak_c3.extend(Total_Complete[j*4])
        #     valley_c3.extend(Total_Complete[j*4+1])
        #     dense_c3.extend(Total_Complete[j*4+2])
        #     sparse_c3.extend(Total_Complete[j*4+3])


# friedman开始执行
        stat_error, p_value_error = friedmanchisquare(peak_e1, peak_e2, peak_e3)
        # stat_time, p_value_time = friedmanchisquare(peak_c1, peak_c2, peak_c3)
        print("Peak-Finding:")
        print(f'Friedman test for Error Rates: stat = {stat_error}, p-value = {p_value_error}')
        # print(f'Friedman test for Completion Times: stat = {stat_time}, p-value = {p_value_time}')

        # 执行Nemenyi事后检验
        data_matrix = np.array([peak_e1, peak_e2, peak_e3]).T
        nemenyi_results = sp.posthoc_nemenyi_friedman(data_matrix)
        print("Nemenyi Results:")
        print(nemenyi_results)
        print("=============================================================")

        stat_error, p_value_error = friedmanchisquare(valley_e1, valley_e2, valley_e3)
        # stat_time, p_value_time = friedmanchisquare(valley_c1, valley_c2, valley_c3)
        print("Valley-Finding:")
        print(f'Friedman test for Error Rates: stat = {stat_error}, p-value = {p_value_error}')
        # print(f'Friedman test for Completion Times: stat = {stat_time}, p-value = {p_value_time}')

        # 执行Nemenyi事后检验
        data_matrix = np.array([valley_e1, valley_e2, valley_e3]).T
        nemenyi_results = sp.posthoc_nemenyi_friedman(data_matrix)
        print("Nemenyi Results:")
        print(nemenyi_results)
        print("=============================================================")

        stat_error, p_value_error = friedmanchisquare(dense_e1, dense_e2, dense_e3)
        # stat_time, p_value_time = friedmanchisquare(dense_c1, dense_c2, dense_c3)
        print("Dense-Finding:")
        print(f'Friedman test for Error Rates: stat = {stat_error}, p-value = {p_value_error}')
        # print(f'Friedman test for Completion Times: stat = {stat_time}, p-value = {p_value_time}')

        # 执行Nemenyi事后检验
        data_matrix = np.array([dense_e1, dense_e2, dense_e3]).T
        nemenyi_results = sp.posthoc_nemenyi_friedman(data_matrix)
        print("Nemenyi Results:")
        print(nemenyi_results)
        print("=============================================================")

        stat_error, p_value_error = friedmanchisquare(sparse_e1, sparse_e2, sparse_e3)
        # stat_time, p_value_time = friedmanchisquare(sparse_c1, sparse_c2, sparse_c3)
        print("Sparse-Finding:")
        print(f'Friedman test for Error Rates: stat = {stat_error}, p-value = {p_value_error}')
        # print(f'Friedman test for Completion Times: stat = {stat_time}, p-value = {p_value_time}')

        # 执行Nemenyi事后检验
        data_matrix = np.array([sparse_e1, sparse_e2, sparse_e3]).T
        nemenyi_results = sp.posthoc_nemenyi_friedman(data_matrix)
        print("Nemenyi Results:")
        print(nemenyi_results)

friedman_test()
        
