from slwork_function.add_code import *


import pandas as pd
import numpy as np

from slwork_function.caluate_func import *


# # 当前水库的文件夹的路径1
# shuiku_file_path=''
# # 当前水库的文件夹的路径2
# shuiku_file_path2=''
# # 水库1名称
# shuiku_name1=''
# # 水库2名称
# shuiku_name2=''



# 先计算水库，再计算区间
def moshi5(
        shuiku_name1,  # 水库名称1
        shuiku_name2,  # 水库名称2
        fenqu_name,
        shuru_cjs  # 輸入出境水
):
    #  todo 试一下用给出的汛线库容计算汛线水位的数据对不对
    #
    get_file_path(fenqu_name)
    # 准备读取表格，获取需要的数据

    # 水库的需水获取
    # 1.单独调算，所有的参数都输入，包括需水
    # 2.不单独调算，所有的参数都输入，需水 从河道径流计算后缺水传入
    # 就全都读取，然后在计算河道径流的时候修改输入就行

    (sqls, xu_shui, di_xia_xu_shui, zxskjl, dxsk, wds,
     phxs,  # 破坏系数
     bqjl,  # 本区径流
     hdjl,  # 河道径流
     hgxs,  # 回归水系数
     Vx,  # 兴利库容
     Vxx,  # 汛限库容
     Vdead,  # 死库容
     ) = prepare_moshi4_data()

    if shuru_cjs is not None:
        sqls = shuru_cjs

    # 计算破坏后需水x
    # 需水_破坏后

    xs_phh = xs_phxs(xu_shui, phxs)

    # global shuiku_file_path1, shuiku_file_path2
    shuiku_file_path1 = get_skfile_path_with_return(shuiku_name1)
    shuiku_file_path2 = get_skfile_path_with_return(shuiku_name2)

    # 丰满 牡丹江 尼尔基 镜泊湖 察尔森 需要调度图，需要获取调度线，其他暂时不用
    # 但是也有需要调度图的
    (
        dd_table1, flmb_table1, bxsw_line1, bxll_line1,
        S1, Z1, kr_line1, mj_line1, sw_line1, Vx1, Vxx1, Vdead1,
        dxsk_rk1, stxx1, skxu_shui1,
        Q_max1,  # 机组最大过流能力
        N_max1,  # 最大出力
        if_N1,  # 是否计算发电
    ) = prepare_shuiku_data_common(shuiku_file_path1, shuiku_name1)
    (
        dd_table2, flmb_table2, bxsw_line2, bxll_line2,
        S2, Z2, kr_line2, mj_line2, sw_line2, Vx2, Vxx2, Vdead2,
        dxsk_rk2, stxx2, skxu_shui2,
                          Q_max2,  # 机组最大过流能力
                          N_max2,  # 最大出力
                          if_N2,  # 是否计算发电
    ) = prepare_shuiku_data_common(shuiku_file_path2, shuiku_name2)
    # todo 那后边的大型水库还要不要计算了 不计算了，但中小型还需要
    #  计算这个17个分行业的大型水库之后，这两个水库之间要传递什么数据？之后返回的
    #  大型水库的 供水？

    # todo 要从表里获取

    # 大型水库的需水也需要乘破坏系数，破坏系数用区间的破坏系数
    skxs1_phh = xs_phxs(skxu_shui1, phxs)
    skxs2_phh = xs_phxs(skxu_shui2, phxs)
    # todo stxx1,  # 生态下泄 的需水用不用乘破坏系数

    # 先大型水平衡， 传递缺水给区间平衡， 区间总需水-大型水库供水=区间缺水，就 不需要从分区的缺水表里获取缺水数据了
    # 大型水库供水也需要先破坏，破坏系数也是区间读取的破坏系数
    # todo 大型水库的缺水，用来干啥了？ 之后可能需要计算水库的保证率
    #  区间总需水是从区间的需水表里获取的吧？对
    #  是破坏后的需水-大型水库供水1-大型水库供水2，还是-大型水库供水之后再破坏
    skgs1 = shuiku_common(dxsk_rk1,
                          skxs1_phh,  # 分行业的缺水 需水
                          Vx1, Vxx1, Vdead1,
                          Z1,  # 水库 蒸发强度过程线
                          S1,  # 水库 渗漏强度过程线
                          mj_line1,  # 面积曲线
                          sw_line1,  # 水位曲线
                          kr_line1,  # 库容曲线 v
                          dd_table1,  # 调度线
                          flmb_table1,  # 放流目标表 下泄

                          bxsw_line1,  # 坝下水位 曲线
                          bxll_line1,  # 坝下流量 曲线
                          stxx1,  # 生态下泄
                          shuiku_file_path1,
                          Q_max1,  # 机组最大过流能力
                          N_max1,  # 最大出力
                          if_N1,  # 是否计算发电
                          )

    skgs2 = shuiku_common(dxsk_rk2,
                          skxs2_phh,  # 分行业的缺水 需水
                          Vx2, Vxx2, Vdead2,
                          Z2,  # 水库 蒸发强度过程线
                          S2,  # 水库 渗漏强度过程线
                          mj_line2,  # 面积曲线
                          sw_line2,  # 水位曲线
                          kr_line2,  # 库容曲线 v
                          dd_table2,  # 调度线
                          flmb_table2,  # 放流目标表 下泄

                          bxsw_line2,  # 坝下水位 曲线
                          bxll_line2,  # 坝下流量 曲线
                          stxx2,  # 生态下泄
                          shuiku_file_path2,
                          Q_max2,  # 机组最大过流能力
                          N_max2,  # 最大出力
                          if_N2,  # 是否计算发电
                          )

    xs_phh = xs_phh - skgs1 - skgs2

    #  每个水库不能只运行一次吧？有没有可能运行多次，导致输出的时候都输出在水库的文件夹里，就冲突了  ok 不会有

    print('-' * 50)
    print('河道径流平衡')
    # 计算 河道径流平衡   返回是否有缺水
    dx_gs16, GS17, ls17, ques16 = jlph_fun(hdjl, xs_phh, di_xia_xu_shui)

    V0 = Vx

    # 地下需水做成0的np 使用 zeros 创建一个形状相同的全零数组
    di_xia_xu_shui_zero = np.zeros_like(di_xia_xu_shui)

    # 创建一个和 河道径流 供水 一样格式的0矩阵，用于统计的时候没有 过境水 的时候引用
    gs_zero = np.zeros_like(GS17)

    if (ques16 > 0).any():
        print('-' * 50)
        print('中小型水库平衡')
        # ls 就是 zxskjl 的
        # xs 就是 上一层的缺水
        # shuiku_zxx_dxsk 没分行业，但是计算了 蒸发、渗透、面积，最后需要输出
        # shuikuGS_16 分行业了但是没计算  蒸发、渗透、面积，就有v,m,z,s 的时候再调用 shuikuGS_16 返回蒸发吧
        # 中小型水库
        (zxx_SKGS0, ZF, SL, qs, V2, V3, jh, GS0, zxxsk_ques, df2) = shuiku_zxx_dxsk(
            V0, zxskjl,
            ques16, Vx, Vxx, Vdead,
            None, None, None, None)

        # 中小型水库 如果缺水
        if zxxsk_ques.any() > 0:
            print('-' * 50)
            print('干流过境水供需分析')
            # 大型水库平衡如果有缺水
            # 计算 干流过境水供需分析 使用 河道径流平衡   返回是否有缺水
            # 地下需水做成0的
            # 来水一直都是表中输入的来水
            # 缺水是上层计算的缺水
            (glgj_dx_gs16, glgj_gs, ls17, glgj_que) = jlph_fun(sqls, zxxsk_ques, di_xia_xu_shui_zero)

            # 干流过境水供需分析 如果还有缺水
            if glgj_que.any() > 0:
                print('-' * 50)
                print('外调水供需分析')

                # 计算 外调水供需分析 使用 河道径流平衡   返回是否有缺水
                # 地下需水做成0的
                # 来水一直都是表中输入的 外调水 wds
                # 缺水是上层计算的缺水
                (wdgs_dx_gs16, wdgs_gs, ls17, wdgs_que) = jlph_fun(wds, glgj_que, di_xia_xu_shui_zero)

                #     统计供水、回归水、弃水、保证率输出
                cjs = tj(
                    dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
                    GS17,  # 本区地表
                    zxx_SKGS0,  # 中小水库
                    gs_zero,  # 大型水库
                    glgj_gs,  # 过境水
                    wdgs_gs,  # 外调水
                    hgxs,  # 回归水系数

                    xu_shui,  # 输入的需水
                    bqjl,  # 本区径流
                    sqls,  # 上区来水
                    wds,  # 输入的外调水
                )
            else:

                #  干流过境水供需分析 没有缺水  统计供水、回归水、弃水、保证率输出
                # 外调水 的供水都 为0矩阵
                cjs = tj(
                    dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
                    GS17,  # 本区地表
                    zxx_SKGS0,  # 中小水库
                    gs_zero,  # 大型水库
                    glgj_gs,  # 过境水
                    gs_zero,  # 外调水
                    hgxs,  # 回归水系数

                    xu_shui,  # 输入的需水
                    bqjl,  # 本区径流
                    sqls,  # 上区来水
                    wds,  # 输入的外调水
                )


        else:
            #   中小型水库平衡没有缺水  统计供水、回归水、弃水、保证率输出
            # 大型水库、过境水、外调水 的供水都 为0矩阵

            cjs = tj(
                dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
                GS17,  # 本区地表
                zxx_SKGS0,  # 中小水库
                gs_zero,  # 大型水库
                gs_zero,  # 过境水
                gs_zero,  # 外调水
                hgxs,  # 回归水系数

                xu_shui,  # 输入的需水
                bqjl,  # 本区径流
                sqls,  # 上区来水
                wds,  # 输入的外调水
            )


    else:
        #   河道径流平衡没有缺水  统计供水、回归水、弃水、保证率输出
        # 中小水库、大型水库、过境水、外调水 的供水都 为0矩阵
        cjs = tj(
            dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
            GS17,  # 本区地表
            gs_zero,  # 中小水库
            gs_zero,  # 大型水库
            gs_zero,  # 过境水
            gs_zero,  # 外调水
            hgxs,  # 回归水系数
            xu_shui,  # 输入的需水
            bqjl,  # 本区径流
            sqls,  # 上区来水
            wds,  # 输入的外调水
        )
    return cjs
