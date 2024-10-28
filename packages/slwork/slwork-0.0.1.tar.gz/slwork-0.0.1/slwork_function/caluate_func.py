import pandas as pd
import numpy as np
from slwork_function.add_code import *
from pathlib import Path

columns_arr = ['城镇生活', '农村生活', '牲畜', '三产', '火核电', '一般工业', '高耗水工业', '建筑业',
               '水田', '水浇地', '菜田', '林果地', '草场', '鱼塘', '城镇生态', '湿地']


# 年月日的列 pandas dataframe 格式
g_year=[]
g_xun=[]
g_day= []

# 当前分区的文件夹的路径
# fenqu_file_path='C:\\Users\\Administrator\\Desktop\\slwork_function\\data_base\\xx_files\\七台河市\\莲花水库以下\\莲花水库以下七台河市'
fenqu_file_path=''
# 分区名称
fenqu_name=''

# 当前水库的文件夹的路径1
shuiku_file_path=''
# 当前水库的文件夹的路径2
shuiku_file_path2=''
# 水库1名称
shuiku_name=''
# 水库2名称
shuiku_name2=''

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




def dict_add(d,key,add_num):
    if key not in d:
        d[key] = 0
    d[key] = d[key] + add_num
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
                dict_add(que_xun_year,list_n,1)
                # que_xun_year[list_n]+=1
        # 如果当前列没有缺水数，就初始化一个0
        dict_add(que_xun_year, list_n, 0)
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
                    dict_add(que_xun_year,list_n,1)
                    # que_xun_year[list_n]+=1
                #  旬的循环回到1，新一年重新记录
                row_xun=1
            else:
                # 旬+1
                row_xun+=1

        # 如果当前列没有缺水数，就初始化一个0
        dict_add(que_xun_year, list_n, 0)
        # 列数+1
        list_n+=1

    bzl=[]
    for i in que_xun_year:
        if i<=8:
            b_answer=1-que_xun_year[i]/2196
            bzl.append(b_answer)
        else:
            b_answer=1-que_xun_year[i]/61
            bzl.append(b_answer)


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
    # 都是计算平衡后返回的供水
    hjgs = dxs + bqdb + zzxsk + dxsk + gjs + wds
    #  总供水，用 供水合计 的合计 计算每行的总和，并将结果组成一列
    hjgs_sums = hjgs.sum(axis=1)

    hebing_shuchu(hjgs, '合计供水')


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

    hebing_shuchu(hgs,'总回归水')

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


    cjs=bqjl+sqls+wds_shuru+hgs_sums-(hjgs_sums-dxgs_sums)

    bqjl_pd = pd.DataFrame(bqjl)
    bqjl_pd = bqjl_pd.set_axis(['本区径流'], axis='columns')
    sqls_pd = pd.DataFrame(sqls)
    sqls_pd = sqls_pd.set_axis(['上区来水'], axis='columns')
    wds_shuru_pd = pd.DataFrame(wds_shuru)
    wds_shuru_pd = wds_shuru_pd.set_axis(['外调水'], axis='columns')
    hgs_sums_pd = pd.DataFrame(hgs_sums)
    hgs_sums_pd = hgs_sums_pd.set_axis(['总回归水'], axis='columns')
    hjgs_sums_pd = pd.DataFrame(hjgs_sums)
    hjgs_sums_pd = hjgs_sums_pd.set_axis(['总供水'], axis='columns')
    dxgs_sums_pd = pd.DataFrame(dxgs_sums)
    dxgs_sums_pd = dxgs_sums_pd.set_axis(['总地下水供水'], axis='columns')

    cjs_pd = pd.DataFrame(cjs)
    cjs_pd = cjs_pd.set_axis(['出境水'], axis='columns')
    cjs_shuchu = pd.concat([g_year, g_xun, g_day, cjs_pd,bqjl_pd,
                            sqls_pd,wds_shuru_pd,hgs_sums_pd,
                            hjgs_sums_pd,dxgs_sums_pd], axis=1)  # 按列合并
    #  输出 合计供水
    shuchu_exl('出境水', cjs_shuchu)


    # ----------------------------------------地下水供水-------------------------------------------------
    # 地下水供水=河道径流平衡时，计算返回的地下水供水
    hebing_shuchu(dxs,'地下水供水')

    # ----------------------------------------本区地表供水-------------------------------------------------
    #  本区地表供水 =河道径流平衡后输出的供水
    hebing_shuchu(bqdb,'本区地表供水')

    # ----------------------------------------中小水库供水-------------------------------------------------
    hebing_shuchu(zzxsk,'中小水库供水')

    # ----------------------------------------大型水库供水-------------------------------------------------
    hebing_shuchu(dxsk,'大型水库供水')

    # ----------------------------------------过境水供水-------------------------------------------------
    hebing_shuchu(gjs,'过境水供水')

    # ----------------------------------------外调水供水-------------------------------------------------
    hebing_shuchu(wds, '外调水供水')
    return cjs

# 统计输出的时候，计算一个按行计算的 合计 ，然后输出exl表
def hebing_shuchu(np_data,exl_name):
    data_sums = np_data.sum(axis=1)
    data_sums = data_sums.reshape(data_sums.shape[0], 1)
    # 按列合并矩阵
    hebing_np = np.concatenate((np_data, data_sums), axis=1)

    hebing_columns_arr=columns_arr+['合计']
    hebing_pd = pd.DataFrame(hebing_np)
    hebing_pd = hebing_pd.set_axis(hebing_columns_arr, axis='columns')
    hebing_shuchu = pd.concat([g_year, g_xun, g_day, hebing_pd], axis=1)  # 按列合并
    #  输出 exl
    shuchu_exl( exl_name, hebing_shuchu)



def shuchu_exl(exl_name, data):
    # 同名表如果存在就覆盖
    shuchu_file=Path(f'{fenqu_file_path}/输出')
    f_path=Path(f'{shuchu_file}/输出_{exl_name}.xlsx')
    # 如果文件夹不存在，就创建它
    if not shuchu_file.exists():
        shuchu_file.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(f_path, engine='openpyxl',
                        mode='w',#追加模式,不覆盖其他文件
                        ) as writer:
                        # mode='a',#追加模式,不覆盖其他文件
                        # if_sheet_exists='replace'
                        # ) as writer:

        data.to_excel(writer, sheet_name='sheet1',index=False)


def Chazhi_new(x, y, xi):  # 参数一组升序排列的长度相等的x列表和y列表，以及给定一个x值
    # todo：超出处理 数值在曲线范围外，就用他临近的两个点来算斜率，来计算差值
    # 中小型不计算
    # 已知月初库容，求月初水位，和月初面积
    # 求水位 x=库容 y=水位
    # 求面积 x=库容

    # 水库坝下水位-流量关系曲线
    # 坝下水位流量关系曲线
    # 已知流量，求水位
    # x=流量=下泄（可能是水量，要转换成） = xi
    min_num=0
    max_num=len(x)-2

    for j in range(len(x)):
        # 超出处理 数值在曲线范围外，就用他临近的两个点来算斜率
        if xi < x[0]:
            yi = y[min_num] + (xi - x[min_num]) / (x[ min_num+1] - x[min_num]) * (y[min_num+1] - y[min_num])
            return yi
        elif xi >= x[j] and xi < x[j + 1]:
            yi = y[j] + (xi - x[j]) / (x[j + 1] - x[j]) * (y[j + 1] - y[j])
            return yi
        # 超出处理 数值在曲线范围外，就用他临近的两个点来算斜率
        elif xi >= x[max_num]:
            yi = y[max_num] + (xi - x[max_num]) / (x[ max_num+1] - x[max_num]) * (y[max_num+1] - y[max_num])
            return yi

# 转换数据格式
def arrer_to_float(num):
    if type(num) == np.ndarray:
        num=num[0]
    return num

def shuiku_zxx_dxsk(V0, L,
                    xs_fhy,#分行业的缺水 需水
                    Vx, Vxx, Vdead, v, m, Z, S,):
    '''
    # 水库供水只考虑了总供水，未分行业

    中小型水库计算 不包括蒸发、渗透、面积
    大型水库计算包括蒸发、渗透、面积

    bk:
    V0: 初始库容 月初库容
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

    ZF_all=[]
    SL_all=[]
    mj_all=[]

    # 判断 当水库水位低于调度线，需要对各行业需水进行折减
    # 是否可通过调整之前时段下泄，来满足本旬需水
    V5_sum=0
    # 重复了，下边除了两句，都一样
    # for i in range(0, Llength):
    #     # for i in range(0, 732):
    #
    #     V2 = V0 + L[i] - xs[i]  # L.loc[i] 可以读取0  12282.19
    #
    #     assert V2.shape == (1,)
    #
    #     if (g_xun[i] >= 18 and g_xun[i] <= 27):
    #         # if (g_xun[i] >= 6 and g_xun[i] <= 9):
    #         Vm = Vxx
    #     else:
    #         Vm = Vx
    #     if V2 >= Vm:
    #         V2 = Vm
    #     else:
    #         V2 = V2
    #     if V2 <= Vdead:
    #         V2 = Vdead
    #     V1 = (V2 + V0) / 2
    #
    #     if v is not None:
    #
    #         mj = Chazhi_new(v, m, V1)  # 由库容求面积
    #
    #         ZF = mj * Z[i] / 10  # 蒸发
    #         SL = mj * S[i] / 10  # 渗漏
    #     else:
    #         mj = 0
    #         ZF = 0
    #         SL = 0
    #     V3 = L[i] + V0 - ZF - SL
    #     if V3 <= 0:
    #         V3 = V3 + ZF + SL
    #
    #         ZF = 0
    #         SL = 0
    #         # V0 = V3
    #         qs = [0]
    #         gs = 0
    #     else:
    #         V4 = V3 - Vdead
    #         if V4 <= 0:
    #             gs = 0
    #             qs = [0]
    #         else:
    #             V5 = V4 - xs[i]
    #             if V5 >= 0:
    #                 gs = xs[i]
    #                 V5 = V5
    #             else:
    #                 gs = V5 + xs[i]
    #                 V5 = 0
    #             V3 = V5 + Vdead
    #
    #         if V3 >= Vm:
    #             qs = V3 - Vm
    #             V3 = Vm
    #         elif V3 <= Vdead:
    #             qs = [0]
    #             V3 = Vdead  # 没用死库容控制下限，用的是扣除蒸发的，如果到死库容不考虑蒸发， V3=Vdead
    #         else:
    #             qs = [0]
    #             V3 = V3
    #
    #     gs = 0 #这个下边没有
    #     V0 = V3

    for i in range(0, Llength):
        # 粗算 旬末库容 =pdf V1
        V2 = V0 + L[i] - xs[i]
        if (g_xun[i] >= 18 and g_xun[i] <= 27):
            # if (g_xun[i] >= 6 and g_xun[i] <= 9):  #tod
            # o：月改成旬的话，怎么计算
            # Vm=pdf Vmax
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
            mj = Chazhi_new(v, m, V1)  # 由库容求面积

            # todo 按旬算，需要修改数据，程序除3
            ZF = mj * Z[i] / 10  # 蒸发 的损失
            SL = mj * S[i] / 10  # 渗漏
        else:
            mj = 0
            ZF = 0
            SL = 0
        # 精算 旬末库容=月末库容
        V3 = L[i] + V0 - ZF - SL
        if V3 <= 0:
            V3 = V3 + ZF + SL
            ZF = 0
            SL = 0
            qs = [0]
            gs = 0
            # V0 = V3
        else:
            # 可供水量
            V4 = V3 - Vdead
            if V4 <= 0:
                gs = 0
                qs = [0]
            else:
                # v5=可供水量-需水=多余的水 对于这一旬的可供水量
                V5 = V4 - xs[i]
                if V5 >= 0:
                    gs = xs[i]
                    V5 = V5
                else:
                    # todo 需要返回去算
                    gs = V4
                    # gs = V5 + xs[i]

                    # V5 = 0
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
        # 校核 这个上边没有
        jh = V0 + L[i] - gs - ZF - SL - qs - V3

        V5_sum+=V5
        # df2 = df2.append(pd.DataFrame(
        #     {'年': n[i], '月': y[i], '初库容': V0, '来水': L[i], '需水': xs[i], '供水': gs, '蒸发': ZF, '渗漏': SL,
        #      '弃水': qs, '末库容': V3, '校核': jh}), ignore_index=False)
        #
        # df2 = pd.concat([df2, pd.DataFrame(
        #     {'年': year[i], 'x': xun[i], '初库容': V0, '来水': L[i], '需水': xs[i], '供水': gs, '蒸发': ZF, '渗漏': SL,
        #      '弃水': qs, '末库容': V3, '校核': jh})],
        #                 ignore_index=False)
        #
        # GS0.extend([[gs]])  # numpy.int64  not iterable  ，int ，float  not  iterable ？？？？  GS0.append(gs) 输出数据带方括号

        #
        # # print(GS2)
        # QS0.extend(qs)  # extend 要求可迭代数据 ，qs里面含有0，不可迭代的数,[0]是可迭代了
        # # print(qs)
        # # SKGS=pd.DataFrame(GS2)
        # # SKQS = pd.DataFrame(QS2)
        V0 = V3
        gs = 0

        ZF_all.append(arrer_to_float(ZF))
        SL_all.append(arrer_to_float(SL))
        mj_all.append(arrer_to_float(mj))


    # # list 转 numpy
    # GS0 = np.array(GS0)
    # # 只有一列，总缺水，
    # QS0 = np.array(QS0)
    # # 返回16个分行业的缺水

    # L=gs_all
    SKQS17,SKGS0=shuikuGS_16(L,xs_fhy)

    # 大型水库平衡 输出库容求面积、蒸发、渗漏 ，应该是分旬的
    if v is not None:
        zf_sl_mj_np=np.array([mj_all,ZF_all,SL_all])
        zf_sl_mj_pd = pd.DataFrame(zf_sl_mj_np.T)
        zf_sl_mj_pd = zf_sl_mj_pd.set_axis(['库容求面积','蒸发','渗漏'], axis='columns')
        pd_shuchu = pd.concat([g_year, g_xun, g_day, zf_sl_mj_pd], axis=1)  # 按列合并
        #  输出 exl
        shuchu_exl( '库容求面积、蒸发、渗漏', pd_shuchu)

    return SKGS0, ZF, SL, qs, V2, V3, jh, GS0, SKQS17, df2

# 尼尔基水库
def shuiku_nej(
                V0, L,
                xs_fhy,#分行业的缺水 需水
                Vx, Vxx, Vdead,
                Z, #水库 蒸发强度过程线
                S,#水库 渗漏强度过程线
                mj_line,#面积曲线
                sw_line,#水位曲线
                kr_line,# 库容曲线 v
                dd_table,# 调度线
                flmb_table,# 放流目标表 下泄

                bxsw_line,#坝下水位 曲线
                bxll_line,#坝下流量 曲线
               ):
    '''
    #todo 是不是都不分行业算？ 水库供水只考虑了总供水，未分行业
          之后输出啥？还要继续怎么算？

    中小型水库计算 不包括蒸发、渗透、面积
    大型水库计算包括蒸发、渗透、面积

    bk:
    V0: 初始库容 月初库容
    L: 来水
    xs: 需水
    Vx: 兴利库容
    Vxx: 汛限库容  todo 汛限水位（m） 用上了么？
    Vdead: 死库容
    v: 体积
    m: 面积
    Z: 蒸发
    S: 渗漏
    mj_line:面积曲线
    sw_line:水位曲线
    kr_line:库容曲线

    flmb_table:放流目标表
    ddx_table: 调度线 表

                bxsw_line,#坝下水位 曲线
                bxll_line,#坝下流量 曲线

                #todo 干啥的？
                stxx_line,#生态下泄过程线 曲线
                ,#水库长系列径流，需要相当于来水了？
    '''

    assert type(g_xun) == pd.core.series.Series


    xs= xs_fhy.sum(axis=1)

    # 表格的行数，动态获取
    Llength = L.shape[0]

    GS0 = []
    QS0 = []  # 应该是缺水
    df2 = pd.DataFrame()

    ZF_all=[]
    SL_all=[]
    mj_all=[]


    for i in range(0, Llength):
        V1 = V0 + L[i] - xs[i]

        if V1<=Vdead:
            V1 = V0 + L[i]

        gs=xs[i]

        if (g_xun[i] >= 18 and g_xun[i] <= 27):
            # if (g_xun[i] >= 6 and g_xun[i] <= 9):  #todo：月改成旬的话，怎么计算

            Vmax = Vxx
        else:
            Vmax = Vx

        if V1>Vmax:
            # todo 下泄 ？库容
            # todo 这个怎么算面积1，水位1，？？？
            Vxiax=V0-Vmax
            # todo 也是要算两遍？
            # 根据V1试算面积1，水位1 粗算
            sw1 = Chazhi_new(kr_line, sw_line, Vxiax)  # 由库容求水位  todo 没用上？
            mj1 = Chazhi_new(kr_line, mj_line, Vxiax)  # 由库容求面积

            ZF1 = mj1 * Z[i] / 10  # 蒸发 的损失
            SL1 = mj1 * S[i] / 10  # 渗漏

            # 精算的库容2
            Vj=Vxiax-xs[i]-ZF1-SL1


            #  根据V2试算面积2，水位2 精细算
            sw2 = Chazhi_new(kr_line, sw_line, Vj)  # 由库容求水位
            mj2 = Chazhi_new(kr_line, mj_line, Vj)  # 由库容求面积 todo 然后用它干啥了

            # 保存
            ZF2 = mj2 * Z[i] / 10  # 蒸发 的损失
            SL2 = mj2 * S[i] / 10  # 渗漏


            # 上游库容
            sy_kr=(Vxiax+Vj)/2
            # 上游水位
            sy_sw=Chazhi_new(kr_line,sw_line,sy_kr)

        else:
            #  根据V1试算面积1，水位1 粗算
            sw1 = Chazhi_new(kr_line, sw_line, V1)  # 由库容求水位  todo 没用上？
            mj1 = Chazhi_new(kr_line, mj_line, V1)  # 由库容求面积

            ZF1 = mj1 * Z[i] / 10  # 蒸发 的损失
            SL1 = mj1 * S[i] / 10  # 渗漏
            ZF1=0
            SL1=0
            # 精算的库容2
            V2=V1-xs[i]-ZF1-SL1


            #  根据V2试算面积2，水位2 精细算
            sw2 = Chazhi_new(kr_line, sw_line, V2)  # 由库容求水位
            mj2 = Chazhi_new(kr_line, mj_line, V2)  # 由库容求面积 todo 然后用它干啥了

            # 保存
            ZF2 = mj2 * Z[i] / 10  # 蒸发 的损失
            #  蒸发的曲线长度不够，传入数据是
            #  unsupported operand type(s) for *: 'NoneType' and 'float'
            SL2 = mj2 * S[i] / 10  # 渗漏

            # 用sw2
            #  判断水位位于调度图的位置，然后按照调度图（放流目标）确定下泄流量
            # 获取下泄流量或是发电保证出力
            ll_cl=get_dd_xx(sw2,dd_table,flmb_table,g_xun[i])

            # 上游库容
            sy_kr=(V1+V2)/2
            # 上游水位
            sy_sw=Chazhi_new(kr_line,sw_line,sy_kr)

            # 如果是4-10月就是下泄流量
            if (g_xun[i] >= 11 and g_xun[i] <= 30):
                #  差值求得下游水位，
                xy_sw=Chazhi_new(bxll_line,bxsw_line,ll_cl)

                # 直接计算发电出力
                Nok=9.81*ll_cl*(sy_sw-xy_sw)*0.85
                Qok=ll_cl

            # 如果是1-3  11-12月
            else:
                # 确定发电保证出力，todo sl_cl就是出力吧 ？
                # todo 不同月份  保证出力要×不同区域的系数    系数=sl_cl   保证力是输入还是写死？再问
                # 保证出力
                Nbz=ll_cl
                # todo 初步拟定下泄流量？就是生态下泄流量吧？
                #  然后拟定计算的出力与保证出力误差0.001 就增多少拟定的下泄流量？用二分法，50到150取值

                max_num=150
                min_num=50
                # 返回确定的下泄流量,确定的保证出力

                Qok,Nok=get_Nok(min_num,max_num,bxll_line, bxsw_line,sy_sw,Nbz)




    # return SKGS0, ZF, SL, qs, V2, V3, jh, GS0, SKQS17, df2

# 根据二分法计算在最大最小值内，计算保证出力和拟定出力误差小于0.001的拟定下泄流量
def get_Nok(min_num,max_num,
            bxll_line,#坝上流量曲线
            bxsw_line,#坝上水位曲线
            sy_sw,#上游水位
            Nbz #保证出力
            ):
    # 根据最大最小值 拟定下泄流量，拟定出力
    Qguess, Nguess = get_ef_data(min_num, max_num, bxll_line, bxsw_line, sy_sw)
    # 抛物线顶点x坐标
    x_top = sy_sw / 2

    print('Qguess')
    print(Qguess)
    print('Nguess')
    print(Nguess)

    while min_num < max_num:
        print('-'*100)
        print(Nguess)
        print(Nbz)
        if abs(Nguess - Nbz) > 0.001:
            # （200-x）*x是个抛物线口向下的形状
            # 可以根据判断抛物线顶点x坐标 ax2+bx+c   -(b/(2*a))
            # sy_sw/2  然后看取值应该往哪里取

            # Nguess大于Nbz
            if Nguess - Nbz > 0:
                if x_top > max_num:
                    max_num = Qguess
                    # 根据最大最小值 拟定下泄流量，拟定出力
                    Qguess, Nguess = get_ef_data(min_num, max_num,
                                                 bxll_line, bxsw_line, sy_sw)

                elif x_top < min_num:
                    min_num = Qguess
                    # 根据最大最小值 拟定下泄流量，拟定出力
                    Qguess, Nguess = get_ef_data(min_num, max_num,
                                                 bxll_line, bxsw_line, sy_sw)
                else:
                    # 最高点在两值中间……先为了省水，选择小流量吧
                    max_num = Qguess
                    # 根据最大最小值 拟定下泄流量，拟定出力
                    Qguess, Nguess = get_ef_data(min_num, max_num,
                                                 bxll_line, bxsw_line, sy_sw)

            # Nguess 小于Nbz
            else:
                if x_top > max_num:
                    min_num = Qguess
                    # 根据最大最小值 拟定下泄流量，拟定出力
                    Qguess, Nguess = get_ef_data(min_num, max_num,
                                                 bxll_line, bxsw_line, sy_sw)

                elif x_top < min_num:
                    max_num = Qguess
                    # 根据最大最小值 拟定下泄流量，拟定出力
                    Qguess, Nguess = get_ef_data(min_num, max_num,
                                                 bxll_line, bxsw_line, sy_sw)
                else:
                    # 最高点在两值中间……先为了省水，选择小流量吧
                    max_num = Qguess
                    # 根据最大最小值 拟定下泄流量，拟定出力
                    Qguess, Nguess = get_ef_data(min_num, max_num,
                                                 bxll_line, bxsw_line, sy_sw)


        else:
            # 返回确定的下泄流量,确定的保证出力
            return Qguess,Nguess

# 计算出力N
def get_N(H,Q):
    return 9.81*H*Q*0.85

# 返回 拟定下泄流量，拟定出力
def get_ef_data(min_num,max_num,bxll_line, bxsw_line,sy_sw):
    Qguess=(min_num+max_num)/2
    #  差值求得下游水位，
    xy_sw = Chazhi_new(bxll_line, bxsw_line, Qguess)
    # 拟定出力
    Nguess = get_N((sy_sw - xy_sw), Qguess)
    return Qguess,Nguess


# 判断水位位于调度图的位置，然后按照调度图（放流目标）确定下泄流量，或是得到发电系数？
def get_dd_xx(sw,dd_table,flmb_table,xun):
    # 获取对应旬的那一列 调度线的 数据
    get_dd_xun=dd_table[:,xun-1]

    # print(get_dd_xun)
    # print(sw)
    # 使用numpy.where函数获取值小于sw的数的所有索引
    indices = np.where(get_dd_xun <= sw)

    # 如果没有比sw小的值，todo 就取最小的值
    if len(indices)==0:
        line_num=0
    else:
        # 获取最后一个索引
        line_num=indices[-1][-1]
        # line_num=indices[-1]

    # 获取对应在 放流目标 里的 下泄量
    get_data=flmb_table[line_num,xun-1]


    return get_data



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
    skgs1, skhgs1, skques1, skzgs2 = calc_shuiku(skxs1, skzgs)
    skgs2, skhgs2, skques2, skzgs3 = calc_shuiku(skxs2, skzgs2)
    skgs3, skhgs3, skques3, skzgs4 = calc_shuiku(skxs3, skzgs3)
    skgs4, skhgs4, skques4, skzgs5 = calc_shuiku(skxs4, skzgs4)
    skgs5, skhgs5, skques5, skzgs6 = calc_shuiku(skxs5, skzgs5)
    skgs6, skhgs6, skques6, skzgs7 = calc_shuiku(skxs6, skzgs6)
    skgs7, skhgs7, skques7, skzgs8 = calc_shuiku(skxs7, skzgs7)
    skgs8, skhgs8, skques8, skzgs9 = calc_shuiku(skxs8, skzgs8)
    skgs9, skhgs9, skques9, skzgs10 = calc_shuiku(skxs9, skzgs9)
    skgs10, skhgs10, skques10, skzgs11 = calc_shuiku(skxs10, skzgs10)
    skgs11, skhgs11, skques11, skzgs12 = calc_shuiku(skxs11, skzgs11)
    skgs12, skhgs12, skques12, skzgs13 = calc_shuiku(skxs12, skzgs12)
    skgs13, skhgs13, skques13, skzgs14 = calc_shuiku(skxs13, skzgs13)
    skgs14, skhgs14, skques14, skzgs15 = calc_shuiku(skxs14, skzgs14)
    skgs15, skhgs15, skques15, skzgs16 = calc_shuiku(skxs15, skzgs15)
    skgs16, skhgs16, skques16, skzgs17 = calc_shuiku(skxs16, skzgs16)


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
    GS1 = pd.DataFrame(skgs1, columns=[columns_arr[0]])
    GS2 = pd.DataFrame(skgs2, columns=[columns_arr[1]])
    GS3 = pd.DataFrame(skgs3, columns=[columns_arr[2]])
    GS4 = pd.DataFrame(skgs4, columns=[columns_arr[3]])
    GS5 = pd.DataFrame(skgs5, columns=[columns_arr[4]])
    GS6 = pd.DataFrame(skgs6, columns=[columns_arr[5]])
    GS7 = pd.DataFrame(skgs7, columns=[columns_arr[6]])
    GS8 = pd.DataFrame(skgs8, columns=[columns_arr[7]])
    GS9 = pd.DataFrame(skgs9, columns=[columns_arr[8]])
    GS10 = pd.DataFrame(skgs10, columns=[columns_arr[9]])
    GS11 = pd.DataFrame(skgs11, columns=[columns_arr[10]])
    GS12 = pd.DataFrame(skgs12, columns=[columns_arr[11]])
    GS13 = pd.DataFrame(skgs13, columns=[columns_arr[12]])
    GS14 = pd.DataFrame(skgs14, columns=[columns_arr[13]])
    GS15 = pd.DataFrame(skgs15, columns=[columns_arr[14]])
    GS16 = pd.DataFrame(skgs16, columns=[columns_arr[15]])
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


    QS1 = pd.DataFrame(skques1, columns=[columns_arr[0]])
    QS2 = pd.DataFrame(skques2, columns=[columns_arr[1]])
    QS3 = pd.DataFrame(skques3, columns=[columns_arr[2]])
    QS4 = pd.DataFrame(skques4, columns=[columns_arr[3]])
    QS5 = pd.DataFrame(skques5, columns=[columns_arr[4]])
    QS6 = pd.DataFrame(skques6, columns=[columns_arr[5]])
    QS7 = pd.DataFrame(skques7, columns=[columns_arr[6]])
    QS8 = pd.DataFrame(skques8, columns=[columns_arr[7]])
    QS9 = pd.DataFrame(skques9, columns=[columns_arr[8]])
    QS10 = pd.DataFrame(skques10, columns=[columns_arr[9]])
    QS11 = pd.DataFrame(skques11, columns=[columns_arr[10]])
    QS12 = pd.DataFrame(skques12, columns=[columns_arr[11]])
    QS13 = pd.DataFrame(skques13, columns=[columns_arr[12]])
    QS14 = pd.DataFrame(skques14, columns=[columns_arr[13]])
    QS15 = pd.DataFrame(skques15, columns=[columns_arr[14]])
    QS16 = pd.DataFrame(skques16, columns=[columns_arr[15]])

    # 缺水
    SKQS17 = pd.concat([QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16], axis=1)
    # return skzqis, SKZQS, SKHGS, SKGS17, SKQS17, SKHJGS, F_SKGS, F_SKGS18, GS9_1, SKHGS_9, SKHJGS1_9, SKGS0, skgs9

    SKQS17 = np.array(SKQS17)
    return SKQS17,SKGS0




def calc_shuiku(skxs2, skzgs2):
    skgs2 = np.where(skzgs2 >= skxs2, skxs2, np.where(skzgs2 >= 0, skzgs2, 0))
    skques2 = np.where(skzgs2 >= skxs2, 0, np.where(skzgs2 >= 0, skxs2 - skzgs2, 0))#缺水
    skqis2 = np.where(skzgs2 >= skxs2, skzgs2 - skxs2, 0)#弃水
    # skhgs2 = skgs2 * dbhgsxs2#回归水先不计算
    # skzgs3 = skqis2
    skhgs2=0
    return skgs2, skhgs2, skques2, skqis2




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

def test():
    print('================xushui_exl')
    xushui_exl = Path(f'{fenqu_file_path}/需水')
    print(xushui_exl)
    read_exl = load_pd_data(fenqu_file_path,fenqu_name,'需水', 'Sheet1', index_col=False, usecols=None)
    print(read_exl)

# 清楚矩阵中值为0的行和列
def empty_np_0(np_0):
    # 找出矩阵中为0的行和列
    zero_rows = (np_0 == 0).all(axis=1)
    zero_cols = (np_0 == 0).all(axis=0)

    # 删除为0的行和列
    matrix = np_0[~zero_rows, :]
    matrix = matrix[:, ~zero_cols]
    return matrix

# 获取水库需要读取的数据 尼尔基水库
def prepare_shuiku_nej_data():

    diaodu_exl = load_pd_data(shuiku_file_path, shuiku_name, '调度图调度线', 'Sheet1', index_col=False, usecols=None)

    # 调度图
    dd_table = diaodu_exl.iloc[:8, 1:]
    dd_table = np.array(dd_table)

    # 放流目标
    flmb_table = diaodu_exl.iloc[9:18, 1:]
    flmb_table = np.array(flmb_table)

    # 坝下水位 流量
    bxswll_exl = load_pd_data(shuiku_file_path, shuiku_name, '水库坝下水位-流量关系曲线', 'Sheet1', index_col=False, usecols=None)
    bxsw_line = np.array(bxswll_exl['水位'])
    bxll_line = np.array(bxswll_exl['流量'])

    bxsw_line = bxsw_line.reshape(bxsw_line.shape[0], 1)
    bxll_line = bxll_line.reshape(bxll_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    bxll_line=empty_np_0(bxll_line)
    bxsw_line=empty_np_0(bxsw_line)

    # 水库输入长系列
    skcxl_exl = load_pd_data(shuiku_file_path, shuiku_name, '水库输入长系列', 'Sheet1', index_col=False, usecols=None)
    dxsk_rk = np.array(skcxl_exl['大型水库入库'])
    stxx = np.array(skcxl_exl['生态下泄'])

    dxsk_rk = dxsk_rk.reshape(dxsk_rk.shape[0], 1)
    stxx = stxx.reshape(stxx.shape[0], 1)

    # 渗漏强度过程线
    S_exl = load_pd_data(shuiku_file_path, shuiku_name, '渗漏强度过程线', 'Sheet1', index_col=False, usecols=None)
    S = np.array(S_exl['渗漏强度过程线'])
    S = S.reshape(S.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    S=empty_np_0(S)

    # 蒸发强度过程线
    Z_exl = load_pd_data(shuiku_file_path, shuiku_name, '蒸发强度过程线', 'Sheet1', index_col=False, usecols=None)
    Z = np.array(Z_exl['蒸发强度过程线'])
    Z = Z.reshape(Z.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    Z=empty_np_0(Z)

    # 水库输入-库容
    kr_exl = load_pd_data(shuiku_file_path, shuiku_name, '水库输入-库容', 'Sheet1', index_col=False, usecols=None)
    kr_line = np.array(kr_exl['水库输入-库容'])
    kr_line = kr_line.reshape(kr_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    kr_line=empty_np_0(kr_line)

    # 水库输入-面积
    mj_exl = load_pd_data(shuiku_file_path, shuiku_name, '水库输入-面积', 'Sheet1', index_col=False, usecols=None)
    mj_line = np.array(mj_exl['水库输入-面积'])
    mj_line = mj_line.reshape(mj_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    mj_line=empty_np_0(mj_line)

    # 水库输入-水位
    sw_exl = load_pd_data(shuiku_file_path, shuiku_name, '水库输入-水位', 'Sheet1', index_col=False, usecols=None)
    sw_line = np.array(sw_exl['水库输入-水位'])
    sw_line = sw_line.reshape(sw_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    sw_line=empty_np_0(sw_line)

    # 水库特性
    vvxd_exl = load_pd_data(shuiku_file_path, shuiku_name, '水库特性', 'Sheet1', index_col=False, usecols=None)
    # 兴利库容
    Vx = vvxd_exl.iloc[0, 1]
    # 汛限库容
    Vxx = vvxd_exl.iloc[0, 3]
    # 死库容
    Vdead = vvxd_exl.iloc[0, 0]



    return (dd_table,flmb_table,bxsw_line,bxll_line,
            S,Z,kr_line,mj_line,sw_line,Vx,Vxx,Vdead,
            dxsk_rk,stxx)


# 获取年旬天的pd，并初始化年旬天的全局变量
def get_nxt(df):

    global g_year
    global g_xun
    global g_day

    g_year, g_xun, g_day = get_nxt_with_return(df)


def prepare_moshi4_data():
    xushui_exl = load_pd_data(fenqu_file_path, fenqu_name, '需水', 'Sheet1', index_col=False, usecols=None)

    # 如果年旬天，没初始化，就调用 get_nxt 初始化一下
    if len(g_year)==0 :
        get_nxt(xushui_exl)


    # 需水
    xu_shui = xushui_exl.iloc[:, 3:-1]
    xu_shui = np.array(xu_shui)


    k_exl = load_pd_data(fenqu_file_path, fenqu_name, '径流分割系数', 'Sheet1', index_col=False, usecols=None)
    # 径流分割系数
    k=k_exl.iloc[0, 0]

    vvx_exl = load_pd_data(fenqu_file_path, fenqu_name, '中小型水库打捆设计参数', 'Sheet1', index_col=False, usecols=None)
    # 兴利库容
    Vx=vvx_exl.iloc[0, 0]
    # 汛限库容
    Vxx =vvx_exl.iloc[0, 1]
    # 死库容
    Vdead =vvx_exl.iloc[0, 2]

    hgsxs_exl = load_pd_data(fenqu_file_path, fenqu_name, '回归水系数', 'Sheet1', index_col=False, usecols=None)
    # 回归水系数
    hgxs =np.array(hgsxs_exl.iloc[0, :-1])
    hgxs = hgxs.reshape(hgxs.shape[0], 1)


    bqjl_exl = load_pd_data(fenqu_file_path, fenqu_name, '本区径流', 'Sheet1', index_col=False, usecols=None)
    bqjl = bqjl_exl['本区径流']
    bqjl_np = np.array(bqjl)
    bqjl_np = bqjl_np.reshape(bqjl_np.shape[0], 1)



    jcsj_exl = load_pd_data(fenqu_file_path, fenqu_name, '基础数据', 'Sheet1', index_col=False, usecols=None)
    # bqjl = jcsj_exl['本区径流']
    # bqjl_np = np.array(bqjl)
    # bqjl_np = bqjl_np.reshape(bqjl_np.shape[0], 1)ad_exl.iloc[1:,5:6] 读

    dxsk = jcsj_exl['大型水库入库']

    # 上区来水
    sqls = np.array(jcsj_exl['上区来水'])
    sqls = sqls.reshape(sqls.shape[0], 1)

    # 河道径流=引提水径流 =（本区径流 - 大型水库）*径流系数
    hdjl = (bqjl - dxsk) * k

    # 中小水库径流=本区-大型-引体
    zxskjl = np.array(bqjl - dxsk - hdjl)
    # np的数据格式从一维的（24，），转为二维的（24，1）
    zxskjl = zxskjl.reshape(zxskjl.shape[0], 1)

    # 大型水库的数据需要再计算完  zxskjl 后，再数据格式一维转二维
    dxsk = np.array(dxsk)
    dxsk = dxsk.reshape(dxsk.shape[0], 1)


    # 外调水
    wds = np.array(jcsj_exl['调水量'])
    wds_np = wds.reshape(wds.shape[0], 1)


    dxxs_exl = load_pd_data(fenqu_file_path, fenqu_name, '地下水供水', 'Sheet1', index_col=False, usecols=None)
    # 地下需水
    di_xia_xu_shui = dxxs_exl.iloc[:, 3:-1]
    di_xia_xu_shui = np.array(di_xia_xu_shui)

    phxs_exl = load_pd_data(fenqu_file_path, fenqu_name, '破坏系数', 'Sheet1', index_col=False, usecols=None)
    # 破坏系数
    phxs = np.array(phxs_exl.iloc[:, 3:])


    hdjl_np = np.array(hdjl)
    hdjl_np = hdjl_np.reshape(hdjl_np.shape[0], 1)
    return (sqls, xu_shui, di_xia_xu_shui, zxskjl, dxsk,  wds_np,
            phxs,# 破坏系数
            bqjl_np,# 本区径流
            hdjl_np,# 河道径流
            hgxs,# 回归水系数
            Vx,# 兴利库容
            Vxx,# 汛限库容
            Vdead,# 死库容
            )


# 根据分区名称，获取文件夹路径位置，并返回fenqu_file_path
def return_file_path(target_folder_name):
    # 当前路径
    current_path = Path.cwd()
    # linux 环境路径 ,windows也适用
    f_p=Path(current_path).joinpath('./data_base/xx_files')

    for path in Path(f_p).rglob('*'):
        if path.is_dir() and path.name == target_folder_name:
            fenqu_file_path=path
            print(f'Found folder: {path}')

            return fenqu_file_path

# 根据分区名称，获取文件夹路径位置，并声明为全局变量
def get_file_path(target_folder_name):
    global fenqu_file_path
    global fenqu_name
    fenqu_name=target_folder_name

    fenqu_file_path=return_file_path(target_folder_name)



# 根据水库名称，获取文件夹路径位置
def get_file_path_sk(target_folder_name):
    global shuiku_file_path
    global shuiku_name
    shuiku_name=target_folder_name
    # 当前路径
    current_path = Path.cwd()
    # linux 环境路径 ,windows也适用
    f_p=Path(current_path).joinpath('./data_base/xx_水库')

    # windows 使用路径用\，不同系统要修改
    for path in Path(f_p).rglob('*'):
        if path.is_dir() and path.name == target_folder_name:
            shuiku_file_path=path
            print(f'Found folder: {path}')
# 根据水库名称，获取文件夹路径位置
def get_file_path_sk2(target_folder_name):
    global shuiku_file_path2
    global shuiku_name2
    shuiku_name2=target_folder_name
    # 当前路径
    current_path = Path.cwd()
    # linux 环境路径 ,windows也适用
    f_p=Path(current_path).joinpath('./data_base/xx_水库')

    # windows 使用路径用\，不同系统要修改
    for path in Path(f_p).rglob('*'):
        if path.is_dir() and path.name == target_folder_name:
            shuiku_file_path2=path
            print(f'Found folder: {path}')


def trans_pd(ques1, ques2, ques3, ques4, ques5, ques6,
             ques7, ques8, ques9,ques10, ques11, ques12, ques13, ques14, ques15, ques16, HJQUES, hj_name):
    QS1 = pd.DataFrame(ques1, columns=[columns_arr[0]])
    QS2 = pd.DataFrame(ques2, columns=[columns_arr[1]])
    QS3 = pd.DataFrame(ques3, columns=[columns_arr[2]])
    QS4 = pd.DataFrame(ques4, columns=[columns_arr[3]])
    QS5 = pd.DataFrame(ques5, columns=[columns_arr[4]])
    QS6 = pd.DataFrame(ques6, columns=[columns_arr[5]])
    QS7 = pd.DataFrame(ques7, columns=[columns_arr[6]])
    QS8 = pd.DataFrame(ques8, columns=[columns_arr[7]])
    QS9 = pd.DataFrame(ques9, columns=[columns_arr[8]])
    QS10 = pd.DataFrame(ques10, columns=[columns_arr[9]])
    QS11 = pd.DataFrame(ques11, columns=[columns_arr[10]])
    QS12 = pd.DataFrame(ques12, columns=[columns_arr[11]])
    QS13 = pd.DataFrame(ques13, columns=[columns_arr[12]])
    QS14 = pd.DataFrame(ques14, columns=[columns_arr[13]])
    QS15 = pd.DataFrame(ques15, columns=[columns_arr[14]])
    QS16 = pd.DataFrame(ques16, columns=[columns_arr[15]])
    HJQUES1 = pd.DataFrame(HJQUES)
    HJQUES2 = pd.DataFrame(HJQUES, columns=[hj_name])
    return HJQUES1, HJQUES2, QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9,QS10, QS11, QS12, QS13, QS14, QS15, QS16


# 根据水库名称，获取文件夹路径位置，并返回文件夹路径
def get_skfile_path_with_return(target_folder_name):
    shuiku_file_path = None
    # 当前路径
    current_path = Path.cwd()
    f_p = Path(current_path).joinpath('./data_base/xx_水库')

    for path in Path(f_p).rglob('*'):
        if path.is_dir() and path.name == target_folder_name:
            shuiku_file_path = path
            print(f'Found folder: {path}')

    return shuiku_file_path


def shuikuGS_17(skzgs,
                skxs,
                stxx,  # 生态下泄的需水
                ):
    '''
    bk: 水库供水，分行业
    skzgs:  总供水
    skxs: 需水，分行业
    skzxs: 总需水


    # xs_fhy 计算后返回的 加一个shuikuGS_17 第一个计算生态的供水缺水，最后返回
    # SKQS17,SKGS0  或分着SKQS16 单独返回，然后单独返回生态的供水 ，直接加到出境水里，接下来的河道径流计算不算
    # 供水 SKGS0 2-17   先不算   计算发电量 的合计值 为流量，  N
    # 生态排第一，2-17对应区间供水的1-16
    # 计算返回的生态下写 直接加到 出境水里
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
    # todo 计算平衡 skzgsxx 保存 作为水库下泄，用到区间出境，最后加进去，出境水
    # 出境水=+xiaxie
    # skgsxx 要作为水库里计算输出的下泄里 的生态下泄

    skgsxx, skhgsxx, skquesxx, skqsxx = calc_shuiku(stxx, skzgs)
    # skques1 可能需要单独算水库的保证率
    skgs1, skhgs1, skques1, skzgs2 = calc_shuiku(skxs1, skqsxx)
    skgs2, skhgs2, skques2, skzgs3 = calc_shuiku(skxs2, skzgs2)
    skgs3, skhgs3, skques3, skzgs4 = calc_shuiku(skxs3, skzgs3)
    skgs4, skhgs4, skques4, skzgs5 = calc_shuiku(skxs4, skzgs4)
    skgs5, skhgs5, skques5, skzgs6 = calc_shuiku(skxs5, skzgs5)
    skgs6, skhgs6, skques6, skzgs7 = calc_shuiku(skxs6, skzgs6)
    skgs7, skhgs7, skques7, skzgs8 = calc_shuiku(skxs7, skzgs7)
    skgs8, skhgs8, skques8, skzgs9 = calc_shuiku(skxs8, skzgs8)
    skgs9, skhgs9, skques9, skzgs10 = calc_shuiku(skxs9, skzgs9)
    skgs10, skhgs10, skques10, skzgs11 = calc_shuiku(skxs10, skzgs10)
    skgs11, skhgs11, skques11, skzgs12 = calc_shuiku(skxs11, skzgs11)
    skgs12, skhgs12, skques12, skzgs13 = calc_shuiku(skxs12, skzgs12)
    skgs13, skhgs13, skques13, skzgs14 = calc_shuiku(skxs13, skzgs13)
    skgs14, skhgs14, skques14, skzgs15 = calc_shuiku(skxs14, skzgs14)
    skgs15, skhgs15, skques15, skzgs16 = calc_shuiku(skxs15, skzgs15)
    skgs16, skhgs16, skques16, skzgs17 = calc_shuiku(skxs16, skzgs16)

    # 二维矩阵按列合并
    SKGS0 = np.concatenate((skgs1, skgs2, skgs3,
                            skgs4, skgs5, skgs6,
                            skgs7, skgs8, skgs9,
                            skgs10, skgs11, skgs12,
                            skgs13, skgs14, skgs15, skgs16), axis=1)

    SKQS17 = np.concatenate((skques1, skques2, skques3,
                             skques4, skques5, skques6,
                             skques7, skques8, skques9,
                             skques10, skques11, skques12,
                             skques13, skques14, skques15, skques16), axis=1)

    return SKQS17, SKGS0, skgsxx


# 判断文件是否存在
def check_file_exist(f_path, fname):
    exl_file = Path(f'{f_path}/{fname}.xlsx')

    return exl_file.exists()


# 获取水库需要读取的数据 尼尔基水库等需要调度图就返回，还有不需要调度图的就返回空，
#  根据判断本地文件是否有调度图文件来返回？暂时就先这样
# 丰满 牡丹江 尼尔基 镜泊湖 察尔森 需要调度图，需要获取调度线，其他暂时不用
# 但是也有需要调度图的
def prepare_shuiku_data_common(sk_f_path, sk_name):
    xushui_exl = load_pd_data(sk_f_path, sk_name, '需水', 'Sheet1', index_col=False, usecols=None)

    # 如果年旬天，没初始化，就调用 get_nxt 初始化一下
    if len(g_year)==0 :
        get_nxt(xushui_exl)

    # 需水
    xu_shui = xushui_exl.iloc[:, 3:-1]
    xu_shui = np.array(xu_shui)

    if not check_file_exist(sk_f_path, '调度图调度线'):
        flmb_table = None
        dd_table = None
        bxll_line = None
        bxsw_line = None

        if_N = False  # 是否计算发电
    else:
        if_N = True  # 是否计算发电

        diaodu_exl = load_pd_data(sk_f_path, sk_name, '调度图调度线', 'Sheet1', index_col=False, usecols=None)

        # 调度图
        dd_table = diaodu_exl.iloc[:8, 1:]
        dd_table = np.array(dd_table)

        # 放流目标
        flmb_table = diaodu_exl.iloc[9:18, 1:]
        flmb_table = np.array(flmb_table)

        # 坝下水位 流量
        bxswll_exl = load_pd_data(sk_f_path, sk_name, '水库坝下水位-流量关系曲线', 'Sheet1', index_col=False,
                                  usecols=None)
        bxsw_line = np.array(bxswll_exl['水位'])
        bxll_line = np.array(bxswll_exl['流量'])

        bxsw_line = bxsw_line.reshape(bxsw_line.shape[0], 1)
        bxll_line = bxll_line.reshape(bxll_line.shape[0], 1)
        # 清除曲线中的0值，否则差值计算的时候会出错
        bxll_line = empty_np_0(bxll_line)
        bxsw_line = empty_np_0(bxsw_line)

    # 水库输入长系列
    skcxl_exl = load_pd_data(sk_f_path, sk_name, '水库输入长系列', 'Sheet1', index_col=False, usecols=None)
    dxsk_rk = np.array(skcxl_exl['大型水库入库'])
    stxx = np.array(skcxl_exl['生态下泄'])

    dxsk_rk = dxsk_rk.reshape(dxsk_rk.shape[0], 1)
    stxx = stxx.reshape(stxx.shape[0], 1)

    # 渗漏强度过程线
    S_exl = load_pd_data(sk_f_path, sk_name, '渗漏强度过程线', 'Sheet1', index_col=False, usecols=None)
    S = np.array(S_exl['渗漏强度过程线'])
    S = S.reshape(S.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    S = empty_np_0(S)

    # 蒸发强度过程线
    Z_exl = load_pd_data(sk_f_path, sk_name, '蒸发强度过程线', 'Sheet1', index_col=False, usecols=None)
    Z = np.array(Z_exl['蒸发强度过程线'])
    Z = Z.reshape(Z.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    Z = empty_np_0(Z)

    # 水库输入-库容
    kr_exl = load_pd_data(sk_f_path, sk_name, '水库输入-库容', 'Sheet1', index_col=False, usecols=None)
    kr_line = np.array(kr_exl['水库输入-库容'])
    kr_line = kr_line.reshape(kr_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    kr_line = empty_np_0(kr_line)

    # 水库输入-面积
    mj_exl = load_pd_data(sk_f_path, sk_name, '水库输入-面积', 'Sheet1', index_col=False, usecols=None)
    mj_line = np.array(mj_exl['水库输入-面积'])
    mj_line = mj_line.reshape(mj_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    mj_line = empty_np_0(mj_line)

    # 水库输入-水位
    sw_exl = load_pd_data(sk_f_path, sk_name, '水库输入-水位', 'Sheet1', index_col=False, usecols=None)
    sw_line = np.array(sw_exl['水库输入-水位'])
    sw_line = sw_line.reshape(sw_line.shape[0], 1)
    # 清除曲线中的0值，否则差值计算的时候会出错
    sw_line = empty_np_0(sw_line)

    # 水库特性
    vvxd_exl = load_pd_data(sk_f_path, sk_name, '水库特性', 'Sheet1', index_col=False, usecols=None)
    # 兴利库容
    Vx = vvxd_exl.iloc[0, 1]
    # 汛限库容
    Vxx = vvxd_exl.iloc[0, 3]
    # 死库容
    Vdead = vvxd_exl.iloc[0, 0]


    # todo 需要读取表格中的数据
    Q_max = 2  # 机组最大过流能力
    N_max = 1000  # 最大出力
    # if_N = True  # 是否计算发电

    return (dd_table, flmb_table, bxsw_line, bxll_line,
            S, Z, kr_line, mj_line, sw_line, Vx, Vxx, Vdead,
            dxsk_rk, stxx, xu_shui,
        Q_max,  # 机组最大过流能力
        N_max,  # 最大出力
        if_N,  # 是否计算发电
     )

# 尼尔基水库 函数修改来的，通用水库计算，判断是否有调度曲线则是否获取出力等
def shuiku_common(
        L,
        xs_fhy,  # 分行业的缺水 需水
        Vx, Vxx, Vdead,
        Z,  # 水库 蒸发强度过程线
        S,  # 水库 渗漏强度过程线
        mj_line,  # 面积曲线
        sw_line,  # 水位曲线
        kr_line,  # 库容曲线 v
        dd_table,  # 调度线
        flmb_table,  # 放流目标表 下泄

        bxsw_line,  # 坝下水位 曲线
        bxll_line,  # 坝下流量 曲线

        stxx,  # 生态下泄
        # todo 生态那个肯定是流量 得*0.36*天数*24 就是生态的需水量
        sk_f_path,  # 水库的文件夹地址
        Q_max,  # 机组最大过流能力
        N_max,  # 最大出力
        if_N,  # 是否计算发电
):
    '''

    中小型水库计算 不包括蒸发、渗透、面积
    大型水库计算包括蒸发、渗透、面积

    V0: 初始库容 旬初库容
    L: 来水
    xs: 需水
    Vx: 兴利库容
    Vxx: 汛限库容  todo 汛限水位（m） 用上了么？
    Vdead: 死库容
    v: 体积
    m: 面积
    Z: 蒸发
    S: 渗漏
    mj_line:面积曲线
    sw_line:水位曲线
    kr_line:库容曲线

    flmb_table:放流目标表
    ddx_table: 调度线 表

                bxsw_line,#坝下水位 曲线
                bxll_line,#坝下流量 曲线

                #todo 干啥的？
                ,#水库长系列径流，需要相当于来水了？
    '''

    assert type(g_xun) == pd.core.series.Series
    # 16个行业的需水总和
    xs = xs_fhy.sum(axis=1)
    xs_16_sum = xs.reshape(xs.shape[0], 1)

    xs_17_sum = xs_16_sum + stxx

    # 表格的行数，动态获取
    Llength = L.shape[0]
    # ZF_all = [] 就会在ZF_all作为参数传递的时候然后就被改变，所以需要让他的数据类型是numpy
    # 函数参数默认是引用传递，这意味着当你将一个对象传递给函数并在函数内部改变它时，这个改变会反映在原始对象上。如果你不想改变原始对象
    ZF_all = np.empty(0)
    SL_all = np.empty(0)
    # 保存的旬末面积
    mj_xm_all = np.empty(0)
    # 保存的旬初面积
    mj_xc_all = np.empty(0)
    qs_all = np.empty(0)
    gs_all = np.empty(0)

    # 保存的旬末库容
    V_xm_all = np.empty(0)
    # 保存的旬初库容
    V_xc_all = np.empty(0)

    # 保存的旬末水位
    sw_xm_all = np.empty(0)
    # 保存的旬初水位
    sw_xc_all = np.empty(0)

    Q_all = np.empty(0)
    # 出力
    N_all = np.empty(0)

    # 上游库容
    sy_kr_all = np.empty(0)
    # 上游水位
    sy_sw_all = np.empty(0)
    #
    # # 下游水位
    xy_sw_all = np.empty(0)
    #
    # # 发电量
    # W_all = np.empty(0)

    # 第一遍试算的时候的v0
    V0 = Vx
    # 返回第一遍试算的数据
    (N_all_ss, Q_all_ss, SL_all_ss, V_xc_all_ss, V_xm_all_ss, ZF_all_ss,
     gs_all_ss, mj_xm_all_ss, qs_all_ss, sw_xm_all_ss, xy_sw_all_ss,
     mj_xc_all_ss, sw_xc_all_ss,
     sy_kr_all_ss, sy_sw_all_ss) = caluate_sk_x_gs(L, Llength, N_all, Q_all, SL_all,
                                                   V0, V_xc_all,
                                                   V_xm_all, Vdead, Vx, Vxx, ZF_all,
                                                   bxll_line,
                                                   bxsw_line,
                                                   dd_table, flmb_table, gs_all,
                                                   kr_line, mj_line,
                                                   mj_xm_all, qs_all, sw_line,
                                                   sw_xm_all, xs_17_sum,
                                                   xy_sw_all, Z, S,
                                                   mj_xc_all, sw_xc_all,
                                                   sy_kr_all, sy_sw_all)

    # 第一遍试算之后获取的第一个时段的V0就等于最后一个时段的旬末库容
    V0 = V_xm_all_ss[-1]

    (N_all, Q_all, SL_all, V_xc_all, V_xm_all, ZF_all,
     gs_all, mj_xm_all, qs_all, sw_xm_all, xy_sw_all,
     mj_xc_all, sw_xc_all,
     sy_kr_all, sy_sw_all) = caluate_sk_x_gs(L, Llength, N_all, Q_all, SL_all, V0, V_xc_all,
                                             V_xm_all, Vdead, Vx, Vxx, ZF_all, bxll_line,
                                             bxsw_line,
                                             dd_table, flmb_table, gs_all, kr_line, mj_line,
                                             mj_xm_all, qs_all, sw_line, sw_xm_all, xs_17_sum,
                                             xy_sw_all, Z, S,
                                             mj_xc_all, sw_xc_all,
                                             sy_kr_all, sy_sw_all)
    #
    # # 当前路径
    # current_path = Path(f'{Path.cwd()}/xx_测试输出')
    #
    # shuchu_test(current_path, 'ZF_all', ZF_all, ['ZF_all'])
    # shuchu_test(current_path, 'SL_all', SL_all, ['SL_all'])
    # shuchu_test(current_path, 'mj_all', mj_xm_all, ['mj_all'])
    # if dd_table is not None:
    #     shuchu_test(current_path, 'Q_all', Q_all, ['Q_all'])
    #     shuchu_test(current_path, 'N_all', N_all, ['N_all'])
    #     shuchu_test(current_path, 'xy_sw_all', xy_sw_all, ['xy_sw_all'])
    # #     todo 输出长度不够……对应应该是有缺少的地方
    #
    # gs_all_np = np.array([gs_all]).T

    # 一维变二维
    gs_all_2 = gs_all.reshape(gs_all.shape[0], 1)
    SKQS17, SKGS0, skgsxx = shuikuGS_17(gs_all_2,
                                        xs_fhy,
                                        stxx,  # 生态下泄的需水
                                        )
    # shuchu_test(current_path, 'SKQS17', SKQS17, columns_arr)
    # shuchu_test(current_path, 'SKGS0', SKGS0, columns_arr)
    #
    # qs_all_np = np.array([qs_all]).T
    # #  下泄=生态的供水+弃水 todo? 这个是保存在exl表里的？上边那个是 用上了的意思
    # # 如果有调度图，下泄就是Q
    # xiaxie = skgsxx + qs_all_np
    # shuchu_test(current_path, 'xiaxie', xiaxie, ['xiaxie'])

    # print('---------------------mj_xc_all')
    # print(mj_xc_all)
    # todo 下泄 = 生态的供水 + 弃水 ？

    qs = qs_all.reshape(qs_all.shape[0], 1)
    # if dd_table is None:
    #     Q_all = qs + skgsxx
    Q_all = qs + skgsxx

    # # 判断是否要计算发电
    if if_N:
        Q_all=get_W_N(Q_all, Q_max, bxll_line, bxsw_line, sy_sw_all, N_max,sk_f_path)



    sk_shuchu(
        sk_f_path,  # 水库的文件夹地址
        V_xc_all,  # 旬初库容
        mj_xc_all,  # 旬初面积
        sw_xc_all,  # 旬初水位
        xs_fhy,  # 水库分行业破坏后需水
        SKGS0,  # 水库分行业供水
        V_xm_all,  # 旬末库容
        mj_xm_all,  # 旬末面积
        sw_xm_all,  # 旬末水位
        ZF_all,  # 蒸发
        SL_all,  # 渗漏
        Q_all,  # 下泄
        skgsxx,  # 生态下泄的计算后供水
        L,  # 入库
        qs,  #
    )

    return SKGS0
    # return SKGS0, ZF, SL, qs, V2, V3, jh, GS0, SKQS17, df2


def get_W_N(Q_all,Q_max,bxll_line,bxsw_line, sy_sw_all,N_max,sk_file_path):
    # 出力
    N_all = np.empty(0)
    # 下游水位
    xy_sw_all = np.empty(0)

    # 发电量
    W_all = np.empty(0)

    for i in range(Q_all.shape[0]):
        # 如果Q大于1300立方米每秒，按1300来计算 todo 这个是尼尔基的机组最大过流量，不是尼尔基不用判断
        if Q_max is not None:

            if Q_all[i] >= Q_max:
                Q_all[i] = Q_max

        #  差值求得下游水位，
        xy_sw = Chazhi_new(bxll_line, bxsw_line, Q_all[i])
        xy_sw_all = np.append(xy_sw_all, arrer_to_float(xy_sw))

        # 拟定出力
        N = get_N((sy_sw_all[i] - xy_sw), Q_all[i])
        if N_max is not None:
            if N >= N_max:
                N = N_max
        N_all = np.append(N_all, arrer_to_float(N))

        # 发电量=N*时间（天）
        W = N * g_day[i] * 24
        W_all = np.append(W_all, arrer_to_float(W))



    shuchu_path = Path(f'{sk_file_path}/输出')
    # 一维的numpy合并作为列
    N_W_shuchu = np.column_stack((sy_sw_all, xy_sw_all,Q_all, N_all,W_all))

    shuchu_test(shuchu_path, '出力、发电量', N_W_shuchu, ['上游水位', '下游水位','下游流量', '出力','发电量'])

    return Q_all


# 逐时段循环计算水库的合计供水、各种库容等
def caluate_sk_x_gs(L, Llength, N_all, Q_all, SL_all, V0, V_xc_all, V_xm_all, Vdead, Vx, Vxx, ZF_all,
                    bxll_line, bxsw_line, dd_table, flmb_table,
                    gs_all, kr_line, mj_line, mj_xm_all, qs_all, sw_line, sw_xm_all, xs,
                    xy_sw_all, Z, S,
                    mj_xc_all, sw_xc_all,
                    sy_kr_all, sy_sw_all):
    for i in range(0, Llength):
        if (g_xun[i] >= 18 and g_xun[i] <= 27):
            # if (g_xun[i] >= 6 and g_xun[i] <= 9):

            Vmax = Vxx
        #     汛线水位库容应该包括死库容Vdead
        else:
            Vmax = Vx

        # 第一遍计算V0=Vx，之后在计算一遍。获取最终时段末尾的旬末库容，为V0
        if i != 0:
            V0 = V_xm_all[i - 1]

        Vc = V0
        # 上一个时段的旬末库容等于这个时段的旬初库容
        # Vc 旬初库容
        if Vc >= Vmax:
            Vc = Vmax

        V1 = Vc + L[i] - xs[i]  # 旬末库容

        # 如果小于死库，大于的时候16个分行业的供水就等于需水
        if V1 <= Vdead:
            # 不供水

            V2 = Vdead

            # V平均
            Vpj = (Vc + V1) / 2
            # sw2 = Chazhi_new(kr_line, sw_line, V2)  # 由库容求水位  todo 没用上？
            # mj2 = Chazhi_new(kr_line, mj_line, V2)  # 由库容求面积
            #
            # ZF2 = mj2 * Z[g_xun[i] - 1] / 10  # 蒸发 的损失
            # SL2 = mj2 * S[g_xun[i] - 1] / 10  # 渗漏

            # 对应的蒸发渗漏乘以的是对应旬的曲线，对应是第二旬的，获取蒸发的第二个数据，Z从0记第一个数据，所以要旬-1
            sw2, mj2, ZF2, SL2 = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, Vpj)
            # sw2, mj2, ZF2, SL2 = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, V2)

            # gs =0
            gs = V0 + L[i] - Vdead - ZF2 - SL2

            V2 = V0 + L[i] - gs - ZF2 - SL2
            qs = 0

        #     直接算发电 todo ？要干啥来着

        else:
            gs = xs[i]
            qs = 0
            if V1 >= Vmax:

                # Vxiax = V0 - Vmax
                # qs = V0 - Vmax
                V1 = Vmax

                # 根据V1试算面积1，水位1 粗算
                #  有的水位的曲线全是0，就可能数据不全，可能就根本不计算这个水库

                sw1, mj1, ZF1, SL1 = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, V1)
                # # sw1 = Chazhi_new(kr_line, sw_line, V1)  # 由库容求水位   没用上？
                # mj1 = Chazhi_new(kr_line, mj_line, V1)  # 由库容求面积
                #
                # ZF1 = mj1 * Z[g_xun[i] - 1] / 10  # 蒸发 的损失
                # SL1 = mj1 * S[g_xun[i] - 1] / 10  # 渗漏

                # 精算的库容2 todo 是不是旬末库容？
                V2 = V1 - ZF1 - SL1
                # V2 = V1 - xs[i] - ZF1 - SL1
                # V2 = qs - xs[i] - ZF1 - SL1

                V2 = (V2 + V1) / 2
                #  根据V2试算面积2，水位2 精细算

                sw2, mj2, ZF2, SL2 = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, V2)

                # V2 = V1  - ZF2 - SL2
                V2 = V0 + L[i] - gs - ZF2 - SL2
                # V2 = V1 - xs[i] - ZF2 - SL2

                # 上游库容
                sy_kr = (Vc + V2) / 2
                # sy_kr = (V1 + V2) / 2
                # sy_kr = (qs + V2) / 2
                # 上游水位
                sy_sw = Chazhi_new(kr_line, sw_line, sy_kr)
                #     todo 这个上游水位是？对应要干啥？
                #      对应保存再输出表里的旬末水位是sw2 啊，
                #      这个是要算发电？

                # 只要超过Vmax，弃水就等于V初+L-zf-sl-gs-Vmax
                qs = V0 + L[i] - ZF2 - SL1 - Vmax
            else:
                #  根据V1试算面积1，水位1 粗算 todo 这个是旬末的库容粗算的水位？

                sw1, mj1, ZF1, SL1 = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, V1)
                # 精算的库容2
                V2 = V1 - ZF1 - SL1
                # V2 = V1 - xs[i] - ZF1 - SL1

                V2 = (V2 + V1) / 2

                # breakpoint()
                # #  根据V2试算面积2，水位2 精细算
                # sw2 = Chazhi_new(kr_line, sw_line, V2)  # 由库容求水位
                # mj2 = Chazhi_new(kr_line, mj_line, V2)  # 由库容求面积 todo 然后用它干啥了
                #
                # # 保存
                # ZF2 = mj2 * Z[g_xun[i] - 1] / 10  # 蒸发 的损失
                # SL2 = mj2 * S[g_xun[i] - 1] / 10  # 渗漏

                sw2, mj2, ZF2, SL2 = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, V2)

                V2 = V0 + L[i] - gs - ZF2 - SL2
                # todo 这个的发电，计算啥的，得再看一遍是咋计算的
                # # 如果有调度图曲线，再获取下泄流量，出力，下游水位
                # if dd_table is not None:
                #     Qok, Nok, xy_sw = get_qnsw(V1, V2, bxll_line, bxsw_line, dd_table, flmb_table, i, kr_line, sw2,
                #                                sw_line)
                #
                #     Q_all.append(arrer_to_float(Qok))
                #     N_all.append(arrer_to_float(Nok))
                #     xy_sw_all.append(arrer_to_float(xy_sw))
        #             xy_sw_all 如果有 水库坝下水位-流量关系曲线 ，就计算，

        # ZF_all.append(arrer_to_float(ZF2))
        # 用np的方式添加数据
        ZF_all = np.append(ZF_all, arrer_to_float(ZF2))
        SL_all = np.append(SL_all, arrer_to_float(SL2))
        # 弃水保存，用在下泄
        qs_all = np.append(qs_all, arrer_to_float(qs))
        gs_all = np.append(gs_all, arrer_to_float(gs))

        V_xm_all = np.append(V_xm_all, arrer_to_float(V2))
        sw_xm_all = np.append(sw_xm_all, arrer_to_float(sw2))
        mj_xm_all = np.append(mj_xm_all, arrer_to_float(mj2))
        V_xc_all = np.append(V_xc_all, arrer_to_float(Vc))

        # 根据旬初库容获取旬初的面积水位
        swc, mjc, ZFc, SLc = v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, g_xun[i] - 1, Vc)
        mj_xc_all = np.append(mj_xc_all, arrer_to_float(mjc))
        sw_xc_all = np.append(sw_xc_all, arrer_to_float(swc))

        # 上游库容
        sy_kr = (Vc + V2) / 2

        sy_kr_all = np.append(sy_kr_all, arrer_to_float(sy_kr))

        # 上游水位
        sy_sw = Chazhi_new(kr_line, sw_line, sy_kr)
        sy_sw_all = np.append(sy_sw_all, arrer_to_float(sy_sw))

    return (N_all, Q_all, SL_all, V_xc_all, V_xm_all, ZF_all,
            gs_all, mj_xm_all, qs_all, sw_xm_all, xy_sw_all,
            mj_xc_all, sw_xc_all,
            sy_kr_all, sy_sw_all)


# 由库容获取水位、面积、蒸发、渗漏
def v_get_sw_mj_zf_sl(kr_line, sw_line, mj_line, Z, S, xun_num, V):
    #  根据V2试算面积2，水位2 精细算
    sw = Chazhi_new(kr_line, sw_line, V)  # 由库容求水位
    mj = Chazhi_new(kr_line, mj_line, V)  # 由库容求面积 todo 然后用它干啥了

    # 保存
    ZF = mj * Z[xun_num] / 10  # 蒸发 的损失
    SL = mj * S[xun_num] / 10  # 渗漏

    return sw, mj, ZF, SL


# 计算下游水位，出力，下泄
def get_qnsw(V1, V2, bxll_line, bxsw_line, dd_table, flmb_table, i, kr_line, sw2, sw_line):
    # 用sw2
    #  判断水位位于调度图的位置，然后按照调度图（放流目标）确定下泄流量
    # 获取下泄流量或是发电保证出力
    ll_cl = get_dd_xx(sw2, dd_table, flmb_table, g_xun[i])
    # 上游库容
    sy_kr = (V1 + V2) / 2
    # 上游水位
    sy_sw = Chazhi_new(kr_line, sw_line, sy_kr)
    # 如果是4-10月就是下泄流量
    if (g_xun[i] >= 11 and g_xun[i] <= 30):
        #  差值求得下游水位，

        xy_sw = Chazhi_new(bxll_line, bxsw_line, ll_cl)

        # 直接计算发电出力
        Nok = 9.81 * ll_cl * (sy_sw - xy_sw) * 0.85
        Qok = ll_cl

    # 如果是1-3  11-12月
    else:
        # 确定发电保证出力，todo sl_cl就是出力吧 ？
        # todo 不同月份  保证出力要×不同区域的系数    系数=sl_cl   保证力是输入还是写死？再问
        # 保证出力
        Nbz = ll_cl
        # todo 初步拟定下泄流量？就是生态下泄流量吧？
        #  然后拟定计算的出力与保证出力误差0.001 就增多少拟定的下泄流量？用二分法，50到150取值

        max_num = 150
        min_num = 50
        # 返回确定的下泄流量,确定的保证出力
        Qok, Nok = get_Nok(min_num, max_num, bxll_line, bxsw_line, sy_sw, Nbz)

        xy_sw = Chazhi_new(bxll_line, bxsw_line, Qok)

    return Qok, Nok, xy_sw


# 输出临时查看文件

def shuchu_test(shuchu_path, exl_name, data, colm_name):
    # 同名表如果存在就覆盖
    # shuchu_file=Path(f'{fenqu_file_path}/输出')
    data_pd = pd.DataFrame(data)
    data_pd = data_pd.set_axis(colm_name, axis='columns')
    hebing_shuchu = pd.concat([g_year, g_xun, g_day, data_pd], axis=1)  # 按列合并
    shuchu_file = Path(shuchu_path)
    f_path = Path(f'{shuchu_path}/输出_{exl_name}.xlsx')
    # 如果文件夹不存在，就创建它
    if not shuchu_file.exists():
        shuchu_file.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(f_path, engine='openpyxl',
                        mode='w',  # 追加模式,不覆盖其他文件
                        ) as writer:
        hebing_shuchu.to_excel(writer, sheet_name='sheet1', index=False)


def sk_shuchu(
        sk_file_path,  # 水库的文件夹地址
        V_xc_all,  # 旬初库容
        mj_xc_all,  # 旬初面积
        sw_xc_all,  # 旬初水位
        xs_fhy,  # 水库分行业破坏后需水
        SKGS0,  # 水库分行业供水
        V_xm_all,  # 旬末库容
        mj_xm_all,  # 旬末面积
        sw_xm_all,  # 旬末水位
        ZF_all,  # 蒸发
        SL_all,  # 渗漏
        Q_all,  # 下泄
        skgsxx,  # 生态下泄的计算后供水
        L,  # 入库
        qs,  #
):
    shuchu_path = Path(f'{sk_file_path}/输出')
    # --------------------------------旬初库容--旬初水位-旬初面积---------------------------------
    # 一维的numpy合并作为列
    Vcswmj = np.column_stack((V_xc_all, sw_xc_all, mj_xc_all))
    shuchu_test(shuchu_path, '旬初库容、水位、面积', Vcswmj, ['旬初库容', '旬初水位', '旬初面积'])

    # ------------------------------水库分行业破坏后需水-----------------------------------
    sum_xushui = xs_fhy.sum(axis=1)
    hebing_columns_arr = columns_arr + ['合计']

    # 一个二维的numpy数组和一个一维的numpy数组合并，hstack水平合并
    xs_shuchu_np = np.hstack((xs_fhy, sum_xushui[:, None]))
    shuchu_test(shuchu_path, '水库破坏后需水', xs_shuchu_np, hebing_columns_arr)

    # ------------------------------水库分行业供水-----------------------------------
    # 一个二维的numpy数组和一个一维的numpy数组合并，hstack水平合并
    sum_SKGS0 = SKGS0.sum(axis=1)
    hebing_columns_arr = columns_arr + ['合计']

    gs_shuchu_np = np.hstack((SKGS0, sum_SKGS0[:, None]))
    shuchu_test(shuchu_path, '水库分行业供水', gs_shuchu_np, hebing_columns_arr)

    # --------------------------------旬末库容--旬末水位-旬末面积---------------------------------
    # 一维的numpy合并作为列
    Vcswmj = np.column_stack((V_xm_all, sw_xm_all, mj_xm_all))
    shuchu_test(shuchu_path, '旬末库容、水位、面积', Vcswmj, ['旬末库容', '旬末水位', '旬末面积'])

    # ------------------------------     检验=旬初库容+入库-供水（包含生态、16供水）-蒸发-渗漏-下泄-旬末库容-----------------------------------
    # ------------------------------检验=旬初库容+入库-蒸发-渗漏-下泄-旬末库容-16供水-----------------------------------
    # 一维变二维，方便计算
    sum_GS = sum_SKGS0.reshape(sum_SKGS0.shape[0], 1)
    V_xc = V_xc_all.reshape(V_xc_all.shape[0], 1)
    V_xm = V_xm_all.reshape(V_xm_all.shape[0], 1)
    ZF = ZF_all.reshape(ZF_all.shape[0], 1)
    SL = SL_all.reshape(SL_all.shape[0], 1)
    Q = Q_all.reshape(Q_all.shape[0], 1)

    # jy = V_xc + L - sum_GS - skgsxx - ZF - SL - Q - V_xm
    jy = V_xc + L - ZF - SL - Q - V_xm - sum_GS
    # todo 如果供水和下泄有重复的行业，应单独计算
    #  如果供水给河道，然后就在下泄里计入的供水行业，就不再重复扣除

    # 二维矩阵按列合并
    jy_hebing = np.concatenate((V_xc, L, sum_GS, skgsxx, ZF, SL, Q, qs, V_xm, jy), axis=1)
    shuchu_test(shuchu_path, '检验', jy_hebing,
                ['旬初库容', '入库', '16行业合计供水', '生态下泄供水', '蒸发', '渗漏', '下泄', '弃水', '旬末库容',
                 '检验'])
