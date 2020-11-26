#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：instruction_operand_reverse
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/3 14:58
@Desc   ：指令操作数逆向方法
=================================================='''

import numpy as np
import matplotlib.pyplot as plt
from commons.trs_util import TrsUtil


def get_hamming_weight(number):
    '''求汉明重量'''
    cnt=0
    for i in range(8):
        if (number>>i) & 1:
            cnt+=1
    return cnt

def get_plaintext_hamming_weight(plaintexts, pos):
    '''求明文列某个字节的汉明重量'''
    hws=[]
    for i in range(len(plaintexts)):
        hws.append(get_hamming_weight(plaintexts[i][pos]))
    return hws

def calc_intermediate(plaintext, ins_func):
    '''中间值计算'''
    res=[]
    for row in plaintext:
        res_row=[]
        for p in row:
            res_row.append(ins_func([p]))
        res.append(res_row)
    return res

def get_correlation(traces, plaintext, intervals, position):
    '''相关系数计算'''
    hws = get_plaintext_hamming_weight(plaintext, position)
    matrix=np.mat(traces)
    matrix=matrix.T
    corr=[]
    for i in range(intervals[0], intervals[1]):
        corr.append(np.corrcoef(hws, matrix[i,:])[0,1])
    return corr

if __name__ == '__main__':

    # mov_A_0x20
    # traces=TrsUtil.read_trs("correlation/mov_A_0x20_ran.trs")
    # plaintext, ciphertext=TrsUtil.get_trs_plaintext_ciphertext("correlation/mov_A_0x20_ran.trs", 13, 4, 17, 4)
    # corr=get_correlation(traces, plaintext, (0,1500),0)
    # plt.plot(corr)
    # plt.show()

    # inc A
    #
    # traces=TrsUtil.read_trs("correlation/inc_A.trs")
    # plaintext, ciphertext=TrsUtil.get_trs_plaintext_ciphertext("correlation/inc_A.trs", 13, 4, 17, 4)
    # print(plaintext)
    # print(ciphertext)
    #
    # plain_corr=get_correlation(traces, plaintext, (250,1750),0)
    # ciph_corr=get_correlation(traces, ciphertext, (250,1750),0)
    # plt.plot(plain_corr)
    # plt.plot(ciph_corr)
    # plt.show()

    # anl A

    # traces=TrsUtil.read_trs("correlation/anl_A.trs")
    # plaintext, ciphertext=TrsUtil.get_trs_plaintext_ciphertext("correlation/anl_A.trs", 13, 4, 17, 4)
    # print(plaintext)
    # print(ciphertext)
    #
    # plain_corr=get_correlation(traces, plaintext, (250,1750),0)
    # plain_corr_1=get_correlation(traces, plaintext, (250,1750),1)
    # ciph_corr=get_correlation(traces, ciphertext, (250,1750),0)
    # plt.plot(plain_corr, c='r')
    # plt.plot(plain_corr_1, c='b')
    # plt.plot(ciph_corr, c='y')
    # plt.show()

    # xrl A
    #
    # traces=TrsUtil.read_trs("correlation/xrl_A.trs")
    # plaintext, ciphertext=TrsUtil.get_trs_plaintext_ciphertext("correlation/xrl_A.trs", 13, 4, 17, 4)
    # print(plaintext)
    # print(ciphertext)
    #
    # plain_corr=get_correlation(traces, plaintext, (250,1750),0)
    # plain_corr_1=get_correlation(traces, plaintext, (250,1750),1)
    # ciph_corr=get_correlation(traces, ciphertext, (250,1750),0)
    # plt.plot(plain_corr, c='r')
    # plt.plot(plain_corr_1, c='b')
    # plt.plot(ciph_corr, c='y')
    # plt.show()
    #

    # mul AB
    # traces=TrsUtil.read_trs("correlation/mul_A.trs")
    # plaintext, ciphertext=TrsUtil.get_trs_plaintext_ciphertext("correlation/mul_A.trs", 13, 4, 17, 4)
    # print(plaintext)
    # print(ciphertext)
    #
    # plain_corr=get_correlation(traces, plaintext, (250,3750),0)
    # plain_corr_1=get_correlation(traces, plaintext, (250,3750),1)
    # ciph_corr=get_correlation(traces, ciphertext, (250,3750),0)
    # plt.plot(plain_corr, c='r')
    # plt.plot(plain_corr_1, c='b')
    # plt.plot(ciph_corr, c='y')
    # plt.show()

    # code reverse test
    # traces=TrsUtil.read_trs("correlation/code_reverse_test.trs")
    # plaintext, ciphertext=TrsUtil.get_trs_plaintext_ciphertext("correlation/code_reverse_test.trs", 13, 4, 17, 4)
    # print(plaintext)
    # print(ciphertext)

    # plain_corr=get_correlation(traces, calc_plaintext(plaintext, INS_FUNC_MAPS['rl']), (0,7000),0)
    # plain_corr_1=get_correlation(traces, plaintext, (250,7000),1)
    # ciph_corr=get_correlation(traces, ciphertext, (250,3750),0)
    # plt.plot(plain_corr, c='r')
    # plt.plot(plain_corr_1, c='b')
    # plt.plot(ciph_corr, c='y')
    # plt.show()

    # rl
    #
    # traces = TrsUtil.read_trs("correlation/rl_A.trs")
    # plaintext, ciphertext = TrsUtil.get_trs_plaintext_ciphertext("correlation/rl_A.trs", 13, 4, 17, 4)
    # plain_corr=get_correlation(traces, plaintext, (250, 1250),0)
    # plt.plot(plain_corr)
    # plt.show()


    # rl

    traces = TrsUtil.read_trs("traces/correlation/mov_rlA.trs")
    plaintext, ciphertext = TrsUtil.get_trs_plaintext_ciphertext("traces/correlation/mov_rlA.trs", 13, 4, 17, 4)
    # plaintext1=[[0]*4 for _ in range(1000)]

    plain_corr=get_correlation(traces, plaintext, (250, 2250),0)
    plt.plot(plain_corr)
    plt.show()
