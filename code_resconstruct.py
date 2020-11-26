#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：code_reverse
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/11/20 10:29
@Desc   ：代码重构
=================================================='''


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
        return (input[0] >> 1) | (input[0] << 7) & 0xff

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


INS_FUNC = insFunc()
INS_FUNC_MAPS = {'mov': insFunc.mov, 'anl': insFunc.anl, 'orl': insFunc.orl, 'xrl': insFunc.xrl,
                 'mul': insFunc.mul, 'div': insFunc.div, 'inc': insFunc.inc, 'rl': insFunc.rl}


class node:
    name = ''
    input_len = -1
    ins_len = -1
    input = []
    output = []

    def __init__(self, name, input_len, ins_len):
        self.name = name
        self.input_len = input_len
        self.ins_len = ins_len

    def set_input(self, input):
        for i in range(self.input_len):
            self.input.append(input[i])

    def get_output(self):
        if len(self.input) == self.input_len:
            ins_fun = INS_FUNC_MAPS[self.name]
            res = ins_fun(self.input)
        else:
            print("input not enough")
            res = None
        return res


if __name__ == '__main__':
    # print(INS_FUNC.div([0xf2, 0x43]))
    ins_f = INS_FUNC_MAPS['rl']
    print(ins_f([0x11]))
    #
    # ins_list=[]
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("rl",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("rl",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,2))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,2))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("anl",2,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("anl",2,1))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("anl",2,1))
    # ins_list.append(node("mov",1,2))
    # ins_list.append(node("div",2,4))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("anl",2,1))
    # ins_list.append(node("mov",1,2))
    # ins_list.append(node("mul",2,4))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("anl",2,1))
    # ins_list.append(node("mov",1,2))
    # ins_list.append(node("div",2,4))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("anl",2,1))
    # ins_list.append(node("mov",1,2))
    # ins_list.append(node("mul",2,4))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("orl",2,1))
    # ins_list.append(node("xrl",2,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("orl",2,1))
    # ins_list.append(node("xrl",2,1))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("xrl",2,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("xrl",2,1))
    # ins_list.append(node("mov",1,1))
    #
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("xrl",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("mov",1,1))
    # ins_list.append(node("xrl",1,1))
    # ins_list.append(node("mov",1,1))
