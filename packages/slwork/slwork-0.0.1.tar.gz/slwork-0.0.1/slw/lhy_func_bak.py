import pandas as pd
import numpy as np
from .add_code import save_frame
from .slw_const import *


def Chazhi(x, y, xi):  # 参数一组升序排列的长度相等的x列表和y列表，以及给定一个x值
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
        # print(L[i])
        # print(V2)
        # print(type(V2))

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

    skgs1 = np.where(skzgs >= skxs1, skxs1, np.where(skzgs >= 0, skzgs, 0))
    skques1 = np.where(skzgs >= skxs1, 0, np.where(skzgs >= 0, skxs1 - skzgs, 0))
    skqis1 = np.where(skzgs >= skxs1, skzgs - skxs1, 0)
    skhgs1 = skgs1 * dbhgsxs1
    skzgs2 = skqis1

    skgs2 = np.where(skzgs2 >= skxs2, skxs2, np.where(skzgs2 >= 0, skzgs2, 0))
    skques2 = np.where(skzgs2 >= skxs2, 0, np.where(skzgs2 >= 0, skxs2 - skzgs2, 0))
    skqis2 = np.where(skzgs2 >= skxs2, skzgs2 - skxs2, 0)
    skhgs2 = skgs2 * dbhgsxs2
    skzgs3 = skqis2

    skgs3 = np.where(skzgs3 >= skxs3, skxs3, np.where(skzgs3 >= 0, skzgs3, 0))
    skques3 = np.where(skzgs3 >= skxs3, 0, np.where(skzgs3 >= 0, skxs3 - skzgs3, 0))
    skqis3 = np.where(skzgs3 >= skxs3, skzgs3 - skxs3, 0)
    skhgs3 = skgs3 * dbhgsxs3
    skzgs4 = skqis3

    skgs4 = np.where(skzgs4 >= skxs4, skxs4, np.where(skzgs4 >= 0, skzgs4, 0))
    skques4 = np.where(skzgs4 >= skxs4, 0, np.where(skzgs4 >= 0, skxs4 - skzgs4, 0))
    skqis4 = np.where(skzgs4 >= skxs4, skzgs4 - skxs4, 0)
    skhgs4 = skgs4 * dbhgsxs4
    skzgs5 = skqis4

    skgs5 = np.where(skzgs5 >= skxs5, skxs5, np.where(skzgs5 >= 0, skzgs5, 0))
    skques5 = np.where(skzgs5 >= skxs5, 0, np.where(skzgs5 >= 0, skxs5 - skzgs5, 0))
    skqis5 = np.where(skzgs5 >= skxs5, skzgs5 - skxs5, 0)
    skhgs5 = skgs5 * dbhgsxs5
    skzgs6 = skqis5

    skgs6 = np.where(skzgs6 >= skxs6, skxs6, np.where(skzgs6 >= 0, skzgs6, 0))
    skques6 = np.where(skzgs6 >= skxs6, 0, np.where(skzgs6 >= 0, skxs6 - skzgs6, 0))
    skqis6 = np.where(skzgs6 >= skxs6, skzgs6 - skxs6, 0)
    skhgs6 = skgs6 * dbhgsxs6
    skzgs7 = skqis6

    skgs7 = np.where(skzgs7 >= skxs7, skxs7, np.where(skzgs7 >= 0, skzgs7, 0))
    skques7 = np.where(skzgs7 >= skxs7, 0, np.where(skzgs7 >= 0, skxs7 - skzgs7, 0))
    skqis7 = np.where(skzgs7 >= skxs7, skzgs7 - skxs7, 0)
    skhgs7 = skgs7 * dbhgsxs7
    skzgs8 = skqis7

    skgs8 = np.where(skzgs8 >= skxs8, skxs8, np.where(skzgs8 >= 0, skzgs8, 0))
    skques8 = np.where(skzgs8 >= skxs8, 0, np.where(skzgs8 >= 0, skxs8 - skzgs8, 0))
    skqis8 = np.where(skzgs8 >= skxs8, skzgs8 - skxs8, 0)
    skhgs8 = skgs8 * dbhgsxs8
    skzgs9 = skqis8

    skgs9 = np.where(skzgs9 >= skxs9, skxs9, np.where(skzgs9 >= 0, skzgs9, 0))
    skques9 = np.where(skzgs9 >= skxs9, 0, np.where(skzgs9 >= 0, skxs9 - skzgs9, 0))
    skqis9 = np.where(skzgs9 >= skxs9, skzgs9 - skxs9, 0)
    skhgs9 = skgs9 * dbhgsxs9
    skzgs10 = skqis9

    skgs10 = np.where(skzgs10 >= skxs10, skxs10, np.where(skzgs10 >= 0, skzgs10, 0))
    skques10 = np.where(skzgs10 >= skxs10, 0, np.where(skzgs10 >= 0, skxs10 - skzgs10, 0))
    skqis10 = np.where(skzgs10 >= skxs10, skzgs10 - skxs10, 0)
    skhgs10 = skgs10 * dbhgsxs10
    skzgs11 = skqis10

    skgs11 = np.where(skzgs11 >= skxs11, skxs11, np.where(skzgs11 >= 0, skzgs11, 0))
    skques11 = np.where(skzgs11 >= skxs11, 0, np.where(skzgs11 >= 0, skxs11 - skzgs11, 0))
    skqis11 = np.where(skzgs11 >= skxs11, skzgs11 - skxs11, 0)
    skhgs11 = skgs11 * dbhgsxs11
    skzgs12 = skqis11

    skgs12 = np.where(skzgs12 >= skxs12, skxs12, np.where(skzgs12 >= 0, skzgs12, 0))
    skques12 = np.where(skzgs12 >= skxs12, 0, np.where(skzgs12 >= 0, skxs12 - skzgs12, 0))
    skqis12 = np.where(skzgs12 >= skxs12, skzgs12 - skxs12, 0)
    skhgs12 = skgs12 * dbhgsxs12
    skzgs13 = skqis12

    skgs13 = np.where(skzgs13 >= skxs13, skxs13, np.where(skzgs13 >= 0, skzgs13, 0))
    skques13 = np.where(skzgs13 >= skxs13, 0, np.where(skzgs13 >= 0, skxs13 - skzgs13, 0))
    skqis13 = np.where(skzgs13 >= skxs13, skzgs13 - skxs13, 0)
    skhgs13 = skgs13 * dbhgsxs13
    skzgs14 = skqis13

    skgs14 = np.where(skzgs14 >= skxs14, skxs14, np.where(skzgs14 >= 0, skzgs14, 0))
    skques14 = np.where(skzgs14 >= skxs14, 0, np.where(skzgs14 >= 0, skxs14 - skzgs14, 0))
    skqis14 = np.where(skzgs14 >= skxs14, skzgs14 - skxs14, 0)
    skhgs14 = skgs14 * dbhgsxs14
    skzgs15 = skqis14

    skgs15 = np.where(skzgs15 >= skxs15, skxs15, np.where(skzgs15 >= 0, skzgs15, 0))
    skques15 = np.where(skzgs15 >= skxs15, 0, np.where(skzgs15 >= 0, skxs15 - skzgs15, 0))
    skqis15 = np.where(skzgs15 >= skxs15, skzgs15 - skxs15, 0)
    skhgs15 = skgs15 * dbhgsxs15
    skzgs16 = skqis15

    skgs16 = np.where(skzgs16 >= skxs16, skxs16, np.where(skzgs16 >= 0, skzgs16, 0))
    skques16 = np.where(skzgs16 >= skxs16, 0, np.where(skzgs16 >= 0, skxs16 - skzgs16, 0))
    skqis16 = np.where(skzgs16 >= skxs16, skzgs16 - skxs16, 0)
    skhgs16 = skgs16 * dbhgsxs16

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
    GS1 = pd.DataFrame(skgs1, columns=['城镇生活'])
    GS2 = pd.DataFrame(skgs2, columns=['农村生活'])
    GS3 = pd.DataFrame(skgs3, columns=['牲畜'])
    GS4 = pd.DataFrame(skgs4, columns=['三产'])
    GS5 = pd.DataFrame(skgs5, columns=['火核电'])
    GS6 = pd.DataFrame(skgs6, columns=['一般工业'])
    GS7 = pd.DataFrame(skgs7, columns=['高耗水工业'])
    GS8 = pd.DataFrame(skgs8, columns=['建筑业'])
    GS9 = pd.DataFrame(skgs9, columns=['水田'])
    GS10 = pd.DataFrame(skgs10, columns=['水浇地'])
    GS11 = pd.DataFrame(skgs11, columns=['菜田'])
    GS12 = pd.DataFrame(skgs12, columns=['林果地'])
    GS13 = pd.DataFrame(skgs13, columns=['草场'])
    GS14 = pd.DataFrame(skgs14, columns=['鱼塘'])
    GS15 = pd.DataFrame(skgs15, columns=['城镇生态'])
    GS16 = pd.DataFrame(skgs16, columns=['湿地'])
    SKHJGS1 = pd.DataFrame(SKHJGS, columns=['供水合计'])
    SKGS17 = pd.concat(
        [GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, SKHJGS1],
        axis=1)
    SKGS0 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16], axis=1)

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

    QS1 = pd.DataFrame(skques1, columns=['城镇生活'])
    QS2 = pd.DataFrame(skques2, columns=['农村生活'])
    QS3 = pd.DataFrame(skques3, columns=['牲畜'])
    QS4 = pd.DataFrame(skques4, columns=['三产'])
    QS5 = pd.DataFrame(skques5, columns=['火核电'])
    QS6 = pd.DataFrame(skques6, columns=['一般工业'])
    QS7 = pd.DataFrame(skques7, columns=['高耗水工业'])
    QS8 = pd.DataFrame(skques8, columns=['建筑业'])
    QS9 = pd.DataFrame(skques9, columns=['水田'])
    QS10 = pd.DataFrame(skques10, columns=['水浇地'])
    QS11 = pd.DataFrame(skques11, columns=['菜田'])
    QS12 = pd.DataFrame(skques12, columns=['林果地'])
    QS13 = pd.DataFrame(skques13, columns=['草场'])
    QS14 = pd.DataFrame(skques14, columns=['鱼塘'])
    QS15 = pd.DataFrame(skques15, columns=['城镇生态'])
    QS16 = pd.DataFrame(skques16, columns=['湿地'])
    SKQS17 = pd.concat([QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16], axis=1)
    return skzqis, SKZQS, SKHGS, SKGS17, SKQS17, SKHJGS, F_SKGS, F_SKGS18, GS9_1, SKHGS_9, SKHJGS1_9, SKGS0, skgs9


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

    gs1 = np.where(lai_shui >= xs1, xs1, np.where(lai_shui >= 0, lai_shui, 0))
    ques1 = np.where(lai_shui >= xs1, 0, np.where(lai_shui >= 0, xs1 - lai_shui, 0))
    qis1 = np.where(lai_shui >= xs1, lai_shui - xs1, 0)
    dx_gs1 = dx_xs1
    hgs1 = gs1 * dbhgsxs1
    dx_hgs1 = dx_gs1 * dxhgsxs1
    zhgs1 = hgs1 + dx_hgs1
    ls2 = qis1

    gs2 = np.where(ls2 >= xs2, xs2, np.where(ls2 >= 0, ls2, 0))
    ques2 = np.where(ls2 >= xs2, 0, np.where(ls2 >= 0, xs2 - ls2, 0))
    qis2 = np.where(ls2 >= xs2, ls2 - xs2, 0)
    dx_gs2 = dx_xs2
    hgs2 = gs2 * dbhgsxs2
    dx_hgs2 = dx_gs2 * dxhgsxs2
    zhgs2 = hgs2 + dx_hgs2
    ls3 = qis2

    gs3 = np.where(ls3 >= xs3, xs3, np.where(ls3 >= 0, ls3, 0))
    ques3 = np.where(ls3 >= xs3, 0, np.where(lai_shui >= 0, xs3 - ls3, 0))
    qis3 = np.where(ls3 >= xs3, ls3 - xs3, 0)
    dx_gs3 = dx_xs3
    hgs3 = gs3 * dbhgsxs3
    dx_hgs3 = dx_gs3 * dxhgsxs3
    zhgs3 = hgs3 + dx_hgs3
    ls4 = qis3

    gs4 = np.where(ls4 >= xs4, xs4, np.where(ls4 >= 0, ls4, 0))
    ques4 = np.where(ls4 >= xs4, 0, np.where(ls4 >= 0, xs4 - ls4, 0))
    qis4 = np.where(ls4 >= xs4, ls4 - xs4, 0)
    dx_gs4 = dx_xs4
    hgs4 = gs4 * dbhgsxs4
    dx_hgs4 = dx_gs4 * dxhgsxs4
    zhgs4 = hgs4 + dx_hgs4
    ls5 = qis4

    gs5 = np.where(ls5 >= xs5, xs5, np.where(ls5 >= 0, ls5, 0))
    ques5 = np.where(ls5 >= xs5, 0, np.where(ls5 >= 0, xs5 - ls5, 0))
    qis5 = np.where(ls5 >= xs5, ls5 - xs5, 0)
    dx_gs5 = dx_xs5
    hgs5 = gs5 * dbhgsxs5
    dx_hgs5 = dx_gs5 * dxhgsxs5
    zhgs5 = hgs5 + dx_hgs5
    ls6 = qis5

    gs6 = np.where(ls6 >= xs6, xs6, np.where(ls6 >= 0, ls6, 0))
    ques6 = np.where(ls6 >= xs6, 0, np.where(ls6 >= 0, xs6 - ls6, 0))
    qis6 = np.where(ls6 >= xs6, ls6 - xs6, 0)
    dx_gs6 = dx_xs6
    dx_hgs3 = dx_gs3 * dxhgsxs3
    zhgs3 = hgs3 + dx_hgs3
    hgs6 = gs6 * dbhgsxs6
    dx_hgs6 = dx_gs6 * dxhgsxs6
    zhgs6 = hgs6 + dx_hgs6
    ls7 = qis6

    gs7 = np.where(ls7 >= xs7, xs7, np.where(ls7 >= 0, ls7, 0))
    ques7 = np.where(ls7 >= xs7, 0, np.where(ls7 >= 0, xs7 - ls7, 0))
    qis7 = np.where(ls7 >= xs7, ls7 - xs7, 0)
    dx_gs7 = dx_xs7
    hgs7 = gs7 * dbhgsxs7
    dx_hgs7 = dx_gs7 * dxhgsxs7
    zhgs7 = hgs7 + dx_hgs7
    ls8 = qis7

    gs8 = np.where(ls8 >= xs8, xs8, np.where(ls8 >= 0, ls8, 0))
    ques8 = np.where(ls8 >= xs8, 0, np.where(ls8 >= 0, xs8 - ls8, 0))
    qis8 = np.where(ls8 >= xs8, ls8 - xs8, 0)
    dx_gs8 = dx_xs8
    hgs8 = gs8 * dbhgsxs8
    dx_hgs8 = dx_gs8 * dxhgsxs8
    zhgs8 = hgs8 + dx_hgs8
    ls9 = qis8

    xs99 = xs9 * ss
    gs9 = np.where(ls9 >= xs99, xs99, np.where(ls9 >= 0, ls9, 0))
    ques9 = np.where(ls9 >= xs99, 0, np.where(ls9 >= 0, xs99 - ls9, 0)) + (xs9 - xs99)
    qis9 = np.where(ls9 >= xs99, ls9 - xs99, 0)
    dx_gs9 = dx_xs9
    hgs9 = gs9 * dbhgsxs9
    dx_hgs9 = dx_gs9 * dxhgsxs9
    zhgs9 = hgs9 + dx_hgs9
    ls10 = qis9

    gs10 = np.where(ls10 >= xs10, xs10, np.where(ls10 >= 0, ls10, 0))
    ques10 = np.where(ls10 >= xs10, 0, np.where(ls10 >= 0, xs10 - ls10, 0))
    qis10 = np.where(ls10 >= xs10, ls10 - xs10, 0)
    dx_gs10 = dx_xs10
    hgs10 = gs10 * dbhgsxs10
    dx_hgs10 = dx_gs3 * dxhgsxs10
    zhgs10 = hgs10 + dx_hgs10
    ls11 = qis10

    gs11 = np.where(ls11 >= xs11, xs11, np.where(ls11 >= 0, ls11, 0))
    ques11 = np.where(ls11 >= xs11, 0, np.where(ls11 >= 0, xs11 - ls11, 0))
    qis11 = np.where(ls11 >= xs11, ls11 - xs11, 0)
    dx_gs11 = dx_xs11
    hgs11 = gs11 * dbhgsxs11
    dx_hgs11 = dx_gs11 * dxhgsxs11
    zhgs11 = hgs11 + dx_hgs11
    ls12 = qis11

    gs12 = np.where(ls12 >= xs12, xs12, np.where(ls12 >= 0, ls12, 0))
    ques12 = np.where(ls12 >= xs12, 0, np.where(ls12 >= 0, xs12 - ls12, 0))
    qis12 = np.where(ls12 >= xs12, ls12 - xs12, 0)
    dx_gs12 = dx_xs12
    hgs12 = gs12 * dbhgsxs12
    dx_hgs12 = dx_gs12 * dxhgsxs12
    zhgs12 = hgs12 + dx_hgs12
    ls13 = qis12

    gs13 = np.where(ls13 >= xs13, xs13, np.where(ls13 >= 0, ls13, 0))
    ques13 = np.where(ls13 >= xs13, 0, np.where(ls13 >= 0, xs13 - ls13, 0))
    qis13 = np.where(ls13 >= xs13, ls13 - xs13, 0)
    dx_gs13 = dx_xs13
    hgs13 = gs13 * dbhgsxs13
    dx_hgs13 = dx_gs13 * dxhgsxs13
    zhgs13 = hgs13 + dx_hgs13
    ls14 = qis13

    gs14 = np.where(ls14 >= xs14, xs14, np.where(ls14 >= 0, ls14, 0))
    ques14 = np.where(ls14 >= xs14, 0, np.where(ls14 >= 0, xs14 - ls14, 0))
    qis14 = np.where(ls14 >= xs14, ls14 - xs14, 0)
    dx_gs14 = dx_xs14
    hgs14 = gs14 * dbhgsxs14
    dx_hgs14 = dx_gs14 * dxhgsxs14
    zhgs14 = hgs14 + dx_hgs14
    ls15 = qis14

    gs15 = np.where(ls15 >= xs15, xs15, np.where(ls15 >= 0, ls15, 0))
    ques15 = np.where(ls15 >= xs15, 0, np.where(ls15 >= 0, xs15 - ls15, 0))
    qis15 = np.where(ls15 >= xs15, ls15 - xs15, 0)
    dx_gs15 = dx_xs15
    hgs15 = gs15 * dbhgsxs15
    dx_hgs15 = dx_gs15 * dxhgsxs15
    zhgs15 = hgs15 + dx_hgs15
    ls16 = qis15

    gs16 = np.where(ls16 >= xs16, xs16, np.where(ls16 >= 0, ls16, 0))
    ques16 = np.where(ls15 >= xs16, 0, np.where(ls16 >= 0, xs16 - ls16, 0))
    qis16 = np.where(ls16 >= xs16, ls16 - xs16, 0)
    dx_gs16 = dx_xs16
    hgs16 = gs16 * dbhgsxs16
    dx_hgs16 = dx_gs16 * dxhgsxs16
    zhgs16 = hgs16 + dx_hgs16

    # bk:  # 总回归水， 退水，弃水
    zhgs = hgs1 + hgs2 + hgs3 + hgs4 + hgs5 + hgs6 + hgs7 + hgs8 + hgs9 + hgs10 + hgs11 + hgs12 + hgs13 + hgs14 + hgs15 + hgs16
    dx_zhgs = dx_hgs1 + dx_hgs2 + dx_hgs3 + dx_hgs4 + dx_hgs5 + dx_hgs6 + dx_hgs7 + dx_hgs8 + dx_hgs9 + dx_hgs10 + dx_hgs11 + dx_hgs12 + dx_hgs13 + dx_hgs14 + dx_hgs15 + dx_hgs16
    zhgs17 = zhgs1 + zhgs2 + zhgs3 + zhgs4 + zhgs5 + zhgs6 + zhgs7 + zhgs8 + zhgs9 + zhgs10 + zhgs11 + zhgs12 + zhgs13 + zhgs14 + zhgs15 + zhgs16
    zqis = np.where(lai_shui >= zong_xu_shui, lai_shui - zong_xu_shui, 0.00)
    ZQS = pd.DataFrame(zqis)

    # GS = pd.DataFrame({'城镇生活': gs1,'农村生活':[gs2],'牲畜':[gs3],'三产':[gs4],'火核电':[gs5],'一般工业':[gs6],'高耗水工业':[gs7],'建筑业':[gs8],'水田':[gs9],'水浇地':[gs10],'菜田':[gs11],'林果地':[gs12],'草场':[gs13],'鱼塘':[gs14],'城镇生态':[gs15],'湿地':[gs16]})  #'城镇生活','农村生活','牲畜','三产','火核电','一般工业','高耗水工业','建筑业','水田','水浇地''菜田','林果地','草场','鱼塘','城镇生态','湿地'

    # bk: ?合计供水?
    HJGS = gs1 + gs2 + gs3 + gs4 + gs5 + gs6 + gs7 + gs8 + gs9 + gs10 + gs11 + gs12 + gs13 + gs14 + gs15 + gs16
    HJDXGS = dx_gs1 + dx_gs2 + dx_gs3 + dx_gs4 + dx_gs5 + dx_gs6 + dx_gs7 + dx_gs8 + dx_gs9 + dx_gs10 + dx_gs11 + dx_gs12 + dx_gs13 + dx_gs14 + dx_gs15 + dx_gs16
    HJQUES = ques1 + ques2 + ques3 + ques4 + ques5 + ques6 + ques7 + ques8 + ques9 + ques10 + ques11 + ques12 + ques13 + ques14 + ques15 + ques16
    # print(GS1)
    # GS1=np.reshape(732,16)
    # GS = pd.DataFrame(GS1,columns=['城镇生活','农村生活','牲畜','三产','火核电','一般工业','高耗水工业','高耗水工业','水田','水浇地''菜田','林果地','草场','鱼塘','城镇生态','湿地'])
    # QS = pd.DataFrame(ques)

    # bk: 以下主要进行转换，得到DataFrame
    # bk: ?16种类型的需水?
    XS16 = pd.DataFrame((xu_shui + di_xia_xu_shui),
                        columns=['城镇生活', '农村生活', '牲畜', '三产', '火核电', '一般工业', '高耗水工业', '建筑业',
                                 '水田', '水浇地', '菜田', '林果地', '草场', '鱼塘', '城镇生态', '湿地'])
    zdxxs = dx_xs1 + dx_xs2 + dx_xs3 + dx_xs4 + dx_xs5 + dx_xs6 + dx_xs7 + dx_xs8 + dx_xs9 + dx_xs10 + dx_xs11 + dx_xs12 + dx_xs13 + dx_xs14 + dx_xs15 + dx_xs16

    XS17 = pd.DataFrame((zong_xu_shui + zdxxs), columns=['总需水'])
    GS1 = pd.DataFrame(gs1, columns=['城镇生活'])
    GS2 = pd.DataFrame(gs2, columns=['农村生活'])
    GS3 = pd.DataFrame(gs3, columns=['牲畜'])
    GS4 = pd.DataFrame(gs4, columns=['三产'])
    GS5 = pd.DataFrame(gs5, columns=['火核电'])
    GS6 = pd.DataFrame(gs6, columns=['一般工业'])
    GS7 = pd.DataFrame(gs7, columns=['高耗水工业'])
    GS8 = pd.DataFrame(gs8, columns=['建筑业'])
    GS9 = pd.DataFrame(gs9, columns=['水田'])
    GS10 = pd.DataFrame(gs10, columns=['水浇地'])
    GS11 = pd.DataFrame(gs11, columns=['菜田'])
    GS12 = pd.DataFrame(gs12, columns=['林果地'])
    GS13 = pd.DataFrame(gs13, columns=['草场'])
    GS14 = pd.DataFrame(gs14, columns=['鱼塘'])
    GS15 = pd.DataFrame(gs15, columns=['城镇生态'])
    GS16 = pd.DataFrame(gs16, columns=['湿地'])
    HJGS2 = pd.DataFrame(HJGS, columns=['地表水供水合计'])
    HJGS1 = pd.DataFrame(HJGS)
    GS178 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, HJGS2],
                      axis=1)
    GS17 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16], axis=1)

    DXGS1 = pd.DataFrame(dx_gs1, columns=['城镇生活'])
    DXGS2 = pd.DataFrame(dx_gs2, columns=['农村生活'])
    DXGS3 = pd.DataFrame(dx_gs3, columns=['牲畜'])
    DXGS4 = pd.DataFrame(dx_gs4, columns=['三产'])
    DXGS5 = pd.DataFrame(dx_gs5, columns=['火核电'])
    DXGS6 = pd.DataFrame(dx_gs6, columns=['一般工业'])
    DXGS7 = pd.DataFrame(dx_gs7, columns=['高耗水工业'])
    DXGS8 = pd.DataFrame(dx_gs8, columns=['建筑业'])
    DXGS9 = pd.DataFrame(dx_gs9, columns=['水田'])
    DXGS10 = pd.DataFrame(dx_gs10, columns=['水浇地'])
    DXGS11 = pd.DataFrame(dx_gs11, columns=['菜田'])
    DXGS12 = pd.DataFrame(dx_gs12, columns=['林果地'])
    DXGS13 = pd.DataFrame(dx_gs13, columns=['草场'])
    DXGS14 = pd.DataFrame(dx_gs14, columns=['鱼塘'])
    DXGS15 = pd.DataFrame(dx_gs15, columns=['城镇生态'])
    DXGS16 = pd.DataFrame(dx_gs16, columns=['湿地'])
    HJDXGS1 = pd.DataFrame(HJDXGS)
    HJDXGS2 = pd.DataFrame(HJDXGS, columns=['地下水供水合计'])
    DXGS178 = pd.concat(
        [DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8, DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15,
         DXGS16, HJDXGS2], axis=1)
    DXGS17 = pd.concat(
        [DXGS1, DXGS2, DXGS3, DXGS4, DXGS5, DXGS6, DXGS7, DXGS8, DXGS9, DXGS10, DXGS11, DXGS12, DXGS13, DXGS14, DXGS15,
         DXGS16], axis=1)

    QS1 = pd.DataFrame(ques1, columns=['城镇生活'])
    QS2 = pd.DataFrame(ques2, columns=['农村生活'])
    QS3 = pd.DataFrame(ques3, columns=['牲畜'])
    QS4 = pd.DataFrame(ques4, columns=['三产'])
    QS5 = pd.DataFrame(ques5, columns=['火核电'])
    QS6 = pd.DataFrame(ques6, columns=['一般工业'])
    QS7 = pd.DataFrame(ques7, columns=['高耗水工业'])
    QS8 = pd.DataFrame(ques8, columns=['建筑业'])
    QS9 = pd.DataFrame(ques9, columns=['水田'])
    QS10 = pd.DataFrame(ques10, columns=['水浇地'])
    QS11 = pd.DataFrame(ques11, columns=['菜田'])
    QS12 = pd.DataFrame(ques12, columns=['林果地'])
    QS13 = pd.DataFrame(ques13, columns=['草场'])
    QS14 = pd.DataFrame(ques14, columns=['鱼塘'])
    QS15 = pd.DataFrame(ques15, columns=['城镇生态'])
    QS16 = pd.DataFrame(ques16, columns=['湿地'])
    HJQUES1 = pd.DataFrame(HJQUES)
    HJQUES2 = pd.DataFrame(HJQUES, columns=['缺水合计'])
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

    SGGS1 = pd.DataFrame(sggs1, columns=['城镇生活'])
    SGGS2 = pd.DataFrame(sggs2, columns=['农村生活'])
    SGGS3 = pd.DataFrame(sggs3, columns=['牲畜'])
    SGGS4 = pd.DataFrame(sggs4, columns=['三产'])
    SGGS5 = pd.DataFrame(sggs5, columns=['火核电'])
    SGGS6 = pd.DataFrame(sggs6, columns=['一般工业'])
    SGGS7 = pd.DataFrame(sggs7, columns=['高耗水工业'])
    SGGS8 = pd.DataFrame(sggs8, columns=['建筑业'])
    SGGS9 = pd.DataFrame(sggs9, columns=['水田'])
    SGGS10 = pd.DataFrame(sggs10, columns=['水浇地'])
    SGGS11 = pd.DataFrame(sggs11, columns=['菜田'])
    SGGS12 = pd.DataFrame(sggs12, columns=['林果地'])
    SGGS13 = pd.DataFrame(sggs13, columns=['草场'])
    SGGS14 = pd.DataFrame(sggs14, columns=['鱼塘'])
    SGGS15 = pd.DataFrame(sggs15, columns=['城镇生态'])
    SGGS16 = pd.DataFrame(sggs16, columns=['湿地'])
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

      HJGS变量为gx_QTSY函数中调用的：
      HJGS = gs1+ gs2+gs3+gs4+gs5+gs6+gs7+gs8+gs9+gs10+gs11+gs12+gs13+gs14+gs15+gs16
     但是整个文件中 gx_QTSY()函数并未用到，打印变量qjxs0类型为numpy.ndarray，所以HJGS按numpy.ndarray类型定义

    :param qjxs:
    :param gq_xs:
    :return:
    '''
    HJGS = np.array([])  # 自己后加变量，类型参照1121行说明
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
    GS1 = pd.DataFrame(qjxs1, columns=['城镇生活'])
    GS2 = pd.DataFrame(qjxs2, columns=['农村生活'])
    GS3 = pd.DataFrame(qjxs3, columns=['牲畜'])
    GS4 = pd.DataFrame(qjxs4, columns=['三产'])
    GS5 = pd.DataFrame(qjxs5, columns=['火核电'])
    GS6 = pd.DataFrame(qjxs6, columns=['一般工业'])
    GS7 = pd.DataFrame(qjxs7, columns=['高耗水工业'])
    GS8 = pd.DataFrame(qjxs8, columns=['建筑业'])
    GS9 = pd.DataFrame(qjxs9, columns=['水田'])
    GS10 = pd.DataFrame(qjxs10, columns=['水浇地'])
    GS11 = pd.DataFrame(qjxs11, columns=['菜田'])
    GS12 = pd.DataFrame(qjxs12, columns=['林果地'])
    GS13 = pd.DataFrame(qjxs13, columns=['草场'])
    GS14 = pd.DataFrame(qjxs14, columns=['鱼塘'])
    GS15 = pd.DataFrame(qjxs15, columns=['城镇生态'])
    GS16 = pd.DataFrame(qjxs16, columns=['湿地'])
    HJGS2 = pd.DataFrame(HJGS, columns=['地表水供水合计'])
    GQXS = pd.DataFrame(gq_xs, columns=['水田'])
    GS178 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9, GS10, GS11, GS12, GS13, GS14, GS15, GS16, HJGS2],
                      axis=1)
    QJxs0 = pd.concat([GS1, GS2, GS3, GS4, GS5, GS6, GS7, GS8, GS9 + GQXS, GS10, GS11, GS12, GS13, GS14, GS15, GS16],
                      axis=1)

    return qjxs0, QJxs0, ZHJ, GQXS
