#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：template_attack
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/10/3 14:57
@Desc   ：指令操作码逆向方法
=================================================='''

import numpy as np
from commons.trs_util import TrsUtil
from scipy.stats import multivariate_normal


def deal_pro(pro):
    '''概率保留小数点后几位'''
    pro = str(pro)
    if len(pro) > 15:
        res = pro[:4] + pro[-5:]
    else:
        res = pro
    return res


class TemplateAttack:
    '''模板攻击方法进行指令识别'''

    @staticmethod
    def get_avg(matrix):
        '''求矩阵的均值'''
        return np.mean(matrix, axis=0)  # 对列求平均值

    @staticmethod
    def get_covariance(matrix):
        '''求协方差矩阵
        rowvar参数默认为True：每行代表一个Sample(属性)，每一列表示一条波形（观测）
        rowvar参数False: 每列代表一个Sample(属性)，每一行表示一条波形（观测）
        '''
        return np.cov(matrix, rowvar=False)

    @staticmethod
    def template_construct(matrixs):
        '''
        模板构建
        :param matrixs: 不同指令的波形数据
        :return: 不同指令的模板
        '''
        templates = {}
        for ins in matrixs:
            avg = TemplateAttack.get_avg(matrixs[ins])
            # # 求均值的协方差矩阵
            mean_matrix = []
            for row in matrixs[ins]:
                mean_matrix.append(row - avg)
            cov = TemplateAttack.get_covariance(mean_matrix)
            templates[ins] = (avg, cov)
        return templates

    @staticmethod
    def template_match(templates, trace, right_ans=""):
        '''
        波形模板匹配
        :param templates: 指令模板
        :param trace: 待匹配波形
        :param right_ans: 正确的对应指令
        :return: 计算出不同指令模板的匹配概率
        '''
        properties = []
        for ins in templates:
            try:
                template = templates[ins]
                pro = multivariate_normal.pdf(trace, mean=template[0], cov=template[1], allow_singular=True)
                properties.append([ins, pro])
            except:
                properties.append(None)
        properties.sort(key=lambda k: -k[1])
        res = []
        correct_rank = ""
        rank = 0
        for item in properties:
            res.append([item[0], deal_pro(item[1])])
            rank += 1
            if right_ans == item[0]:
                correct_rank = str(rank)
        return right_ans + " 's rank is " + correct_rank + " " + " ".join(str(r) for r in res)


class KNN:
    '''knn方法进行指令识别'''
    @staticmethod
    def euclidean_distance(trace_1, trace_2):
        '''计算两条波形之间的欧氏距离'''
        distance = 0
        for i in range(len(trace_1)):
            distance += (trace_1[i] - trace_2[i]) * (trace_1[i] - trace_2[i])
        return distance
    #
    # ins_names = ['inc', 'rl', 'mov_a_dir', 'mov_dir_a', 'mov_C_dir', 'anl', 'orl', 'xrl',
    #              'mov_dir_C_1', "mov_dir_C_2", "mov_r_dir_1", "mov_r_dir_2", "mov_b_data_1", "mov_b_data_2",
    #              'MUL_1', 'MUL_2', 'MUL_3', 'MUL_4', 'DIV_1', 'DIV_2', 'DIV_3', 'DIV_4']
    @staticmethod
    def save_knn_template(traces, ins_name, ins_count, ins_number, knn_template_path):
        # traces_all = np.load("traces/npy/trace_all.npy")
        knn_template = {}
        for i in range(ins_count):
            knn_template[ins_name[i]]=np.mean(traces[i * ins_number:(i + 1) * ins_number, :], axis=0).tolist()
        TrsUtil.save_ins_template(knn_template, knn_template_path)
    #
    # @staticmethod
    # def knn_attack(knn_template_path, traces, match_number, ):
    #
    #
    #     for i in range(match_number):
    #         # attack = trace[250 + 500 * i:250 + (i + 1) * 500]
    #         attack = traces[0 + i * 100]
    #         dis = []
    #         for j in range(22):
    #             dis.append((ins_names[j], euclidean_distance(attack, means[j])))
    #             # d = 0
    #             # for k in range(200):
    #             #     d += (attack[topk[k]] - means[j][topk[k]]) * (attack[topk[k]] - means[j][topk[k]])
    #             # dis.append((ins_names[j], d))
    #         dis.sort(key=lambda k: k[1])
    #         # print(i+1,dis)
    #         rank = 0
    #         for j in range(22):
    #             rank += 1
    #             if dis[j][0] == right_ins[i]:
    #                 print(i + 1, right_ins[i], rank)
    #                 break

if __name__ == '__main__':

    # 问题1：更改操作数之后，模板匹配效果不理想
    # 问题2：之前的指令会影响模板匹配效果
    #
    # matrix = TrsUtil.read_trs("traces/汇编指令模版_随机数.trs")
    # ins_names=['MOV_dir_atRi_pre','MOV_dir_atRi_post','INC','MOV','RL','ANL','ORL','XRL','MOV_B_pre','MOV_B_post',
    #            'MUL_1','MUL_2','MUL_3','MUL_4','DIV_1','DIV_2','DIV_3','DIV_4','MOV_C_dir','MOV_dir_C_pre',
    #            'MOV_dir_C_post']
    # matrixs=TrsUtil.split_by_instruction(matrix, ins_names)
    # #
    # templates=TemplateAttack.template_construct(matrixs)
    # #
    # TrsUtil.save_obj(templates, "templates")

    # templates = TrsUtil.load_obj("templates")
    #
    # matrix = TrsUtil.read_trs("traces/汇编指令模版_随机数.trs")
    # traces= matrix[0]
    # for i in range(22):
    #     trace=traces[250+i*500: 250+(i+1)*500]
    #     print(i, TemplateAttack.template_match(templates, trace))
    #
    # matrix = TrsUtil.read_trs("traces/汇编指令模版_随机数.trs")
    # traces=[]
    # for i in range(21):
    #     trace=matrix[:, 250+i*500: 250+(i+1)*500]
    #     traces.extend(trace)
    #
    # # PCA降维
    # from sklearn.decomposition import PCA
    # pca=PCA(n_components=100)
    # pca.fit(traces)
    # print('各主成分的方差值占总方差值百分比:', pca.explained_variance_ratio_)
    # print('各主成分的方差值:', pca.explained_variance_)
    # 转化后的数据
    # trans_data = pca.transform(traces)
    # print(trans_data)
    # print(trans_data.shape)
    # PlotUtil.show3(trans_data)
    # plt.show()
    #
    # ins_names=['MOV_dir_atRi_pre','MOV_dir_atRi_post','INC','MOV','RL','ANL','ORL','XRL','MOV_B_pre','MOV_B_post',
    #            'MUL_1','MUL_2','MUL_3','MUL_4','DIV_1','DIV_2','DIV_3','DIV_4','MOV_C_dir','MOV_dir_C_pre',
    #            'MOV_dir_C_post']
    # matrixs=TrsUtil.split_by_instruction_by_traces(trans_data, ins_names, 2000)
    # templates = TemplateAttack.template_construct(matrixs)
    # TrsUtil.save_obj(templates, "low_templates")

    # lda降维
    # split = [i for i in range(250, 11750,500)]
    # matrix = TrsUtil.read_trs("traces/汇编指令模版_随机数.trs")
    # traces, labels = TrsUtil.append_matrix(matrix, split)
    # low_traces_lda = LinearDiscriminantAnalysis(n_components=3).fit_transform(traces, labels)
    # PlotUtil.show3(low_traces_lda)
    # plt.show()

    pass