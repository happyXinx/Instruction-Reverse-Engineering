#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plot_util
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/17 22:29
@Desc   ：绘图工具类
=================================================='''

import matplotlib.pyplot as plt
from commons.trs_util import TrsUtil


class PlotUtil:
    @staticmethod
    def show3(X):
        X = X.tolist()
        x, y, z = [], [], []
        for i in range(len(X)):
            x.append(X[i][0])
            y.append(X[i][1])
            z.append(X[i][2])
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(x, y, z, c='r', marker='x')
        # plt.show()

    @staticmethod
    def plot_mean_trace(template_name):
        template = TrsUtil.load_ins_template(template_name)
        for i in template:
            key = i
        plt.plot(template[key][0], label=key)
        # plt.show()


if __name__ == '__main__':
    # PlotUtil.plot_mean_trace("7Mall_anl")
    # PlotUtil.plot_mean_trace("7Mall_rl")
    # PlotUtil.plot_mean_trace("7Mall_mov_b_data_1")
    # PlotUtil.plot_mean_trace("7Mall_mov_b_data_2")
    # PlotUtil.plot_mean_trace("7Mall_mov_r0_dir_1")
    # PlotUtil.plot_mean_trace("7Mall_mov_r0_dir_2")
    #

    PlotUtil.plot_mean_trace("7Mall_mul_1")
    PlotUtil.plot_mean_trace("7Mall_mul_2")
    PlotUtil.plot_mean_trace("7Mall_mul_3")
    PlotUtil.plot_mean_trace("7Mall_mul_4")
    #
    PlotUtil.plot_mean_trace("7Mall_dir_1")
    PlotUtil.plot_mean_trace("7Mall_dir_2")
    PlotUtil.plot_mean_trace("7Mall_dir_3")
    PlotUtil.plot_mean_trace("7Mall_dir_4")
    plt.legend()
    plt.show()

    #
    # fig = plt.figure(figsize=(8, 6))
    # ax = plt.axes(projection='3d')
    #
    # x = np.arange(-50, 50, 0.5)  # x定义域，离散
    # y = np.arange(-50, 50, 0.5)  # y定义域，离散
    # X, Y = np.meshgrid(x, y)
    #
    # Z = X ** 2 + Y ** 2  # 需要换图形就改这里
    # plt.title('Z=X**2+Y**2')  # 添加标题
    #
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
    # plt.show()
    #
