#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：instruction_operand_reverse
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/11/20 10:29
@Desc   ：指令操作数恢复
=================================================='''
import numpy as np
import matplotlib.pyplot as plt
from commons.trs_util import TrsUtil
from operand_reverse_test import *


class simonFunc:
    @staticmethod
    def S_1(b1, b2):
        '''2字节整体循环左移1位，返回循环左移1位后的两个字节'''
        r1 = ((b1 << 1) & 0xff) | ((b2 & 0x80) >> 7)
        r2 = ((b2 << 1) & 0xff) | ((b1 & 0x80) >> 7)
        return r1, r2

    @staticmethod
    def swap_anl(b1, b2):
        '''循环左移八位加与操作'''
        r1, r2 = simonFunc.S_1(b1, b2)
        return r1 & b2, r2 & b1


class insFunc:
    @staticmethod
    def mov(input):
        return input[0]

    @staticmethod
    def anl(input):
        return input[0] & input[1]

    @staticmethod
    def orl(input):
        return input[0] | input[1]

    @staticmethod
    def xrl(input):
        return input[0] ^ input[1]

    @staticmethod
    def inc(input):
        return (input[0] + 1) % 0xff

    @staticmethod
    def rl(input):
        '''rl循环左移1比特'''
        return ((input[0] << 1) | (input[0] >> 7)) & 0xff

    @staticmethod
    def mul(input):
        res = input[0] * input[1]
        nums = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
        for i in range(len(nums) - 1, -1, -1):
            if res > nums[i]:
                res -= nums[i]
        return res

    @staticmethod
    def div(input):
        return input[0] // input[1]


class node:
    index = -1   # 指令的编号，按照指令在波形上从前往后的顺序
    name = ''     # 指令的操作码名字
    input_number = -1 # 指令输入数据的个数
    cycle_number = -1  #指令的机器周期个数
    first = None  # 用于保存单输入操作码的操作数，以及双输入操作码的非A操作数，可能存在多个，则都加入到集合中
    second = None  # 用于保存双输入操作码的A操作数
    output = None  # 指令的输出操作数
    trace = None   # 此指令对应的波形

    def __init__(self, name, input_number, cycle_number, index):
        '''初始化指令节点：指令名字，指令输入数据的个数，指令周期长度，指令的索引'''
        self.index = index
        self.name = name
        self.input_number = input_number
        self.cycle_number = cycle_number

    def set_name(self, name):
        self.name = name

    def set_trace(self, trace):
        self.trace = trace

    def set_first(self, input):
        if self.first is None:
            self.first = set()
            self.first.add(input)
        else:
            if self.index > DATA_SET_INDEX[input]:  # 操作数的计算位置须在指令操作码之前才能加入
                self.first.add(input)

    def add_first(self, input):
        if self.first is None:
            self.first = set()
            self.first.add(input)
        else:
            self.first.add(input)

    def set_second(self, input):
        self.second = input

    def corr_first(self, input):
        self.first = [input]

    def corr_second(self, input):
        self.second = [input]

    def corr_name(self, name):
        self.name = name

    def get_output(self):
        return self.output

    def calc_correlation(self, data):
        '''计算数据的汉明重量与波形的相关系数'''
        trace = self.trace
        trace = trace.T
        corr = []
        hws = get_hamming_weights(data)
        for i in range(len(trace)):
            corr.append(np.corrcoef(hws, trace[i])[0, 1])
        return corr

    def calc_id_correlation(self, data):
        '''计算数据的值与波形的相关系数'''
        trace = self.trace
        trace = trace.T
        corr = []
        for i in range(len(trace)):
            corr.append(np.corrcoef(data, trace[i])[0, 1])
        return corr

    def set_output(self, output):
        self.output = output

    def print_node(self):
        '''输出此节点的信息'''
        print(
            "instruction information: name: {}, input number: {}, cycle number: {}, ins frist: {}, ins second:{}, ins output: {}, ins index: {}".format(
                self.name, self.input_number, self.cycle_number, self.first, self.second, self.output, self.index
            ))


INS_FUNC = insFunc()
# 保存指令的名字对应的指令函数映射
INS_FUNC_MAPS = {'mov_a_dir': insFunc.mov, 'mov_dir_a': insFunc.mov, 'mov_dir_c': insFunc.mov
    , 'mov_c_dir': insFunc.mov, 'anl': insFunc.anl, 'orl': insFunc.orl,
                 'xrl': insFunc.xrl, 'anl_data': insFunc.anl,
                 'mul': insFunc.mul, 'div': insFunc.div, 'inc': insFunc.inc, 'rl': insFunc.rl,
                 "mov_b_data": insFunc.mov}
# 保存操作数的计算指令索引
DATA_SET_INDEX = {}


def get_max_abs(corr, intervals):
    '''获取数据某区间最大的绝对值'''
    ans = 0
    for i in range(intervals[0], intervals[1]):
        if abs(corr[i]) > ans:
            ans = abs(corr[i])
    return ans


def check_correlation(corr, threshold):
    '''检测此相关系数是否有泄露'''
    for i in range(400, 450):
        if abs(corr[i]) > threshold:
            return True
    return False


def set_output_rl(data_set, ins: node):
    '''设置rl的输出'''
    if ins.first and ins.input_number == len(ins.first):
        ins_fun = INS_FUNC_MAPS[ins.name]
        new_data = []
        data_name = ""
        for d in iter(ins.first):
            data_name = d
        data = data_set[data_name]
        for i in range(len(data)):
            new_data.append(ins_fun([data[i]]))
        new_name = data_name + "__" + ins.name
        ins.set_output([new_name])
        data_set[new_name] = new_data
        DATA_SET_INDEX[new_name] = ins.index


def set_output_anlxrlorl(data_set, ins_list, index):
    '''设置与或非指令的输出'''
    ins = ins_list[index]
    if ins.second:
        max_A_name = ""
        max_O_name = ""
        max_new_data = []
        max_ins_name = ""
        max_hd_corr = 0

        if ins.first == None:
            '''由于操作数数据原因导致找不到数据的泄露，则需要降低阈值'''
            for data_name in iter(data_set):
                corr = ins.calc_correlation(data_set[data_name])
                if min(corr[400:500]) < -0.75:
                    ins.set_first(data_name)

        mov_a_dir_ins = None
        if ins.second == None:
            # 降低阈值向前找mov_a_dir
            for i in range(index - 1, -1, 0):
                if ins_list[i].name == "mov_a_dir":
                    mov_a_dir_ins = ins_list[i]
                    break
            for data_name in iter(data_set):
                corr = ins.calc_correlation(data_set[data_name])
                if min(corr[400:500]) < -0.75:
                    mov_a_dir_ins.set_frist(data_name)
            ins.set_second = mov_a_dir_ins.first

        if len(ins.first) == 2:
            '''通过计算操作数的数值与波形的相关系数来筛选候选值'''
            temps = 0
            data_name = ""
            for name in iter(ins.first):
                data = data_set[name]
                corr = ins.calc_id_correlation(data)
                if temps < abs(corr[100]):
                    data_name = name
                    temps = abs(corr[100])
            temp_first = {data_name}
        else:
            temp_first = ins.first

        '''通过输出值与非A操作数的汉明距离来确定指令操作码'''
        for ins_name in ["anl", "orl", "xrl"]:
            ins_fun = INS_FUNC_MAPS[ins_name]
            for A_name in iter(ins.second):
                data_A = data_set[A_name]
                for O_name in iter(temp_first):
                    data_O = data_set[O_name]
                    new_data = []
                    hds = []
                    for i in range(len(data_A)):
                        new_data.append(ins_fun([data_A[i], data_O[i]]))
                    for i in range(len(data_A)):
                        hds.append(new_data[i] ^ data_O[i])
                    hd_corr = ins.calc_correlation(hds)
                    if get_max_abs(hd_corr, (450, 500)) > max_hd_corr:
                        max_hd_corr = get_max_abs(hd_corr, (450, 500))
                        max_ins_name = ins_name
                        max_A_name = A_name
                        max_O_name = O_name
                        max_new_data = new_data

        # 设置相关信息
        new_name = "_" + max_A_name + "__" + max_O_name + "__" + max_ins_name
        ins.name = max_ins_name
        ins.corr_first(max_O_name)
        ins.corr_second(max_A_name)
        ins.set_output([new_name])
        data_set[new_name] = max_new_data
        DATA_SET_INDEX[new_name] = ins.index

        # 上一条mov_a_dir的操作数输入输出也需要进行设置
        for i in range(index - 1, -1, -1):
            if ins_list[i].output:
                break
            if ins_list[i].name == "mov_a_dir":
                mov_a_dir_ins = ins_list[i]
                mov_a_dir_ins.corr_first(max_O_name)
                mov_a_dir_ins.set_output([max_O_name])
                break
        return True

    return False


def set_output_anldata(data_set, ins):
    '''设置anl_data的输出'''
    if ins.second:
        ins_fun = INS_FUNC_MAPS[ins.name]
        max_value = 0
        max_data_name = ""
        max_value_name = 0
        max_new_data = []
        max_dataO = []
        for data_name in iter(ins.second):
            dataA = data_set[data_name]
            # 非A操作数的值需要遍历256种情况
            for value in range(256):
                new_data = []
                dataO = [value] * len(dataA)
                for i in range(len(dataA)):
                    new_data.append(ins_fun([dataA[i], dataO[i]]))
                data_A_xor_new_data = []
                for i in range(len(dataO)):
                    data_A_xor_new_data.append(dataA[i] ^ new_data[i])
                corr = ins.calc_correlation(data_A_xor_new_data)
                if corr[400] >= max_value:
                    max_value = max(corr)
                    max_data_name = data_name
                    max_value_name = value
                    max_dataO = dataO
                    max_new_data = new_data
        new_name = max_data_name + "__" + hex(max_value_name) + "__" + ins.name
        ins.corr_first(hex(max_value_name))
        ins.corr_second(max_data_name)
        ins.set_output([new_name])
        data_set[hex(max_value_name)] = max_dataO
        data_set[new_name] = max_new_data
        DATA_SET_INDEX[new_name] = ins.index
        return True
    return False


def split_bits(data):
    '''分离8个比特，从高到低排列'''
    bits = []
    for i in range(7, -1, -1):
        bits.append((data & (1 << i)) >> i)
    return bits


def merge_bits(bits):
    '''合并8个比特返回值'''
    data = 0
    for i in range(7, -1, -1):
        data += (bits[7 - i] << i)
    return data


def mov_c_dir_correlation(ins_list, data_set, mov_c_dir_index):
    '''根据HD泄露穷搜求mov_c_dir, mov_dir_c的输出'''
    mov_c_dir = ins_list[mov_c_dir_index]
    mov_dir_c_index = mov_c_dir_index

    for i in range(mov_c_dir_index + 1, len(ins_list)):
        ins = ins_list[i]
        if ins.name == "mov_dir_c":
            mov_dir_c_index = i
            break
    mov_dir_c = ins_list[mov_dir_c_index]

    C_set = mov_c_dir.first
    dir_set = mov_dir_c.first
    for C in iter(C_set):
        for dir in iter(dir_set):
            C_data = data_set[C]
            dir_data = data_set[dir]
            # 遍历8个比特
            for i in range(8):
                new_dir = []
                for j in range(len(C_data)):
                    bits_c = split_bits(C_data[j])
                    bits_dir = split_bits(dir_data[j])
                    bits_dir[7] = bits_c[i]
                    new_dir.append(merge_bits(bits_dir))
                dir_hds = []
                for j in range(len(dir_data)):
                    dir_hds.append(dir_data[j] ^ new_dir[j])
                corrs = mov_dir_c.calc_correlation(dir_hds)
                if max(corrs) > 0.55:
                    data_set[dir + "mov_dir_c" + str(mov_dir_c.index)] = new_dir
                    mov_c_dir.set_output([C])
                    mov_dir_c.set_output([dir + "mov_dir_c" + str(mov_dir_c.index)])
                    mov_c_dir.corr_first(C)
                    mov_dir_c.corr_first(dir)
                    DATA_SET_INDEX[dir + "mov_dir_c" + str(mov_dir_c.index)] = mov_dir_c.index
                    return True
    return False


def code_reconstruct_main_test(traces, ins_list, plaintext, ciphertext):
    cnt = 0
    # 初始化节点的波形
    for i in range(len(ins_list)):
        ins = ins_list[i]
        ins.set_trace(
            TrsUtil.get_trace_specific_interval(traces, 250 + cnt * 500, 250 + (cnt + ins.cycle_number) * 500))
        cnt += ins.cycle_number

    # 2. 初始化指令操作数集合
    data_set = {}
    p0 = []
    p1 = []
    p2 = []
    p3 = []
    for i in range(len(plaintext)):
        p0.append(plaintext[i][0])
        p1.append(plaintext[i][1])
        p2.append(plaintext[i][2])
        p3.append(plaintext[i][3])
    data_set["p0"] = p0
    data_set["p1"] = p1
    data_set["p2"] = p2
    data_set["p3"] = p3
    DATA_SET_INDEX["p0"] = 0
    DATA_SET_INDEX["p1"] = 0
    DATA_SET_INDEX["p2"] = 0
    DATA_SET_INDEX["p3"] = 0

    origin_len = 0
    new_len = len(data_set)
    memory = set()  # 保存已经计算过的操作数和指令波形的相关系数
    # 循环直至没有新的操作数加入为止
    while new_len > origin_len:
        origin_len = new_len  # 保存原始操作数集合长度
        A = None
        # 遍历所有指令操作数
        for data_name in data_set.keys():
            data = data_set[data_name]
            # 遍历所有指令
            for i in range(len(ins_list)):
                if (data_name, i) in memory:
                    continue
                ins = ins_list[i]
                if ins.output is None:
                    corr = ins.calc_correlation(data)
                    if check_correlation(corr, 0.87):  # 若大于阈值,则将操作数加入该指令
                        ins.set_first(data_name)
                    memory.add((data_name, i))

        # 计算所有指令的输出
        for i in range(len(ins_list)):
            ins = ins_list[i]
            if ins.output:
                continue
            if A is None:
                if ins.name == 'mov_a_dir' and ins.first:
                    A = ins.first
                    if len(A) == 1:
                        for data in iter(A):
                            ins.set_output([data])
                    elif len(A) == 2:
                        data_name = ""
                        temps = 0
                        for name in iter(A):
                            data = data_set[name]
                            corr = ins.calc_id_correlation(data)
                            if temps > corr[400]:
                                data_name = name
                                temps = corr[400]
                        ins.corr_first(data_name)
                        A = {data_name}
                        ins.set_output([data_name])
                elif ins.name == "mov_c_dir":
                    mov_c_dir_correlation(ins_list, data_set, i)
                    break
            else:
                if ins.name == "rl":
                    for data in iter(A):
                        ins.set_first(data)
                        set_output_rl(data_set, ins)
                        A = {ins.get_output()[0]}
                # elif ins.name == "anl" or ins.name=="xrl" or ins.name=="orl":
                elif ins.name == "anl_orl_xrl":
                    ins.set_second(A)
                    if set_output_anlxrlorl(data_set, ins_list, i):
                        A = {ins.get_output()[0]}
                    else:
                        A = None
                elif ins.name == 'anl_data':
                    ins.set_second(A)
                    if set_output_anldata(data_set, ins):
                        A = {ins.get_output()[0]}
                    else:
                        A = None
                elif ins.name == "mov_dir_a":
                    for d in iter(A):
                        ins.set_first(d)
                        ins.set_output([d])
                    break
        print(data_set.keys())
        new_len = len(data_set)  # 保存新的操作数集合长度

    for i in range(len(ins_list)):
        print(i)
        ins_list[i].print_node()
    for name in iter(data_set):
        print(name, data_set[name])


if __name__ == '__main__':
    pass
