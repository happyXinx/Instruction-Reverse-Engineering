#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：template_attack
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/3 14:57
@Desc   ：指令操作码逆向方法
=================================================='''

import numpy as np
from trs_util import TrsUtil
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

class TemplateAttack:
    @staticmethod
    def get_avg(matrix):
        '''求矩阵的均值'''
        return np.mean(matrix, axis=1)  #对列求平均值

    @staticmethod
    def get_covariance(matrix):
        '''求协方差矩阵'''
        return np.cov(matrix)

    @staticmethod
    def template_construct(matrixs):
        '''
        模板构建
        :param matrixs: 不同指令的波形数据
        :return: 不同指令的模板
        '''
        templates=[]
        for matrix in matrixs:
            avg=TemplateAttack.get_avg(matrix)
            cov=TemplateAttack.get_covariance(matrix)
            templates.append((avg,cov))
        return templates

    @staticmethod
    def template_match(templates, trace):
        '''
        波形模板匹配
        :param templates: 指令模板
        :param trace: 待匹配波形
        :return: 计算出不同模板下的概率
        '''
        properties=[]
        for template in templates:
            try:
                pro=multivariate_normal.pdf(trace, mean=template[0], cov=template[1], allow_singular=True)
                properties.append(pro)
            except:
                properties.append(None)
        return properties

if __name__ == '__main__':
    #
    # matrix = TrsUtil.read_trs("traces/Oscilloscope4.trs")
    # matrixs = TrsUtil.split_matrix(matrix, [250, 1250, 2250, 2750])
    # templates = TemplateAttack.template_construct(matrixs)
    #
    # for i in range(100):
    #     print("i:",i)
    #     trace=matrixs[1][:,i]
    #     print(TemplateAttack.template_match(templates, trace))
    #

    matrix=TrsUtil.read_trs("traces/single_machine_cycle_instruction.trs")
    split=[250, 750, 1250, 1750, 2250, 2750, 3250, 3750, 4250, 4750,
           5250, 5750, 6250, 6750, 7250, 7750, 8250, 8750, 9250,
           9750, 10250]
    matrixs=TrsUtil.split_matrix(matrix,split)
    templates=TemplateAttack.template_construct(matrixs)

    for i in range(20):
        print("ins:",i)
        trace=matrixs[i][:,500]
        print(TemplateAttack.template_match(templates, trace))
