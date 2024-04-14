import filecmp
from scipy.stats import norm
import pandas as pd
import numpy as np
import math



def calc_score(rows, cols, mul, first_row, first_column, range_data, weight):

    non_zero_counts_row = np.count_nonzero(range_data, axis=1)
    non_zero_counts_col = np.count_nonzero(range_data, axis=0)

    #####################################  step1  ######################################### 归一化
    max_value = np.max(range_data)
    min_value = np.min(range_data[range_data != 0])

    transformed_data = (100 - 60) / (max_value - min_value) * (range_data - min_value) + 60

    # with open('step1_out.txt', 'w') as file:
    #     for i in range(transformed_data.shape[0]):
    #         for j in range(transformed_data.shape[1]):
    #             value = transformed_data[i, j]
    #             file.write(str(round(value, 5)) + ' ')
    #         file.write('\n')
    #######################################################################################  


    #####################################  step2  ######################################### 平均值
    # 计算每一列非零元素的和
    sum_non_zero_col = np.sum(transformed_data, axis=0)

    # 计算 non_zero_means，即每一列非零元素的和除以非空元素的个数
    # 如果除数为0，则对应值为0
    non_zero_means = np.where(non_zero_counts_col > 0, sum_non_zero_col / non_zero_counts_col, 0)
    
    # with open('step2_out.txt', 'w') as file:
    #     for num in non_zero_means:
    #             file.write(str(round(num, 5)) + ' ')
    
    #######################################################################################

    #####################################  step3  ######################################### 标准差

    # 计算每一列元素与该列非零平均值的差的绝对值
    absolute_differences_non_zero = np.where(non_zero_counts_col > 0, np.abs(transformed_data - non_zero_means), 0)

    # 只考虑非零元素的平均差
    sum_absolute_non_zero_col = np.sum(absolute_differences_non_zero, axis=0)
    mean_differences_non_zero = np.where(non_zero_counts_col > 0, sum_absolute_non_zero_col / non_zero_counts_col, 0)

    # with open('step3_out.txt', 'w') as file:
    #     for num in mean_differences_non_zero:
    #             file.write(str(round(num, 5)) + ' ') 
    #########################################################################################

    #######################################  step4  ######################################### 偏差倍数
    deviation_multiple = np.zeros_like(transformed_data)
    for i in range(transformed_data.shape[0]):
        for j in range(transformed_data.shape[1]):
            deviation_multiple[i, j] = np.abs(transformed_data[i, j] - non_zero_means[j]) / mean_differences_non_zero[j]

    # with open('step4_out.txt', 'w') as file:
    #     for i in range(deviation_multiple.shape[0]):
    #         for j in range(deviation_multiple.shape[1]):
    #             file.write(str(round(deviation_multiple[i, j], 5)) + ' ')
    #         file.write('\n')

    #########################################################################################

    #######################################  step5  ######################################### 调整异常数据并记录异常数据
    abnormal_data = []
    for i in range(transformed_data.shape[0]):
        for j in range(transformed_data.shape[1]):
            if deviation_multiple[i, j] > mul:
                origin_value = transformed_data[i, j]
                if transformed_data[i, j] > non_zero_means[j]:
                    transformed_data[i, j] = non_zero_means[j] + mul*mean_differences_non_zero[j]
                else:
                    transformed_data[i, j] = non_zero_means[j] - mul*mean_differences_non_zero[j]
                
                abnormal_data.append({"evaluate_id": first_column[i], "evaluated_id": first_row[j],"origin_value": origin_value,"fix_value": transformed_data[i, j]})
    
    # with open('step5_out.txt', 'w') as file:
    #     for i in range(transformed_data.shape[0]):
    #         for j in range(transformed_data.shape[1]):
    #             file.write(str(round(transformed_data[i, j], 5)) + ' ')
    #         file.write('\n')
    
    #########################################################################################

    #######################################  step6  ######################################### 计算中位数
    # 将numpy数组转换为pandas的DataFrame
    df = pd.DataFrame(transformed_data)

    # 计算每一行的中位数
    medians = df.median(axis=1)

    # 将结果转换回numpy数组
    medians_np = medians.to_numpy()

    # with open('step6_out.txt', 'w') as file:
    #     for num in medians_np:
    #             file.write(str(round(num, 5)) + '\n')
    #########################################################################################


    #######################################  step7  ######################################### 计算中位数偏差
    average_value = np.mean(medians_np)
    median_bias = medians_np - average_value

    # with open('step7_out.txt', 'w') as file:
    #     for num in median_bias:
    #             file.write(str(round(num, 5)) + '\n')
    #########################################################################################

    #######################################  step8  ######################################### 计算左侧偏移S
    # 设置正态分布的均值和标准差
    mean = 80
    std_dev = 15

    # 使用 norm.cdf 计算每个元素的 CDF 值
    S = norm.cdf(60-median_bias, mean, std_dev)
    # with open('step8_out.txt', 'w') as file:
    #     for num in S:
    #             file.write(str(round(num, 5)) + '\n')
    #########################################################################################

    #######################################  step9  ######################################### 计算步长
    T = (norm.cdf(100-median_bias, mean, std_dev) - S) / (non_zero_counts_row - 1)

    # with open('step9_out.txt', 'w') as file:
    #     for num in T:
    #             file.write(str(round(num, 5)) + '\n')
    #########################################################################################

    #######################################  step10  ######################################## 计算norm.inv后的值
    sorted_indices = np.argsort(transformed_data, axis=1)
    
    z_score = np.zeros_like(transformed_data)
    for i in range(transformed_data.shape[0]):
        for j in range(transformed_data.shape[1]):
            z_score[i,j] = norm.ppf(S[i] + T[i]*sorted_indices[i,j], loc=mean, scale=std_dev)

    # with open('step10_out.txt', 'w') as file:
    #     for i in range(z_score.shape[0]):
    #         for j in range(z_score.shape[1]):
    #             file.write(str(round(z_score[i,j], 5)) + ' ')
    #         file.write("\n")
    ##########################################################################################

    #######################################  step11  ######################################## 计算归一化数组
    # 计算整个数组的最大值
    overall_max = np.max(z_score)

    # 计算整个数组的最小值
    overall_min = np.min(z_score)

    for i in range(z_score.shape[0]):
        for j in range(z_score.shape[1]):
            z_score[i,j] = 40 / (overall_max - overall_min) * (z_score[i, j] - overall_min) + 60

    # with open('step11_out.txt', 'w') as file:
    #     for i in range(z_score.shape[0]):
    #         for j in range(z_score.shape[1]):
    #             file.write(str(round(z_score[i,j], 5)) + ' ')
    #         file.write("\n")
    ##########################################################################################

    #######################################  step12  #########################################   最终排名
    dot_product = np.zeros_like(first_row)
    for i in range(z_score.shape[1]):
        column = z_score[:, i]
        dot_product[i] = np.dot(column, weight/100)

    dot_product = dot_product.astype(float)
    sorted_indices = np.argsort(-dot_product)

    # with open('step12_out.txt', 'w') as file:
    #     for i in range(sorted_indices.shape[0]):
    #         file.write(str(i + 1) + " " + str(int(first_row[sorted_indices[i]])) + " " str(dot_product[i])+ '\n')
    ##########################################################################################

    #######################################  step13  #########################################  异常数据
    # with open('step13_out.txt', 'w') as file:
    #     file.write('evaluate' + ' ' + 'evaluated' + ' ' + 'origin_value' + ' ' + 'fixed_value' + '\n')
    #     for data in abnormal_data:
    #         file.write(str(data['evaluate']) + ' ' + str(data['evaluated']) + ' ' + str(data['origin_value']) + ' ' + str(data['fix_value']) + '\n')
    ##########################################################################################
    rank = []
    for i in range(sorted_indices.shape[0]):
        rank.append({"rank": i + 1, "id": first_row[sorted_indices[i]], "score": dot_product[sorted_indices[i]]})

    return rank, abnormal_data