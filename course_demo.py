#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：course_demo
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/17 23:47
@Desc   ：
=================================================='''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def plot_3D(data, label):

    red_x, red_y, red_z = [], [], []
    blue_x, blue_y, blue_z = [], [], []
    green_x, green_y, green_z = [], [], []

    for i in range(len(data)):
        if label[i] == 0:
            red_x.append(data[i][1])
            red_y.append(data[i][2])
            red_z.append(data[i][0])
        elif label[i] == 1:
            blue_x.append(data[i][1])
            blue_y.append(data[i][2])
            blue_z.append(data[i][0])
        else:
            green_x.append(data[i][1])
            green_y.append(data[i][2])
            green_z.append(data[i][0])

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(red_x, red_y, red_z, c='r', marker='x')
    ax.scatter(blue_x, blue_y, blue_z, c='b', marker='*')
    ax.scatter(green_x, green_y, green_z, c='g', marker='.')

    ax.set_xlabel('数学')
    ax.set_ylabel('专业课')
    ax.set_zlabel('政治')
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 150)
    ax.set_zlim(0, 100)


def plot_2D(data, label):

    red_x, red_y= [], []
    blue_x, blue_y = [], []
    green_x, green_y = [], []

    for i in range(len(data)):
        if label[i]==0:
            red_x.append(data[i][0])
            red_y.append(data[i][1])
        elif label[i]==1:
            blue_x.append(data[i][0])
            blue_y.append(data[i][1])
        else:
            green_x.append(data[i][0])
            green_y.append(data[i][1])

    fig,ax = plt.subplots()
    ax.scatter(red_x, red_y, c='r', marker='x')
    ax.scatter(blue_x, blue_y, c='b', marker='*')
    ax.scatter(green_x, green_y, c='g', marker='.')
    # ax.set_xlim(-75, 75)
    # ax.set_ylim(-75, 75)


if __name__ == '__main__':

    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 学生成绩矩阵
    grades = np.array([
                        [63, 140, 120],
                        [62, 120, 90],
                        [56, 125, 100],

                        [57, 105, 98],
                        [54, 108, 110],
                        [58, 110, 120],
                        [60, 99, 108],
                        [50, 103, 112],

                        [52, 88, 97],
                        [53, 96, 110],
                        [51, 82, 77]
                       ]
                     )
    # 学校标签
    schools=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2]

    # 绘制原始成绩分布
    plot_3D(grades, schools)

    # pca降维
    pca = PCA(n_components=2)
    low_grades_pca = pca.fit_transform(grades)
    plot_2D(low_grades_pca, schools)

    # lda降维
    low_traces_lda = LinearDiscriminantAnalysis(n_components=2).fit_transform(grades, schools)
    plot_2D(low_traces_lda, schools)

    plt.show()
