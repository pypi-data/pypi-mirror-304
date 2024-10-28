import pandas as pd
import numpy as np
from slw.lhy_func import *
# from slw.slw_const import *
from slw.slw_const import *
from slw.add_code import *
# from xx_0 import bzlsc
from pathlib import Path

# 年月日的列 pandas dataframe 格式
g_year=None
g_xun=None
g_day=None

# 当前分区的文件夹的路径
# fenqu_file_path='C:\\Users\\Administrator\\Desktop\\slwork_function\\data_base\\xx_files\\七台河市\\莲花水库以下\\莲花水库以下七台河市'
fenqu_file_path=''

def jlph_fun(lai_shui, xu_shui, di_xia_xu_shui):
    '''
    计算 河道径流平衡   返回是否有缺水

    raw: 暂时只考虑了地表水，地下水 ，地下水供水=地下水需水

    bk: 计算供水量
    :param lai_shui: 来水
    :param xu_shui:  需水
    :param zong_xu_shui: 总需水
    :param di_xia_xu_shui: 地下需水
    :param ss: 农业破坏系数
    :return:

    计算全部类型
    城镇生活	农村生活	牲畜	三产	火核电	一般工业	高耗水工业	建筑业	水田	水浇地	菜田	林果地	草场	鱼塘	城镇生态	湿地	需水
    '''
    # print('------------lai_shui')
    # print(lai_shui)
    # print(lai_shui.shape)

    # 输入的来水，需水需要是二维numpy
    assert lai_shui.shape[1] == 1
    assert xu_shui.ndim == 2
    assert di_xia_xu_shui.ndim == 2

    xs1 = xu_shui[:, :1]  # 所有行的第一列数据

    xs2 = xu_shui[:, 1:2]  # 所有行的第二列数据

    xs3 = xu_shui[:, 2:3]
    xs4 = xu_shui[:, 3:4]
    xs5 = xu_shui[:, 4:5]
    xs6 = xu_shui[:, 5:6]
    xs7 = xu_shui[:, 6:7]
    xs8 = xu_shui[:, 7:8]
    xs9 = xu_shui[:, 8:9]
    xs10 = xu_shui[:, 9:10]
    xs11 = xu_shui[:, 10:11]
    xs12 = xu_shui[:, 11:12]
    xs13 = xu_shui[:, 12:13]
    xs14 = xu_shui[:, 13:14]
    xs15 = xu_shui[:, 14:15]
    xs16 = xu_shui[:, 15:16]

    dx_xs1 = di_xia_xu_shui[:, :1]
    dx_xs2 = di_xia_xu_shui[:, 1:2]
    dx_xs3 = di_xia_xu_shui[:, 2:3]
    dx_xs4 = di_xia_xu_shui[:, 3:4]
    dx_xs5 = di_xia_xu_shui[:, 4:5]
    dx_xs6 = di_xia_xu_shui[:, 5:6]
    dx_xs7 = di_xia_xu_shui[:, 6:7]
    dx_xs8 = di_xia_xu_shui[:, 7:8]
    dx_xs9 = di_xia_xu_shui[:, 8:9]
    dx_xs10 = di_xia_xu_shui[:, 9:10]
    dx_xs11 = di_xia_xu_shui[:, 10:11]
    dx_xs12 = di_xia_xu_shui[:, 11:12]
    dx_xs13 = di_xia_xu_shui[:, 12:13]
    dx_xs14 = di_xia_xu_shui[:, 13:14]
    dx_xs15 = di_xia_xu_shui[:, 14:15]
    dx_xs16 = di_xia_xu_shui[:, 15:16]

    dx_gs1, gs1, ls2, ques1 = calc_laishui(dx_xs1, lai_shui, xs1)
    dx_gs2, gs2, ls3, ques2 = calc_laishui(dx_xs2, ls2, xs2)
    dx_gs3, gs3, ls4, ques3 = calc_laishui(dx_xs3, ls3, xs3)
    dx_gs4, gs4, ls5, ques4 = calc_laishui(dx_xs4, ls4, xs4)
    dx_gs5, gs5, ls6, ques5 = calc_laishui(dx_xs5, ls5, xs5)
    dx_gs6, gs6, ls7, ques6 = calc_laishui(dx_xs6, ls6, xs6)
    dx_gs7, gs7, ls8, ques7 = calc_laishui(dx_xs7, ls7, xs7)
    dx_gs8, gs8, ls9, ques8 = calc_laishui(dx_xs8, ls8, xs8)
    dx_gs9, gs9, ls10, ques9 = calc_laishui(dx_xs9, ls9, xs9)
    dx_gs10, gs10, ls11, ques10 = calc_laishui(dx_xs10, ls10, xs10)
    dx_gs11, gs11, ls12, ques11 = calc_laishui(dx_xs11, ls11, xs11)
    dx_gs12, gs12, ls13, ques12 = calc_laishui(dx_xs12, ls12, xs12)
    dx_gs13, gs13, ls14, ques13 = calc_laishui(dx_xs13, ls13, xs13)
    dx_gs14, gs14, ls15, ques14 = calc_laishui(dx_xs14, ls14, xs14)
    dx_gs15, gs15, ls16, ques15 = calc_laishui(dx_xs15, ls15, xs15)
    dx_gs16, gs16, ls17, ques16 = calc_laishui(dx_xs16, ls16, xs16)


    # print(ques1)
    # print(ques1.shape)



    HJQUES = ques1 + ques2 + ques3 + ques4 + ques5 + ques6 + ques7 + ques8 + ques9 + ques10 + ques11 + ques12 + ques13 + ques14 + ques15 + ques16

    (HJQUES1, HJQUES2, QS1,QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9,
     QS10, QS11, QS12, QS13, QS14, QS15, QS16) = trans_pd(
         ques1,ques2, ques3, ques4, ques5, ques6, ques7,
        ques8, ques9,ques10, ques11, ques12, ques13, ques14, ques15, ques16,HJQUES,'缺水合计')

    QS17 = pd.concat(
        [QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16],
        axis=1
    )
    QS17 = np.array(QS17)

    HJGS = gs1 + gs2 + gs3 + gs4 + gs5 + gs6 + gs7 + gs8 + gs9 + gs10 + gs11 + gs12 + gs13 + gs14 + gs15 + gs16
    (HJGS1, HJGS2, GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9,
     GS10, GS11, GS12, GS13, GS14, GS15, GS16) = trans_pd(
        gs1,gs2, gs3, gs4, gs5, gs6, gs7,
        gs8, gs9, gs10, gs11, gs12, gs13, gs14, gs15, gs16, HJGS, '地表水供水合计')
    # gs16 供水 =本区地表
    GS17 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16], axis=1)
    GS17 = np.array(GS17)




    (HJDXGS1, HJDXGS2, DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8,
     DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15, DXGS16) = trans_pd(
        dx_gs1,
        dx_gs2, dx_gs3, dx_gs4, dx_gs5, dx_gs6, dx_gs7,
        dx_gs8, dx_gs9, dx_gs10, dx_gs11, dx_gs12, dx_gs13, dx_gs14, dx_gs15, dx_gs16, HJQUES, '地下水供水合计')

    DXGS17 = pd.concat(
        [DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8, DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15,
         DXGS16], axis=1)

    DXGS17 = np.array(DXGS17)
    return DXGS17, GS17, ls17, QS17
    # return zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1, HJDXGS1, GS178, DXGS178, QS178, XS17, XS16, zdxxs


def calc_laishui(dx_xs2, ls2, xs2):
    gs2 = np.where(ls2 >= xs2, xs2, np.where(ls2 >= 0, ls2, 0))
    ques2 = np.where(ls2 >= xs2, 0, np.where(ls2 >= 0, xs2 - ls2, 0))
    qis2 = np.where(ls2 >= xs2, ls2 - xs2, 0)
    dx_gs2 = dx_xs2
    # 暂时不计算回归水，在最后计算
    # hgs2 = gs2 * dbhgsxs2  #dbhgsxs2 回归水系数
    # dx_hgs2 = dx_gs2 * dxhgsxs2
    # zhgs2 = hgs2 + dx_hgs2
    ls3 = qis2
    return dx_gs2, gs2, ls3, ques2
    # return dx_gs2, dx_hgs2, gs2, hgs2, ls3, ques2, zhgs2

def dict_add(d,key):
    if key not in d:
        d[key] = 0
    d[key] = d[key] + 1
    return d


def BZL_new(que_np):
    # 结果是16个分行业16个数

    # 保证率计算公式：前8项，保证率=1-缺水旬数量/2196；后八项，保证率=1-缺水年数/61
    # 缺水旬数，缺水量大于0的数据统计旬数
    # 缺水年数，按照每36旬统计一次，大于0的，统计为缺水年数
    # que_new_pd=pd.DataFrame(que_np)
    # que_new_pd=que_new_pd.set_axis(columns_arr, axis='columns')
    # que=pd.concat([g_year, g_xun, g_day, que_new_pd], axis=1)
    # 当前遍历的年
    now_year=0
    # 缺水旬数量
    que_xun=0
    # 缺水年数
    que_year=0

    # 缺水前8列
    que_1_8=que_np[:,:8]
    # 缺水后8列
    que_8_16=que_np[:,-8:]
    # 缺水旬数量、缺水年数字典
    que_xun_year={}
    # 当前计算的列的值
    list_n=1

    # 计算前8列
    for coluumn in que_1_8.T:
        for i in coluumn:
            if i>0:
                # 缺水旬+1
                dict_add(que_xun_year,list_n)
                # que_xun_year[list_n]+=1
        # 下一列
        list_n+=1


    # 记录当前年是否有计数
    now_year_if=0
    # 记录当前行数
    row_xun=1
    # 计算前后8列
    for coluumn in que_8_16.T:
        for i in coluumn:
            if i>0:
                if now_year_if==0:
                    now_year_if=1
                else:
                    pass
            # 如果当前循环到了36一个循环，就是一个年的结束
            if row_xun==36:
                if now_year_if==1:
                    # 缺水年+1
                    dict_add(que_xun_year,list_n)
                    # que_xun_year[list_n]+=1
                #  旬的循环回到1，新一年重新记录
                row_xun=1
            else:
                # 旬+1
                row_xun+=1
        # 列数+1
        list_n+=1

    bzl=[]
    print(que_xun_year)
    for i in que_xun_year:
        print(i,que_xun_year[i])
        if i<=8:
            b_answer=1-que_xun_year[i]/2196
            bzl.append(b_answer)
        else:
            b_answer=1-que_xun_year[i]/61
            bzl.append(b_answer)

    print(bzl)
    bzl=np.array(bzl)
    bzl = bzl.reshape(bzl.shape[0], 1)
    return bzl


def tj(
        dxs,  # 地下水
        bqdb,  # 本区地表
        zzxsk,  # 中小水库
        dxsk,  # 大型水库
        gjs,  # 过境水
        wds,  # 外调水
        hgsxs,  # 回归水系数
        ques, # 最后的缺水
        input_df,# 所有输入的值
        xu_shui,# 输入的需水
        bqjl,# 本区径流
        sqls,# 上区来水
        wds_shuru,#输入的外调水
):
        # g_year, g_xun, g_day,
    # 大型水库等供水需要输出表，16个分行业都是一样的数

    #     统计供水、回归水、弃水、保证率输出

    # --------------------------------合计供水------------------------------------
    #  “供水合计” 就是最后统计要输出的“统计供水”
    # 地下水+本区地表+中小水库+大型水库+过境水+外调水=供水合计
    # 地下水  就是输入的“地下水供水”
    #     todo 本区地表 是本区径流吧？
    # 本区地表 过境水 外调水 是不是都是“计算 河道径流平衡”时 的来水
    hjgs = dxs + bqdb + zzxsk + dxsk + gjs + wds
    #  总供水，用 供水合计 的合计 计算每行的总和，并将结果组成一列
    hjgs_sums = hjgs.sum(axis=1)
    # hjgs_sums = hjgs_sums.reshape(hjgs_sums.shape[0], 1)
    hjgs_pd=pd.DataFrame(hjgs)
    hjgs_pd=hjgs_pd.set_axis(columns_arr, axis='columns')
    hjgs_sums_pd=pd.DataFrame(hjgs_sums)
    hjgs_sums_pd = hjgs_sums_pd.set_axis(['合计'], axis='columns')

    hjgs_shuchu = pd.concat([g_year,g_xun,g_day,hjgs_pd,hjgs_sums_pd ], axis=1)  # 按列合并
    #  输出 合计供水
    shuchu_exl('合计供水',hjgs_shuchu)



    # -------------------------------保证率---------------------------------------
    #缺水=需水-供水   按此缺水统计保证率
    # 这个需水用的是计算破坏系数之前的需水，供水是计算好的合计供水
    que_new=xu_shui-hjgs

    bzl=BZL_new(que_new)
    bzl_pd = pd.DataFrame(bzl.T)
    bzl_pd = bzl_pd.set_axis(columns_arr, axis='columns')
    #  输出 exl
    shuchu_exl('保证率',bzl_pd)

    # -------------------------------总回归水---------------------------------------
    #      各行业供水*回归水系数=回归水
    #      ’各行业供水‘是’供水合计‘

    #  回归系数  hgsxs先转置，然后复制这一行hgsxs.T，以产生和hjgs行相同的矩阵
    hgsxs_copy = np.tile(hgsxs.T, (hjgs.shape[0], 1))


    hgs = hjgs * hgsxs_copy
    hgs_pd = pd.DataFrame(hgs)
    hgs_pd = hgs_pd.set_axis(columns_arr, axis='columns')

    # hgs_pd = pd.concat([hgs_pd, g_year], axis=0)  # 按行合并
    hgs_pd = pd.concat([g_year,g_xun,g_day,hgs_pd ], axis=1)  # 按列合并
    #  输出 总回归水
    shuchu_exl('总回归水',hgs_pd)

    # ----------------------------------------出境水=弃水-------------------------------------------------
    # 出境水=弃水 = 本区径流 + 上区来水 + 外调水 + 总回归水的16分行业总和 -（总供水 - 地下水供水）
    # 出境水 = 本区径流 + 上区来水 + 外调水 + 地下水回归 + 地表水回归水 -（总供水 - 地下水供水）
    # 总供水 =hjgs
    #     外调水 输入的外调水
    # # 创建一个和bqdb形状相同，数值为hgxs_hj的新矩阵
    # hgxs_hj_np = np.full(bqdb.shape, hgxs_hj)
    # # print(hgxs_hj_np)

    #  地下水供水 地下供水总和
    dxgs_sums = dxs.sum(axis=1)
    #  总回归水
    hgs_sums = hgs.sum(axis=1)
    hgs_sums = hgs_sums.reshape(hgs_sums.shape[0], 1)


    hjgs_sums = hjgs_sums.reshape(hjgs_sums.shape[0], 1)
    dxgs_sums = dxgs_sums.reshape(dxgs_sums.shape[0], 1)

    # bqjl = bqjl.reshape(bqjl.shape[0], 1)

    # print('---------------------bqjl')
    # print(bqjl.shape)
    # print(type(bqjl))
    # print('---------------------sqls')
    # print(sqls.shape)
    # print(type(sqls))
    # print('---------------------wds')
    # print(wds.shape)
    # print(type(wds))
    # print('---------------------hgs_sums')
    # print(hgs_sums.shape)
    # print(type(hgs_sums))
    # print('---------------------hjgs_sums')
    # print(hjgs_sums.shape)
    # print(type(hjgs_sums))
    # print('---------------------dxgs_sums')
    # print(dxgs_sums.shape)
    # print(type(dxgs_sums))


    cjs=bqjl+sqls+wds_shuru+hgs_sums-(hjgs_sums-dxgs_sums)

    cjs_pd = pd.DataFrame(cjs)
    cjs_pd = cjs_pd.set_axis(['出境水'], axis='columns')
    cjs_shuchu = pd.concat([g_year, g_xun, g_day, cjs_pd], axis=1)  # 按列合并
    #  输出 合计供水
    shuchu_exl('出境水', cjs_shuchu)




    # ----------------------------------------地下水供水-------------------------------------------------
    # 地下水供水=地下水需水
    dxs_pd = pd.DataFrame(dxs)
    dxs_pd = dxs_pd.set_axis(columns_arr, axis='columns')
    dxs_shuchu = pd.concat([g_year, g_xun, g_day, dxs_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl('地下水供水', dxs_shuchu)


    # ----------------------------------------本区地表供水-------------------------------------------------
    # todo 本区地表供水 是不是河道径流？还是上区来水？
    # 使用np.repeat沿着第二维（列）方向复制每一行16次
    bqdb_16 = np.repeat(bqdb[:, 0:1], 16, axis=1)
    bqdb_pd = pd.DataFrame(bqdb_16)
    bqdb_pd = bqdb_pd.set_axis(columns_arr, axis='columns')
    bqdb_shuchu = pd.concat([g_year, g_xun, g_day, bqdb_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl('本区地表供水', bqdb_shuchu)

    # ----------------------------------------中小水库供水-------------------------------------------------
    # 使用np.repeat沿着第二维（列）方向复制每一行16次
    zzxsk_16 = np.repeat(zzxsk[:, 0:1], 16, axis=1)
    zzxsk_pd = pd.DataFrame(zzxsk_16)
    zzxsk_pd = zzxsk_pd.set_axis(columns_arr, axis='columns')
    zzxsk_shuchu = pd.concat([g_year, g_xun, g_day, zzxsk_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl('中小水库供水', zzxsk_shuchu)

    # ----------------------------------------大型水库供水-------------------------------------------------
    # 使用np.repeat沿着第二维（列）方向复制每一行16次
    dxsk_16 = np.repeat(dxsk[:, 0:1], 16, axis=1)
    dxsk_pd = pd.DataFrame(dxsk_16)
    dxsk_pd = dxsk_pd.set_axis(columns_arr, axis='columns')
    dxsk_shuchu = pd.concat([g_year, g_xun, g_day, dxsk_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl('大型水库供水', dxsk_shuchu)

    # ----------------------------------------过境水供水-------------------------------------------------
    # 使用np.repeat沿着第二维（列）方向复制每一行16次
    gjs_16 = np.repeat(gjs[:, 0:1], 16, axis=1)
    gjs_pd = pd.DataFrame(gjs_16)
    gjs_pd = gjs_pd.set_axis(columns_arr, axis='columns')
    gjs_shuchu = pd.concat([g_year, g_xun, g_day, gjs_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl( '过境水供水', gjs_shuchu)

    # ----------------------------------------外调水供水-------------------------------------------------
    # 使用np.repeat沿着第二维（列）方向复制每一行16次
    wds_16 = np.repeat(wds[:, 0:1], 16, axis=1)
    wds_pd = pd.DataFrame(wds_16)
    wds_pd = wds_pd.set_axis(columns_arr, axis='columns')
    wds_shuchu = pd.concat([g_year, g_xun, g_day, wds_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl( '外调水供水', wds_shuchu)





    # xu_shui_hj=xu_shui.sum(axis=1)
    # xu_shui_hj=pd.DataFrame(xu_shui_hj)
    # prepare_shuchudata(
    #     input_df,  #输入值的全部df
    #     xu_shui_hj,# 需水 合计
    #     hgs_pd,# 回归水
    # )


    gs = 1
    hgs = 1
    qs = 1
    bzl = 1
    return (gs, hgs, qs, bzl)

# 按照输出的大表来输出一个表，太费劲
def prepare_shuchudata(
        input_df,  #输入值的全部df
        xu_shui_hj,# 需水 合计
        hgs_pd,# 回归水
         ):
    # 删除第2列到第8列，这里使用iloc进行基于位置的索引
    input_0 = input_df.iloc[1:, :23]
    read_exl = load_pd_data("输入系列值","输出格式", index_col=False, usecols=None)
    # print(read_exl.columns)
    # print(read_exl.head(1))
    # input_0.columns = read_exl.columns+input_0.columns

    # 获取df的第二行
    row_to_add = read_exl.iloc[1]
    # 将第二行添加到df2的最前面
    read_exl =  pd.concat([pd.DataFrame(row_to_add).T, read_exl], ignore_index=True)

    shuchu_pd = pd.concat([
                            input_0,
                           xu_shui_hj,
                           hgs_pd,
                           ], axis=1)  # 按列合并
    # print(read_exl)



def shuchu_exl(exl_name, data):
    # 同名表如果存在就覆盖
    f_path=Path(f'{fenqu_file_path}/输出_{exl_name}.xlsx')
    with pd.ExcelWriter(f_path, engine='openpyxl',
    # with pd.ExcelWriter(f'xx_result/{exl_name}.xlsx', engine='openpyxl',
                        mode='w',#追加模式,不覆盖其他文件
                        ) as writer:
                        # mode='a',#追加模式,不覆盖其他文件
                        # if_sheet_exists='replace'
                        # ) as writer:
        #                 todo 输出一个表是一个文件，都存在xx_file 对应位置里
        data.to_excel(writer, sheet_name='sheet1',index=False)
# def shuchu_exl(exl_name, sheet_name, data):
#     # 同名表如果存在就覆盖
#     with pd.ExcelWriter(f'xx_result/{exl_name}.xlsx', engine='openpyxl',
#                         mode='w',#追加模式,不覆盖其他文件
#                         ) as writer:
#                         # mode='a',#追加模式,不覆盖其他文件
#                         # if_sheet_exists='replace'
#                         # ) as writer:
#         #                 todo 输出一个表是一个文件，都存在xx_file 对应位置里
#         data.to_excel(writer, sheet_name=sheet_name,index=False)


# def shuiku_zxx_dxsk(V0, L, xs,  Vx, Vxx, Vdead, v, m, Z, S):
def shuiku_zxx_dxsk(V0, L,
                    xs_fhy,#分行业的缺水 需水
                    Vx, Vxx, Vdead, v, m, Z, S,):
    '''
    # 水库供水只考虑了总供水，未分行业

    中小型水库计算 不包括蒸发、渗透、面积
    大型水库计算包括蒸发、渗透、面积

    bk:
    V0: 初始库容
    L: 来水
    xs: 需水
    Vx: 兴利库容
    Vxx: 汛限库容
    Vdead: 死库容
    v: 体积
    m: 面积
    Z: 蒸发
    S: 渗漏
    '''

    assert type(g_xun) == pd.core.series.Series


    xs= xs_fhy.sum(axis=1)

    # 表格的行数，动态获取
    Llength = L.shape[0]

    GS0 = []
    QS0 = []  # 应该是缺水
    df2 = pd.DataFrame()

    for i in range(0, Llength):
        # for i in range(0, 732):

        V2 = V0 + L[i] - xs[i]  # L.loc[i] 可以读取0  12282.19

        assert V2.shape == (1,)

        if (g_xun[i] >= 18 and g_xun[i] <= 27):
            # if (g_xun[i] >= 6 and g_xun[i] <= 9):
            Vm = Vxx
        else:
            Vm = Vx
        if V2 >= Vm:
            V2 = Vm
        else:
            V2 = V2
        if V2 <= Vdead:
            V2 = Vdead
        V1 = (V2 + V0) / 2

        if v is not None:

            mj = Chazhi(v, m, V1)  # 由库容求面积

            ZF = mj * Z[i] / 10  # 蒸发
            SL = mj * S[i] / 10  # 渗漏
        else:
            mj = 0
            ZF = 0
            SL = 0
        V3 = L[i] + V0 - ZF - SL
        if V3 <= 0:
            V3 = V3 + ZF + SL

            ZF = 0
            SL = 0
            # V0 = V3
            qs = [0]
            gs = 0
        else:
            V4 = V3 - Vdead
            if V4 <= 0:
                gs = 0
                qs = [0]
            else:
                V5 = V4 - xs[i]
                if V5 >= 0:
                    gs = xs[i]
                    V5 = V5
                else:
                    gs = V5 + xs[i]
                    V5 = 0
                V3 = V5 + Vdead

            if V3 >= Vm:
                qs = V3 - Vm
                V3 = Vm
            elif V3 <= Vdead:
                qs = [0]
                V3 = Vdead  # 没用死库容控制下限，用的是扣除蒸发的，如果到死库容不考虑蒸发， V3=Vdead
            else:
                qs = [0]
                V3 = V3

        gs = 0
        V0 = V3

    for i in range(0, Llength):
        V2 = V0 + L[i] - xs[i]
        if (g_xun[i] >= 18 and g_xun[i] <= 27):
            # if (g_xun[i] >= 6 and g_xun[i] <= 9):  #todo：月改成旬的话，怎么计算
            Vm = Vxx
        else:
            Vm = Vx

        if V2 >= Vm:
            V2 = Vm
        else:
            V2 = V2
        if V2 <= Vdead:
            V2 = Vdead
        V1 = (V2 + V0) / 2

        if v is not None:
            mj = Chazhi(v, m, V1)  # 由库容求面积

            ZF = mj * Z[i] / 10  # 蒸发
            SL = mj * S[i] / 10  # 渗漏
        else:
            mj = 0
            ZF = 0
            SL = 0
        V3 = L[i] + V0 - ZF - SL
        if V3 <= 0:
            V3 = V3 + ZF + SL
            ZF = 0
            SL = 0
            qs = [0]
            gs = 0
            # V0 = V3
        else:
            V4 = V3 - Vdead
            if V4 <= 0:
                gs = 0
                qs = [0]
            else:
                V5 = V4 - xs[i]
                if V5 >= 0:
                    gs = xs[i]
                    V5 = V5
                else:
                    gs = V5 + xs[i]
                    V5 = 0
                V3 = V5 + Vdead
            if V3 >= Vm:
                qs = V3 - Vm
                V3 = Vm
            elif V3 <= Vdead:
                qs = [0]
                V3 = Vdead  # 没用死库容控制下限，用的是扣除蒸发的，如果到死库容不考虑蒸发， V3=Vdead
            else:
                qs = [0]
                V3 = V3
        # 校核
        jh = V0 + L[i] - gs - ZF - SL - qs - V3

        # df2 = df2.append(pd.DataFrame(
        #     {'年': n[i], '月': y[i], '初库容': V0, '来水': L[i], '需水': xs[i], '供水': gs, '蒸发': ZF, '渗漏': SL,
        #      '弃水': qs, '末库容': V3, '校核': jh}), ignore_index=False)
        #
        # df2 = pd.concat([df2, pd.DataFrame(
        #     {'年': year[i], 'x': xun[i], '初库容': V0, '来水': L[i], '需水': xs[i], '供水': gs, '蒸发': ZF, '渗漏': SL,
        #      '弃水': qs, '末库容': V3, '校核': jh})],
        #                 ignore_index=False)
        #
        GS0.extend([[gs]])  # numpy.int64  not iterable  ，int ，float  not  iterable ？？？？  GS0.append(gs) 输出数据带方括号

        #
        # # print(GS2)
        QS0.extend(qs)  # extend 要求可迭代数据 ，qs里面含有0，不可迭代的数,[0]是可迭代了
        # # print(qs)
        # # SKGS=pd.DataFrame(GS2)
        # # SKQS = pd.DataFrame(QS2)
        V0 = V3
    # todo:原代码返回  ： return(gs,qs),按此代码执行会报错：Traceback (most recent call last):
    #   File "/home/lihy/coding/forge/slw/raw_2/xx_run_lhy_1.py", line 53, in <module>
    #     ph_hcgsk = df2
    #     所以改为了按全局变量返回

    # NameError: name 'df2' is not defined
    # return (gs, qs)

    # list 转 numpy
    GS0 = np.array(GS0)
    # 只有一列，总缺水，
    QS0 = np.array(QS0)
    # 返回16个分行业的缺水
    #  复制这一行hgsxs.T，以产生和列数相同的矩阵
    # L_fhy = np.tile(L[:0], (xs_fhy.shape[0], 1))
    # print(xs_fhy)
    SKQS17,SKGS0=shuikuGS_16(L,xs_fhy)

    return SKGS0, ZF, SL, qs, V2, V3, jh, GS0, SKQS17, df2



def shuikuGS_16(skzgs, skxs):
    '''
    bk: 水库供水，分行业
    skzgs:  总供水
    skxs: 需水，分行业
    skzxs: 总需水


    '''
    # # 水库总需水
    # skzxs= skxs.sum(axis=1)

    skxs1 = skxs[:, :1]
    skxs2 = skxs[:, 1:2]
    skxs3 = skxs[:, 2:3]
    skxs4 = skxs[:, 3:4]
    skxs5 = skxs[:, 4:5]
    skxs6 = skxs[:, 5:6]
    skxs7 = skxs[:, 6:7]
    skxs8 = skxs[:, 7:8]
    skxs9 = skxs[:, 8:9]
    skxs10 = skxs[:, 9:10]
    skxs11 = skxs[:, 10:11]
    skxs12 = skxs[:, 11:12]
    skxs13 = skxs[:, 12:13]
    skxs14 = skxs[:, 13:14]
    skxs15 = skxs[:, 14:15]
    skxs16 = skxs[:, 15:16]
    #计算平衡
    skgs1, skhgs1, skques1, skzgs2 = calc_shuiku(skxs1, skzgs, dbhgsxs1)
    skgs2, skhgs2, skques2, skzgs3 = calc_shuiku(skxs2, skzgs2, dbhgsxs2)
    skgs3, skhgs3, skques3, skzgs4 = calc_shuiku(skxs3, skzgs3, dbhgsxs3)
    skgs4, skhgs4, skques4, skzgs5 = calc_shuiku(skxs4, skzgs4, dbhgsxs4)
    skgs5, skhgs5, skques5, skzgs6 = calc_shuiku(skxs5, skzgs5, dbhgsxs5)
    skgs6, skhgs6, skques6, skzgs7 = calc_shuiku(skxs6, skzgs6, dbhgsxs6)
    skgs7, skhgs7, skques7, skzgs8 = calc_shuiku(skxs7, skzgs7, dbhgsxs7)
    skgs8, skhgs8, skques8, skzgs9 = calc_shuiku(skxs8, skzgs8, dbhgsxs8)
    skgs9, skhgs9, skques9, skzgs10 = calc_shuiku(skxs9, skzgs9, dbhgsxs9)
    skgs10, skhgs10, skques10, skzgs11 = calc_shuiku(skxs10, skzgs10, dbhgsxs10)
    skgs11, skhgs11, skques11, skzgs12 = calc_shuiku(skxs11, skzgs11, dbhgsxs11)
    skgs12, skhgs12, skques12, skzgs13 = calc_shuiku(skxs12, skzgs12, dbhgsxs12)
    skgs13, skhgs13, skques13, skzgs14 = calc_shuiku(skxs13, skzgs13, dbhgsxs13)
    skgs14, skhgs14, skques14, skzgs15 = calc_shuiku(skxs14, skzgs14, dbhgsxs14)
    skgs15, skhgs15, skques15, skzgs16 = calc_shuiku(skxs15, skzgs15, dbhgsxs15)
    skgs16, skhgs16, skques16, skzgs17 = calc_shuiku(skxs16, skzgs16, dbhgsxs16)

    # todo skhgs16 合计的中小型水库的供水

    # skzhgs = skhgs1 + skhgs2 + skhgs3 + skhgs4 + skhgs5 + skhgs6 + skhgs7 + skhgs8 + skhgs9 + skhgs10 + skhgs11 + skhgs12 + skhgs13 + skhgs14 + skhgs15 + skhgs16
    # skzhgs_9 = skhgs1 + skhgs2 + skhgs3 + skhgs4 + skhgs5 + skhgs6 + skhgs7 + skhgs8 + skhgs10 + skhgs11 + skhgs12 + skhgs13 + skhgs14 + skhgs15 + skhgs16
    # SKHGS_9 = pd.DataFrame(skzhgs_9)
    #
    # # bk: 下面一行单独添加的。
    # skzgs, skzxs = skzgs.align(skzxs, axis=1, copy=False)
    # skzqis = np.where(skzgs >= skzxs, skzgs - skzxs, 0.00)
    # SKZQS = pd.DataFrame(skzqis)
    # SKHGS = pd.DataFrame(skzhgs)
    #
    # SKHJGS = skgs1 + skgs2 + skgs3 + skgs4 + skgs5 + skgs6 + skgs7 + skgs8 + skgs9 + skgs10 + skgs11 + skgs12 + skgs13 + skgs14 + skgs15 + skgs16
    # SKHJGS_9 = skgs1 + skgs2 + skgs3 + skgs4 + skgs5 + skgs6 + skgs7 + skgs8 + skgs10 + skgs11 + skgs12 + skgs13 + skgs14 + skgs15 + skgs16
    # SKHJGS1_9 = pd.DataFrame(SKHJGS_9)  # 不算水田
    # # F_SKGS =np.array([skgs1, skgs2, skgs3, skgs4, skgs5, skgs6, skgs7, skgs8, skgs9, skgs10, skgs11, skgs12, skgs13, skgs14, skgs15, skgs16])
    # GS9_1 = pd.DataFrame(skgs9)
    #
    GS1 = pd.DataFrame(skgs1, columns=[BiaoTouHangYe[0]])
    GS2 = pd.DataFrame(skgs2, columns=[BiaoTouHangYe[1]])
    GS3 = pd.DataFrame(skgs3, columns=[BiaoTouHangYe[2]])
    GS4 = pd.DataFrame(skgs4, columns=[BiaoTouHangYe[3]])
    GS5 = pd.DataFrame(skgs5, columns=[BiaoTouHangYe[4]])
    GS6 = pd.DataFrame(skgs6, columns=[BiaoTouHangYe[5]])
    GS7 = pd.DataFrame(skgs7, columns=[BiaoTouHangYe[6]])
    GS8 = pd.DataFrame(skgs8, columns=[BiaoTouHangYe[7]])
    GS9 = pd.DataFrame(skgs9, columns=[BiaoTouHangYe[8]])
    GS10 = pd.DataFrame(skgs10, columns=[BiaoTouHangYe[9]])
    GS11 = pd.DataFrame(skgs11, columns=[BiaoTouHangYe[10]])
    GS12 = pd.DataFrame(skgs12, columns=[BiaoTouHangYe[11]])
    GS13 = pd.DataFrame(skgs13, columns=[BiaoTouHangYe[12]])
    GS14 = pd.DataFrame(skgs14, columns=[BiaoTouHangYe[13]])
    GS15 = pd.DataFrame(skgs15, columns=[BiaoTouHangYe[14]])
    GS16 = pd.DataFrame(skgs16, columns=[BiaoTouHangYe[15]])
    # SKHJGS1 = pd.DataFrame(SKHJGS, columns=['供水合计'])
    # SKGS17 = pd.concat(
    #     [GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, SKHJGS1],
    #     axis=1)
    SKGS0 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16],
                      axis=1)
    SKGS0 = np.array(SKGS0)
    #
    # F_SKGS = SKGS0.values.tolist()
    # SKGS18 = pd.concat(
    #     [GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9 - GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16],
    #     axis=1)  # 去掉水田供水
    # F_SKGS18 = SKGS18.values.tolist()


    QS1 = pd.DataFrame(skques1, columns=[BiaoTouHangYe[0]])
    QS2 = pd.DataFrame(skques2, columns=[BiaoTouHangYe[1]])
    QS3 = pd.DataFrame(skques3, columns=[BiaoTouHangYe[2]])
    QS4 = pd.DataFrame(skques4, columns=[BiaoTouHangYe[3]])
    QS5 = pd.DataFrame(skques5, columns=[BiaoTouHangYe[4]])
    QS6 = pd.DataFrame(skques6, columns=[BiaoTouHangYe[5]])
    QS7 = pd.DataFrame(skques7, columns=[BiaoTouHangYe[6]])
    QS8 = pd.DataFrame(skques8, columns=[BiaoTouHangYe[7]])
    QS9 = pd.DataFrame(skques9, columns=[BiaoTouHangYe[8]])
    QS10 = pd.DataFrame(skques10, columns=[BiaoTouHangYe[9]])
    QS11 = pd.DataFrame(skques11, columns=[BiaoTouHangYe[10]])
    QS12 = pd.DataFrame(skques12, columns=[BiaoTouHangYe[11]])
    QS13 = pd.DataFrame(skques13, columns=[BiaoTouHangYe[12]])
    QS14 = pd.DataFrame(skques14, columns=[BiaoTouHangYe[13]])
    QS15 = pd.DataFrame(skques15, columns=[BiaoTouHangYe[14]])
    QS16 = pd.DataFrame(skques16, columns=[BiaoTouHangYe[15]])

    # 缺水
    SKQS17 = pd.concat([QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16], axis=1)
    # return skzqis, SKZQS, SKHGS, SKGS17, SKQS17, SKHJGS, F_SKGS, F_SKGS18, GS9_1, SKHGS_9, SKHJGS1_9, SKGS0, skgs9

    SKQS17 = np.array(SKQS17)
    return SKQS17,SKGS0

def xs_phxs(
        xs, #需水
        phxs #破坏系数
):
    # todo 需水 应该是总的需水吧 ，需水+地下需水？
    #  但地下供水呢？地下供水等于破坏系数之前的
    #  地下的破坏系数先不计算
    # 破坏系数有三列数据，，需水1~8
    # 乘以第一列数据；9~11乘以第二
    # 列数据，12~16乘以第三列数据
    xs_1=xs[:,:8]
    xs_2=xs[:,8:11]
    xs_3=xs[:,11:]

    phxs_1=phxs[:,:1]
    phxs_2=phxs[:,1:2]
    phxs_3=phxs[:,2:3]

    new_xs_1=xs_1*phxs_1
    new_xs_2=xs_2*phxs_2
    new_xs_3=xs_3*phxs_3

    # 按列合并矩阵
    new_xs = np.concatenate((new_xs_1, new_xs_2,new_xs_3), axis=1)

    return new_xs



def prepare_moshi4_data(
        exl_name,
        sheet_name,
        k,  # 径流划分系数
):
    read_exl = load_pd_data(exl_name, sheet_name, index_col=False, usecols=None)
    global g_year
    global g_xun
    global g_day
    # 年
    g_year = read_exl.iloc[:, 0].iloc[1:].reset_index(drop=True)
    # 旬
    g_xun = read_exl.iloc[:, 1].iloc[1:].reset_index(drop=True)
    # g_xun = read_exl.iloc[:, 1].iloc[1:]

    # print(g_year)
    # 天
    g_day = read_exl.iloc[:, 2].iloc[1:].reset_index(drop=True)
    # g_day = read_exl.iloc[:, 2].iloc[1:]

    bqjl = read_exl['本区径流'][1:]
    bqjl_np = np.array(bqjl)
    bqjl_np = bqjl_np.reshape(bqjl_np.shape[0], 1)
    #  转为np维度不是二维就按照 read_exl.iloc[1:,5:6] 读
    dxsk = read_exl['大型水库入库'][1:]

    # 上区来水
    sqls = np.array(read_exl.iloc[1:, 5:6])

    hdjl = (bqjl - dxsk) * k
    # 河道径流=引提水径流 =（本区径流 - 大型水库）*径流系数

    zxskjl = np.array(bqjl - dxsk - hdjl)
    # 中小水库径流=本区-大型-引体
    zxskjl = zxskjl.reshape(zxskjl.shape[0], 1)
    # np的数据格式从一维的（24，），转为二维的（24，1）

    # 大型水库的数据需要再计算完  zxskjl 后，再数据格式一维转二维
    dxsk = np.array(dxsk)
    dxsk = dxsk.reshape(dxsk.shape[0], 1)

    # 需水
    xu_shui = read_exl.iloc[1:, 7:23]
    xu_shui = np.array(xu_shui)

    # 地下需水
    di_xia_xu_shui = read_exl.iloc[1:, 24:40]
    di_xia_xu_shui = np.array(di_xia_xu_shui)

    # 外调水
    wds = np.array(read_exl.iloc[1:, 6])
    wds_np = wds.reshape(wds.shape[0], 1)


    # 破坏系数
    phxs = np.array(read_exl.iloc[1:, 41:44])


    hdjl_np = np.array(hdjl)
    hdjl_np = hdjl_np.reshape(hdjl_np.shape[0], 1)
    return (sqls, xu_shui, di_xia_xu_shui, zxskjl, dxsk,  wds_np,
            read_exl,# 输出的时候用
            phxs,# 破坏系数
            bqjl_np,# 本区径流
            hdjl_np,# 河道径流
            )


# 根据分区名称，获取文件夹路径位置
def get_file_path(target_folder_name):
    global fenqu_file_path
    current_path = Path.cwd()
    print(current_path)
    f_p=Path(current_path).joinpath('data_base\\xx_files')
    print(f_p)
    # windows 使用路径用\，不同系统要修改
    for path in Path(f_p).rglob('*'):
        # print('path')
        # print(path)
        if path.is_dir() and path.name == target_folder_name:
            fenqu_file_path=path
            print(f'Found folder: {path}')
            for item in path.iterdir():
                print(f'  - Name: {item.name}, Path: {item.resolve()}')


read_fqexl = load_pd_data('计算分区径流分割系数', 'Sheet1', index_col=False, usecols=None)


# 输入 分区名称代码，获取分区的 径流分割系数、兴利库容	汛限库容	死库容，回归水系数
def get_xs(
        fq_code  # 分区代码  分区名称
):
    # # 假设列1的列名为'Column1'，后边的列名为'Column2'
    # value_to_find = 'aaa'
    # column_to_find = 'Column2'  # 后边需要的列名

    # 使用条件过滤找到列1中值为'aaa'的行，并获取对应的列2的值
    # jlxs = read_fqexl.loc[read_fqexl.iloc[:, 3] == fq_code, 4]
    # print(jlxs)

    key_row = read_fqexl.loc[read_fqexl.iloc[:, 3] == fq_code]
    # print(key_row)
    # print(type(key_row))

    # 径流分割系数
    k = key_row.iloc[:, 4].values[0]

    # 兴利库容
    Vx = key_row.iloc[:, 5].values[0]

    # 汛限库容
    Vxx = key_row.iloc[:, 6].values[0]

    # 死库容
    Vdead = key_row.iloc[:, 7].values[0]

    # 回归水系数
    hgxs = key_row.iloc[:, 8:24].values[0]
    hgxs = hgxs.reshape(hgxs.shape[0], 1)


    return k, Vx, Vxx, Vdead, hgxs