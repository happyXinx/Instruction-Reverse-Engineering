#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：template_construct
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/11/26 14:14
@Desc   ：对真实波形进行指令模板构建
=================================================='''
import numpy as np
from commons.trs_util import TrsUtil
from instruction_opcode_reverse import TemplateAttack

# simon算法第一轮的对应指令波形正确答案
RIGHT_ANS = ["mov_r_dir_1", "mov_r_dir_2", "inc", "mov_r_dir_1", "mov_r_dir_2", "inc", "mov_r_dir_1", "mov_r_dir_2",
             "inc",
             "mov_r_dir_1", "mov_r_dir_2", "mov_r_dir_1", "mov_r_dir_2", "inc", "mov_r_dir_1", "mov_r_dir_2",

             "mov_a_dir", "rl", "mov_dir_a", "mov_a_dir", "rl", "mov_dir_a", "mov_C_dir", "mov_dir_C_1", "mov_dir_C_2",
             "mov_C_dir", "mov_dir_C_1", "mov_dir_C_2",

             "mov_a_dir", "anl", "mov_dir_a", "mov_a_dir", "anl", "mov_dir_a",

             "mov_a_dir", "anl", "mov_b_data_1", "mov_b_data_2", "DIV_1", "DIV_2", "DIV_3", "DIV_4", "mov_dir_a",
             "mov_a_dir", "anl", "mov_b_data_1", "mov_b_data_2", "MUL_1", "MUL_2", "MUL_3", "MUL_4", "mov_dir_a",
             "mov_a_dir", "anl", "mov_b_data_1", "mov_b_data_2", "DIV_1", "DIV_2", "DIV_3", "DIV_4", "mov_dir_a",
             "mov_a_dir", "anl", "mov_b_data_1", "mov_b_data_2", "MUL_1", "MUL_2", "MUL_3", "MUL_4", "mov_dir_a",

             "mov_a_dir", "orl", "xrl", "mov_dir_a", "mov_a_dir", "orl", "xrl", "mov_dir_a",
             "mov_a_dir", "xrl", "mov_dir_a", "mov_a_dir", "xrl", "mov_dir_a",
             "mov_a_dir", "xrl", "mov_dir_a", "mov_a_dir", "xrl", "mov_dir_a",
             ]


def get_specific_traces(trace_path, intervals, pre=0):
    '''
    获取特定段的波形数据
    :param trace_path: 波形路径
    :param intervals: 区间
    :param pre: 前缀
    :return: 特定区间的波形数据
    '''
    traces = TrsUtil.read_trs(trace_path)
    inc_traces = []
    for interval in intervals:
        inc_traces.extend(traces[:, interval + pre:interval + pre + 500])
    return inc_traces


def get_one_cycle_intervals():
    '''获取单指令的波形开始区间'''
    interval = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 2000, 2000, 3000, 3000]  # 1-6
    interval_1 = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 2000, 2000, 3000, 3500]  # 7
    interval_2 = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2500, 2500, 3500, 3500]  # 8
    interval_3 = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2500, 2500, 3500, 4500]  # 9
    interval_4 = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3500, 3500, 4500, 4500]  # 10
    intervals = [750]
    for _ in range(6):
        for i in interval:
            intervals.append(intervals[-1] + i)
    for i in interval_1:
        intervals.append(intervals[-1] + i)
    for i in interval_2:
        intervals.append(intervals[-1] + i)
    for i in interval_3:
        intervals.append(intervals[-1] + i)
    for _ in range(2):
        for i in interval_4:
            intervals.append(intervals[-1] + i)
    return intervals


def get_two_cycle_intervals():
    '''获取双周期指令的波形区间'''
    interval = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2500, 2500, 3500, 3500]  # 1-6
    interval_1 = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2500, 2500, 3500, 4000]  # 7
    interval_2 = [2500, 2500, 2500, 2500, 2500, 2500, 2500, 3000, 3000, 4000, 4000]  # 8
    interval_3 = [2500, 2500, 2500, 2500, 2500, 2500, 2500, 3000, 3000, 4000, 5000]  # 9
    interval_4 = [3500, 3500, 3500, 3500, 3500, 3500, 3500, 4000, 4000, 5000, 5000]  # 10
    intervals = [750]
    for _ in range(6):
        for i in interval:
            intervals.append(intervals[-1] + i)
    for i in interval_1:
        intervals.append(intervals[-1] + i)
    for i in interval_2:
        intervals.append(intervals[-1] + i)
    for i in interval_3:
        intervals.append(intervals[-1] + i)
    for _ in range(2):
        for i in interval_4:
            intervals.append(intervals[-1] + i)
    return intervals


def get_four_cycle_intervals():
    '''获取四周期指令的波形区间'''
    interval = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3500, 3500, 4500, 4500]  # 1-6
    interval_1 = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3500, 3500, 4500, 5000]  # 7
    interval_2 = [3500, 3500, 3500, 3500, 3500, 3500, 3500, 4000, 4000, 5000, 5000]  # 8
    interval_3 = [3500, 3500, 3500, 3500, 3500, 3500, 3500, 4000, 4000, 5000, 6000]  # 9
    interval_4 = [4500, 4500, 4500, 4500, 4500, 4500, 4500, 5000, 5000, 6000, 6000]  # 10
    intervals = [750]
    for _ in range(6):
        for i in interval:
            intervals.append(intervals[-1] + i)
    for i in interval_1:
        intervals.append(intervals[-1] + i)
    for i in interval_2:
        intervals.append(intervals[-1] + i)
    for i in interval_3:
        intervals.append(intervals[-1] + i)
    for _ in range(2):
        for i in interval_4:
            intervals.append(intervals[-1] + i)
    return intervals


def construct_template_one_cycle(intervals, trace_path, inc_name, template_path):
    '''构建单周期指令的模板'''
    ins_traces = get_specific_traces(trace_path, intervals[:-1])
    traces = {inc_name: ins_traces}
    templates = TemplateAttack.template_construct(traces)
    TrsUtil.save_ins_template(templates, template_path)


def construct_template_two_cycle(intervals, trace_path, name_1, name_2, template_path_1, template_path_2):
    '''构建双周期指令的模板'''
    pre_traces = get_specific_traces(trace_path, intervals[:-1])
    post_traces = get_specific_traces(trace_path, intervals[:-1], pre=500)

    traces_1 = {name_1: pre_traces}
    traces_2 = {name_2: post_traces}

    templates_1 = TemplateAttack.template_construct(traces_1)
    templates_2 = TemplateAttack.template_construct(traces_2)
    TrsUtil.save_ins_template(templates_1, template_path_1)
    TrsUtil.save_ins_template(templates_2, template_path_2)


def construct_template_four_cycle(intervals, trace_path, name_1, name_2, name_3, name_4,
                                  template_path_1, template_path_2, template_path_3, template_path_4):
    '''构建四指令周期的模板'''
    p1_traces = get_specific_traces(trace_path, intervals[:-1])
    p2_traces = get_specific_traces(trace_path, intervals[:-1], pre=500)
    p3_traces = get_specific_traces(trace_path, intervals[:-1], pre=1000)
    p4_traces = get_specific_traces(trace_path, intervals[:-1], pre=1500)

    traces_1 = {name_1: p1_traces}
    traces_2 = {name_2: p2_traces}
    traces_3 = {name_3: p3_traces}
    traces_4 = {name_4: p4_traces}

    templates_1 = TemplateAttack.template_construct(traces_1)
    templates_2 = TemplateAttack.template_construct(traces_2)
    templates_3 = TemplateAttack.template_construct(traces_3)
    templates_4 = TemplateAttack.template_construct(traces_4)

    TrsUtil.save_ins_template(templates_1, template_path_1)
    TrsUtil.save_ins_template(templates_2, template_path_2)
    TrsUtil.save_ins_template(templates_3, template_path_3)
    TrsUtil.save_ins_template(templates_4, template_path_4)


def save_one_cycle_instruction_traces(trace_path, ins_path):
    '''保存单周期指令波形'''
    intervals = get_one_cycle_intervals()
    ins_traces = get_specific_traces(trace_path, intervals[:-1])
    inc_np = np.asarray(ins_traces)
    np.save(ins_path, inc_np)
    return inc_np


def save_two_cycle_instruction_traces(trace_path, ins_path):
    '''保存双周期指令波形'''
    intervals = get_two_cycle_intervals()
    pre_traces = get_specific_traces(trace_path, intervals[:-1])
    post_traces = get_specific_traces(trace_path, intervals[:-1], pre=500)
    traces = []
    traces.extend(pre_traces)
    traces.extend(post_traces)
    inc_np = np.asarray(traces)
    np.save(ins_path, inc_np)
    return traces


def save_four_cycle_instruction_traces(trace_path, ins_path):
    '''保存四周期指令波形'''
    intervals = get_four_cycle_intervals()
    p1_traces = get_specific_traces(trace_path, intervals[:-1])
    p2_traces = get_specific_traces(trace_path, intervals[:-1], pre=500)
    p3_traces = get_specific_traces(trace_path, intervals[:-1], pre=1000)
    p4_traces = get_specific_traces(trace_path, intervals[:-1], pre=1500)
    traces = []
    traces.extend(p1_traces)
    traces.extend(p2_traces)
    traces.extend(p3_traces)
    traces.extend(p4_traces)
    inc_np = np.asarray(traces)
    np.save(ins_path, inc_np)
    return traces


if __name__ == '__main__':
    ##########################################################################################
    # 根据templates文件夹下的11个指令波形构建模板
    # construct_template_one_cycle("template/anl_template_270500.trs","anl","anl_template")
    # construct_template_one_cycle("template/inc_template_270500.trs","inc","inc_template")
    # construct_template_one_cycle("template/mov_A_dir_template_270500.trs","mov_a_dir","mov_a_dir_template")
    # construct_template_one_cycle("template/mov_dir_A_template_270500.trs","mov_dir_a","mov_dir_a_template")
    # construct_template_one_cycle("template/mov_C_dir_template_270500.trs","mov_C_dir","mov_C_dir_template")
    # construct_template_one_cycle("template/orl_template_270500.trs","orl","orl_template")
    # construct_template_one_cycle("template/xrl_template_270500.trs","xrl","xrl_template")
    # construct_template_one_cycle("template/rl_template_270500.trs","rl","rl_template")
    # construct_template_two_cycle("template/mov_b_data_331000.trs","mov_b_data_1", "mov_b_data_2", "mov_b_data_1_template", "mov_b_data_2_template")
    # construct_template_two_cycle("template/mov_r0_dir_331000.trs","mov_r0_dir_1", "mov_r0_dir_2", "mov_r0_dir_1_template", "mov_r0_dir_2_template")
    # construct_template_two_cycle("template/mov_dir_C_template_331000.trs","mov_dir_C_1", "mov_dir_C_2", "mov_dir_C_1_template", "mov_dir_C_2_template")
    # construct_template_four_cycle("template/mul_template_452000.trs","mul_1", "mul_2", "mul_3", "mul_4",
    #                               "mul_1_template", "mul_2_template", "mul_3_template", "mul_4_template")
    # construct_template_four_cycle("template/div_template_452000.trs","dir_1", "dir_2", "dir_3", "dir_4" ,
    #                               "dir_1_template", "dir_2_template", "dir_3_template", "dir_4_template")

    #########################################################################################################
    # 指令恢复
    # inc_templates = TrsUtil.load_obj("inc_template")
    # rl_templates = TrsUtil.load_obj("rl_template")
    #
    # anl_templates = TrsUtil.load_obj("anl_template")
    # orl_templates = TrsUtil.load_obj("orl_template")
    # xrl_templates = TrsUtil.load_obj("xrl_template")
    #
    # mov_a_dir_template = TrsUtil.load_obj("mov_a_dir_template")
    # mov_dir_a_template = TrsUtil.load_obj("mov_dir_a_template")
    # mov_C_dir_template = TrsUtil.load_obj("mov_C_dir_template")
    # mov_dir_C_template_1 = TrsUtil.load_obj("mov_dir_C_1_template")
    # mov_dir_C_template_2 = TrsUtil.load_obj("mov_dir_C_2_template")
    #
    # mov_b_data_1_template = TrsUtil.load_obj("mov_b_data_1_template")
    # mov_b_data_2_template = TrsUtil.load_obj("mov_b_data_2_template")
    # mov_r0_dir_1_template = TrsUtil.load_obj("mov_r0_dir_1_template")
    # mov_r0_dir_2_template = TrsUtil.load_obj("mov_r0_dir_2_template")
    # #
    # mul_1_template = TrsUtil.load_obj("mul_1_template")
    # mul_2_template = TrsUtil.load_obj("mul_2_template")
    # mul_3_template = TrsUtil.load_obj("mul_3_template")
    # mul_4_template = TrsUtil.load_obj("mul_4_template")
    # dir_1_template = TrsUtil.load_obj("dir_1_template")
    # dir_2_template = TrsUtil.load_obj("dir_2_template")
    # dir_3_template = TrsUtil.load_obj("dir_3_template")
    # dir_4_template = TrsUtil.load_obj("dir_4_template")
    #
    # ** mov_a_dir_template, ** mov_dir_a_template, ** mov_b_data_1_template, ** mov_b_data_2_template,
    # ** mov_r0_dir_1_template, ** mov_r0_dir_2_template,

    # templates=dict(inc_templates,**rl_templates,**anl_templates, **orl_templates,**xrl_templates,
    #                   **mul_1_template, **mul_2_template,**mul_3_template, **mul_4_template,
    #                **dir_1_template, **dir_2_template, **dir_3_template, **dir_4_template,
    #                **mov_a_dir_template, **mov_dir_a_template, **mov_C_dir_template, **mov_dir_C_template_1, **mov_dir_C_template_2,
    #                **mov_b_data_1_template, **mov_b_data_2_template, **mov_r0_dir_1_template, **mov_r0_dir_2_template)
    #
    # traces = TrsUtil.read_trs("traces/simon_first_round_11_14_104.trs")
    # trace=traces[0]
    # print(len(trace))
    # for i in range(104):
    #     attack=trace[250+500*i:250+(i+1)*500]
    #     print(i+1, TemplateAttack.template_match(templates, attack))
    #########################################################################################################

    #########################################################################################################
    # pca降维指令恢复
    #  1.保存指令波形
    #
    # inc=get_instruction_traces_one_cycle("template/inc_template_270500.trs", "npy/inc.npy")
    # rl = get_instruction_traces_one_cycle("template/rl_template_270500.trs","npy/rl.npy")
    # mov_a_dir=get_instruction_traces_one_cycle("template/mov_A_dir_template_270500.trs","npy/mov_a_dir.npy")
    # mob_dir_a=get_instruction_traces_one_cycle("template/mov_dir_A_template_270500.trs","npy/mov_dir_a.npy")
    # mov_C_dir=get_instruction_traces_one_cycle("template/mov_C_dir_template_270500.trs","npy/mov_C_dir.npy")
    # anl = get_instruction_traces_one_cycle("template/anl_template_270500.trs","npy/anl.npy")
    # orl=get_instruction_traces_one_cycle("template/orl_template_270500.trs","npy/orl.npy")
    # xrl=get_instruction_traces_one_cycle("template/xrl_template_270500.trs","npy/xrl.npy")
    #
    # mov_dir_C=get_instruction_traces_two_cycle("template/mov_dir_C_template_331000.trs","npy/mov_dir_C.npy")
    # mov_r_dir=get_instruction_traces_two_cycle("template/mov_r0_dir_331000.trs","npy/mov_r_dir.npy")
    # mov_b_data=get_instruction_traces_two_cycle("template/mov_b_data_331000.trs","npy/mov_b_data.npy")
    #
    # mul=get_instruction_traces_four_cycle("template/mul_template_452000.trs","npy/mul.npy")
    # div=get_instruction_traces_four_cycle("template/div_template_452000.trs","npy/div.npy")

    # 2. 读取指令波形
    # traces_all=[]
    # inc=np.load("npy/inc.npy")
    # rl=np.load("npy/rl.npy")
    # mov_a_dir=np.load("npy/mov_a_dir.npy")
    # mov_dir_a=np.load("npy/mov_dir_a.npy")
    # mov_C_dir=np.load("npy/mov_C_dir.npy")
    # anl=np.load("npy/anl.npy")
    # orl=np.load("npy/orl.npy")
    # xrl=np.load("npy/xrl.npy")
    # dir_C=np.load("npy/mov_dir_C.npy")
    # mov_r_dir=np.load("npy/mov_r_dir.npy")
    # mov_b_data=np.load("npy/mov_b_data.npy")
    # mul=np.load("npy/mul.npy")
    # div=np.load("npy/div.npy")
    #
    # traces_all.extend(inc)
    # traces_all.extend(rl)
    # traces_all.extend(mov_a_dir)
    # traces_all.extend(mov_dir_a)
    # traces_all.extend(mov_C_dir)
    # traces_all.extend(anl)
    # traces_all.extend(orl)
    # traces_all.extend(xrl)
    # traces_all.extend(dir_C)
    # traces_all.extend(mov_r_dir)
    # traces_all.extend(mov_b_data)
    # traces_all.extend(mul)
    # traces_all.extend(div)
    # print(len(traces_all))
    #
    # trace_all_np=np.asarray(traces_all)
    # np.save('npy/trace_all.npy',trace_all_np)
    #
    # #

    # knn_attack()
    # top_k=sum_of_difference_of_means(200)
    # top_k=means_variance(200)
    #
    # traces_all=np.load("npy/trace_all.npy")
    # traces_new=[]
    # for i in range(len(traces_all)):
    #     row=[]
    #     for j in range(200):
    #         row.append(traces_all[i][top_k[j]])
    #     traces_new.append(row)
    # print("traces_new...")
    # row=traces_all[i][50:100].tolist()
    # row.extend(traces_all[i][250:430])
    # row.extend(traces_all[i][480:500])
    # traces_new.append(row)

    # variance=[]
    # for i in range(500):
    #     variance.append(np.var(traces_all[:,i]))
    # plt.plot(variance)
    # plt.show()

    #
    # ins_names = ['inc', 'rl', 'mov_a_dir', 'mov_dir_a', 'mov_C_dir', 'anl', 'orl', 'xrl',
    #              'mov_dir_C_1',"mov_dir_C_2", "mov_r_dir_1","mov_r_dir_2", "mov_b_data_1", "mov_b_data_2",
    #              'MUL_1', 'MUL_2', 'MUL_3', 'MUL_4', 'DIV_1', 'DIV_2', 'DIV_3', 'DIV_4']
    # matrixs={}
    # for i in range(22):
    #     matrixs[ins_names[i]]=traces_new[i*24200:(i+1)*24200]
    #
    # templates = TemplateAttack.template_construct(matrixs)
    #
    # traces = TrsUtil.read_trs("traces/simon_first_round_11_14_104.trs")
    # trace=traces[0]
    # print(len(trace))
    #
    #
    # for i in range(104):
    #     attack=[]
    #     for j in range(200):
    #         attack.append(trace[250+500*i:250+(i+1)*500][top_k[j]])
    #
    #     # attack=trace[250+500*i:250+(i+1)*500].tolist()
    #     # attack.extend(trace[250+500*i:250+(i+1)*500][250:430])
    #     # attack.extend(trace[250+500*i:250+(i+1)*500][480:500])
    #     if i<89:
    #         print(i+1, TemplateAttack.template_match(templates, attack, right_ins[i]))
    #     else:
    #         print(i + 1, TemplateAttack.template_match(templates, attack, right_ins[i]))

    # print(traces_all.shape)
    # pca = PCA(n_components=200)
    # pca.fit(traces_all)
    # trans_data = pca.transform(traces_all)
    # knn_attack(trans_data)

    #
    # ins_names = ['inc', 'rl', 'mov_a_dir', 'mov_dir_a', 'mov_C_dir', 'anl', 'orl', 'xrl',
    #              'mov_dir_C_1',"mov_dir_C_2", "mov_r_dir_1","mov_r_dir_2", "mov_b_data_1", "mov_b_data_2",
    #              'MUL_1', 'MUL_2', 'MUL_3', 'MUL_4', 'DIV_1', 'DIV_2', 'DIV_3', 'DIV_4']
    # matrixs={}
    # for i in range(22):
    #     matrixs[ins_names[i]]=trans_data[i*24200:(i+1)*24200]
    # templates = TemplateAttack.template_construct(matrixs)
    #
    # matrixs = TrsUtil.split_by_instruction_by_traces(trans_data, ins_names,200)
    # print(matrixs)
    # templates = TemplateAttack.template_construct(matrixs)
    # TrsUtil.save_obj(templates, "pca_template_all")
    # construct_template_pca("traces/汇编指令模版_随机数.trs", 100, "template_pca_100")

    # template_match_practice("traces/simon_first_round_11_14_104.trs", 200, templates,104)

    #
    ######################################################################

    ###########################################################################################
    # 对前后都是两个NOP的指令进行分析
    #
    # intervals_mov_a_dir=[1250]
    # construct_template_one_cycle(intervals_mov_a_dir, "target_traces/NOPNOP.trs", "7M_mov_a_dir", "7M_mov_a_dir")
    #
    # intervals_mov_dir_a = [2750]
    # construct_template_one_cycle(intervals_mov_dir_a, "target_traces/NOPNOP.trs", "7M_mov_dir_a", "7M_mov_dir_a")
    #
    # intervals_rl = [4250]
    # construct_template_one_cycle(intervals_rl, "target_traces/NOPNOP.trs", "7M_rl", "7M_rl")
    #
    # intervals_mov_c_dir = [5750]
    # construct_template_one_cycle(intervals_mov_c_dir, "target_traces/NOPNOP.trs", "7M_mov_c_dir", "7M_mov_c_dir")
    #
    # intervals_anl = [7250]
    # construct_template_one_cycle(intervals_anl, "target_traces/NOPNOP.trs", "7M_anl", "7M_anl")
    #
    # intervals_orl = [8750]
    # construct_template_one_cycle(intervals_orl, "target_traces/NOPNOP.trs", "7M_orl", "7M_orl")
    #
    # intervals_xrl = [10250]
    # construct_template_one_cycle(intervals_xrl, "target_traces/NOPNOP.trs", "7M_xrl", "7M_xrl")
    #
    # intervals_mov_dir_c_1=[11750]
    # construct_template_one_cycle(intervals_mov_dir_c_1, "target_traces/NOPNOP.trs", "7M_mov_dir_c_1", "7M_mov_dir_c_1")
    #
    # intervals_mov_dir_c_2 = [12250]
    # construct_template_one_cycle(intervals_mov_dir_c_2, "target_traces/NOPNOP.trs", "7M_mov_dir_c_2", "7M_mov_dir_c_2")
    #
    # intervals_mov_b_data_1 = [13750]
    # construct_template_one_cycle(intervals_mov_b_data_1, "target_traces/NOPNOP.trs", "7M_mov_b_data_1", "7M_mov_b_data_1")
    #
    # intervals_mov_b_data_2 = [14250]
    # construct_template_one_cycle(intervals_mov_b_data_2, "target_traces/NOPNOP.trs", "7M_mov_b_data_2", "7M_mov_b_data_2")
    #
    # intervals_mul_1 = [15750]
    # construct_template_one_cycle(intervals_mul_1, "target_traces/NOPNOP.trs", "7M_mul_1", "7M_mul_1")
    #
    # intervals_mul_2 = [16250]
    # construct_template_one_cycle(intervals_mul_2, "target_traces/NOPNOP.trs", "7M_mul_2", "7M_mul_2")
    #
    # intervals_mul_3 = [16750]
    # construct_template_one_cycle(intervals_mul_3, "target_traces/NOPNOP.trs", "7M_mul_3", "7M_mul_3")
    #
    # intervals_mul_4 = [17250]
    # construct_template_one_cycle(intervals_mul_4, "target_traces/NOPNOP.trs", "7M_mul_4", "7M_mul_4")
    #
    # intervals_div_1 = [18750]
    # construct_template_one_cycle(intervals_div_1, "target_traces/NOPNOP.trs", "7M_div_1", "7M_div_1")
    #
    # intervals_div_2 = [19250]
    # construct_template_one_cycle(intervals_div_2, "target_traces/NOPNOP.trs", "7M_div_2", "7M_div_2")
    #
    # intervals_div_3 = [19750]
    # construct_template_one_cycle(intervals_div_3, "target_traces/NOPNOP.trs", "7M_div_3", "7M_div_3")
    #
    # intervals_div_4 = [20250]
    # construct_template_one_cycle(intervals_div_4, "target_traces/NOPNOP.trs", "7M_div_4", "7M_div_4")
    #
    #
    # mov_a_dir = TrsUtil.load_obj("7M_mov_a_dir")
    # mov_dir_a = TrsUtil.load_obj("7M_mov_dir_a")
    # mov_c_dir = TrsUtil.load_obj("7M_mov_c_dir")
    #
    # rl = TrsUtil.load_obj("7M_rl")
    # anl = TrsUtil.load_obj("7M_anl")
    # xrl = TrsUtil.load_obj("7M_xrl")
    # orl = TrsUtil.load_obj("7M_orl")
    #
    # mov_b_data_1 = TrsUtil.load_obj("7M_mov_b_data_1")
    # mov_b_data_2 = TrsUtil.load_obj("7M_mov_b_data_2")
    # mov_dir_c_1 = TrsUtil.load_obj("7M_mov_dir_c_1")
    # mov_dir_c_2 = TrsUtil.load_obj("7M_mov_dir_c_2")
    #
    # #
    #
    # mul_1_template = TrsUtil.load_obj("7M_mul_1")
    # mul_2_template = TrsUtil.load_obj("7M_mul_2")
    # mul_3_template = TrsUtil.load_obj("7M_mul_3")
    # mul_4_template = TrsUtil.load_obj("7M_mul_4")
    # div_1_template = TrsUtil.load_obj("7M_div_1")
    # div_2_template = TrsUtil.load_obj("7M_div_2")
    # div_3_template = TrsUtil.load_obj("7M_div_3")
    # div_4_template = TrsUtil.load_obj("7M_div_4")
    #
    # templates=dict(mov_a_dir,**mov_dir_a,**mov_c_dir, **rl,**anl, **xrl, **orl,
    #                **mov_b_data_1, **mov_b_data_2, **mov_dir_c_1, **mov_dir_c_2,
    #                   **mul_1_template, **mul_2_template,**mul_3_template, **mul_4_template,
    #                **div_1_template, **div_2_template, **div_3_template, **div_4_template,
    #                )
    # TrsUtil.save_obj(templates,"7M_templates")

    #########################################################################################################
    # 对7M滤波器采集的指令进行建模，前后都是随机指令
    intervals_one = get_one_cycle_intervals()
    intervals_two = get_two_cycle_intervals()
    intervals_four = get_four_cycle_intervals()
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_anl_270500.trs", "7Mall_anl", "7Mall_anl")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_inc_270500.trs", "7Mall_inc", "7Mall_inc")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_mov_a_dir_270500.trs", "7Mall_mov_a_dir",
                                 "7Mall_mov_a_dir")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_mov_dir_A_270500.trs", "7Mall_mov_dir_a",
                                 "7Mall_mov_dir_a")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_mov_C_dir_270500.trs", "7Mall_mov_C_dir",
                                 "7M_mov_C_dir")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_orl_270500.trs", "7Mall_orl", "7Mall_orl")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_xrl_270500.trs", "7Mall_xrl", "7Mall_xrl")
    construct_template_one_cycle(intervals_one, "traces/template_traces/7M_rl_270500.trs", "7Mall_rl", "7Mall_rl")
    construct_template_two_cycle(intervals_two, "traces/template_traces/7M_mov_b_data_331000.trs", "7Mall_mov_b_data_1",
                                 "7Mall_mov_b_data_2", "7Mall_mov_b_data_1", "7Mall_mov_b_data_2")
    construct_template_two_cycle(intervals_two, "traces/template_traces/7M_mov_r0_dir_331000.trs", "7Mall_mov_r0_dir_1",
                                 "7Mall_mov_r0_dir_2", "7Mall_mov_r0_dir_1", "7Mall_mov_r0_dir_2")
    construct_template_two_cycle(intervals_two, "traces/template_traces/7M_mov_dir_C_331000.trs", "7Mall_mov_dir_C_1",
                                 "7Mall_mov_dir_C_2", "7Mall_mov_dir_C_1", "7Mall_mov_dir_C_2")
    construct_template_four_cycle(intervals_four, "traces/template_traces/7M_mul_452000.trs", "7Mall_mul_1",
                                  "7Mall_mul_2", "7Mall_mul_3", "7Mall_mul_4",
                                  "7Mall_mul_1", "7Mall_mul_2", "7Mall_mul_3", "7Mall_mul_4")
    construct_template_four_cycle(intervals_four, "traces/template_traces/7M_div_452000.trs", "7Mall_dir_1",
                                  "7Mall_dir_2", "7Mall_dir_3", "7Mall_dir_4",
                                  "7Mall_dir_1", "7Mall_dir_2", "7Mall_dir_3", "7Mall_dir_4")

    _7Mall_anl = TrsUtil.load_ins_template("7Mall_anl")
    _7Mall_rl = TrsUtil.load_ins_template("7Mall_rl")
    _7Mall_mov_b_data_1 = TrsUtil.load_ins_template("7Mall_mov_b_data_1")
    _7Mall_mov_b_data_2 = TrsUtil.load_ins_template("7Mall_mov_b_data_2")
    _7Mall_mov_r0_dir_1 = TrsUtil.load_ins_template("7Mall_mov_r0_dir_1")
    _7Mall_mov_r0_dir_2 = TrsUtil.load_ins_template("7Mall_mov_r0_dir_2")
    _7Mall_mul_1 = TrsUtil.load_ins_template("7Mall_mul_1")
    _7Mall_mul_2 = TrsUtil.load_ins_template("7Mall_mul_2")
    _7Mall_mul_3 = TrsUtil.load_ins_template("7Mall_mul_3")
    _7Mall_mul_4 = TrsUtil.load_ins_template("7Mall_mul_4")
    _7Mall_div_1 = TrsUtil.load_ins_template("7Mall_dir_1")
    _7Mall_div_2 = TrsUtil.load_ins_template("7Mall_dir_2")
    _7Mall_div_3 = TrsUtil.load_ins_template("7Mall_dir_3")
    _7Mall_div_4 = TrsUtil.load_ins_template("7Mall_dir_4")

    templates = dict(_7Mall_anl, **_7Mall_rl, **_7Mall_mov_b_data_1, **_7Mall_mov_b_data_2,
                     **_7Mall_mov_r0_dir_1, **_7Mall_mov_r0_dir_2,
                     **_7Mall_mul_1, **_7Mall_mul_2, **_7Mall_mul_3, **_7Mall_mul_4,
                     **_7Mall_div_1, **_7Mall_div_2, **_7Mall_div_3, **_7Mall_div_4
                     )

    TrsUtil.load_ins_template(templates, "7Mall_templates")
