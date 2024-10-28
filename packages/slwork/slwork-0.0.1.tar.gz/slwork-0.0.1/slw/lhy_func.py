import pandas as pd
import numpy as np
from .add_code import save_frame
from .slw_const import *


def Chazhi(x, y, xi):  # 参数一组升序排列的长度相等的x列表和y列表，以及给定一个x值
    # todo：超出处理 数值在曲线范围外，就用他临近的两个点来算斜率，来计算差值
    # 中小型不计算
    for j in range(len(x)):
        if xi >= x[j] and xi < x[j + 1]:
            yi = y[j] + (xi - x[j]) / (x[j + 1] - x[j]) * (y[j + 1] - y[j])
    return yi


def shuiku0(V0, L, xs, y, n, Vx, Vxx, Vdead, v, m, Z, S):
    '''
    # 水库供水只考虑了总供水，未分行业

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



    GS0 = []
    QS0 = []
    df2 = pd.DataFrame()

    for i in range(0, 732):
        V2 = V0 + L[i] - xs[i]  # L.loc[i] 可以读取0  12282.19


        if (y[i] >= 6 and y[i] <= 9):
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
        # print(V1)
        mj = Chazhi(v, m, V1)  # 由库容求面积

        ZF = mj * Z[i] / 10  # 蒸发
        SL = mj * S[i] / 10  # 渗漏
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
    for i in range(0, 732):
        V2 = V0 + L[i] - xs[i]
        if (y[i] >= 6 and y[i] <= 9):  #todo：月改成旬的话，怎么计算
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

        mj = Chazhi(v, m, V1)  # 由水位求库容

        ZF = mj * Z[i] / 10
        SL = mj * S[i] / 10
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

        df2 = pd.concat([df2, pd.DataFrame(
            {'年': n[i], '月': y[i], '初库容': V0, '来水': L[i], '需水': xs[i], '供水': gs, '蒸发': ZF, '渗漏': SL,
             '弃水': qs, '末库容': V3, '校核': jh})],
                        ignore_index=False)

        GS0.extend([[gs]])  # numpy.int64  not iterable  ，int ，float  not  iterable ？？？？  GS0.append(gs) 输出数据带方括号

        # print(GS2)
        QS0.extend(qs)  # extend 要求可迭代数据 ，qs里面含有0，不可迭代的数,[0]是可迭代了
        # print(qs)
        # SKGS=pd.DataFrame(GS2)
        # SKQS = pd.DataFrame(QS2)
        V0 = V3
    # todo:原代码返回  ： return(gs,qs),按此代码执行会报错：Traceback (most recent call last):
    #   File "/home/lihy/coding/forge/slw/raw_2/xx_run_lhy_1.py", line 53, in <module>
    #     ph_hcgsk = df2
    #     所以改为了按全局变量返回

    # NameError: name 'df2' is not defined
    # return (gs, qs)
    return gs, ZF, SL, qs, V2, V3, jh, GS0, QS0, df2
def zxx_shuiku0(V0, L, xs, y, n, Vx, Vxx, Vdead):
    '''
    中小型水库计算
    # 水库供水只考虑了总供水，未分行业

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


    GS0 = []
    QS0 = []
    df2 = pd.DataFrame()

    for i in range(0, 732):
        V2 = V0 + L[i] - xs[i]  # L.loc[i] 可以读取0  12282.19


        if (y[i] >= 6 and y[i] <= 9):
            Vm = Vxx
        else:
            Vm = Vx
        assert V2.shape == (1,)


        if V2 >= Vm:
            V2 = Vm
        else:
            V2 = V2
        if V2 <= Vdead:
            V2 = Vdead
        V1 = (V2 + V0) / 2


        mj = 0  # 由库容求面积

        ZF = 0  # 蒸发
        SL = 0  # 渗漏
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
    for i in range(0, 732):
        V2 = V0 + L[i] - xs[i]
        if (y[i] >= 6 and y[i] <= 9):#todo：月改成旬的话，怎么计算
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

        mj = 0  # 由水位求库容

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

        df2 = pd.concat([df2, pd.DataFrame(
            {'年': n[i], '月': y[i], '初库容': V0, '来水': L[i], '需水': xs[i], '供水': gs, '蒸发': ZF, '渗漏': SL,
             '弃水': qs, '末库容': V3, '校核': jh})],
                        ignore_index=False)

        GS0.extend([[gs]])  # numpy.int64  not iterable  ，int ，float  not  iterable ？？？？  GS0.append(gs) 输出数据带方括号

        # print(GS2)
        QS0.extend(qs)  # extend 要求可迭代数据 ，qs里面含有0，不可迭代的数,[0]是可迭代了
        # print(qs)
        # SKGS=pd.DataFrame(GS2)
        # SKQS = pd.DataFrame(QS2)
        V0 = V3
    # todo:原代码返回  ： return(gs,qs),按此代码执行会报错：Traceback (most recent call last):
    #   File "/home/lihy/coding/forge/slw/raw_2/xx_run_lhy_1.py", line 53, in <module>
    #     ph_hcgsk = df2
    #     所以改为了按全局变量返回

    # NameError: name 'df2' is not defined
    # return (gs, qs)
    return gs, ZF, SL, qs, V2, V3, jh, GS0, QS0, df2


def shuikuGS(skzgs, skxs, skzxs):
    '''
    bk: 水库供水，分行业
    skzgs:  总供水
    skxs: 需水，分行业
    skzxs: 总需水
    '''
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

    skzhgs = skhgs1 + skhgs2 + skhgs3 + skhgs4 + skhgs5 + skhgs6 + skhgs7 + skhgs8 + skhgs9 + skhgs10 + skhgs11 + skhgs12 + skhgs13 + skhgs14 + skhgs15 + skhgs16
    skzhgs_9 = skhgs1 + skhgs2 + skhgs3 + skhgs4 + skhgs5 + skhgs6 + skhgs7 + skhgs8 + skhgs10 + skhgs11 + skhgs12 + skhgs13 + skhgs14 + skhgs15 + skhgs16
    SKHGS_9 = pd.DataFrame(skzhgs_9)

    # bk: 下面一行单独添加的。
    skzgs, skzxs = skzgs.align(skzxs, axis=1, copy=False)
    skzqis = np.where(skzgs >= skzxs, skzgs - skzxs, 0.00)
    SKZQS = pd.DataFrame(skzqis)
    SKHGS = pd.DataFrame(skzhgs)

    SKHJGS = skgs1 + skgs2 + skgs3 + skgs4 + skgs5 + skgs6 + skgs7 + skgs8 + skgs9 + skgs10 + skgs11 + skgs12 + skgs13 + skgs14 + skgs15 + skgs16
    SKHJGS_9 = skgs1 + skgs2 + skgs3 + skgs4 + skgs5 + skgs6 + skgs7 + skgs8 + skgs10 + skgs11 + skgs12 + skgs13 + skgs14 + skgs15 + skgs16
    SKHJGS1_9 = pd.DataFrame(SKHJGS_9)  # 不算水田
    # F_SKGS =np.array([skgs1, skgs2, skgs3, skgs4, skgs5, skgs6, skgs7, skgs8, skgs9, skgs10, skgs11, skgs12, skgs13, skgs14, skgs15, skgs16])
    GS9_1 = pd.DataFrame(skgs9)

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
    SKHJGS1 = pd.DataFrame(SKHJGS, columns=['供水合计'])
    SKGS17 = pd.concat(
        [GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, SKHJGS1],
        axis=1)
    SKGS0 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16],
                      axis=1)

    F_SKGS = SKGS0.values.tolist()
    SKGS18 = pd.concat(
        [GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9 - GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16],
        axis=1)  # 去掉水田供水
    F_SKGS18 = SKGS18.values.tolist()

    # columns = SKGS0.columns
    # F_SKGS= []
    # for c in columns:
    # d = SKGS0[c].values.tolist()
    # F_SKGS.append(d)

    # print(GS1)
    # F_SKGS=np.concatenate(([skgs1],[skgs2],[skgs3],[skgs4],[skgs5],[skgs6],[skgs7],[skgs8],[skgs9],[skgs10],[skgs11],[skgs12],[skgs13],[skgs14],[skgs15],[skgs16]),axis=0)             # F_SKGS0=np.array(GS1).tolist()=skgs1

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
    SKQS17 = pd.concat([QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16], axis=1)
    return skzqis, SKZQS, SKHGS, SKGS17, SKQS17, SKHJGS, F_SKGS, F_SKGS18, GS9_1, SKHGS_9, SKHJGS1_9, SKGS0, skgs9


def calc_shuiku(skxs2, skzgs2, dbhgsxs2):
    skgs2 = np.where(skzgs2 >= skxs2, skxs2, np.where(skzgs2 >= 0, skzgs2, 0))
    skques2 = np.where(skzgs2 >= skxs2, 0, np.where(skzgs2 >= 0, skxs2 - skzgs2, 0))
    skqis2 = np.where(skzgs2 >= skxs2, skzgs2 - skxs2, 0)
    skhgs2 = skgs2 * dbhgsxs2
    skzgs3 = skqis2
    return skgs2, skhgs2, skques2, skzgs3


def gx(lai_shui, xu_shui, zong_xu_shui, di_xia_xu_shui, ss):
    '''
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

    xs1 = xu_shui[:, :1]  # 所有行的第一列数据

    # assert xs[:, :1].all() == xs [:, 1].all()
    xs2 = xu_shui[:, 1:2]  # 所有行的第二列数据
    # print(xs[:, 1:2].shape)
    # print(xs[:, 1].shape)
    assert xu_shui[:, 1:2].all() == xu_shui[:, 1].all()

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

    dx_gs1, dx_hgs1, gs1, hgs1, ls2, ques1, zhgs1 = calc_laishui(dx_xs1, lai_shui, xs1, dbhgsxs1)
    dx_gs2, dx_hgs2, gs2, hgs2, ls3, ques2, zhgs2 = calc_laishui(dx_xs2, ls2, xs2, dbhgsxs2)
    dx_gs3, dx_hgs3, gs3, hgs3, ls4, ques3, zhgs3 = calc_laishui(dx_xs3, ls3, xs3, dbhgsxs3)
    dx_gs4, dx_hgs4, gs4, hgs4, ls5, ques4, zhgs4 = calc_laishui(dx_xs4, ls4, xs4, dbhgsxs4)
    dx_gs5, dx_hgs5, gs5, hgs5, ls6, ques5, zhgs5 = calc_laishui(dx_xs5, ls5, xs5, dbhgsxs5)
    dx_gs6, dx_hgs6, gs6, hgs6, ls7, ques6, zhgs6 = calc_laishui(dx_xs6, ls6, xs6, dbhgsxs6)
    dx_gs7, dx_hgs7, gs7, hgs7, ls8, ques7, zhgs7 = calc_laishui(dx_xs7, ls7, xs7, dbhgsxs7)
    dx_gs8, dx_hgs8, gs8, hgs8, ls9, ques8, zhgs8 = calc_laishui(dx_xs8, ls8, xs8, dbhgsxs8)
    dx_gs9, dx_hgs9, gs9, hgs9, ls10, ques9, zhgs9 = calc_laishui(dx_xs9, ls9, xs9, dbhgsxs9)
    dx_gs10, dx_hgs10, gs10, hgs10, ls11, ques10, zhgs10 = calc_laishui(dx_xs10, ls10, xs10, dbhgsxs10)
    dx_gs11, dx_hgs11, gs11, hgs11, ls12, ques11, zhgs11 = calc_laishui(dx_xs11, ls11, xs11, dbhgsxs11)
    dx_gs12, dx_hgs12, gs12, hgs12, ls13, ques12, zhgs12 = calc_laishui(dx_xs12, ls12, xs12, dbhgsxs12)
    dx_gs13, dx_hgs13, gs13, hgs13, ls14, ques13, zhgs13 = calc_laishui(dx_xs13, ls13, xs13, dbhgsxs13)
    dx_gs14, dx_hgs14, gs14, hgs14, ls15, ques14, zhgs14 = calc_laishui(dx_xs14, ls14, xs14, dbhgsxs14)
    dx_gs15, dx_hgs15, gs15, hgs15, ls16, ques15, zhgs15 = calc_laishui(dx_xs15, ls15, xs15, dbhgsxs15)
    dx_gs16, dx_hgs16, gs16, hgs16, ls17, ques16, zhgs16 = calc_laishui(dx_xs16, ls16, xs16, dbhgsxs16)

    # bk:  # 总回归水， 退水，弃水
    zhgs = hgs1 + hgs2 + hgs3 + hgs4 + hgs5 + hgs6 + hgs7 + hgs8 + hgs9 + hgs10 + hgs11 + hgs12 + hgs13 + hgs14 + hgs15 + hgs16
    dx_zhgs = dx_hgs1 + dx_hgs2 + dx_hgs3 + dx_hgs4 + dx_hgs5 + dx_hgs6 + dx_hgs7 + dx_hgs8 + dx_hgs9 + dx_hgs10 + dx_hgs11 + dx_hgs12 + dx_hgs13 + dx_hgs14 + dx_hgs15 + dx_hgs16
    zhgs17 = zhgs1 + zhgs2 + zhgs3 + zhgs4 + zhgs5 + zhgs6 + zhgs7 + zhgs8 + zhgs9 + zhgs10 + zhgs11 + zhgs12 + zhgs13 + zhgs14 + zhgs15 + zhgs16
    zqis = np.where(lai_shui >= zong_xu_shui, lai_shui - zong_xu_shui, 0.00)
    ZQS = pd.DataFrame(zqis)

    # GS = pd.DataFrame({BiaoTouHangYe[0]: gs1,BiaoTouHangYe[1]:[gs2],BiaoTouHangYe[2]:[gs3],BiaoTouHangYe[3]:[gs4],BiaoTouHangYe[4]:[gs5],BiaoTouHangYe[5]:[gs6],BiaoTouHangYe[6]:[gs7],BiaoTouHangYe[7]:[gs8],BiaoTouHangYe[8]:[gs9],BiaoTouHangYe[9]:[gs10],BiaoTouHangYe[10]:[gs11],BiaoTouHangYe[11]:[gs12],BiaoTouHangYe[12]:[gs13],BiaoTouHangYe[13]:[gs14],BiaoTouHangYe[14]:[gs15],BiaoTouHangYe[15]:[gs16]})  #'城镇生活','农村生活','牲畜','三产','火核电','一般工业','高耗水工业','建筑业','水田','水浇地''菜田','林果地','草场','鱼塘','城镇生态','湿地'

    # bk: ?合计供水?
    HJGS = gs1 + gs2 + gs3 + gs4 + gs5 + gs6 + gs7 + gs8 + gs9 + gs10 + gs11 + gs12 + gs13 + gs14 + gs15 + gs16
    HJDXGS = dx_gs1 + dx_gs2 + dx_gs3 + dx_gs4 + dx_gs5 + dx_gs6 + dx_gs7 + dx_gs8 + dx_gs9 + dx_gs10 + dx_gs11 + dx_gs12 + dx_gs13 + dx_gs14 + dx_gs15 + dx_gs16
    HJQUES = ques1 + ques2 + ques3 + ques4 + ques5 + ques6 + ques7 + ques8 + ques9 + ques10 + ques11 + ques12 + ques13 + ques14 + ques15 + ques16
    # print(GS1)
    # GS1=np.reshape(732,16)
    # GS = pd.DataFrame(GS1,columns=BiaoTouHangYe)
    # QS = pd.DataFrame(ques)

    # bk: 以下主要进行转换，得到DataFrame
    # bk: ?16种类型的需水?

    XS16 = pd.DataFrame((xu_shui + di_xia_xu_shui),
                        columns=BiaoTouHangYe)
    zdxxs = dx_xs1 + dx_xs2 + dx_xs3 + dx_xs4 + dx_xs5 + dx_xs6 + dx_xs7 + dx_xs8 + dx_xs9 + dx_xs10 + dx_xs11 + dx_xs12 + dx_xs13 + dx_xs14 + dx_xs15 + dx_xs16

    XS17 = pd.DataFrame((zong_xu_shui + zdxxs), columns=['总需水'])


    (HJGS1, HJGS2, GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9,
     GS10, GS11, GS12, GS13, GS14, GS15, GS16) = trans_pd(
        gs1,gs2, gs3, gs4, gs5, gs6, gs7,
        gs8, gs9, gs10, gs11, gs12, gs13, gs14, gs15, gs16, HJGS, '地表水供水合计')


    GS178 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, HJGS2],
                      axis=1)
    GS17 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16], axis=1)


    (HJDXGS1, HJDXGS2, DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8,
     DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15, DXGS16) = trans_pd(
        dx_gs1,
        dx_gs2, dx_gs3, dx_gs4, dx_gs5, dx_gs6, dx_gs7,
        dx_gs8, dx_gs9, dx_gs10, dx_gs11, dx_gs12, dx_gs13, dx_gs14, dx_gs15, dx_gs16, HJQUES, '地下水供水合计')



    DXGS178 = pd.concat(
        [DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8, DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15,
         DXGS16, HJDXGS2], axis=1)
    DXGS17 = pd.concat(
        [DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8, DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15,
         DXGS16], axis=1)

    (HJQUES1, HJQUES2, QS1,QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9,
     QS10, QS11, QS12, QS13, QS14, QS15, QS16) = trans_pd(
         ques1,ques2, ques3, ques4, ques5, ques6, ques7,
        ques8, ques9,ques10, ques11, ques12, ques13, ques14, ques15, ques16,HJQUES,'缺水合计')


    QS178 = pd.concat(
        [QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16, HJQUES2],
        axis=1
    )
    QS17 = pd.concat(
        [QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16],
        axis=1
    )

    HGS = pd.DataFrame(zhgs)
    DXHGS = pd.DataFrame(dx_zhgs)
    ZHGS = pd.DataFrame(zhgs17, columns=['总回归水'])

    save_frame(ZHGS, 'xx_a')

    '''
    bk ?zqis:地表弃水?
    bk ?ZQS:地表弃水DF?
    bk ?HGS:综合供水?
    '''

    return zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1, HJDXGS1, GS178, DXGS178, QS178, XS17, XS16, zdxxs


def trans_pd(ques1, ques2, ques3, ques4, ques5, ques6,
             ques7, ques8, ques9,ques10, ques11, ques12, ques13, ques14, ques15, ques16, HJQUES, hj_name):
    QS1 = pd.DataFrame(ques1, columns=[BiaoTouHangYe[0]])
    QS2 = pd.DataFrame(ques2, columns=[BiaoTouHangYe[1]])
    QS3 = pd.DataFrame(ques3, columns=[BiaoTouHangYe[2]])
    QS4 = pd.DataFrame(ques4, columns=[BiaoTouHangYe[3]])
    QS5 = pd.DataFrame(ques5, columns=[BiaoTouHangYe[4]])
    QS6 = pd.DataFrame(ques6, columns=[BiaoTouHangYe[5]])
    QS7 = pd.DataFrame(ques7, columns=[BiaoTouHangYe[6]])
    QS8 = pd.DataFrame(ques8, columns=[BiaoTouHangYe[7]])
    QS9 = pd.DataFrame(ques9, columns=[BiaoTouHangYe[8]])
    QS10 = pd.DataFrame(ques10, columns=[BiaoTouHangYe[9]])
    QS11 = pd.DataFrame(ques11, columns=[BiaoTouHangYe[10]])
    QS12 = pd.DataFrame(ques12, columns=[BiaoTouHangYe[11]])
    QS13 = pd.DataFrame(ques13, columns=[BiaoTouHangYe[12]])
    QS14 = pd.DataFrame(ques14, columns=[BiaoTouHangYe[13]])
    QS15 = pd.DataFrame(ques15, columns=[BiaoTouHangYe[14]])
    QS16 = pd.DataFrame(ques16, columns=[BiaoTouHangYe[15]])
    HJQUES1 = pd.DataFrame(HJQUES)
    HJQUES2 = pd.DataFrame(HJQUES, columns=[hj_name])
    return HJQUES1, HJQUES2, QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9,QS10, QS11, QS12, QS13, QS14, QS15, QS16


def calc_laishui(dx_xs2, ls2, xs2, dbhgsxs2):
    gs2 = np.where(ls2 >= xs2, xs2, np.where(ls2 >= 0, ls2, 0))
    ques2 = np.where(ls2 >= xs2, 0, np.where(ls2 >= 0, xs2 - ls2, 0))
    qis2 = np.where(ls2 >= xs2, ls2 - xs2, 0)
    dx_gs2 = dx_xs2
    hgs2 = gs2 * dbhgsxs2
    dx_hgs2 = dx_gs2 * dxhgsxs2
    zhgs2 = hgs2 + dx_hgs2
    ls3 = qis2
    return dx_gs2, dx_hgs2, gs2, hgs2, ls3, ques2, zhgs2


def guanqu(gq_xs, wd, dx, gq_ls, sx):
    '''
    # 灌区

    :param gq_xs:
    :param wd:
    :param dx:
    :param gq_ls:
    :param sx:
    :return:
    '''

    gq_xs0 = gq_xs * sx
    dx_gs = dx
    wd_gs = wd * sx
    qy = gq_xs0 - wd_gs
    db_gs = np.where(gq_ls >= qy, qy, gq_ls)
    zgs = dx_gs + wd_gs + db_gs
    gq_qs = gq_xs - db_gs - wd_gs  # 灌区缺水
    hgs_db = (wd_gs + db_gs) * dxhgsxs9
    hgs_dx = dx_gs * dxhgsxs9  # 回归水系数提前定义
    gq_hg = hgs_db + hgs_dx
    gq_qis = gq_ls - db_gs
    return dx_gs, wd_gs, db_gs, zgs, gq_hg, gq_qs, gq_qis, hgs_db, hgs_dx, gq_hg


def sgs(ky, xs):
    '''
    bk:  疏干水 ??
    :param ky:
    :param xs:
    :return:
    '''
    sgs_gs = np.where(ky >= xs, xs, np.where(ky > 0, ky, 0))
    sgs_zgs = sgs_gs.sum(axis=1)
    GS = pd.DataFrame(sgs_gs)
    ZGS = pd.DataFrame(sgs_zgs)
    sggs1 = sgs_gs[:, :1]
    sggs2 = sgs_gs[:, 1:2]
    sggs3 = sgs_gs[:, 2:3]
    sggs4 = sgs_gs[:, 3:4]
    sggs5 = sgs_gs[:, 4:5]
    sggs6 = sgs_gs[:, 5:6]
    sggs7 = sgs_gs[:, 6:7]
    sggs8 = sgs_gs[:, 7:8]
    sggs9 = sgs_gs[:, 8:9]
    sggs10 = sgs_gs[:, 9:10]
    sggs11 = sgs_gs[:, 10:11]
    sggs12 = sgs_gs[:, 11:12]
    sggs13 = sgs_gs[:, 12:13]
    sggs14 = sgs_gs[:, 13:14]
    sggs15 = sgs_gs[:, 14:15]
    sggs16 = sgs_gs[:, 15:16]

    zgs_sg = sggs1 + sggs2 + sggs3 + sggs4 + sggs5 + sggs6 + sggs7 + sggs8 + sggs9 + sggs10 + sggs11 + sggs12 + sggs13 + sggs14 + sggs15 + sggs16
    sghgs1 = sggs1 * dbhgsxs1
    sghgs2 = sggs2 * dbhgsxs2
    sghgs3 = sggs3 * dbhgsxs3
    sghgs4 = sggs4 * dbhgsxs4
    sghgs5 = sggs5 * dbhgsxs5
    sghgs6 = sggs6 * dbhgsxs6
    sghgs7 = sggs7 * dbhgsxs7
    sghgs8 = sggs8 * dbhgsxs8
    sghgs9 = sggs9 * dbhgsxs9
    sghgs10 = sggs10 * dbhgsxs10
    sghgs11 = sggs11 * dbhgsxs11
    sghgs12 = sggs12 * dbhgsxs12
    sghgs13 = sggs13 * dbhgsxs13
    sghgs14 = sggs14 * dbhgsxs14
    sghgs15 = sggs15 * dbhgsxs15
    sghgs16 = sggs16 * dbhgsxs16
    zhgs_sg = sghgs1 + sghgs2 + sghgs3 + sghgs4 + sghgs5 + sghgs6 + sghgs7 + sghgs8 + sghgs9 + sghgs10 + sghgs11 + sghgs12 + sghgs13 + sghgs14 + sghgs15 + sghgs16

    SGGS1 = pd.DataFrame(sggs1, columns=[BiaoTouHangYe[0]])
    SGGS2 = pd.DataFrame(sggs2, columns=[BiaoTouHangYe[1]])
    SGGS3 = pd.DataFrame(sggs3, columns=[BiaoTouHangYe[2]])
    SGGS4 = pd.DataFrame(sggs4, columns=[BiaoTouHangYe[3]])
    SGGS5 = pd.DataFrame(sggs5, columns=[BiaoTouHangYe[4]])
    SGGS6 = pd.DataFrame(sggs6, columns=[BiaoTouHangYe[5]])
    SGGS7 = pd.DataFrame(sggs7, columns=[BiaoTouHangYe[6]])
    SGGS8 = pd.DataFrame(sggs8, columns=[BiaoTouHangYe[7]])
    SGGS9 = pd.DataFrame(sggs9, columns=[BiaoTouHangYe[8]])
    SGGS10 = pd.DataFrame(sggs10, columns=[BiaoTouHangYe[9]])
    SGGS11 = pd.DataFrame(sggs11, columns=[BiaoTouHangYe[10]])
    SGGS12 = pd.DataFrame(sggs12, columns=[BiaoTouHangYe[11]])
    SGGS13 = pd.DataFrame(sggs13, columns=[BiaoTouHangYe[12]])
    SGGS14 = pd.DataFrame(sggs14, columns=[BiaoTouHangYe[13]])
    SGGS15 = pd.DataFrame(sggs15, columns=[BiaoTouHangYe[14]])
    SGGS16 = pd.DataFrame(sggs16, columns=[BiaoTouHangYe[15]])
    SGGS17 = pd.concat(
        [SGGS1, SGGS2, SGGS3, SGGS4, SGGS5, SGGS6, SGGS7, SGGS8, SGGS9, SGGS10, SGGS11, SGGS12, SGGS13, SGGS14, SGGS15,
         SGGS16], axis=1)
    ZGS_SG = pd.DataFrame(zgs_sg)
    ZHGS_SG = pd.DataFrame(zhgs_sg)
    return sgs_gs, sgs_zgs, ZHGS_SG, SGGS17, ZGS_SG, GS, ZGS


def BZL(qs):
    '''
    bk: 保障率
    '''
    bzl = 0.0  # todo：之前为全局变量，如下用到所以定义一个，1024行bzl变量类型为float，所以变量bzl定义为float类型
    df_bzl1 = pd.DataFrame()
    df_bzl2 = pd.DataFrame()
    xs = np.array(qs)  # x=df3.values.tolist()  转列表
    xs1 = xs[:, :1]
    xs2 = xs[:, 1:2]
    xs3 = xs[:, 2:3]
    xs4 = xs[:, 3:4]
    xs5 = xs[:, 4:5]
    xs6 = xs[:, 5:6]
    xs7 = xs[:, 6:7]
    xs8 = xs[:, 7:8]
    xs9 = xs[:, 8:9]
    xs10 = xs[:, 9:10]
    xs11 = xs[:, 10:11]
    xs12 = xs[:, 11:12]
    xs13 = xs[:, 12:13]
    xs14 = xs[:, 13:14]
    xs15 = xs[:, 14:15]
    xs16 = xs[:, 15:16]

    xs1 = np.array([xs1, xs2, xs3, xs4, xs5, xs6, xs7, xs8, xs14, xs15, xs16])
    xs2 = np.array([xs9, xs10, xs11, xs12, xs13])
    for h in xs2:
        # bk: 年
        geshu = 0
        cc = np.add.reduceat(h, np.arange(0, len(h), 12))  # 按照年统计
        for ques in cc:
            if abs(ques - 0) < 0.0001:
                geshu = geshu + 1
                bzl = geshu / (len(h) / 12) * 100
        # df_bzl1 = df_bzl1.append(pd.DataFrame({'保证率': bzl}, index=[0]))
        df_bzl1 = pd.concat([df_bzl1, pd.DataFrame({'保证率': bzl}, index=[0])])
    for h in xs1:
        # bk: 月
        geshu = 0
        for ques in h:
            if abs(ques - 0) < 0.0001:  # 按照月统计
                geshu = geshu + 1
                bzl = geshu / len(h) * 100
        # df_bzl2 = df_bzl2.append(pd.DataFrame({'保证率': bzl}, index=[0]))
        df_bzl2 = pd.concat([df_bzl2, pd.DataFrame({'保证率': bzl}, index=[0])])
    df_bzl = pd.concat([df_bzl2, df_bzl1])
    return bzl, df_bzl


def JZ(jz1):
    '''
    bk: 计算均值
    :param jz1:
    :return:
    '''
    jz = jz1.groupby('年').sum()
    hj = jz.mean()
    zz = pd.DataFrame(hj).transpose()
    zz = zz.set_axis(['多年平均值'], axis='index', copy=False)
    jz2 = pd.concat([jz, zz])
    save_frame(jz2, 'xx_a')
    save_frame(zz, 'xx_b')
    return jz2, zz


def TJ(qjxs, gq_xs):
    '''

     todo:
    HJGS 合计供水
      HJGS变量为gx_QTSY函数中调用的：
      HJGS = gs1+ gs2+gs3+gs4+gs5+gs6+gs7+gs8+gs9+gs10+gs11+gs12+gs13+gs14+gs15+gs16
     但是整个文件中 gx_QTSY()函数并未用到，打印变量qjxs0类型为numpy.ndarray，所以HJGS按numpy.ndarray类型定义

    :param qjxs:区间需水
    :param gq_xs:灌区需水
    :return:
    '''
    HJGS = np.array([])  # 自己后加变量，类型参照注释中说明
    # 区间需水
    qjxs1 = qjxs[:, :1]
    qjxs2 = qjxs[:, 1:2]
    qjxs3 = qjxs[:, 2:3]
    qjxs4 = qjxs[:, 3:4]
    qjxs5 = qjxs[:, 4:5]
    qjxs6 = qjxs[:, 5:6]
    qjxs7 = qjxs[:, 6:7]
    qjxs8 = qjxs[:, 7:8]
    qjxs9 = qjxs[:, 8:9]
    qjxs10 = qjxs[:, 9:10]
    qjxs11 = qjxs[:, 10:11]
    qjxs12 = qjxs[:, 11:12]
    qjxs13 = qjxs[:, 12:13]
    qjxs14 = qjxs[:, 13:14]
    qjxs15 = qjxs[:, 14:15]
    qjxs16 = qjxs[:, 15:16]

    qjxs0 = qjxs1 + qjxs2 + qjxs3 + qjxs4 + qjxs5 + qjxs6 + qjxs7 + qjxs8 + qjxs9 + gq_xs + qjxs10 + qjxs11 + qjxs12 + qjxs13 + qjxs14 + qjxs15 + qjxs16

    ZHJ = pd.DataFrame(qjxs0)
    GS1 = pd.DataFrame(qjxs1, columns=[BiaoTouHangYe[0]])
    GS2 = pd.DataFrame(qjxs2, columns=[BiaoTouHangYe[1]])
    GS3 = pd.DataFrame(qjxs3, columns=[BiaoTouHangYe[2]])
    GS4 = pd.DataFrame(qjxs4, columns=[BiaoTouHangYe[3]])
    GS5 = pd.DataFrame(qjxs5, columns=[BiaoTouHangYe[4]])
    GS6 = pd.DataFrame(qjxs6, columns=[BiaoTouHangYe[5]])
    GS7 = pd.DataFrame(qjxs7, columns=[BiaoTouHangYe[6]])
    GS8 = pd.DataFrame(qjxs8, columns=[BiaoTouHangYe[7]])
    GS9 = pd.DataFrame(qjxs9, columns=[BiaoTouHangYe[8]])
    GS10 = pd.DataFrame(qjxs10, columns=[BiaoTouHangYe[9]])
    GS11 = pd.DataFrame(qjxs11, columns=[BiaoTouHangYe[10]])
    GS12 = pd.DataFrame(qjxs12, columns=[BiaoTouHangYe[11]])
    GS13 = pd.DataFrame(qjxs13, columns=[BiaoTouHangYe[12]])
    GS14 = pd.DataFrame(qjxs14, columns=[BiaoTouHangYe[13]])
    GS15 = pd.DataFrame(qjxs15, columns=[BiaoTouHangYe[14]])
    GS16 = pd.DataFrame(qjxs16, columns=[BiaoTouHangYe[15]])
    HJGS2 = pd.DataFrame(HJGS, columns=['地表水供水合计'])
    GQXS = pd.DataFrame(gq_xs, columns=[BiaoTouHangYe[8]])
    GS178 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, HJGS2],
                      axis=1)
    QJxs0 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9 + GQXS, GS10, GS11, GS12, GS13, GS14, GS15, GS16],
                      axis=1)

    return qjxs0, QJxs0, ZHJ, GQXS
