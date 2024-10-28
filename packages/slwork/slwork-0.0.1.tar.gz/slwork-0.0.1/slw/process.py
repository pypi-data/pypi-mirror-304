# from xx_tmp import XX_hcgyx_js
from .lhy_func import *
# from .prepare_data import *

from .slw_const import *
import pandas as pd
import numpy as np
from .prepare_data import n, y, KB0

BiaoTouWaterType = ['年', '月', '本地水', '上区间来水', '地表供水', '回归水',
                    '下泄', '校核', '需水', '疏干水', '地下供水', '缺水']


def run1(ls_hcgys_ld, xs_hcgys_ld, zxs_hcgys_ld, dx_xs_hcgys_ld, ss_hcgys_ld):
    '''
    ls_hcgys_ld:来水_寒葱沟水库以上-岭东区
    xs_hcgys_ld:需水
    zxs_hcgys_ld：总需水
    dx_xs_hcgys_ld：地下需水
    ss_hcgys_ld：农业破坏系数
    '''
    (zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1,
     HJDXGS1, GS178, DXGS178, QS178, XS17, XS16, zdxxs) = gx(
        ls_hcgys_ld, xs_hcgys_ld, zxs_hcgys_ld, dx_xs_hcgys_ld, ss_hcgys_ld)

    XX_hcgyx_ld = None
    gs_hcgsk = None
    hgs_hcgsk = None
    SKGS17 = None
    (XX_hcgys_ld, bzl_hcgys_ld,
     dxgs_hcgys_ld, gs_hcgys_ld,
     qus_hcgys_ld, zhgs_hcgys_ld,
     jh_hcgys_ld,
     zxs_hcgys_ld18, ls_hcgyx_js) = cleaner(
        DXGS17, DXGS178, DXHGS, GS17, GS178,
        HGS, HJDXGS1, HJGS1, HJQUES1, QS17, QS178, ZQS,
        XX_hcgyx_ld,
        dx_xs_hcgys_ld, zxs_hcgys_ld, xs_hcgys_ld,
        ls_hcgys_ld, ls_hcgys_ld,
        gs_hcgsk, hgs_hcgsk, SKGS17, zdxxs)

    shuchu3 = pd.concat(
        [n, y, pd.DataFrame(ls_hcgys_ld), HJGS1, zhgs_hcgys_ld, XX_hcgys_ld, jh_hcgys_ld, pd.DataFrame(zxs_hcgys_ld),
         HJDXGS1, HJQUES1],
        axis=1
    )
    shuchu3 = shuchu3.set_axis(['年', '月', '本地水', '地表供水', '回归水', '下泄', '校核',
                                '需水', '地下供水', '缺水'], axis='columns', copy=False)
    jz2, zz = JZ(shuchu3)
    shuchu3_1 = pd.concat([shuchu3, jz2])
    shuchu3_2 = pd.concat([n, y, XS16, XS17, KB0, GS178, KB0, DXGS178, KB0, QS178], axis=1)
    jz2, zz = JZ(shuchu3_2)
    shuchu3_20 = jz2
    """
    with pd.ExcelWriter(file_path + '分行业.xlsx') as writer:
      shuchu3_2.to_excel(writer, sheet_name="区县合计",index=False)
      shuchu3_20.to_excel(writer, sheet_name="区县合计",startcol=0, startrow=733)
    """

    save_frame(shuchu3_2, 'xx_shuchu3_2')
    save_frame(shuchu3_20, 'xx_shuchu3_20')
    # save_frame(shuchu3_2, 'xx_分行业_区县合计')
    # save_frame(shuchu3_20, 'xx_分行业_区县合计')
    hjdxgs_hcgys_ld = None
    hjgs_hcgys_ld = None
    qis_hcgys_ld = None
    hjqus_hcgys_ld = None
    return (shuchu3_1, shuchu3_2, shuchu3_20, XX_hcgys_ld, dxgs_hcgys_ld, gs_hcgys_ld, qus_hcgys_ld,
            zxs_hcgys_ld18, hjdxgs_hcgys_ld, hjgs_hcgys_ld, hjqus_hcgys_ld, zhgs_hcgys_ld, qis_hcgys_ld,
            bzl_hcgys_ld)


def run2(ls_hcgyx_ld, xs_hcgyx_ld, zxs_hcgyx_ld, dx_xs_hcgyx_ld, ss_hcgyx_ld,  # 与 run1 相同的输入
         xs_hcgys_ld, dx_xs_hcgys_ld, zxs_hcgys_ld,  # run1 中的输入。有无问题。
         zxs_hcgsk, v_hcgsk, m_hcgsk, zf_hcgsk, sl_hcgsk, xs_hcgsk,  # 水库计算
         sgs_ld,  # 输干水
         XX_hcgys_ld, dxgs_hcgys_ld, gs_hcgys_ld, qus_hcgys_ld, zxs_hcgys_ld18,  # run1 中返回
         hjdxgs_hcgys_ld, hjgs_hcgys_ld, hjqus_hcgys_ld, zhgs_hcgys_ld, qis_hcgys_ld,
         bzl_hcgys_ld):
    ls_hcgsk = XX_hcgys_ld.values
    #################################################
    QS0, gs_hcgsk, ph_hcgsk = process_shuku(ls_hcgsk, m_hcgsk, sl_hcgsk, v_hcgsk, zf_hcgsk, zxs_hcgsk)
    F_SKGS, SKGS0, SKGS17, fgs_hcgsk, hgs_hcgsk, qs_hcgsk = process_shuku_hangye(QS0, gs_hcgsk, xs_hcgsk, zxs_hcgsk)
    gs_sgs_ld, ls_hcgyx_ld1, xs_hcgyx_ld1, zgs_sgs_ld, zxs_hcgyx_ld1 = process_shuganshui(
        ls_hcgyx_ld, qs_hcgsk, sgs_ld, xs_hcgyx_ld, zxs_hcgyx_ld
    )
    ##################################################################
    (zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1,
     HJDXGS1, GS178, DXGS178, QS178, XS17, XS16, zdxxs) = gx(
        ls_hcgyx_ld1, xs_hcgyx_ld1, zxs_hcgyx_ld1, dx_xs_hcgyx_ld, ss_hcgyx_ld
    )

    (XX_hcgyx_ld, bzl_hcgyx_js,
     dxgs_hcgyx_js, gs_hcgyx_js,
     qus_hcgyx_js, zhgs_hcgyx_ld,
     jh_hcgyx_ld,
     zxs_hcgyx_ld18, ls_hcgyx_js
     ) = cleaner(DXGS17, DXGS178, DXHGS, GS17, GS178, HGS,
                 HJDXGS1, HJGS1, HJQUES1, QS17, QS178, ZQS,
                 XX_hcgys_ld,
                 dx_xs_hcgyx_ld, zxs_hcgyx_ld, xs_hcgyx_ld,
                 ls_hcgyx_ld, ls_hcgyx_ld,
                 gs_hcgsk, hgs_hcgsk, SKGS17,
                 zdxxs)
    # print(XX_hcgyx_ld)
    shuchu4 = pd.concat([n, y, pd.DataFrame(ls_hcgyx_ld), qs_hcgsk, HJGS1,
                         zhgs_hcgyx_ld, XX_hcgyx_ld,
                         jh_hcgyx_ld, pd.DataFrame(zxs_hcgyx_ld),
                         zgs_sgs_ld, HJDXGS1, HJQUES1], axis=1)

    shuchu4 = shuchu4.set_axis(BiaoTouWaterType, axis='columns', copy=False)
    jz2, zz = JZ(shuchu4)
    shuchu4_1 = pd.concat([shuchu4, jz2])

    shuchu4_2 = pd.concat(
        [n, y,
         pd.DataFrame(zxs_hcgyx_ld18,
                      columns=BiaoTouHangYe),
         pd.DataFrame(zxs_hcgyx_ld + zdxxs,
                      columns=['总需水']), KB0, GS178, KB0, DXGS178, KB0, QS178], axis=1)
    jz2, zz = JZ(shuchu4_2)
    shuchu4_20 = jz2  ###

    save_frame(shuchu4_2, 'xx_shuchu4_2')
    save_frame(shuchu4_20, 'xx_shuchu4_20')
    ########################################################################33

    # shj_ld_dbxs = pd.DataFrame(xs_hcgys_ld + xs_hcgyx_ld)
    # shj_ld_dxxs = dx_xs_hcgys_ld + dx_xs_hcgyx_ld
    # shj_ld_dxgs = dxgs_hcgys_ld + dxgs_hcgyx_js
    # shj_ld_dbgs = gs_hcgys_ld + gs_hcgyx_js
    # shj_ld_sgs = gs_sgs_ld
    # shj_ld_qus = qus_hcgys_ld + qus_hcgyx_js
    # shj_ld_xs_fhy = pd.DataFrame(zxs_hcgys_ld18 + zxs_hcgyx_js18, columns=BiaoTouWaterType)
    # shj_ld_gs_fhy = shj_ld_dbgs + shj_ld_dxgs + shj_ld_sgs
    # SHJ_LD0 = pd.concat([n, y, shj_ld_xs_fhy, shj_ld_gs_fhy, shj_ld_qus], axis=1)
    # jz2, zz = JZ(SHJ_LD0)
    # jz_SHJ_LD0 = zz
    # shj_ld_dbzxs = pd.DataFrame(zxs_hcgys_ld + zxs_hcgyx_ld)
    # shj_ld_dxzxs = hjdxgs_hcgys_ld + hjdxgs_hcgyx_ld
    # shj_ld_dbzgs = hjgs_hcgys_ld + hjgs_hcgyx_ld
    # shj_ld_hjqus = hjqus_hcgys_ld + hjqus_hcgyx_ld
    # shj_ld_qis = qis_hcgys_ld + qis_hcgyx_ld
    # shj_ld_hgs = zhgs_hcgys_ld + zhgs_hcgyx_ld
    # SHJ_LD = pd.concat([n, y, shj_ld_dbzxs, shj_ld_dxzxs, shj_ld_dbzxs +
    #                     shj_ld_dxzxs, shj_ld_dbzgs, KB0, shj_ld_dxzxs, KB0, zgs_sgs_ld, KB0,
    #                     shj_ld_dbzgs + shj_ld_dxzxs + zgs_sgs_ld, shj_ld_hjqus, KB0], axis=1)
    # SHJ_LD = SHJ_LD.set_axis(['年', '月', '地表需水', '地下需水', '总需水', '地表供水', '水库供水',
    #                           '地下供水', '三江连通', '疏干水', '中水', '总供水', '缺水', '两江一湖'], axis='columns',
    #                          copy
    #                          =False)
    # jz2, zz = JZ(SHJ_LD)
    # jz_SHJ_LD = zz
    # SHJ_LD_1 = pd.concat([SHJ_LD, jz2])

    # method_name(DXGS17, DXGS178, DXHGS, GS17, GS178, HGS, HJDXGS1, HJGS1, HJQUES1, QS17, QS178, ZQS,
    #             XX_hcgyx_js,
    #             dx_xs_hcgyx_js, zxs_hcgyx_js, xs_hcgyx_js,
    #             ls_hcgyx_js, ls_hcgyx_js1,
    #             gs_hcgsk, hgs_hcgsk, SKGS17,
    #             zdxxs)

    #
    # return (XX_hcgyx_js, dxgs_hcgyx_js,
    #         gs_hcgyx_js, qus_hcgyx_js, zxs_hcgyx_js18, hjdxgs_hcgyx_ld,
    #         hjgs_hcgyx_ld, zhgs_hcgyx_ld,
    #         qis_hcgyx_ld, bzl_hcgyx_ld, gs_hcgsk, F_SKGS, SKGS17, hgs_hcgsk,
    #         SKGS0, jz_SHJ_LD, jz_SHJ_LD0, ph_hcgsk, gs_sgs_ld, shuchu4_1, shuchu4_2, shuchu4_20, fgs_hcgsk)

    return (XX_hcgyx_ld, dxgs_hcgyx_js,
            gs_hcgyx_js, qus_hcgyx_js, zxs_hcgyx_ld18,
            bzl_hcgyx_js, gs_hcgsk, F_SKGS, SKGS17, hgs_hcgsk,
            SKGS0, ph_hcgsk, gs_sgs_ld, shuchu4_1, shuchu4_2, shuchu4_20, fgs_hcgsk)

    """
    ys_gs, ZHGS_YS, YSGS17, ZYSGS, GS, ZGS=ysrs(ysrs_js,xs_hcgyx_js)
    gs_ysrs_js=YSGS17
    zgs_ysrs_js=ZYSGS
    hgs_ysrs_js=ZHGS_YS
    """


def process_shuganshui(ls_hcgyx_ld, qs_hcgsk, sgs_ld, xs_hcgyx_ld, zxs_hcgyx_ld):
    sgs_gs, sgs_zgs, ZHGS_SG, SGGS17, ZGS_SG, GS, ZGS = sgs(sgs_ld, xs_hcgyx_ld)
    gs_sgs_ld = SGGS17
    zgs_sgs_ld = ZGS
    hgs_sgs_ld = ZHGS_SG
    ls_hcgyx_ld1 = ls_hcgyx_ld + qs_hcgsk
    xs_hcgyx_ld1 = xs_hcgyx_ld - gs_sgs_ld.values
    zxs_hcgyx_ld1 = zxs_hcgyx_ld - zgs_sgs_ld
    return gs_sgs_ld, ls_hcgyx_ld1, xs_hcgyx_ld1, zgs_sgs_ld, zxs_hcgyx_ld1


def process_shuku_hangye(QS0, gs_hcgsk, xs_hcgsk, zxs_hcgsk):
    (skzqis, SKZQS, SKHGS, SKGS17, SKQS17, SKHJGS, F_SKGS, F_SKGS18, GS9_1,
     SKHGS_9, SKHJGS1_9, SKGS0, skgs9) = shuikuGS(gs_hcgsk, xs_hcgsk, zxs_hcgsk)
    hgs_hcgsk = SKHGS
    fgs_hcgsk = pd.DataFrame(SKGS17)
    qs_hcgsk = pd.DataFrame(QS0)
    return F_SKGS, SKGS0, SKGS17, fgs_hcgsk, hgs_hcgsk, qs_hcgsk


def process_shuku(ls_hcgsk: np.ndarray, m_hcgsk, sl_hcgsk, v_hcgsk, zf_hcgsk, zxs_hcgsk):
    '''
    ToDo: 变量理清
    '''
    # print(zf_hcgsk.shape, type(zf_hcgsk))
    # print(zxs_hcgsk.shape, type(zxs_hcgsk))
    assert ls_hcgsk.shape == (732, 1)
    assert m_hcgsk.shape == (18,)
    assert sl_hcgsk.shape == (732,)
    assert v_hcgsk.shape == (18,)
    assert zf_hcgsk.shape == (732,)
    assert zxs_hcgsk.shape == (732,)

    Vx_hcgsk, Vxx_hcgsk, Vdead_hcgsk = 7667.00, 7049.00, 80.00
    V0_hcgsk = Vx_hcgsk  # 以下函数调用，清晰起见创建变量
    gs, ZF, SL, qs, V2, V3, jh, GS0, QS0, df2 = shuiku0(
        V0_hcgsk, ls_hcgsk, zxs_hcgsk,
        y, n, Vx_hcgsk,
        Vxx_hcgsk, Vdead_hcgsk, v_hcgsk,
        m_hcgsk, zf_hcgsk, sl_hcgsk)

    # bk: 不必要
    # ph_hcgsk = df2

    # 这个不必单独创建，可从 df2 中获取
    # GF2 = df2['供水']
    # gs_hcgsk = pd.DataFrame(GF2.values)
    # bk: 替换为
    gs_hcgsk = df2[['供水']]

    return QS0, gs_hcgsk, df2


def cleaner(DXGS17, DXGS178, DXHGS, GS17, GS178, HGS, HJDXGS1, HJGS1, HJQUES1, QS17, QS178, ZQS,
            XX_hcgyx_ld,
            dx_xs_hcgyx_js, zxs_hcgyx_js, xs_hcgyx_js,
            ls_hcgyx_js, ls_hcgyx_js1,
            gs_hcgsk, hgs_hcgsk, SKGS17,
            zdxxs):
    assert DXGS17.shape == (732, 16)
    assert DXGS178.shape == (732, 17)
    assert DXHGS.shape == (732, 1)

    assert GS17.shape == (732, 16)
    assert GS178.shape == (732, 17)
    assert HGS.shape == (732, 1)
    assert HJDXGS1.shape == (732, 1)
    assert HJGS1.shape == (732, 1)

    assert HJQUES1.shape == (732, 1)
    assert QS17.shape == (732, 16)

    assert QS178.shape == (732, 17)
    assert ZQS.shape == (732, 1)

    # assert XX_hcgyx_ld.shape == (732,1) #todo:None

    assert dx_xs_hcgyx_js.shape == (732, 16)
    assert zxs_hcgyx_js.shape == (732, 1)
    assert xs_hcgyx_js.shape == (732, 16)

    assert ls_hcgyx_js.shape == (732, 1)
    assert ls_hcgyx_js1.shape == (732, 1)
    # assert gs_hcgsk.shape == (732,1)#todo:None

    # print(SKGS17.shape)
    # print(zdxxs.shape)
    # assert hgs_hcgsk.shape == (732,1) #todo:None
    # assert SKGS17.shape == (732,1) #todo:None
    assert zdxxs.shape == (732, 1)

    gs_hcgyx_js = GS17
    # if SKGS17 is not None:
    #     zgs_hcgyx_js = GS17 + SKGS17
    # else:
    #     zgs_hcgyx_js = GS17
    dxgs_hcgyx_js = DXGS17
    zxs_hcgyx_js18 = xs_hcgyx_js + dx_xs_hcgyx_js
    qus_hcgyx_js = QS17
    qis_hcgyx_js = ZQS
    if hgs_hcgsk is not None:
        dbhgs_hcgyx_js = HGS + hgs_hcgsk
    else:
        dbhgs_hcgyx_js = HGS
    dxhgs_hcgyx_js = DXHGS
    zhgs_hcgyx_js = dxhgs_hcgyx_js + dbhgs_hcgyx_js

    XX_hcgyx_js = qis_hcgyx_js + zhgs_hcgyx_js

    assert XX_hcgyx_js.shape == (732, 1)
    jh_hcgyx_js = ls_hcgyx_js1 - HJGS1 + zhgs_hcgyx_js - XX_hcgyx_js
    qus_hcgyx_js1 = np.array(qus_hcgyx_js)
    bzl, df_bzl = BZL(qus_hcgyx_js1)
    bzl_hcgyx_js = df_bzl

    return (XX_hcgyx_js, bzl_hcgyx_js,
            dxgs_hcgyx_js, gs_hcgyx_js,
            qus_hcgyx_js, zhgs_hcgyx_js,
            jh_hcgyx_js,
            zxs_hcgyx_js18, ls_hcgyx_js)
