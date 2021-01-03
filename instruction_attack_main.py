#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：instruction_attack_main
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/11/8 10:22
@Desc   ：指令操作码逆向主函数
=================================================='''
import numpy as np
from commons.trs_util import TrsUtil
from instruction_opcode_reverse import TemplateAttack
from instruction_leakage_analysis import *
from instruction_template_construct import *
from instruction_operand_reverse import *

if __name__ == '__main__':

    # 指令操作数个数
    OPCODE_OPRAND_NUMBER = {"mov_a_dir": 1, "mov_dir_a": 1, "mov_c_dir": 1, "mov_dir_c": 1,
                            "anl": 2, "orl": 2, "xrl": 2, "anl_data": 2, "mul": 2, "div": 2,
                            "rl": 1, "mov_b_data": 1, "anl_xrl_orl": 2, "mul_div": 2, "mov_dir_c_2": 1,
                            "mov_dir_c_1": 1, "anl_orl_xrl": 2}
    # 指令操作码个数
    OPCODE_CYCYLE_NUMBER = {"mov_a_dir": 1, "mov_dir_a": 1, "mov_c_dir": 1, "mov_dir_c": 2,
                            "anl": 1, "orl": 1, "xrl": 1, "anl_data": 1, "mul": 4, "div": 4,
                            "rl": 1, "mov_b_data": 2, "anl_xrl_orl": 1, "mul_div": 4, "mov_dir_c_2": 2,
                            "mov_dir_c_1": 1, "anl_orl_xrl": 1}

    # 初始化指令节点集合，供测试用
    # ins_list = []
    # ins_list.append(node("mov_a_dir", 1, 1, 0))
    # ins_list.append(node("rl", 1, 1, 1))
    # ins_list.append(node("mov_dir_a", 1, 1, 2))
    # ins_list.append(node("mov_a_dir", 1, 1, 3))
    # ins_list.append(node("rl", 1, 1, 4))
    # ins_list.append(node("mov_dir_a", 1, 1, 5))
    # ins_list.append(node("mov_c_dir", 1, 1, 6))
    # ins_list.append(node("mov_dir_c", 1, 2, 7))
    # ins_list.append(node("mov_c_dir", 1, 1, 8))
    # ins_list.append(node("mov_dir_c", 1, 2, 9))
    #
    # ins_list.append(node("mov_a_dir", 1, 1, 10))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 11))
    # ins_list.append(node("mov_dir_a", 1, 1, 12))
    # ins_list.append(node("mov_a_dir", 1, 1, 13))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 14))
    # ins_list.append(node("mov_dir_a", 1, 1, 15))
    #
    # ins_list.append(node("mov_a_dir", 1, 1, 16))
    # ins_list.append(node("anl_data", 2, 1, 17))
    # ins_list.append(node("mov_dir_a", 1, 1, 18))
    # ins_list.append(node("mov_a_dir", 1, 1, 19))
    # ins_list.append(node("anl_data", 2, 1, 20))
    # ins_list.append(node("mov_dir_a", 1, 1, 21))
    # ins_list.append(node("mov_a_dir", 1, 1, 22))
    # ins_list.append(node("anl_data", 2, 1, 23))
    # ins_list.append(node("mov_dir_a", 1, 1, 24))
    # ins_list.append(node("mov_a_dir", 1, 1, 25))
    # ins_list.append(node("anl_data", 2, 1, 26))
    # ins_list.append(node("mov_dir_a", 1, 1, 27))
    # #
    # ins_list.append(node("mov_a_dir", 1, 1, 28))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 29))
    # ins_list.append(node("rl", 1, 1, 30))
    # ins_list.append(node("rl", 1, 1, 31))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 32))
    # ins_list.append(node("mov_dir_a", 1, 1, 33))
    #
    # ins_list.append(node("mov_a_dir", 1, 1, 34))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 35))
    # ins_list.append(node("rl", 1, 1, 36))
    # ins_list.append(node("rl", 1, 1, 37))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 38))
    # ins_list.append(node("mov_dir_a", 1, 1, 39))
    #
    # ins_list.append(node("mov_a_dir", 1, 1,40))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 41))
    # ins_list.append(node("mov_dir_a", 1, 1, 42))
    # ins_list.append(node("mov_a_dir", 1, 1, 43))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 44))
    # ins_list.append(node("mov_dir_a", 1, 1, 45))
    # # #
    # ins_list.append(node("mov_a_dir", 1, 1, 46))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 47))
    # ins_list.append(node("mov_dir_a", 1, 1, 48))
    # ins_list.append(node("mov_a_dir", 1, 1, 49))
    # ins_list.append(node("anl_orl_xrl", 2, 1, 50))
    # ins_list.append(node("mov_dir_a", 1, 1, 51))

    # **************恢复主函数********************
    # *****1.指令操作码识别********
    # 1.1 加载模板
    templates = TrsUtil.load_ins_template("STC_7M_new2/templates")
    # 1.2 加载波形
    traces = TrsUtil.read_trs("traces/target_traces/7M_simonfirst_new2.trs")
    trace = np.mean(traces, axis=0)
    # *****2.指令操作数恢复********
    ins_list = []
    i = 0
    START_STATUS = False
    cnt = 0
    while i < 54:
        attack = trace[250 + 500 * i:250 + (i + 1) * 500]
        properties = TemplateAttack.template_match(templates, attack)
        if START_STATUS == False:
            ins_opcode = "mov_a_dir"
            START_STATUS = True
            ins_list.append(node(ins_opcode, OPCODE_OPRAND_NUMBER[ins_opcode], OPCODE_CYCYLE_NUMBER[ins_opcode], cnt))
            cnt += 1
        else:
            ins_opcode = properties[0][0]
            if ins_opcode == "mov_dir_a":
                START_STATUS = False
                ins_list.append(
                    node(ins_opcode, OPCODE_OPRAND_NUMBER[ins_opcode], OPCODE_CYCYLE_NUMBER[ins_opcode], cnt))
                cnt += 1
            elif ins_opcode == "mov_dir_c_2":
                ins_list.pop()
                ins_list.pop()
                cnt -= 2
                ins_list.append(
                    node("mov_c_dir", OPCODE_OPRAND_NUMBER["mov_c_dir"], OPCODE_CYCYLE_NUMBER["mov_c_dir"], cnt))
                cnt += 1
                ins_list.append(
                    node("mov_dir_c", OPCODE_OPRAND_NUMBER["mov_dir_c"], OPCODE_CYCYLE_NUMBER["mov_dir_c"], cnt))
                cnt += 1
                START_STATUS = False
            elif ins_opcode == "mov_a_dir":
                ins_list.pop()
                cnt -= 1
                ins_list.append(
                    node("mov_dir_a", OPCODE_OPRAND_NUMBER["mov_dir_a"], OPCODE_CYCYLE_NUMBER["mov_dir_a"], cnt))
                cnt += 1
                ins_list.append(
                    node("mov_a_dir", OPCODE_OPRAND_NUMBER["mov_a_dir"], OPCODE_CYCYLE_NUMBER["mov_a_dir"], cnt))
                cnt += 1
            elif ins_opcode == "anl" or ins_opcode == "orl" or ins_opcode == "xrl":
                ins_list.append(
                    node("anl_orl_xrl", OPCODE_OPRAND_NUMBER["anl_orl_xrl"], OPCODE_CYCYLE_NUMBER["anl_orl_xrl"], cnt))
                cnt += 1
            else:
                ins_list.append(
                    node(ins_opcode, OPCODE_OPRAND_NUMBER[ins_opcode], OPCODE_CYCYLE_NUMBER[ins_opcode], cnt))
                cnt += 1
        print(properties)
        i += 1

    for ins in ins_list:
        ins.print_node()
    #
    # print("恢复操作码完成，开始恢复操作数")
    plaintext, ciphertext = TrsUtil.get_trs_plaintext_ciphertext("traces/target_traces/7M_simonfirst_new2.trs", 13, 4,
                                                                 17, 4)
    code_reconstruct_main_test(traces, ins_list, plaintext, ciphertext)
