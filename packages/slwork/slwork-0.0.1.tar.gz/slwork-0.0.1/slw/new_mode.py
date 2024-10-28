from slw.add_code import *
from slw.lhy_func import *
from slw.prepare_data import *

from slw.slw_const import *

import pandas as pd
import numpy as np

from slw.caluate_func_lrh import *

columns_arr = ['城镇生活', '农村生活', '牲畜', '三产', '火核电', '一般工业', '高耗水工业', '建筑业',
               '水田', '水浇地', '菜田', '林果地', '草场', '鱼塘', '城镇生态', '湿地']




def moshi4(
        exl_name,
        sheet_name,
        k,  # 径流划分系数
        Vx,
        Vxx,
        Vdead,
        hgxs,
):
    # 模式4  分区计算流程

    # 准备读取表格，获取需要的数据
    (sqls, xu_shui, di_xia_xu_shui, zxskjl, dxsk, wds,read_exl,phxs,bqjl,
     hdjl,  # 河道径流
     ) = prepare_moshi4_data(
        exl_name, sheet_name,
        k,
    )

    # 计算破坏后需水
    # 需水_破坏后
    xs_phh=xs_phxs(xu_shui,phxs)


    # 计算 河道径流平衡   返回是否有缺水
    # dx_gs16, GS17, ls17, ques16 = jlph_fun(sqls, xs_phh, di_xia_xu_shui)
    dx_gs16, GS17, ls17, ques16 = jlph_fun(hdjl, xs_phh, di_xia_xu_shui)



    # ls 就是 zxskjl 的
    # xs 就是 上一层的缺水

    # 暂时不考虑是否缺水，现在的计算缺水都为0，以后看如果有误再找问题，先跑通过程

    # Vx, Vxx, Vdead = 7667.00, 7049.00, 80.00
    V0 = Vx

    # shuiku_zxx_dxsk 没分行业，但是计算了 蒸发、渗透、面积，最后需要输出
    # shuikuGS_16 分行业了但是没计算  蒸发、渗透、面积，就有v,m,z,s 的时候再调用 shuikuGS_16 返回蒸发吧
    # 中小型水库
    (zxx_SKGS0, ZF, SL, qs, V2, V3, jh, GS0, zxxsk_ques, df2) = shuiku_zxx_dxsk(
        V0, zxskjl,
        ques16, Vx, Vxx, Vdead,
        None, None, None, None)


    # 大型水库平衡，和中小型水库平衡 一个函数，但是包括 蒸发、渗透、面积

    # 根据现在的数据长度来填充m,sl
    shape_num = dxsk.shape[0]
    zf = zf_hcgsk.reindex(range(shape_num), fill_value=0)
    sl = sl_hcgsk.reindex(range(shape_num), fill_value=0)

    (dxsk_SKGS0, ZF, SL, qs, V2, V3, jh, GS0, dxsk_ques, df2) = shuiku_zxx_dxsk(
        V0, dxsk,
        zxxsk_ques,
        Vx, Vxx, Vdead,
        v_hcgsk, m_hcgsk, zf, sl  # 暂时使用之前的数据
        # 蒸发、渗透、面积 需要读取水库表的表 todo 每个区对应哪个水库？
        )

    # # list 转 numpy
    # dxsk_ques=np.array(QS0)
    # 地下需水做成0的np 使用 zeros 创建一个形状相同的全零数组
    # astype ，np.zeros转换不能转换float，用astype转换成int再生成全0数组

    # 一维转二维
    # dxsk_ques = dxsk_ques.reshape(dxsk_ques.shape[0], 1)

    di_xia_xu_shui_zero = np.zeros_like(di_xia_xu_shui)

    # 大型水库平衡如果有缺水
    # 计算 干流过境水供需分析 使用 河道径流平衡   返回是否有缺水
    # 地下需水做成0的
    # 来水一直都是表中输入的来水
    # 缺水是上层计算的缺水
    # todo 过境水供水-> 调用径流计算函数（上区来水，上次计算缺水，供水），输出缺水
    # todo 这一层只输入了上去来水，没输入“供水”，是不是有问题？
    (dx_gs16, glgj_gs, ls17, glgj_que) = jlph_fun(sqls, dxsk_ques, di_xia_xu_shui_zero)

    # 计算 外调水供需分析 使用 河道径流平衡   返回是否有缺水
    # 地下需水做成0的
    # 来水一直都是表中输入的 外调水 wds
    # 缺水是上层计算的缺水
    (dx_gs16, wdgs_gs, ls17, wdgs_que) = jlph_fun(wds, glgj_que, di_xia_xu_shui_zero)



    # 创建一个和上区来水一样格式的0矩阵，用于统计的时候没有 过境水+外调水 的时候引用
    sqls_zero = np.zeros_like(sqls)

    #     统计供水、回归水、弃水、保证率输出
    (gs, hgs, qs, bzl) = tj(
        dx_gs16,  # 地下水  地下水供水 =河道平衡的时候返回的地下供水
        GS17,  # 本区地表
        zxx_SKGS0,  # 中小水库
        dxsk_SKGS0,  # 大型水库
        glgj_gs,  # 过境水
        wdgs_gs,  # 外调水
        hgxs,  # 回归水系数
        wdgs_que, # 最后的缺水
        read_exl,# 所有输入的值
        xu_shui,# 输入的需水
        bqjl,# 本区径流
        sqls,  # 上区来水
        wds,#输入的外调水
    )

    #------------------------------------------------------------------------------------
    # # 判断是否有缺水
    # # todo 缺水是怎么判断的  是总和大于零？
    # # todo 计算的不管怎么改数据都没有缺水，以后看哪里计算出错
    # 还是要按照流程，河道径流计算 没缺水了，就得直接统计了
    # if (ques16 > 0).any():
    # # if ques16.any() > 0:
    #     print('1111111111111111111')
    #     # 是 中小水库平衡计算   不需要差值
    #
    #     # V0: 初始库容
    #     # L: 来水
    #     # xs: 需水
    #     # Vx: 兴利库容
    #     # Vxx: 汛限库容
    #     # Vdead: 死库容  不一样，以后重新调用,暂时引用之前的
    #     # v: 体积
    #     # m: 面积
    #     # Z: 蒸发
    #     # S: 渗漏
    #     V0 = Vx
    #     (gs, ZF, SL, qs, V2, V3, jh, GS0, zxxsk_ques, df2) = shuiku_zxx_dxsk(
    #         V0, zxskjl,
    #         ques16, Vx, Vxx, Vdead,
    #         None, None, None, None)
    #
    #     if zxxsk_ques.any() > 0:
    #         # 大型水库调节计算  需要差值  面积需要差值计算
    #         # 大型水库平衡，和中小型水库平衡 一个函数，但是包括 蒸发、渗透、面积
    #
    #         # 根据现在的数据长度来填充m,sl
    #         shape_num = dxsk.shape[0]
    #         zf = zf_hcgsk.reindex(range(shape_num), fill_value=0)
    #         sl = sl_hcgsk.reindex(range(shape_num), fill_value=0)
    #
    #         (gs, ZF, SL, qs, V2, V3, jh, GS0, dxsk_ques, df2) = shuiku_zxx_dxsk(
    #             V0, dxsk,
    #             zxxsk_ques,
    #             Vx, Vxx, Vdead,
    #             v_hcgsk, m_hcgsk, zf, sl  # 暂时使用之前的数据
    #             # 蒸发、渗透、面积 需要读取水库表的表 todo 每个区对应哪个水库？
    #         )
    #
    #         # 大型水库平衡如果有缺水
    #         if dxsk_ques.any() > 0:
    #             # 计算 干流过境水供需分析 使用 河道径流平衡   返回是否有缺水
    #             # 地下需水做成0的
    #             # 来水一直都是表中输入的来水
    #             # 缺水是上层计算的缺水
    #             # todo 过境水供水-> 调用径流计算函数（上区来水，上次计算缺水，供水），输出缺水
    #             # todo 这一层只输入了上区来水，没输入“供水”，是不是有问题？
    #
    #             # 准备数据 list 转 numpy
    #             # dxsk_ques=np.array(QS0)
    #             # 地下需水做成0的np 使用 zeros 创建一个形状相同的全零数组
    #             # astype ，np.zeros转换不能转换float，用astype转换成int再生成全0数组
    #             di_xia_xu_shui_zero = np.zeros(dxsk_ques.astype(int))
    #             # 一维转二维
    #             dxsk_ques = dxsk_ques.reshape(dxsk_ques.shape[0], 1)
    #             di_xia_xu_shui_zero = di_xia_xu_shui_zero.reshape(di_xia_xu_shui_zero.shape[0], 1)
    #
    #             (dx_gs16, gs16, ls17, glgj_que) = jlph_fun(sqls, dxsk_ques, di_xia_xu_shui_zero)
    #
    #             # 干流过境水供需分析 如果还有缺水
    #             if glgj_que.any() > 0:
    #                 # 计算 外调水供需分析 使用 河道径流平衡   返回是否有缺水
    #                 # 地下需水做成0的
    #                 # 来水一直都是表中输入的来水
    #                 # 缺水是上层计算的缺水
    #                 (dx_gs16, gs16, ls17, ques16) = jlph_fun(sqls, glgj_que, di_xia_xu_shui_zero)
    #
    #                 # 最后计算这个返回的缺水的 缺水旬数
    #
    #                 #     统计供水、回归水、弃水、保证率输出
    #                 (gs, hgs, qs, bzl) = tj(
    #                     di_xia_xu_shui,  # 地下水  地下水供水=地下水需水
    #                     sqls,  # 本区地表
    #                     zxskjl,  # 中小水库
    #                     dxsk,  # 大型水库
    #                     sqls_zero,  # 过境水
    #                     sqls_zero,  # 外调水
    #                     hgxs,  # 回归水系数
    #                     wdgs_que,  # 最后的缺水
    #                     read_exl,  # 所有输入的值
    #                     xu_shui,  # 输入的需水
    #                     bqjl,  # 本区径流
    #                     sqls,  # 上区来水
    #                 )
    #             else:
    #
    #                 #     统计供水、回归水、弃水、保证率输出
    #
    #                 (gs, hgs, qs, bzl) = tj(
    #                     di_xia_xu_shui,  # 地下水  地下水供水=地下水需水
    #                     sqls,  # 本区地表
    #                     zxskjl,  # 中小水库
    #                     dxsk,  # 大型水库
    #                     sqls_zero,  # 过境水
    #                     sqls_zero,  # 外调水
    #                     hgxs,  # 回归水系数
    #                     wdgs_que,  # 最后的缺水
    #                     read_exl,  # 所有输入的值
    #                     xu_shui,  # 输入的需水
    #                     bqjl,  # 本区径流
    #                     sqls,  # 上区来水
    #                 )
    #
    #
    #         else:
    #
    #             (gs, hgs, qs, bzl) = tj(
    #                 di_xia_xu_shui,  # 地下水  地下水供水=地下水需水
    #                 sqls,  # 本区地表
    #                 zxskjl,  # 中小水库
    #                 dxsk,  # 大型水库
    #                 sqls_zero,  # 过境水
    #                 sqls_zero,  # 外调水
    #                 hgxs,  # 回归水系数
    #                 wdgs_que,  # 最后的缺水
    #                 read_exl,  # 所有输入的值
    #                 xu_shui,  # 输入的需水
    #                 bqjl,  # 本区径流
    #                 sqls,  # 上区来水
    #             )
    #
    #     else:
    #         #     统计供水、回归水、弃水、保证率输出
    #                 (gs, hgs, qs, bzl) = tj(
    #                     di_xia_xu_shui,  # 地下水  地下水供水=地下水需水
    #                     sqls,  # 本区地表
    #                     zxskjl,  # 中小水库
    #                     dxsk,  # 大型水库
    #                     sqls_zero,  # 过境水
    #                     sqls_zero,  # 外调水
    #                     hgxs,  # 回归水系数
    #                     wdgs_que,  # 最后的缺水
    #                     read_exl,  # 所有输入的值
    #                     xu_shui,  # 输入的需水
    #                     bqjl,  # 本区径流
    #                     sqls,  # 上区来水
    #                 )





    # else:
    #     #     统计供水、回归水、弃水、保证率输出
    #
    #     (gs, hgs, qs, bzl) = tj(
    #         di_xia_xu_shui,  # 地下水  地下水供水=地下水需水
    #         sqls,  # 本区地表
    #         zxskjl,  # 中小水库
    #         dxsk,  # 大型水库
    #         sqls_zero,  # 过境水
    #         sqls_zero,  # 外调水
    #         hgxs,  # 回归水系数
    #         wdgs_que,  # 最后的缺水
    #         read_exl,  # 所有输入的值
    #         xu_shui,  # 输入的需水
    #         bqjl,  # 本区径流
    #         sqls,  # 上区来水
    #     )

