#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：instruction_practice
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/11/8 10:22
@Desc   ：指令操作码逆向实验
=================================================='''

from commons.trs_util import TrsUtil
from instruction_opcode_reverse import TemplateAttack

if __name__ == '__main__':

    #
    ###########################################################################################
    # 7M滤波器：对前后指令都是NOP的指令进行模板匹配测试
    # template = TrsUtil.load_obj("7M_templates")
    # trace = TrsUtil.read_trs("target_traces/7M_test.trs")[500]
    # for i in range(19):
    #     attack=trace[250+500*i:250+(i+1)*500]
    #     print(i+1, TemplateAttack.template_match(template, attack))

    ###########################################################################################
    # 7M滤波器：对前后指令随机的指令模板进行测试
    # 据templates文件夹下的13个7M指令波形构建模板根
    template = TrsUtil.load_ins_template("7Mall_templates")
    trace = TrsUtil.read_trs("traces/target_traces/7M_test.trs")[200]
    for i in range(19):
        attack = trace[250 + 500 * i:250 + (i + 1) * 500]
        print(i + 1, TemplateAttack.template_match(template, attack))
