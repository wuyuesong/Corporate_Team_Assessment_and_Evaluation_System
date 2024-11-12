"""
@author: wuyuesong
@Remark: 计算工具类
"""
import filecmp
from scipy.stats import norm
import pandas as pd
import numpy as np
import math


# 用于计算评价任务的最终得分
def calc_score(rows, cols, mul, first_row, first_column, range_data, weight):
    # rows:行数 ，即评价人
    # cols:列数 ，即被评价人
    # mul
    # first_row:所有的被评价人
    # first_column：所有的评价人
    # range_data :scores矩阵
    # weight



    non_zero_counts_row = np.count_nonzero(range_data, axis=1)
    non_zero_counts_col = np.count_nonzero(range_data, axis=0)

    #####################################  step1  ######################################### 归一化
    transformed_data = np.zeros_like(range_data)

    for i in range(transformed_data.shape[0]):
        max_value = np.max(range_data[i])
        min_value = np.min(range_data[i][range_data[i] != 0])
        for j in range(transformed_data.shape[1]):
            if range_data[i][j] == 0:
                transformed_data[i, j] = 0
            else:
                transformed_data[i, j] = (100 - 60) / (max_value - min_value) * (range_data[i, j] - min_value) + 60

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
    absolute_differences_non_zero = np.zeros_like(transformed_data)
    for i in range(transformed_data.shape[0]):
        for j in range(transformed_data.shape[1]):
            if transformed_data[i, j] != 0:
                absolute_differences_non_zero[i, j] = np.abs(transformed_data[i, j] - non_zero_means[j])

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
            if transformed_data[i, j] == 0:
                deviation_multiple[i, j] = 0
            else:
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
                
                # abnormal_data.append({"evaluate_id": first_column[i], "evaluated_id": first_row[j],"origin_value": origin_value,"fix_value": transformed_data[i, j]})
                abnormal_data.append({"evaluate_id": first_column[i], "evaluated_id": first_row[j],"origin_value": origin_value,"fix_value": non_zero_means[j]})
    
    # with open('step5_out.txt', 'w') as file:
    #     for i in range(transformed_data.shape[0]):
    #         for j in range(transformed_data.shape[1]):
    #             file.write(str(round(transformed_data[i, j], 5)) + ' ')
    #         file.write('\n')
    
    #########################################################################################

    #######################################  step6  ######################################### 计算中位数
    medians = np.zeros(transformed_data.shape[0], dtype=float)
    for i in range(transformed_data.shape[0]):
        medians[i] = np.median(transformed_data[i][np.nonzero(transformed_data[i])])

    # with open('step6_out.txt', 'w') as file:
    #     for num in medians_np:
    #             file.write(str(round(num, 5)) + '\n')
    #########################################################################################


    #######################################  step7  ######################################### 计算中位数偏差
    average_value = np.mean(medians)
    median_bias = medians - average_value


    # with open('step7_out.txt', 'w') as file:
    #     for num in median_bias:
    #             file.write(str(round(num, 5)) + '\n')

    max_val = np.max(median_bias)
    min_val = np.min(median_bias)

    if max_val > 7.5:
        for index, value in enumerate(median_bias):
            if value > 0:
                median_bias[index] = (7.5/max_val) * value

    if min_val < -7.5:
        for index, value in enumerate(median_bias):
            if value < 0:
                median_bias[index] = (-7.5/min_val) * value
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
    transformed_data_none = np.where(transformed_data == 0, np.nan, transformed_data)


    sorted_indices_idx = np.argsort(transformed_data_none, axis=1)
    sorted_indices_rank = np.empty_like(sorted_indices_idx)

    for i in range(sorted_indices_idx.shape[0]):
        for j, index in enumerate(sorted_indices_idx[i]):
            sorted_indices_rank[i, index] = j  

    z_score = np.zeros_like(transformed_data)
    for i in range(transformed_data.shape[0]):
        for j in range(transformed_data.shape[1]):
            if(transformed_data[i, j] != 0):
                z_score[i,j] = norm.ppf(S[i] + T[i]*sorted_indices_rank[i,j], loc=mean, scale=std_dev)
            else:
                sorted_indices_rank[i][j] = -1

    # with open('step10_out.txt', 'w') as file:
    #     for i in range(z_score.shape[0]):
    #         for j in range(z_score.shape[1]):
    #             file.write(str(round(z_score[i,j], 5)) + ' ')
    #         file.write("\n")
    ##########################################################################################

    #######################################  step11  ######################################## 计算归一化数组

    for i in range(z_score.shape[0]):
        max_value = np.max(z_score[i])
        min_value = np.min(z_score[i][z_score[i] != 0])
        index = np.nonzero(z_score[i])
        z_score[i][index] = 40 / (max_value - min_value) * (z_score[i][index] - min_value) + 60

    # with open('step11_out.txt', 'w') as file:
    #     for i in range(z_score.shape[0]):
    #         for j in range(z_score.shape[1]):
    #             file.write(str(round(z_score[i,j], 5)) + ' ')
    #         file.write("\n")
    ##########################################################################################


    # 根据weight计算权重
    #######################################  step12  #########################################   最终排名
    dot_product = np.zeros_like(first_row)
    for i in range(z_score.shape[1]):

        index = np.nonzero(z_score[:,i])
        column = z_score[:, i][index]
        weight_index = weight[index]
        sum_weight = np.sum(weight_index)
        weight_index = weight_index/sum_weight

        dot_product[i] = np.dot(column, weight_index)

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

# 用于计算部门相关权重
def calc_relation(relation):
    relation = relation.astype(np.float64)
    column_sums = np.sum(relation, axis=0)
    all_sum = np.sum(column_sums)
    importance_list = column_sums/all_sum
    im_relation = np.zeros_like(relation)
    for i in range(relation.shape[0]):
        im_relation[i, :] = relation[i, :] * importance_list[i]
    relation_normal = np.zeros_like(relation)
    column_sums2 = np.sum(im_relation, axis=0)
    for i in range(im_relation.shape[1]):
        relation_normal[:, i] = 100 / column_sums2[i] * im_relation[:, i]
 
    return relation_normal