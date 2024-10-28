
def YSRS(xs):
    '''
    # 引松入双

    bk: 未用到
    :param xs:
    :return:
    '''

    ysgs1 = xs[:, :1]
    ysgs2 = xs[:, 1:2]
    ysgs3 = xs[:, 2:3]
    ysgs4 = xs[:, 3:4]
    ysgs5 = xs[:, 4:5]
    ysgs6 = xs[:, 5:6]
    ysgs7 = xs[:, 6:7]
    ysgs8 = xs[:, 7:8]
    ysgs9 = xs[:, 8:9]
    ysgs10 = xs[:, 9:10]
    ysgs11 = xs[:, 10:11]
    ysgs12 = xs[:, 11:12]
    ysgs13 = xs[:, 12:13]
    ysgs14 = xs[:, 13:14]
    ysgs15 = xs[:, 14:15]
    ysgs16 = xs[:, 15:16]

    yshgs1 = ysgs1 * dbhgsxs1
    yshgs2 = ysgs2 * dbhgsxs2
    yshgs3 = ysgs3 * dbhgsxs3
    yshgs4 = ysgs4 * dbhgsxs4
    yshgs5 = ysgs5 * dbhgsxs5
    yshgs6 = ysgs6 * dbhgsxs6
    yshgs7 = ysgs7 * dbhgsxs7
    yshgs8 = ysgs8 * dbhgsxs8
    yshgs9 = ysgs9 * dbhgsxs9
    yshgs10 = ysgs10 * dbhgsxs10
    yshgs11 = ysgs11 * dbhgsxs11
    yshgs12 = ysgs12 * dbhgsxs12
    yshgs13 = ysgs13 * dbhgsxs13
    yshgs14 = ysgs14 * dbhgsxs14
    yshgs15 = ysgs15 * dbhgsxs15
    yshgs16 = ysgs16 * dbhgsxs16

    zhgs_ys = yshgs1 + yshgs2 + yshgs3 + yshgs4 + yshgs5 + yshgs6 + yshgs7 + yshgs8 + yshgs9 + yshgs10 + yshgs11 + yshgs12 + yshgs13 + yshgs14 + yshgs15 + yshgs16

    zgs_ys = ysgs1 + ysgs2 + ysgs3 + ysgs4 + ysgs5 + ysgs6 + ysgs7 + ysgs8 + ysgs9 + ysgs10 + ysgs11 + ysgs12 + ysgs13 + ysgs14 + ysgs15 + ysgs16
    YSGS1 = pd.DataFrame(ysgs1, columns=['城镇生活'])
    YSGS2 = pd.DataFrame(ysgs2, columns=['农村生活'])
    YSGS3 = pd.DataFrame(ysgs3, columns=['牲畜'])
    YSGS4 = pd.DataFrame(ysgs4, columns=['三产'])
    YSGS5 = pd.DataFrame(ysgs5, columns=['火核电'])
    YSGS6 = pd.DataFrame(ysgs6, columns=['一般工业'])
    YSGS7 = pd.DataFrame(ysgs7, columns=['高耗水工业'])
    YSGS8 = pd.DataFrame(ysgs8, columns=['建筑业'])
    YSGS9 = pd.DataFrame(ysgs9, columns=['水田'])
    YSGS10 = pd.DataFrame(ysgs10, columns=['水浇地'])
    YSGS11 = pd.DataFrame(ysgs11, columns=['菜田'])
    YSGS12 = pd.DataFrame(ysgs12, columns=['林果地'])
    YSGS13 = pd.DataFrame(ysgs13, columns=['草场'])
    YSGS14 = pd.DataFrame(ysgs14, columns=['鱼塘'])
    YSGS15 = pd.DataFrame(ysgs15, columns=['城镇生态'])
    YSGS16 = pd.DataFrame(ysgs16, columns=['湿地'])
    ZYSGS = pd.DataFrame(zgs_ys)
    YSGS17 = pd.concat(
        [YSGS1, YSGS2, YSGS3, YSGS4, YSGS5, YSGS6, YSGS7, YSGS8, YSGS9, YSGS10, YSGS11, YSGS12, YSGS13, YSGS14,
         YSGS15, YSGS16], axis=1)

    ZHGS_YS = pd.DataFrame(zhgs_ys)
    return zhgs_ys, ZHGS_YS, YSGS17, ZYSGS


def ysrs(ky, xs):
    '''
    bk: 未用到
    :param ky:
    :param xs:
    :return:
    '''
    ys_gs = np.where(ky >= xs, xs, np.where(ky > 0, ky, 0))
    ys_zgs = ys_gs.sum(axis=1)
    GS = pd.DataFrame(ys_gs)
    ZGS = pd.DataFrame(ys_zgs)
    sggs1 = ys_gs[:, :1]
    sggs2 = ys_gs[:, 1:2]
    sggs3 = ys_gs[:, 2:3]
    sggs4 = ys_gs[:, 3:4]
    sggs5 = ys_gs[:, 4:5]
    sggs6 = ys_gs[:, 5:6]
    sggs7 = ys_gs[:, 6:7]
    sggs8 = ys_gs[:, 7:8]
    sggs9 = ys_gs[:, 8:9]
    sggs10 = ys_gs[:, 9:10]
    sggs11 = ys_gs[:, 10:11]
    sggs12 = ys_gs[:, 11:12]
    sggs13 = ys_gs[:, 12:13]
    sggs14 = ys_gs[:, 13:14]
    sggs15 = ys_gs[:, 14:15]
    sggs16 = ys_gs[:, 15:16]

    zgs_ys = sggs1 + sggs2 + sggs3 + sggs4 + sggs5 + sggs6 + sggs7 + sggs8 + sggs9 + sggs10 + sggs11 + sggs12 + sggs13 + sggs14 + sggs15 + sggs16
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
    zhgs_ys = sghgs1 + sghgs2 + sghgs3 + sghgs4 + sghgs5 + sghgs6 + sghgs7 + sghgs8 + sghgs9 + sghgs10 + sghgs11 + sghgs12 + sghgs13 + sghgs14 + sghgs15 + sghgs16

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
    YSGS17 = pd.concat(
        [SGGS1, SGGS2, SGGS3, SGGS4, SGGS5, SGGS6, SGGS7, SGGS8, SGGS9, SGGS10, SGGS11, SGGS12, SGGS13, SGGS14, SGGS15,
         SGGS16], axis=1)
    ZYSGS = pd.DataFrame(zgs_ys)
    ZHGS_YS = pd.DataFrame(zhgs_ys)
    return ys_gs, ZHGS_YS, YSGS17, ZYSGS, GS, ZGS


def SGS(xs):
    '''
    疏干水

    bk: 未用到
    '''

    sggs1 = xs[:, :1]
    sggs2 = xs[:, 1:2]
    sggs3 = xs[:, 2:3]
    sggs4 = xs[:, 3:4]
    sggs5 = xs[:, 4:5]
    sggs6 = xs[:, 5:6]
    sggs7 = xs[:, 6:7]
    sggs8 = xs[:, 7:8]
    sggs9 = xs[:, 8:9]
    sggs10 = xs[:, 9:10]
    sggs11 = xs[:, 10:11]
    sggs12 = xs[:, 11:12]
    sggs13 = xs[:, 12:13]
    sggs14 = xs[:, 13:14]
    sggs15 = xs[:, 14:15]
    sggs16 = xs[:, 15:16]
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
    return SGGS17, zhgs_sg, ZHGS_SG, ZGS_SG




def gx_QTSY(ls, xs, zxs):
    '''
    # 暂时只考虑了地表水，地下水 ，地下水供水=地下水需水

    bk: 未用到。应该是计算供水的一种方式。
    '''
    global HJGS
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

    gs1 = np.where(ls >= xs1, xs1, np.where(ls >= 0, ls, 0))
    ques1 = np.where(ls >= xs1, 0, np.where(ls >= 0, xs1 - ls, 0))
    qis1 = np.where(ls >= xs1, ls - xs1, 0)
    hgs1 = gs1 * dbhgsxs1
    ls2 = qis1

    gs2 = np.where(ls2 >= xs2, xs2, np.where(ls2 >= 0, ls2, 0))
    ques2 = np.where(ls2 >= xs2, 0, np.where(ls2 >= 0, xs2 - ls2, 0))
    qis2 = np.where(ls2 >= xs2, ls2 - xs2, 0)
    hgs2 = gs2 * dbhgsxs2
    ls3 = qis2

    gs3 = np.where(ls3 >= xs3, xs3, np.where(ls3 >= 0, ls3, 0))
    ques3 = np.where(ls3 >= xs3, 0, np.where(ls >= 0, xs3 - ls3, 0))
    qis3 = np.where(ls3 >= xs3, ls3 - xs3, 0)
    hgs3 = gs3 * dbhgsxs3
    ls4 = qis3

    gs4 = np.where(ls4 >= xs4, xs4, np.where(ls4 >= 0, ls4, 0))
    ques4 = np.where(ls4 >= xs4, 0, np.where(ls4 >= 0, xs4 - ls4, 0))
    qis4 = np.where(ls4 >= xs4, ls4 - xs4, 0)
    hgs4 = gs4 * dbhgsxs4
    ls5 = qis4

    gs5 = np.where(ls5 >= xs5, xs5, np.where(ls5 >= 0, ls5, 0))
    ques5 = np.where(ls5 >= xs5, 0, np.where(ls5 >= 0, xs5 - ls5, 0))
    qis5 = np.where(ls5 >= xs5, ls5 - xs5, 0)
    hgs5 = gs5 * dbhgsxs5
    ls6 = qis5

    gs6 = np.where(ls6 >= xs6, xs6, np.where(ls6 >= 0, ls6, 0))
    ques6 = np.where(ls6 >= xs6, 0, np.where(ls6 >= 0, xs6 - ls6, 0))
    qis6 = np.where(ls6 >= xs6, ls6 - xs6, 0)
    hgs6 = gs6 * dbhgsxs6
    ls7 = qis6

    gs7 = np.where(ls7 >= xs7, xs7, np.where(ls7 >= 0, ls7, 0))
    ques7 = np.where(ls7 >= xs7, 0, np.where(ls7 >= 0, xs7 - ls7, 0))
    qis7 = np.where(ls7 >= xs7, ls7 - xs7, 0)
    hgs7 = gs7 * dbhgsxs7
    ls8 = qis7

    gs8 = np.where(ls8 >= xs8, xs8, np.where(ls8 >= 0, ls8, 0))
    ques8 = np.where(ls8 >= xs8, 0, np.where(ls8 >= 0, xs8 - ls8, 0))
    qis8 = np.where(ls8 >= xs8, ls8 - xs8, 0)
    hgs8 = gs8 * dbhgsxs8
    ls9 = qis8

    gs9 = np.where(ls9 >= xs9, xs9, np.where(ls9 >= 0, ls9, 0))
    ques9 = np.where(ls9 >= xs9, 0, np.where(ls9 >= 0, xs9 - ls9, 0))
    qis9 = np.where(ls9 >= xs9, ls9 - xs9, 0)
    hgs9 = gs9 * dbhgsxs9
    ls10 = qis9

    gs10 = np.where(ls10 >= xs10, xs10, np.where(ls10 >= 0, ls10, 0))
    ques10 = np.where(ls10 >= xs10, 0, np.where(ls10 >= 0, xs10 - ls10, 0))
    qis10 = np.where(ls10 >= xs10, ls10 - xs10, 0)
    hgs10 = gs10 * dbhgsxs10
    ls11 = qis10

    gs11 = np.where(ls11 >= xs11, xs11, np.where(ls11 >= 0, ls11, 0))
    ques11 = np.where(ls11 >= xs11, 0, np.where(ls11 >= 0, xs11 - ls11, 0))
    qis11 = np.where(ls11 >= xs11, ls11 - xs11, 0)
    hgs11 = gs11 * dbhgsxs11
    ls12 = qis11

    gs12 = np.where(ls12 >= xs12, xs12, np.where(ls12 >= 0, ls12, 0))
    ques12 = np.where(ls12 >= xs12, 0, np.where(ls12 >= 0, xs12 - ls12, 0))
    qis12 = np.where(ls12 >= xs12, ls12 - xs12, 0)
    hgs12 = gs12 * dbhgsxs12
    ls13 = qis12

    gs13 = np.where(ls13 >= xs13, xs13, np.where(ls13 >= 0, ls13, 0))
    ques13 = np.where(ls13 >= xs13, 0, np.where(ls13 >= 0, xs13 - ls13, 0))
    qis13 = np.where(ls13 >= xs13, ls13 - xs13, 0)
    hgs13 = gs13 * dbhgsxs13
    ls14 = qis13

    gs14 = np.where(ls14 >= xs14, xs14, np.where(ls14 >= 0, ls14, 0))
    ques14 = np.where(ls14 >= xs14, 0, np.where(ls14 >= 0, xs14 - ls14, 0))
    qis14 = np.where(ls14 >= xs14, ls14 - xs14, 0)
    hgs14 = gs14 * dbhgsxs14
    ls15 = qis14

    gs15 = np.where(ls15 >= xs15, xs15, np.where(ls15 >= 0, ls15, 0))
    ques15 = np.where(ls15 >= xs15, 0, np.where(ls15 >= 0, xs15 - ls15, 0))
    qis15 = np.where(ls15 >= xs15, ls15 - xs15, 0)
    hgs15 = gs15 * dbhgsxs15
    ls16 = qis15

    gs16 = np.where(ls16 >= xs16, xs16, np.where(ls16 >= 0, ls16, 0))
    ques16 = np.where(ls15 >= xs16, 0, np.where(ls16 >= 0, xs16 - ls16, 0))
    qis16 = np.where(ls16 >= xs16, ls16 - xs16, 0)
    hgs16 = gs16 * dbhgsxs16

    zhgs = hgs1 + hgs2 + hgs3 + hgs4 + hgs5 + hgs6 + hgs7 + hgs8 + hgs9 + hgs10 + hgs11 + hgs12 + hgs13 + hgs14 + hgs15 + hgs16
    zqis = np.where(ls >= zxs, ls - zxs, 0.00)
    ZQS = pd.DataFrame(zqis)

    # GS = pd.DataFrame({'城镇生活': gs1,'农村生活':[gs2],'牲畜':[gs3],'三产':[gs4],'火核电':[gs5],'一般工业':[gs6],'高耗水工业':[gs7],'建筑业':[gs8],'水田':[gs9],'水浇地':[gs10],'菜田':[gs11],'林果地':[gs12],'草场':[gs13],'鱼塘':[gs14],'城镇生态':[gs15],'湿地':[gs16]})  #'城镇生活','农村生活','牲畜','三产','火核电','一般工业','高耗水工业','建筑业','水田','水浇地''菜田','林果地','草场','鱼塘','城镇生态','湿地'
    HJGS = gs1 + gs2 + gs3 + gs4 + gs5 + gs6 + gs7 + gs8 + gs9 + gs10 + gs11 + gs12 + gs13 + gs14 + gs15 + gs16

    HJQUES = ques1 + ques2 + ques3 + ques4 + ques5 + ques6 + ques7 + ques8 + ques9 + ques10 + ques11 + ques12 + ques13 + ques14 + ques15 + ques16
    # print(GS1)
    # GS1=np.reshape(732,16)
    # GS = pd.DataFrame(GS1,columns=['城镇生活','农村生活','牲畜','三产','火核电','一般工业','高耗水工业','高耗水工业','水田','水浇地''菜田','林果地','草场','鱼塘','城镇生态','湿地'])
    # QS = pd.DataFrame(ques)

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
    HJQUES1 = pd.DataFrame(HJQUES, columns=['缺水合计'])

    # bk: ?缺水带合计?
    QS17 = pd.concat([QS1, QS2, QS3, QS4, QS5, QS6, QS7, QS8, QS9, QS10, QS11, QS12, QS13, QS14, QS15, QS16, HJQUES1],
                     axis=1)
    HGS = pd.DataFrame(zhgs)
    # return gs, ques, qis, GS, QS, QIS, zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1, HJDXGS1
    return zqis, ZQS, HGS, GS17, QS17, HJGS, HJGS1, HJQUES1


def guanqu1(gq_xs, wd, dx, gq_ls):
    '''
    # 灌区

    bk: 这个函数未用到
    :param gq_xs:
    :param wd:
    :param dx:
    :param gq_ls:
    :return:
    '''

    dx_gs = dx
    wd_gs = wd
    qy = gq_xs - wd
    db_gs = np.where(gq_ls >= qy, qy, gq_ls)
    zgs = dx_gs + wd_gs + db_gs
    gq_qs = gq_xs - db_gs - wd_gs  # 灌区缺水
    hgs_db = (wd_gs + db_gs) * dxhgsxs9
    hgs_dx = dx_gs * dxhgsxs9  # 回归水系数提前定义
    gq_hg = hgs_db + hgs_dx
    gq_qis = gq_ls - db_gs
    return dx_gs, wd_gs, db_gs, zgs, gq_hg, gq_qs, gq_qis, hgs_db, hgs_dx, gq_hg


def guanqu_sk(gq_xs, wd, dx, gq_ls, sk, sx):
    '''

    bk: 与上面函数算法稍有差别
    未用到
    :param gq_xs:
    :param wd:
    :param dx:
    :param gq_ls:
    :param sk:
    :param sx:
    :return:
    '''
    gq_xs0 = gq_xs * sx
    dx_gs = dx
    skgs = sk
    gq_xs1 = np.where(gq_xs0 - skgs >= 0, gq_xs0 - skgs, 0)
    wd_gs = wd
    db_gs0 = gq_xs1 - wd_gs
    db_gs = np.where(gq_ls >= db_gs0, db_gs0, gq_ls)
    zgs = wd_gs + db_gs + skgs
    gq_qs = gq_xs - zgs  # 灌区缺水
    hgs_db = (wd_gs + db_gs + skgs) * dxhgsxs9
    hgs_dx = dx_gs * dxhgsxs9  # 回归水系数提前定义
    gq_hg = hgs_db + hgs_dx
    gq_qis = gq_ls - db_gs
    return dx_gs, wd_gs, db_gs, zgs, gq_hg, gq_qs, gq_qis, hgs_db, hgs_dx, gq_hg, skgs


