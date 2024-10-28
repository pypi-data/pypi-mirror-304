from .lhy_func import *
from .prepare_data import *
# from slw_const import RESULT_PATH



def run1():
    (zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1,
        HJDXGS1, GS178, DXGS178, QS178, XS17, XS16, zdxxs) = (gx(ls_hcgys_ld,
        xs_hcgys_ld, zxs_hcgys_ld, dx_xs_hcgys_ld, ss_hcgys_ld))
    save_frame(QS17, 'xx_x')
    gs_hcgys_ld = GS17
    dxgs_hcgys_ld = DXGS17
    hjgs_hcgys_ld = HJGS1
    hjdxgs_hcgys_ld = HJDXGS1
    zxs_hcgys_ld18 = xs_hcgys_ld + dx_xs_hcgys_ld
    qus_hcgys_ld = QS17
    hjqus_hcgys_ld = HJQUES1
    qis_hcgys_ld = ZQS
    dbhgs_hcgys_ld = HGS
    dxhgs_hcgys_ld = DXHGS
    zhgs_hcgys_ld = dbhgs_hcgys_ld + dxhgs_hcgys_ld
    XX_hcgys_ld = qis_hcgys_ld + zhgs_hcgys_ld
    jh_hcgys_ld = ls_hcgys_ld - HJGS1 + zhgs_hcgys_ld - XX_hcgys_ld
    qus_hcgys_ld1 = np.array(qus_hcgys_ld)
    bzl, df_bzl = BZL(qus_hcgys_ld1)
    bzl_hcgys_ld = df_bzl
    shuchu3 = pd.concat([n, y, pd.DataFrame(ls_hcgys_ld), HJGS1, zhgs_hcgys_ld,
        XX_hcgys_ld, jh_hcgys_ld, pd.DataFrame(zxs_hcgys_ld), HJDXGS1, HJQUES1],
        axis=1)
    shuchu3 = shuchu3.set_axis(['年', '月', '本地水', '地表供水', '回归水', '下泄', '校核',
        '需水', '地下供水', '缺水'], axis='columns', copy=False)
    jz2, zz = JZ(shuchu3)
    shuchu3_1 = pd.concat([shuchu3, jz2])
    shuchu3_2 = pd.concat([n, y, XS16, XS17, KB0, GS178, KB0, DXGS178, KB0,
        QS178], axis=1)
    jz2, zz = JZ(shuchu3_2)
    shuchu3_20 = jz2

    """
    with pd.ExcelWriter(file_path + '分行业.xlsx') as writer:
      shuchu3_2.to_excel(writer, sheet_name="区县合计",index=False)
      shuchu3_20.to_excel(writer, sheet_name="区县合计",startcol=0, startrow=733)
    """
    # todo 不返回shuchu ，直接调用函数存储为exl表
    # save_w_sheetname(shuchu3_1,'平衡不分行业-基准年','3')
    # save_w_sheetname(shuchu3_2,'平衡分行业-基准年','3')
    # save_w_startcol(shuchu3_20,'平衡分行业-基准年','3',0,733)
    #
    # save_frame(shuchu3_2, 'xx_分行业_区县合计')
    # save_frame(shuchu3_20, 'xx_分行业_区县合计')

    return (shuchu3_1, shuchu3_2, shuchu3_20, XX_hcgys_ld, dxgs_hcgys_ld, gs_hcgys_ld,
            qus_hcgys_ld, zxs_hcgys_ld18, hjdxgs_hcgys_ld, hjgs_hcgys_ld, hjgs_hcgys_ld,
            zhgs_hcgys_ld, qis_hcgys_ld,bzl_hcgys_ld,hjqus_hcgys_ld,gs_hcgys_ld)




def run2(   XX_hcgys_ld, dxgs_hcgys_ld, gs_hcgys_ld, qus_hcgys_ld, zxs_hcgys_ld18, hjdxgs_hcgys_ld,hjgs_hcgys_ld, hjqus_hcgys_ld, zhgs_hcgys_ld,qis_hcgys_ld,bzl_hcgys_ld):
    ls_hcgsk = XX_hcgys_ld.values
    gs, ZF, SL, qs, V2, V3, jh, GS0, QS0, df2 = shuiku0(V0_hcgsk, ls_hcgsk,
        zxs_hcgsk, y, n, Vx_hcgsk, Vxx_hcgsk, Vdead_hcgsk, v_hcgsk, m_hcgsk,
        zf_hcgsk, sl_hcgsk)
    ph_hcgsk = df2
    GF2 = df2['供水']
    gs_hcgsk = pd.DataFrame(GF2.values)
    (skzqis, SKZQS, SKHGS, SKGS17, SKQS17, SKHJGS, F_SKGS, F_SKGS18, GS9_1,
        SKHGS_9, SKHJGS1_9, SKGS0, skgs9) = shuikuGS(gs_hcgsk, xs_hcgsk, zxs_hcgsk)
    hgs_hcgsk = SKHGS
    fgs_hcgsk = pd.DataFrame(SKGS17)
    qs_hcgsk = pd.DataFrame(QS0)
    """
    ys_gs, ZHGS_YS, YSGS17, ZYSGS, GS, ZGS=ysrs(ysrs_ld,xs_hcgyx_ld)
    gs_ysrs_ld=YSGS17
    zgs_ysrs_ld=ZYSGS
    hgs_ysrs_ld=ZHGS_YS
    """
    sgs_gs, sgs_zgs, ZHGS_SG, SGGS17, ZGS_SG, GS, ZGS = sgs(sgs_ld, xs_hcgyx_ld)
    gs_sgs_ld = SGGS17
    zgs_sgs_ld = ZGS
    hgs_sgs_ld = ZHGS_SG
    ls_hcgyx_ld1 = ls_hcgyx_ld + qs_hcgsk
    xs_hcgyx_ld1 = xs_hcgyx_ld - gs_sgs_ld.values
    zxs_hcgyx_ld1 = zxs_hcgyx_ld - zgs_sgs_ld
    (zqis, ZQS, HGS, GS17, QS17, DXHGS, ZHGS, DXGS17, HJGS, HJGS1, HJQUES1,
        HJDXGS1, GS178, DXGS178, QS178, XS17, XS16, zdxxs) = (gx(ls_hcgyx_ld1,
        xs_hcgyx_ld1, zxs_hcgyx_ld1, dx_xs_hcgyx_ld, ss_hcgyx_ld))
    gs_hcgyx_ld = GS17
    hjgs_hcgyx_ld = HJGS1
    zgs_hcgyx_ld = gs_hcgyx_ld + gs_sgs_ld
    dxgs_hcgyx_ld = DXGS17
    hjdxgs_hcgyx_ld = HJDXGS1
    zxs_hcgyx_ld18 = xs_hcgyx_ld + dx_xs_hcgyx_ld
    qus_hcgyx_ld = QS17
    hjqus_hcgyx_ld = HJQUES1
    qis_hcgyx_ld = ZQS
    dbhgs_hcgyx_ld = HGS + hgs_sgs_ld
    dxhgs_hcgyx_ld = DXHGS
    zhgs_hcgyx_ld = dbhgs_hcgyx_ld + dxhgs_hcgyx_ld
    XX_hcgyx_ld = qis_hcgyx_ld + zhgs_hcgyx_ld
    jh_hcgyx_ld = ls_hcgyx_ld1 - HJGS1 + zhgs_hcgyx_ld - XX_hcgyx_ld
    qus_hcgyx_ld1 = np.array(qus_hcgyx_ld)
    bzl, df_bzl = BZL(qus_hcgyx_ld1)
    bzl_hcgyx_ld = df_bzl
    shuchu4 = pd.concat([n, y, pd.DataFrame(ls_hcgyx_ld), qs_hcgsk, HJGS1,
        zhgs_hcgyx_ld, XX_hcgyx_ld, jh_hcgyx_ld, pd.DataFrame(zxs_hcgyx_ld),
        zgs_sgs_ld, HJDXGS1, HJQUES1], axis=1)
    shuchu4 = shuchu4.set_axis(['年', '月', '本地水', '上区间来水', '地表供水', '回归水', '下泄',
        '校核', '需水', '疏干水', '地下供水', '缺水'], axis='columns', copy=False)
    jz2, zz = JZ(shuchu4)
    shuchu4_1 = pd.concat([shuchu4, jz2])
    shuchu4_2 = pd.concat([n, y, pd.DataFrame(zxs_hcgyx_ld18, columns=['城镇生活',
        '农村生活', '牲畜', '三产', '火核电', '一般工业', '高耗水工业', '建筑业', '水田', '水浇地', '菜田',
        '林果地', '草场', '鱼塘', '城镇生态', '湿地']), pd.DataFrame(zxs_hcgyx_ld + zdxxs,
        columns=['总需水']), KB0, GS178, KB0, DXGS178, KB0, QS178], axis=1)
    jz2, zz = JZ(shuchu4_2)
    shuchu4_20 = jz2
    shj_ld_dbxs = pd.DataFrame(xs_hcgys_ld + xs_hcgyx_ld)
    shj_ld_dxxs = dx_xs_hcgys_ld + dx_xs_hcgyx_ld
    shj_ld_dxgs = dxgs_hcgys_ld + dxgs_hcgyx_ld
    shj_ld_dbgs = gs_hcgys_ld + gs_hcgyx_ld
    shj_ld_sgs = gs_sgs_ld
    shj_ld_qus = qus_hcgys_ld + qus_hcgyx_ld
    shj_ld_xs_fhy = pd.DataFrame(zxs_hcgys_ld18 + zxs_hcgyx_ld18, columns=[
        '城镇生活', '农村生活', '牲畜', '三产', '火核电', '一般工业', '高耗水工业', '建筑业', '水田', '水浇地',
        '菜田', '林果地', '草场', '鱼塘', '城镇生态', '湿地'])
    shj_ld_gs_fhy = shj_ld_dbgs + shj_ld_dxgs + shj_ld_sgs
    SHJ_LD0 = pd.concat([n, y, shj_ld_xs_fhy, shj_ld_gs_fhy, shj_ld_qus], axis=1)
    jz2, zz = JZ(SHJ_LD0)
    jz_SHJ_LD0 = zz
    shj_ld_dbzxs = pd.DataFrame(zxs_hcgys_ld + zxs_hcgyx_ld)
    shj_ld_dxzxs = hjdxgs_hcgys_ld + hjdxgs_hcgyx_ld
    shj_ld_dbzgs = hjgs_hcgys_ld + hjgs_hcgyx_ld
    shj_ld_hjqus = hjqus_hcgys_ld + hjqus_hcgyx_ld
    shj_ld_qis = qis_hcgys_ld + qis_hcgyx_ld
    shj_ld_hgs = zhgs_hcgys_ld + zhgs_hcgyx_ld
    SHJ_LD = pd.concat([n, y, shj_ld_dbzxs, shj_ld_dxzxs, shj_ld_dbzxs +
        shj_ld_dxzxs, shj_ld_dbzgs, KB0, shj_ld_dxzxs, KB0, zgs_sgs_ld, KB0,
        shj_ld_dbzgs + shj_ld_dxzxs + zgs_sgs_ld, shj_ld_hjqus, KB0], axis=1)
    SHJ_LD = SHJ_LD.set_axis(['年', '月', '地表需水', '地下需水', '总需水', '地表供水', '水库供水',
        '地下供水', '三江连通', '疏干水', '中水', '总供水', '缺水', '两江一湖'], axis='columns', copy
        =False)
    jz2, zz = JZ(SHJ_LD)
    jz_SHJ_LD = zz
    SHJ_LD_1 = pd.concat([SHJ_LD, jz2])



    """
    ys_gs, ZHGS_YS, YSGS17, ZYSGS, GS, ZGS=ysrs(ysrs_js,xs_hcgyx_js)
    gs_ysrs_js=YSGS17
    zgs_ysrs_js=ZYSGS
    hgs_ysrs_js=ZHGS_YS
    """

    return (ph_hcgsk,hgs_hcgsk)
