
from slwork_function.add_code import *
from slwork_function.prepare_data import *


import pandas as pd
import numpy as np

from slwork_function.caluate_func import *


def moshi4(
        fenqu_name,
        shuiku_name,  # 水库名称
        shuru_cjs  # 輸入出境水
):
    # 模式4  分区计算流程
    #
    get_file_path(fenqu_name)
    # 准备读取表格，获取需要的数据
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
        sqls=shuru_cjs

    # 计算破坏后需水x
    # 需水_破坏后
    xs_phh = xs_phxs(xu_shui, phxs)

    print('-' * 50)
    print('河道径流平衡')
    # 计算 河道径流平衡   返回是否有缺水
    dx_gs16, GS17, ls17, ques16 = jlph_fun(hdjl, xs_phh, di_xia_xu_shui)

    # # 初始库容
    # V0 = Vx
    # # ls 就是 zxskjl 的
    # # xs 就是 上一层的缺水
    # # shuiku_zxx_dxsk 没分行业，但是计算了 蒸发、渗透、面积，最后需要输出
    # # shuikuGS_16 分行业了但是没计算  蒸发、渗透、面积，就有v,m,z,s 的时候再调用 shuikuGS_16 返回蒸发吧
    # # 中小型水库
    # (zxx_SKGS0, ZF, SL, qs, V2, V3, jh, GS0, zxxsk_ques, df2) = shuiku_zxx_dxsk(
    #     V0, zxskjl,
    #     ques16, Vx, Vxx, Vdead,
    #     None, None, None, None)

    # # 大型水库平衡，和中小型水库平衡 一个函数，但是包括 蒸发、渗透、面积
    # # 根据现在的数据长度来填充m,sl
    # shape_num = dxsk.shape[0]
    # zf = zf_hcgsk.reindex(range(shape_num), fill_value=0)
    # sl = sl_hcgsk.reindex(range(shape_num), fill_value=0)
    #
    # (dxsk_SKGS0, ZF, SL, qs, V2, V3, jh, GS0, dxsk_ques, df2) = shuiku_zxx_dxsk(
    #     V0, dxsk,
    #     zxxsk_ques,
    #     Vx, Vxx, Vdead,
    #     v_hcgsk, m_hcgsk, zf, sl  # 暂时使用之前的数据
    #     # 蒸发、渗透、面积 需要读取水库表的表 todo 每个区对应哪个水库？
    #     )

    # # 地下需水做成0的np 使用 zeros 创建一个形状相同的全零数组
    # di_xia_xu_shui_zero = np.zeros_like(di_xia_xu_shui)

    # # 大型水库平衡如果有缺水
    # # 计算 干流过境水供需分析 使用 河道径流平衡   返回是否有缺水
    # # 地下需水做成0的
    # # 来水一直都是表中输入的来水
    # # 缺水是上层计算的缺水
    # # todo 过境水供水-> 调用径流计算函数（上区来水，上次计算缺水，供水），输出缺水
    # # todo 这一层只输入了上去来水，没输入“供水”，是不是有问题？
    # (glgj_dx_gs16, glgj_gs, ls17, glgj_que) = jlph_fun(sqls, dxsk_ques, di_xia_xu_shui_zero)
    #
    # # 计算 外调水供需分析 使用 河道径流平衡   返回是否有缺水
    # # 地下需水做成0的
    # # 来水一直都是表中输入的 外调水 wds
    # # 缺水是上层计算的缺水
    # (wdgs_dx_gs16, wdgs_gs, ls17, wdgs_que) = jlph_fun(wds, glgj_que, di_xia_xu_shui_zero)

    # # 创建一个和 河道径流 供水 一样格式的0矩阵，用于统计的时候没有 过境水 的时候引用
    # gs_zero = np.zeros_like(GS17)
    #
    # #     统计供水、回归水、弃水、保证率输出
    # tj(
    #     dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
    #     GS17,  # 本区地表
    #     zxx_SKGS0,  # 中小水库
    #     dxsk_SKGS0,  # 大型水库
    #     glgj_gs,  # 过境水
    #     wdgs_gs,  # 外调水
    #     hgxs,  # 回归水系数
    #
    #     xu_shui,# 输入的需水
    #     bqjl,# 本区径流
    #     sqls,  # 上区来水
    #     wds,#输入的外调水
    # )

    # ------------------------------------------------------------------------------------

    # 初始库容
    # todo 月初库容 不能等于 Vx，应该为 从上一年时段赋值过来
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
            print('大型水库平衡')
            # 大型水库平衡，和中小型水库平衡 一个函数，但是包括 蒸发、渗透、面积
            # 根据现在的数据长度来填充m,sl
            shape_num = dxsk.shape[0]
            zf = zf_hcgsk.reindex(range(shape_num), fill_value=0)
            sl = sl_hcgsk.reindex(range(shape_num), fill_value=0)
            #
            # # 根据水库名获取水库
            # get_file_path_sk(shuiku_name)
            #
            # if shuiku_name=='尼尔基水库':
            #     # 获取尼尔基的数据
            #     (
            #         dd_table, flmb_table, bxsw_line, bxll_line,
            #         S, Z, kr_line, mj_line, sw_line, Vx, Vxx, Vdead,
            #         dxsk_rk, stxx
            #     ) = prepare_shuiku_nej_data()
            #
            #     shuiku_nej(
            #         V0, L,
            #         zxxsk_ques,  # 分行业的缺水 需水
            #         Vx, Vxx, Vdead,
            #         Z,  # 水库 蒸发强度过程线
            #         S,  # 水库 渗漏强度过程线
            #         mj_line,  # 面积曲线
            #         sw_line,  # 水位曲线
            #         kr_line,  # 库容曲线 v
            #         dd_table,  # 调度线
            #         flmb_table,  # 放流目标表 下泄
            #
            #         bxsw_line,  # 坝下水位 曲线
            #         bxll_line,  # 坝下流量 曲线
            #     )
            # else:
            (dxsk_SKGS0, ZF, SL, qs, V2, V3, jh, GS0, dxsk_ques, df2) = shuiku_zxx_dxsk(
                V0, dxsk,
                zxxsk_ques,
                Vx, Vxx, Vdead,
                v_hcgsk, m_hcgsk, zf, sl  # 暂时使用之前的数据
                # 蒸发、渗透、面积 需要读取水库表的表 todo 每个区对应哪个水库？
            )

            # 大型水库平衡如果有缺水
            if dxsk_ques.any() > 0:
                print('-' * 50)
                print('干流过境水供需分析')
                # 大型水库平衡如果有缺水
                # 计算 干流过境水供需分析 使用 河道径流平衡   返回是否有缺水
                # 地下需水做成0的
                # 来水一直都是表中输入的来水
                # 缺水是上层计算的缺水
                # todo 过境水供水-> 调用径流计算函数（上区来水，上次计算缺水，供水），输出缺水
                # todo 这一层只输入了上去来水，没输入“供水”，是不是有问题？
                (glgj_dx_gs16, glgj_gs, ls17, glgj_que) = jlph_fun(sqls, dxsk_ques, di_xia_xu_shui_zero)

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
                        dxsk_SKGS0,  # 大型水库
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
                        dxsk_SKGS0,  # 大型水库
                        glgj_gs,  # 过境水
                        gs_zero,  # 外调水
                        hgxs,  # 回归水系数

                        xu_shui,  # 输入的需水
                        bqjl,  # 本区径流
                        sqls,  # 上区来水
                        wds,  # 输入的外调水
                    )


            else:

                #  大型水库平衡没有缺水  统计供水、回归水、弃水、保证率输出
                # 过境水、外调水 的供水都 为0矩阵
                cjs = tj(
                    dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
                    GS17,  # 本区地表
                    zxx_SKGS0,  # 中小水库
                    dxsk_SKGS0,  # 大型水库
                    gs_zero,  # 过境水
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

# 计算一个列表里的所有二维np数组的和，并返回
def hebing(hebing_cjs):
    sum_matrices =sum(hebing_cjs)
    return sum_matrices
