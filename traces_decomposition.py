#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：decomposition
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/13 19:15
@Desc   ：波形降维
=================================================='''

import numpy as np
import matplotlib.pyplot as plt

from commons.trs_util import TrsUtil
from commons.plot_util import PlotUtil
from sklearn.decomposition import PCA


class Descomposition:
    '''
    X中每一行代表一条波形，每一列代表同一个Sample
    '''

    @staticmethod
    def pca_self(X, d):
        '''
        PCA降维
        :param X: 波形组成的矩阵 n*m
        :param d: 降维的维数
        :return: 降维后的矩阵
        '''
        # 1. 进行零均值化
        mean_val = np.mean(X, axis=0)
        X = X - mean_val
        # 2. 求协方差矩阵S m*m矩阵
        S = np.cov(X, rowvar=False)
        # 3. 求S的特征值和特征向量
        eig_val, eig_vec = np.linalg.eig(np.mat(S))
        # 4.  按照特征值从小到大排序
        eig_val_inx = np.argsort(eig_val)
        # 5. 选择其中最大的d个特征向量
        eig_val_top = eig_val_inx[-1:-(d + 1):-1]
        # 6. 将d个特征向量分别作为列向量组成投影矩阵 m*d矩阵
        W = eig_vec[:, eig_val_top]
        # 7. 计算降维后的数据，(n*m)矩阵乘(m*d)矩阵=(n*d)矩阵
        Y = X * W

        return Y

    @staticmethod
    def lda_self(X, l, d):
        X = np.array(X)
        l = np.array(l)
        # 1. 根据标签l对X分类
        li = set(l)
        xi = np.array([X[np.where(l == i)] for i in li])

        # 注：LDA降维最多可以类别数减一的维数
        if d >= (len(li) - 1):
            print("d_min=", len(li) - 1)
            d = len(li) - 1

        # 2. 所有波形的均值
        u = np.array([np.mean(X, axis=0)])
        # 3. 不同类别波形的均值
        ui = np.array([np.mean(xi[i], axis=0) for i in range(xi.shape[0])])
        # 4. 类内散度矩阵
        Sw = sum(np.dot((xi[i] - ui[i]).T, (xi[i] - ui[i]))
                 for i in range(len(li)))
        # 5. 类间散度矩阵
        Sb = sum(len(xi[i]) * (ui[i].T - u).T * (ui[i].T - u)
                 for i in range(len(li)))

        S = np.linalg.inv(Sw).dot(Sb)
        # 6. 将S最大d个特征值对应的特值向量组成投影矩阵
        eig_val, eig_vec = np.linalg.eig(S)
        eig_val_inx = np.argsort(eig_val)
        eig_val_top = eig_val_inx[-1:-(d + 1):-1]
        W = eig_vec[:, eig_val_top]

        # 7. 投影
        Y = np.dot(X, W)
        return Y

    @staticmethod
    def pca(traces, low):
        pca = PCA(n_components=low)
        pca.fit(traces)
        low_data = pca.transform(traces)
        return low_data


if __name__ == '__main__':
    #
    # traces=TrsUtil.read_trs("traces/single_machine_cycle_instruction_1000_1.9Mlowpass.trs")
    # split=[250, 750, 1250, 1750, 2250, 2750, 3250, 3750, 4250, 4750,
    #        5250, 5750, 6250, 6750, 7250, 7750, 8250, 8750, 9250,
    #        9750, 10250]
    # matrixs=TrsUtil.split_matrix(traces, split)
    #

    # 读波形
    matrix = TrsUtil.read_trs("traces/single_machine_cycle_instruction_1000_1.9Mlowpass.trs")
    split = [250, 750, 1250, 1750, 2250, 2750]
    traces, labels = TrsUtil.append_matrix(matrix[:100], split)

    # PCA降维
    low_traces_pca = Descomposition.pca_self(traces, 3)
    # pca = PCA(n_components=3)
    # low_traces_pca = pca.fit_transform(traces)
    PlotUtil.show3(low_traces_pca)

    # LDA降维
    low_traces_lda = Descomposition.lda_self(traces, labels, 3)
    # low_traces_lda = LinearDiscriminantAnalysis(n_components=3).fit_transform(traces, labels)
    PlotUtil.show3(low_traces_lda)
    plt.show()
