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
import pickle


class TrsUtil:
    @staticmethod
    def get_trs_info(traces_path):
        '''
        获取.trs文件基本信息
        :return 波形条数，波形点数
        '''
        with trsfile.open(traces_path, 'r') as traces:
            values = list(traces.get_headers().values())
            number_traces = values[0]  # traces.get_headers()['<Header.NUMBER_TRACES: 65>']
            number_samples = values[1]  # traces.get_headers()['<Header.NUMBER_SAMPLES: 66>']
            info = "traces number is {}, samples number is {}.".format(number_traces, number_samples)
            return info

    @staticmethod
    def read_trs(traces_path, nums=0):
        '''
        获取.trs文件的波形数据，以矩阵的形式返回
        波形条数为N，波形点数为L
        @:return N*L的矩阵，即矩阵的每一行代表一条波形
        '''
        try:
            with trsfile.open(traces_path, 'r') as traces:
                values = list(traces.get_headers().values())
                if nums == 0:
                    N = values[0]
                else:
                    N = nums
                L = values[1]
                matrix = np.zeros((N, L))
                for i in range(N):
                    matrix[i, :] = traces[i].samples
                return matrix
        except:
            print(traceback.format_exc())

    @staticmethod
    def get_trs_plaintext_ciphertext(traces_path, plaintext_pos, plaintext_len, ciphertext_pos, ciphertext_len):
        '''
        获取波形的明文密文
        :param traces_path: 波形的路径
        :param plaintext_pos: 明文的初始位置
        :param plaintext_len: 明文长度
        :param ciphertext_pos: 密文的初始位置
        :param ciphertext_len: 密文长度
        :return: 明文，密文
        '''
        try:
            with trsfile.open(traces_path, 'r') as traces:
                values = list(traces.get_headers().values())
                N = values[0]
                plaintext = []
                ciphertext = []
                for i in range(N):
                    infos = list(traces[i].data)
                    plaintext.append(infos[plaintext_pos:plaintext_pos + plaintext_len])
                    ciphertext.append(infos[ciphertext_pos:ciphertext_pos + ciphertext_len])
                return plaintext, ciphertext
        except:
            print(traceback.format_exc())

    @staticmethod
    def split_matrix(matrix, ins_points):
        '''
        :param matrix:
        :param ins_points:
        :return:
        '''
        matrixs = []
        for i in range(len(ins_points) - 1):
            matrixs.append(matrix[:, ins_points[i]:ins_points[i + 1]])
        return matrixs

    @staticmethod
    def split_by_instruction(matrix, ins_seq, per_ins=500):
        matrixs = {}
        for i in range(len(ins_seq)):
            matrixs[ins_seq[i]] = matrix[:, 250 + i * per_ins: 250 + (i + 1) * per_ins]
        return matrixs

    @staticmethod
    def traces_split_by_traces_number(matrix, ins_seq, trace_num) -> dict:
        '''把数据切分为{指令：波形数据}字典'''
        matrixs = {}
        for i in range(len(ins_seq)):
            matrixs[ins_seq[i]] = matrix[trace_num * i:trace_num * (i + 1), :]
        return matrixs

    @staticmethod
    def append_matrix(matrix, ins_points):
        '''
        拆分不同指令的波形放到一个矩阵中，
        每一行表示一条特定指令的波形，
        :param matrix:
        :param ins_points:
        :return: 波形指令矩阵，标签
        '''
        matrixs = []
        labels = []
        for i in range(len(ins_points) - 1):
            matrixs.extend(matrix[:, ins_points[i]:ins_points[i + 1]])
            labels.extend([i] * len(matrix))
        return matrixs, labels

    @staticmethod
    def save_ins_template(template, path):
        '''保存指令模板：{“指令模板名字”：[均值，斜方差矩阵]}'''
        with open('template/' + path + '.pkl', 'wb') as f:
            pickle.dump(template, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_ins_template(path):
        '''加载指令模板：{“指令模板名字”：[均值，斜方差矩阵]}'''
        with open('template/' + path + '.pkl', 'rb') as f:
            return pickle.load(f)


if __name__ == '__main__':
    # print(TrsUtil.get_trs_info("traces/Oscilloscope4.trs"))
    matrix = TrsUtil.read_trs("../traces/single_machine_cycle_instruction_1000_1.9Mlowpass.trs")
    # split = [250, 750, 1250, 1750, 2250, 2750, 3250, 3750, 4250, 4750,
    #          5250, 5750, 6250, 6750, 7250, 7750, 8250, 8750, 9250,
    #          9750, 10250]
    # matrixs=TrsUtil.split_matrix(matrix,split)
    # for matrix in matrixs:
    #     print(matrix.shape)

    split = [250, 750, 1250, 1750, 2250, 2750]
    matrixs, labels = TrsUtil.append_matrix(matrix[:100], split)
