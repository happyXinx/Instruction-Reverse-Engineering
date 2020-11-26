#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：leakage_analysis
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/11/26 13:51
@Desc   ：泄露分析
=================================================='''

import numpy as np
from commons.trs_util import TrsUtil
from instruction_opcode_reverse import TemplateAttack
from traces_decomposition import Descomposition


def get_means(traces, ins_count, ins_number):
    '''
    波形均值计算
    :param traces: 波形数据矩阵
    :param ins_count: 指令数量
    :param ins_number: 每个指令对应的波形数
    :return: 均值
    '''
    means = []
    for i in range(ins_count):
        means.append(np.mean(traces[i * ins_number:(i + 1) * ins_number, :], axis=0).tolist())
    return means


def sum_of_difference_of_means(means, top_k):
    '''返回均值差的和最大的前k个点'''
    # means=get_means(traces, 22, 24200)
    diff = [0] * 500
    for i in range(len(means)):
        for j in range(len(means)):
            if i == j:
                continue
            for k in range(len(diff)):
                diff[k] += abs(means[i][k] - means[j][k])
    sort_diff = []
    for i, j in enumerate(diff):
        sort_diff.append((i, j))
    sort_diff.sort(key=lambda k: -k[1])
    ans = []
    for i in range(top_k):
        ans.append(sort_diff[i][0])
    return ans


def means_variance(means, top_k):
    '''返回均值方差最大的前k个点'''
    diff = [0] * 500
    for i in range(500):
        column = []
        for j in range(22):
            column.append(means[j][i])
        diff[i] = np.std(column)

    sort_diff = []
    for i, j in enumerate(diff):
        sort_diff.append((i, j))
    sort_diff.sort(key=lambda k: -k[1])
    ans = []
    for i in range(top_k):
        ans.append(sort_diff[i][0])
    return ans


class PCA_Template:
    '''对波形进行PCA降维'''

    @staticmethod
    def pca_practice(matrix, low, ins_nums):
        '''
        对波形进行pca降维
        :param matrix: 波形矩阵
        :param low: 要降维的维数
        :param ins_nums: 波形上有几条指令
        :return:
        '''
        # 指令
        # ***|***|***
        # 转成
        # ***
        # ***
        # ***
        traces = []
        for i in range(ins_nums):
            trace = matrix[:, 250 + i * 500: 250 + (i + 1) * 500]
            traces.extend(trace)
        low_trace = Descomposition.pca(traces, low)
        return low_trace

    @staticmethod
    def construct_template_pca(traces_path, low, template_path):
        '''
        构建指令pca的模板
        :param traces_path: 波形路径
        :param low:  pca要降维的维数
        :param template_path: 保存模板路径
        :return:
        '''
        low_traces = PCA_Template.pca_practice(traces_path, low)
        ins_names = ['MOV_dir_atRi_pre', 'MOV_dir_atRi_post', 'INC', 'MOV', 'RL', 'ANL', 'ORL', 'XRL', 'MOV_B_pre',
                     'MOV_B_post',
                     'MUL_1', 'MUL_2', 'MUL_3', 'MUL_4', 'DIV_1', 'DIV_2', 'DIV_3', 'DIV_4', 'MOV_C_dir',
                     'MOV_dir_C_pre',
                     'MOV_dir_C_post']
        matrixs = TrsUtil.traces_split_by_traces_number(low_traces, ins_names, 2000)
        templates = TemplateAttack.template_construct(matrixs)
        TrsUtil.save_ins_template(templates, template_path)

    @staticmethod
    def template_match_practice(traces_path, templates, low, ins_nums, right_ans):
        '''
        pca模板匹配
        :param traces_path: 攻击波形路径
        :param low: 降维的维数
        :param templates: 模板
        :param ins_nums:
        :return:
        '''
        trans_data = PCA_Template.pca_practice(traces_path, low, ins_nums)
        for i in range(ins_nums):
            trace = trans_data[0 + i * 100]
            print(i + 1, TemplateAttack.template_match(templates, trace, right_ans[i]))
