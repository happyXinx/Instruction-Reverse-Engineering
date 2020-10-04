#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：trs_util
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/3 14:56
@Desc   ：.trs文件读取工具类
=================================================='''
import trsfile
import numpy as np
import traceback

import matplotlib.pyplot as plt

class TrsUtil:
    @staticmethod
    def get_trs_info(traces_path):
        '''
        获取.trs文件基本信息
        :return 波形条数，波形点数
        '''
        with trsfile.open(traces_path,'r') as traces:
            values=list(traces.get_headers().values())
            number_traces=values[0]  #traces.get_headers()['<Header.NUMBER_TRACES: 65>']
            number_samples=values[1]  #traces.get_headers()['<Header.NUMBER_SAMPLES: 66>']
            info="traces number is {}, samples number is {}.".format(number_traces, number_samples)
            return info

    @staticmethod
    def read_trs(traces_path):
        '''
        获取.trs文件的波形数据，以矩阵的形式返回
        波形条数为N，波形点数为L
        @:return L*N的矩阵，即矩阵的每一列代表一条波形
        '''
        try:
            with trsfile.open(traces_path,'r') as traces:
                values = list(traces.get_headers().values())
                N = values[0]
                L = values[1]
                matrix=np.zeros((L,N))
                for i in range(N):
                    matrix[:,i]=traces[i].samples
                return matrix
        except:
            print(traceback.format_exc())

    @staticmethod
    def split_matrix(matrix, ins_points):
        '''

        :param matrix:
        :param ins_points:
        :return:
        '''
        matrixs=[]
        for i in range(len(ins_points)-1):
            matrixs.append(matrix[ins_points[i]:ins_points[i+1],:])
        return matrixs

if __name__ == '__main__':
    # print(TrsUtil.get_trs_info("traces/Oscilloscope4.trs"))
    matrix=TrsUtil.read_trs("traces/Oscilloscope4.trs")
    matrixs=TrsUtil.split_matrix(matrix,[250,1250,2250,2750])
    for matrix in matrixs:
        print(matrix.shape)
