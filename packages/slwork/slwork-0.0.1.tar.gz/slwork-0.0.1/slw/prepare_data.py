from slw.add_code import *

#资料输入
#笔架山水库以上-集贤
ls_bjsys_jx0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [2])
xs_bjsys_jx0 = load_pd_data("地表需水过程线", "笔架山水库以上集贤", index_col = None, usecols = ("B:Q"))
dx_xs_bjsys_jx0 = load_pd_data("地下水需水", "笔架山水库以上集贤", index_col = None, usecols = ("B:Q"))
#df0=ls_bjsys_jx.DataFrame()
zxs_bjsys_jx0 = load_pd_data("地表需水过程线", "笔架山水库以上集贤", index_col = False, usecols = [17])
ls_bjsys_jx=np.array(ls_bjsys_jx0)
xs_bjsys_jx= np.array(xs_bjsys_jx0)
zxs_bjsys_jx=np.array(zxs_bjsys_jx0)
dx_xs_bjsys_jx=np.array(dx_xs_bjsys_jx0)

#笔架山水库以下-集贤
ls_bjsyx_jx0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [3])
xs_bjsyx_jx0 = load_pd_data("地表需水过程线", "笔架山水库以下集贤", index_col = None, usecols = ("B:Q"))
dx_xs_bjsyx_jx0 = load_pd_data("地下水需水", "笔架山水库以下集贤", index_col = None, usecols = ("B:Q"))
zxs_bjsyx_jx0 = load_pd_data("地表需水过程线", "笔架山水库以下集贤", index_col = False, usecols = [17])
ls_bjsyx_jx=np.array(ls_bjsyx_jx0)
xs_bjsyx_jx= np.array(xs_bjsyx_jx0)
zxs_bjsyx_jx= np.array(zxs_bjsyx_jx0)
dx_xs_bjsyx_jx=np.array(dx_xs_bjsyx_jx0)
#寒葱沟水库以上-岭东区
ls_hcgys_ld0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [4])
xs_hcgys_ld0 = load_pd_data("地表需水过程线", "寒葱沟水库以上岭东", index_col = None, usecols = ("B:Q"))
dx_xs_hcgys_ld0 = load_pd_data("地下水需水", "寒葱沟水库以上岭东", index_col = None, usecols = ("B:Q"))
zxs_hcgys_ld0 = load_pd_data("地表需水过程线", "寒葱沟水库以上岭东",
                             index_col = False, usecols = [17])
ls_hcgys_ld=np.array(ls_hcgys_ld0)
xs_hcgys_ld= np.array(xs_hcgys_ld0)
zxs_hcgys_ld= np.array(zxs_hcgys_ld0)
dx_xs_hcgys_ld=np.array(dx_xs_hcgys_ld0)
#寒葱沟水库以下-岭东区
ls_hcgyx_ld0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [5])
xs_hcgyx_ld0 = load_pd_data("地表需水过程线", "寒葱沟水库以下岭东", index_col = None, usecols = ("B:Q"))
dx_xs_hcgyx_ld0 = load_pd_data("地下水需水", "寒葱沟水库以下岭东", index_col = None, usecols = ("B:Q"))
zxs_hcgyx_ld0 = load_pd_data("地表需水过程线", "寒葱沟水库以下岭东", index_col = False, usecols = [17])
ls_hcgyx_ld=np.array(ls_hcgyx_ld0)
xs_hcgyx_ld= np.array(xs_hcgyx_ld0)
zxs_hcgyx_ld= np.array(zxs_hcgyx_ld0)
dx_xs_hcgyx_ld=np.array(dx_xs_hcgyx_ld0)
#寒葱沟水库以下-尖山区
ls_hcgyx_js0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [6])
xs_hcgyx_js0 = load_pd_data("地表需水过程线", "寒葱沟水库以下尖山", index_col = None, usecols = ("B:Q"))
dx_xs_hcgyx_js0 = load_pd_data("地下水需水", "寒葱沟水库以下尖山", index_col = None, usecols = ("B:Q"))
zxs_hcgyx_js0 = load_pd_data("地表需水过程线", "寒葱沟水库以下尖山", index_col = False, usecols = [17])
ls_hcgyx_js=np.array(ls_hcgyx_js0)
xs_hcgyx_js= np.array(xs_hcgyx_js0)
zxs_hcgyx_js= np.array(zxs_hcgyx_js0)
dx_xs_hcgyx_js=np.array(dx_xs_hcgyx_js0)
#寒葱沟水库以下-四方台区
ls_hcgyx_sft0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [7])
xs_hcgyx_sft0 = load_pd_data("地表需水过程线", "寒葱沟水库以下四方台", index_col = None, usecols = ("B:Q"))
dx_xs_hcgyx_sft0 = load_pd_data("地下水需水", "寒葱沟水库以下四方台", index_col = None, usecols = ("B:Q"))
zxs_hcgyx_sft0 = load_pd_data("地表需水过程线", "寒葱沟水库以下四方台", index_col = False, usecols = [17])
ls_hcgyx_sft=np.array(ls_hcgyx_sft0)
xs_hcgyx_sft= np.array(xs_hcgyx_sft0)
zxs_hcgyx_sft= np.array(zxs_hcgyx_sft0)
dx_xs_hcgyx_sft=np.array(dx_xs_hcgyx_sft0)
#寒葱沟水库以下-集贤县
ls_hcgyx_jx0 = load_pd_data("地表需水过程线", "天然来水", index_col = False, usecols = [8])
xs_hcgyx_jx0 = load_pd_data("地表需水过程线", "寒葱沟水库以下集贤", index_col = None, usecols = ("B:Q"))
dx_xs_hcgyx_jx0 = load_pd_data("地下水需水", "寒葱沟水库以下集贤", index_col = None, usecols = ("B:Q"))
zxs_hcgyx_jx0 = load_pd_data("地表需水过程线", "寒葱沟水库以下集贤", index_col = False, usecols = [17])
ls_hcgyx_jx=np.array(ls_hcgyx_jx0)
xs_hcgyx_jx= np.array(xs_hcgyx_jx0)
zxs_hcgyx_jx= np.array(zxs_hcgyx_jx0)
dx_xs_hcgyx_jx=np.array(dx_xs_hcgyx_jx0)
#8龙头桥水库以上宝清县
ls_ltqys_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [9])
xs_ltqys_bq = load_np_data("地表需水过程线", "龙头桥水库以上宝清", index_col = None, usecols = ("B:Q"))
zxs_ltqys_bq = load_np_data("地表需水过程线", "龙头桥水库以上宝清", index_col = False, usecols = [17])
dx_xs_ltqys_bq = load_np_data("地下水需水", "龙头桥水库以上宝清", index_col = None, usecols = ("B:Q"))
#9 龙头桥水库以下-尖山区
ls_ltqyx_js = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [10])
xs_ltqyx_js = load_np_data("地表需水过程线", "龙头桥水库以下尖山", index_col = None, usecols = ("B:Q"))
zxs_ltqyx_js = load_np_data("地表需水过程线", "龙头桥水库以下尖山", index_col = False, usecols = [17])
dx_xs_ltqyx_js = load_np_data("地下水需水", "龙头桥水库以下尖山", index_col = None, usecols = ("B:Q"))
#10 龙头桥水库以下四方台
ls_ltqyx_sft = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [11])
xs_ltqyx_sft = load_np_data("地表需水过程线", "龙头桥水库以下四方台", index_col = None, usecols = ("B:Q"))
zxs_ltqyx_sft = load_np_data("地表需水过程线", "龙头桥水库以下四方台", index_col = False, usecols = [17])
dx_xs_ltqyx_sft = load_np_data("地下水需水", "龙头桥水库以下四方台", index_col = None, usecols = ("B:Q"))
#11龙头桥以下集贤县
ls_ltqyx_jx = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [12])
xs_ltqyx_jx = load_np_data("地表需水过程线", "龙头桥水库以下集贤", index_col = None, usecols = ("B:Q"))
zxs_ltqyx_jx = load_np_data("地表需水过程线", "龙头桥水库以下集贤", index_col = False, usecols = [17])
dx_xs_ltqyx_jx = load_np_data("地下水需水", "龙头桥水库以下集贤", index_col = None, usecols = ("B:Q"))
#12徕凤湖以上宝清
ls_lfhys_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [13])
xs_lfhys_bq = load_np_data("地表需水过程线", "徕凤湖水库以上宝清", index_col = None, usecols = ("B:Q"))
zxs_lfhys_bq = load_np_data("地表需水过程线", "徕凤湖水库以上宝清", index_col = False, usecols = [17])
dx_xs_lfhys_bq = load_np_data("地下水需水", "徕凤湖水库以上宝清", index_col = None, usecols = ("B:Q"))
#13徕凤湖以下宝清
ls_lfhyx_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [14])
xs_lfhyx_bq = load_np_data("地表需水过程线", "徕凤湖水库以下宝清", index_col = None, usecols = ("B:Q"))
zxs_lfhyx_bq = load_np_data("地表需水过程线", "徕凤湖水库以下宝清", index_col = False, usecols = [17])
dx_xs_lfhyx_bq = load_np_data("地下水需水", "徕凤湖水库以下宝清", index_col = None, usecols = ("B:Q"))
#14大索伦水库以上宝清
ls_dslys_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [15])
xs_dslys_bq = load_np_data("地表需水过程线", "大索伦水库以上宝清", index_col = None, usecols = ("B:Q"))
zxs_dslys_bq = load_np_data("地表需水过程线", "大索伦水库以上宝清", index_col = False, usecols = [17])
dx_xs_dslys_bq = load_np_data("地下水需水", "大索伦水库以上宝清", index_col = None, usecols = ("B:Q"))
#15大索伦以下宝清
ls_dslyx_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [16])
xs_dslyx_bq = load_np_data("地表需水过程线", "大索伦水库以下宝清", index_col = None, usecols = ("B:Q"))
zxs_dslyx_bq = load_np_data("地表需水过程线", "大索伦水库以下宝清", index_col = False, usecols = [17])
dx_xs_dslyx_bq = load_np_data("地下水需水", "大索伦水库以下宝清", index_col = None, usecols = ("B:Q"))
#16蛤蟆通以上宝清
ls_hmtys_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [17])
xs_hmtys_bq = load_np_data("地表需水过程线", "蛤蟆通水库以上宝清", index_col = None, usecols = ("B:Q"))
zxs_hmtys_bq = load_np_data("地表需水过程线", "蛤蟆通水库以上宝清", index_col = False, usecols = [17])
dx_xs_hmtys_bq = load_np_data("地下水需水", "蛤蟆通水库以上宝清", index_col = None, usecols = ("B:Q"))
#17蛤蟆通以下宝清
ls_hmtyx_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [18])
xs_hmtyx_bq = load_np_data("地表需水过程线", "蛤蟆通水库以下宝清", index_col = None, usecols = ("B:Q"))
zxs_hmtyx_bq = load_np_data("地表需水过程线", "蛤蟆通水库以下宝清", index_col = False, usecols = [17])
dx_xs_hmtyx_bq = load_np_data("地下水需水", "蛤蟆通水库以下宝清", index_col = None, usecols = ("B:Q"))
#18清河水库以上宝清
ls_qhys_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [19])
xs_qhys_bq = load_np_data("地表需水过程线", "清河水库以上宝清", index_col = None, usecols = ("B:Q"))
zxs_qhys_bq = load_np_data("地表需水过程线", "清河水库以上宝清", index_col = False, usecols = [17])
dx_xs_qhys_bq = load_np_data("地下水需水", "清河水库以上宝清", index_col = None, usecols = ("B:Q"))
#19清河水库以下宝清
ls_qhyx_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [20])
xs_qhyx_bq = load_np_data("地表需水过程线", "清河水库以下宝清", index_col = None, usecols = ("B:Q"))
zxs_qhyx_bq = load_np_data("地表需水过程线", "清河水库以下宝清", index_col = False, usecols = [17])
dx_xs_qhyx_bq = load_np_data("地下水需水", "清河水库以下宝清", index_col = None, usecols = ("B:Q"))
#20大叶沟水库以上岭东区
ls_dygys_ld = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [21])
xs_dygys_ld = load_np_data("地表需水过程线", "大叶沟水库以上岭东", index_col = None, usecols = ("B:Q"))
zxs_dygys_ld = load_np_data("地表需水过程线", "大叶沟水库以上岭东", index_col = False, usecols = [17])
dx_xs_dygys_ld = load_np_data("地下水需水", "大叶沟水库以上岭东", index_col = None, usecols = ("B:Q"))
#21大叶沟水库以上宝山区
ls_dygys_bs = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [22])
xs_dygys_bs = load_np_data("地表需水过程线", "大叶沟水库以上宝山", index_col = None, usecols = ("B:Q"))
zxs_dygys_bs = load_np_data("地表需水过程线", "大叶沟水库以上宝山", index_col = False, usecols = [17])
dx_xs_dygys_bs = load_np_data("地下水需水", "大叶沟水库以上宝山", index_col = None, usecols = ("B:Q"))
#22大叶沟水库以下宝山区
ls_dygyx_bs = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [23])
xs_dygyx_bs = load_np_data("地表需水过程线", "大叶沟水库以下宝山", index_col = None, usecols = ("B:Q"))
zxs_dygyx_bs = load_np_data("地表需水过程线", "大叶沟水库以下宝山", index_col = False, usecols = [17])
dx_xs_dygyx_bs = load_np_data("地下水需水", "大叶沟水库以下宝山", index_col = None, usecols = ("B:Q"))
#23三峰水库以上友谊县
ls_sfys_yy = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [24])
xs_sfys_yy = load_np_data("地表需水过程线", "三峰水库以上友谊", index_col = None, usecols = ("B:Q"))
zxs_sfys_yy = load_np_data("地表需水过程线", "三峰水库以上友谊", index_col = False, usecols = [17])
dx_xs_sfys_yy = load_np_data("地下水需水", "三峰水库以上友谊", index_col = None, usecols = ("B:Q"))
#24三峰水库以下友谊县
ls_sfyx_yy = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [25])
xs_sfyx_yy = load_np_data("地表需水过程线", "三峰水库以下友谊", index_col = None, usecols = ("B:Q"))
zxs_sfyx_yy = load_np_data("地表需水过程线", "三峰水库以下友谊", index_col = False, usecols = [17])
dx_xs_sfyx_yy = load_np_data("地下水需水", "三峰水库以下友谊", index_col = None, usecols = ("B:Q"))
#25七星源水库以上岭东区
ls_qxyys_ld = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [26])
xs_qxyys_ld = load_np_data("地表需水过程线", "七星源水库以上岭东", index_col = None, usecols = ("B:Q"))
zxs_qxyys_ld = load_np_data("地表需水过程线", "七星源水库以上岭东", index_col = False, usecols = [17])
dx_xs_qxyys_ld = load_np_data("地下水需水", "七星源水库以上岭东", index_col = None, usecols = ("B:Q"))
#26七星源水库以上宝山区
ls_qxyys_bs = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [27])
xs_qxyys_bs = load_np_data("地表需水过程线", "七星源水库以上宝山", index_col = None, usecols = ("B:Q"))
zxs_qxyys_bs = load_np_data("地表需水过程线", "七星源水库以上宝山", index_col = False, usecols = [17])
dx_xs_qxyys_bs = load_np_data("地下水需水", "七星源水库以上宝山", index_col = None, usecols = ("B:Q"))
#27七星源水库以上宝清县
ls_qxyys_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [28])
xs_qxyys_bq = load_np_data("地表需水过程线", "七星源水库以上宝清", index_col = None, usecols = ("B:Q"))
zxs_qxyys_bq = load_np_data("地表需水过程线", "七星源水库以上宝清", index_col = False, usecols = [17])
dx_xs_qxyys_bq = load_np_data("地下水需水", "七星源水库以上宝清", index_col = None, usecols = ("B:Q"))
#28七星源水库以上友谊县
ls_qxyys_yy = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [29])
xs_qxyys_yy = load_np_data("地表需水过程线", "七星源水库以上友谊", index_col = None, usecols = ("B:Q"))
zxs_qxyys_yy = load_np_data("地表需水过程线", "七星源水库以上友谊", index_col = False, usecols = [17])
dx_xs_qxyys_yy = load_np_data("地下水需水", "七星源水库以上友谊", index_col = None, usecols = ("B:Q"))
#29七星源水库以下宝清县
ls_qxyyx_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [30])
xs_qxyyx_bq = load_np_data("地表需水过程线", "七星源水库以下宝清", index_col = None, usecols = ("B:Q"))
zxs_qxyyx_bq = load_np_data("地表需水过程线", "七星源水库以下宝清", index_col = False, usecols = [17])
dx_xs_qxyyx_bq = load_np_data("地下水需水", "七星源水库以下宝清", index_col = None, usecols = ("B:Q"))
#30七星源水库以下友谊县
ls_qxyyx_yy = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [31])
xs_qxyyx_yy = load_np_data("地表需水过程线", "七星源水库以下友谊", index_col = None, usecols = ("B:Q"))
zxs_qxyyx_yy = load_np_data("地表需水过程线", "七星源水库以下友谊", index_col = False, usecols = [17])
dx_xs_qxyyx_yy = load_np_data("地下水需水", "七星源水库以下友谊", index_col = None, usecols = ("B:Q"))
#31龙头桥水库以下宝清县
ls_ltqyx_bq = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [32])
xs_ltqyx_bq = load_np_data("地表需水过程线", "龙头桥水库以下宝清", index_col = None, usecols = ("B:Q"))
zxs_ltqyx_bq = load_np_data("地表需水过程线", "龙头桥水库以下宝清", index_col = False, usecols = [17])
dx_xs_ltqyx_bq = load_np_data("地下水需水", "龙头桥水库以下宝清", index_col = None, usecols = ("B:Q"))
#32龙头桥水库以下饶河县
ls_ltqyx_rh = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [33])
xs_ltqyx_rh = load_np_data("地表需水过程线", "龙头桥水库以下饶河", index_col = None, usecols = ("B:Q"))
zxs_ltqyx_rh = load_np_data("地表需水过程线", "龙头桥水库以下饶河", index_col = False, usecols = [17])
dx_xs_ltqyx_rh = load_np_data("地下水需水", "龙头桥水库以下饶河", index_col = None, usecols = ("B:Q"))
#33挠力河饶河县
ls_nlh_rh = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [34])
xs_nlh_rh = load_np_data("地表需水过程线", "挠力河饶河", index_col = None, usecols = ("B:Q"))
zxs_nlh_rh = load_np_data("地表需水过程线", "挠力河饶河", index_col = False, usecols = [17])
dx_xs_nlh_rh = load_np_data("地下水需水", "挠力河饶河", index_col = None, usecols = ("B:Q"))
#34挠力河以下饶河县
ls_nlhyx_rh = load_np_data("地表需水过程线", "天然来水", index_col = False, usecols = [35])
xs_nlhyx_rh = load_np_data("地表需水过程线", "挠力河以下饶河", index_col = None, usecols = ("B:Q"))
zxs_nlhyx_rh = load_np_data("地表需水过程线", "挠力河以下饶河", index_col = False, usecols = [17])
dx_xs_nlhyx_rh = load_np_data("地下水需水", "挠力河以下饶河", index_col = None, usecols = ("B:Q"))

#1笔架山水库
bjsk1 = load_pd_data("水库需水", "笔架山水库", index_col = None, usecols = None)
xs_bjsk = load_np_data("水库需水", "笔架山水库", index_col = None, usecols = ("C:R"))
bjsk = load_pd_data("水库特征曲线", "笔架山水库", index_col = False, usecols = None)
bjsk = bjsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_bjsk, Vxx_bjsk, Vdead_bjsk = 2799.00, 2107.00, 202.00   #汛限和正常蓄水位对应的库容，计算最大库容时不需要再加死库容
V0_bjsk=Vx_bjsk
m_bjsk=bjsk['面积']
v_bjsk=bjsk['库容']
zxs_bjsk=bjsk1['需水']

# bk: 年、月索引，只需读取一次。
y=bjsk1['月']
n=bjsk1['年']

#2寒葱沟水库
hcgsk1 = load_pd_data("水库需水", "寒葱沟水库", index_col = None, usecols = None)
xs_hcgsk = load_np_data("水库需水", "寒葱沟水库", index_col = None, usecols = ("C:R"))
hcgsk = load_pd_data("水库特征曲线", "寒葱沟水库", index_col = False, usecols = None)
hcgsk = hcgsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_hcgsk, Vxx_hcgsk, Vdead_hcgsk = 7667.00, 7049.00, 80.00
V0_hcgsk=Vx_hcgsk
# y=hcgsk1['月']
# n=hcgsk1['年']
m_hcgsk=hcgsk['面积']
v_hcgsk=hcgsk['库容']
zxs_hcgsk=hcgsk1['需水']
#3龙头桥水库
ltqsk1 = load_pd_data("水库需水", "龙头桥水库", index_col = None, usecols = None)
xs_ltqsk = load_np_data("水库需水", "龙头桥水库", index_col = None, usecols = ("C:R"))
ltqsk = load_pd_data("水库特征曲线", "龙头桥水库", index_col = False, usecols = None)
ltqsk = ltqsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_ltqsk, Vxx_ltqsk, Vdead_ltqsk = 32500.00, 29930.00, 2552.00
V0_ltqsk=Vx_ltqsk
# y=ltqsk1['月']
# n=ltqsk1['年']
m_ltqsk=ltqsk['面积']
v_ltqsk=ltqsk['库容']
zxs_ltqsk=ltqsk1['需水']
#4大索伦水库
dslsk1 = load_pd_data("水库需水", "大索伦水库", index_col = None, usecols = None)
xs_dslsk = load_np_data("水库需水", "大索伦水库", index_col = None, usecols = ("C:R"))
dslsk = load_pd_data("水库特征曲线", "大索伦水库", index_col = False, usecols = None)
dslsk = dslsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_dslsk, Vxx_dslsk, Vdead_dslsk = 800.00, 800.00, 170.00
V0_dslsk=Vx_dslsk
# y=dslsk1['月']
# n=dslsk1['年']
m_dslsk=dslsk['面积']
v_dslsk=dslsk['库容']
zxs_dslsk=dslsk1['需水']

#5蛤蟆通水库
hmtsk1 = load_pd_data("水库需水", "蛤蟆通水库", index_col = None, usecols = None)
xs_hmtsk = load_np_data("水库需水", "蛤蟆通水库", index_col = None, usecols = ("C:R"))
hmtsk = load_pd_data("水库特征曲线", "蛤蟆通水库", index_col = False, usecols = None)
hmtsk = hmtsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_hmtsk, Vxx_hmtsk, Vdead_hmtsk = 10223.00, 7670.00, 2550.00
V0_hmtsk=Vx_hmtsk
# y=hmtsk1['月']
# n=hmtsk1['年']
m_hmtsk=hmtsk['面积']
v_hmtsk=hmtsk['库容']
zxs_hmtsk=hmtsk1['需水']
#6清河水库
qhsk1 = load_pd_data("水库需水", "清河水库", index_col = None, usecols = None)
xs_qhsk = load_np_data("水库需水", "清河水库", index_col = None, usecols = ("C:R"))
qhsk = load_pd_data("水库特征曲线", "清河水库", index_col = False, usecols = None)
qhsk = qhsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_qhsk, Vxx_qhsk, Vdead_qhsk = 1150.00, 1150.00, 100.00
V0_qhsk=Vx_hmtsk
# y=qhsk1['月']
# n=qhsk1['年']
m_qhsk=qhsk['面积']
v_qhsk=qhsk['库容']
zxs_qhsk=qhsk1['需水']
#7徕凤湖水库
lfhsk1 = load_pd_data("水库需水", "徕凤湖水库", index_col = None, usecols = None)
xs_lfhsk = load_np_data("水库需水", "徕凤湖水库", index_col = None, usecols = ("C:R"))
lfhsk = load_pd_data("水库特征曲线", "徕凤湖水库", index_col = False, usecols = None)
lfhsk = lfhsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_lfhsk, Vxx_lfhsk, Vdead_lfhsk = 5100.00, 5100.00, 200.00
V0_lfhsk=Vx_lfhsk
# y=lfhsk1['月']
# n=lfhsk1['年']
m_lfhsk=lfhsk['面积']
v_lfhsk=lfhsk['库容']
zxs_lfhsk=lfhsk1['需水']
#8大叶沟水库
dygsk1 = load_pd_data("水库需水", "大叶沟水库", index_col = None, usecols = None)
xs_dygsk = load_np_data("水库需水", "大叶沟水库", index_col = None, usecols = ("C:R"))
dygsk = load_pd_data("水库特征曲线", "大叶沟水库", index_col = False, usecols = None)
dygsk = dygsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_dygsk, Vxx_dygsk, Vdead_dygsk = 2800.00, 2800.00, 230.00
V0_dygsk=Vx_hmtsk
# y=dygsk1['月']
# n=dygsk1['年']
m_dygsk=dygsk['面积']
v_dygsk=dygsk['库容']
zxs_dygsk=dygsk1['需水']
#9三峰水库
sfsk1 = load_pd_data("水库需水", "三峰水库", index_col = None, usecols = None)
xs_sfsk = load_np_data("水库需水", "三峰水库", index_col = None, usecols = ("C:R"))
sfsk = load_pd_data("水库特征曲线", "三峰水库", index_col = False, usecols = None)
sfsk = sfsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_sfsk, Vxx_sfsk, Vdead_sfsk = 1224.00, 1224.00, 230.00
V0_sfsk=Vx_sfsk
# y=sfsk1['月']
# n=sfsk1['年']
m_sfsk=sfsk['面积']
v_sfsk=sfsk['库容']
zxs_sfsk=sfsk1['需水']
#10七星源水库
qxysk1 = load_pd_data("水库需水", "七星源水库", index_col = None, usecols = None)
xs_qxysk = load_np_data("水库需水", "七星源水库", index_col = None, usecols = ("C:R"))
qxysk = load_pd_data("水库特征曲线", "七星源水库", index_col = False, usecols = None)
qxysk = hmtsk.fillna(0)#将缺失值填充为0
#df2=pd.DataFrame()
Vx_qxysk, Vxx_qxysk, Vdead_qxysk = 6500.00, 6500.00, 230.00
V0_qxysk=Vx_qxysk
# y=qxysk1['月']
# n=qxysk1['年']
m_qxysk=qxysk['面积']
v_qxysk=qxysk['库容']
zxs_qxysk=qxysk1['需水']
#水库蒸发和渗漏
skzf = load_pd_data("水库特征曲线", "蒸发", index_col = False, usecols = None)
zf_bjssk=skzf['笔架山水库']
zf_hcgsk=skzf['寒葱沟水库']
zf_ltqsk=skzf['龙头桥水库']
zf_dslsk=skzf['大索伦水库']
zf_hmtsk=skzf['蛤蟆通水库']
zf_qhsk=skzf['清河水库']
zf_sfsk=skzf['三峰水库']
zf_lfhsk=skzf['徕凤湖水库']
zf_dygsk=skzf['大叶沟水库']
zf_qxysk=skzf['七星源水库']
sksl = load_pd_data("水库特征曲线", "渗漏", index_col = False, usecols = None)
sl_bjssk=sksl['笔架山水库']
sl_hcgsk=sksl['寒葱沟水库']
sl_ltqsk=sksl['龙头桥水库']
sl_dslsk=sksl['大索伦水库']
sl_hmtsk=sksl['蛤蟆通水库']
sl_qhsk=sksl['清河水库']
sl_sfsk=sksl['三峰水库']
sl_lfhsk=sksl['徕凤湖水库']
sl_dygsk=sksl['大叶沟水库']
sl_qxysk=sksl['七星源水库']

#灌区数据输入
dxslyxs0 = load_pd_data("灌区和湿地", "地下水利用系数", index_col = None, usecols = [2])
#星火灌区
xs_xhgq0 = load_pd_data("灌区和湿地", "灌区", index_col = False, usecols = [2])
wd_xhgq0 = load_pd_data("灌区和湿地", "灌区", index_col = None, usecols = [17])
dx_xhgq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [2])
xs_xhgq=np.array(xs_xhgq0)
wd_xhgq= np.array(wd_xhgq0)
#集安灌区
xs_jagq0 = load_pd_data("灌区和湿地", "灌区", index_col = False, usecols = [3])
wd_jagq0 = load_pd_data("灌区和湿地", "灌区", index_col = None, usecols = [18])
dx_jagq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [3])
xs_jagq=np.array(xs_jagq0)
wd_jagq= np.array(wd_jagq0)
#集贤灌区1-集贤
xs_jxgq11 = load_pd_data("灌区和湿地", "灌区", index_col = False, usecols = [4])
wd_jxgq11 = load_pd_data("灌区和湿地", "灌区", index_col = None, usecols = [19])
dx_jxgq1 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [4])
xs_jxgq1=np.array(xs_jxgq11)
wd_jxgq1= np.array(wd_jxgq11)
dxslyxs=np.array(dxslyxs0)
#新河宫灌区1
xs_xhggq1 = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [5])
wd_xhggq1 = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [20])
dx_xhggq1 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [5])
#江川灌区
xs_jcgq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [6])
wd_jcgq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [21])
dx_jcgq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [6])
#五九七灌区
xs_597gq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [7])
wd_597gq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [22])
dx_597gq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [7])
#集贤灌区2
xs_jxgq2 = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [8])
wd_jxgq2 = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [23])
dx_jxgq2 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [8])
#二九一灌区
xs_291gq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [9])
wd_291gq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [24])
dx_291gq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [9])
#新河宫灌区2
xs_xhggq2 = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [10])
wd_xhggq2 = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [25])
dx_xhggq2 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [10])
#蛤蟆通灌区
xs_hmtgq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [11])
wd_hmtgq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [26])
dx_hmtgq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [11])
#七里沁灌区
xs_qlqgq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [12])
wd_qlqgq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [27])
dx_qlqgq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [12])
#八五三灌区
xs_853gq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [13])
wd_853gq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [28])
dx_853gq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [13])
#友谊灌区
xs_yygq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [14])
wd_yygq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [29])
dx_yygq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [14])
#龙头桥灌区
xs_ltqgq = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [15])
wd_ltqgq = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [30])
dx_ltqgq = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [15])

#饶河灌区1
xs_rhgq1 = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [32])
wd_rhgq1 = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [34])
dx_rhgq1 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [17])
#饶河灌区2
xs_rhgq2 = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [16])
wd_rhgq2 = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [31])
dx_rhgq2 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [16])
#饶河灌区3
xs_rhgq3 = load_np_data("灌区和湿地", "灌区", index_col = False, usecols = [33])
wd_rhgq3 = load_np_data("灌区和湿地", "灌区", index_col = None, usecols = [35])
dx_rhgq3 = load_np_data("灌区和湿地", "灌区地下", index_col = None, usecols = [18])
#自然保护区数据输入
#安邦河自然保护区
xs_abhsd = load_np_data("灌区和湿地", "安邦河自然保护区", index_col = False, usecols = [17])
xs16_abhsd = load_np_data("灌区和湿地", "安邦河自然保护区", index_col = False, usecols = ("C:R"))
KB = load_np_data("灌区和湿地", "安邦河自然保护区", index_col = False, usecols = [16])
# bk: 这个非常特殊。后面还反复用到。但这个数据里面都是0。
# KB:  空白 ?
KB0=pd.DataFrame(KB)
#挠力河自然保护区	富锦市饶河县
xs_nlhsd = load_np_data("灌区和湿地", "挠力河自然保护区", index_col = False, usecols = [17])
xs16_nlhsd = load_np_data("灌区和湿地", "挠力河自然保护区", index_col = False, usecols = ("C:R"))
#七星河自然保护区	19642	宝清县
xs_qxhsd = load_np_data("灌区和湿地", "七星河自然保护区", index_col = False, usecols = [17])
xs16_qxhsd = load_np_data("灌区和湿地", "七星河自然保护区", index_col = False, usecols = ("C:R"))
#东升自然保护区	19642	宝清县
xs_dshsd = load_np_data("灌区和湿地", "东升自然保护区", index_col = False, usecols = [17])
xs16_dshsd = load_np_data("灌区和湿地", "东升自然保护区", index_col = False, usecols = ("C:R"))
#友谊自然保护区	3182	友谊县
xs_yysd = load_np_data("灌区和湿地", "友谊自然保护区", index_col = False, usecols = [17])
xs16_yysd = load_np_data("灌区和湿地", "友谊自然保护区", index_col = False, usecols = ("C:R"))

#引松入双数据输入
ysrs_jx0 = load_pd_data("引松入双", "引松入双-集贤", index_col = None, usecols = ("C:R"))
ysrs_js0 = load_pd_data("引松入双", "引松入双-尖山", index_col = None, usecols = ("C:R"))
ysrs_ld0 = load_pd_data("引松入双", "引松入双-岭东", index_col = None, usecols = ("C:R"))
ysrs_jx= np.array(ysrs_jx0)
ysrs_js= np.array(ysrs_js0)
ysrs_ld= np.array(ysrs_ld0)

#疏干水数据输入
sgs_jx0 = load_pd_data("引松入双", "疏干水-集贤", index_col = None, usecols = ("C:R"))
sgs_ld0 = load_pd_data("引松入双", "疏干水-岭东", index_col = None, usecols = ("C:R"))
sgs_sft0 = load_pd_data("引松入双", "疏干水-四方台", index_col = None, usecols = ("C:R"))
sgs_jx= np.array(sgs_jx0)
sgs_ld= np.array(sgs_ld0)
sgs_sft= np.array(sgs_sft0)
sgs_dyg_bs0 = load_pd_data("引松入双", "疏干水-大叶沟以下宝山区", index_col = None, usecols = ("C:R"))
sgs_qxy_bs0 = load_pd_data("引松入双", "疏干水-七星源以上宝山区", index_col = None, usecols = ("C:R"))
sgs_bq0 = load_pd_data("引松入双", "疏干水-龙头桥以下宝清县", index_col = None, usecols = ("C:R"))
sgs_dyg_bs= np.array(sgs_dyg_bs0)
sgs_qxy_bs= np.array(sgs_qxy_bs0)
sgs_bq= np.array(sgs_bq0)
zs_bq0 = load_pd_data("引松入双", "中水-龙头桥以下宝清县", index_col = None, usecols = ("C:R"))
zs_bq= np.array(zs_bq0)

#农业破坏系数
nyphxs = load_np_data("破坏系数", "农业破坏系数", index_col = None, usecols = ("C:AJ"))
ss_bjsys_jx = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [2])
ss_bjsyx_jx = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [3])
ss_hcgys_ld = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [4])
ss_hcgyx_ld = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [5])
ss_hcgyx_js = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [6])
ss_hcgyx_sft = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [7])
ss_hcgyx_jx = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [8])
ss_ltqys_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [9])
ss_ltqyx_js = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [10])
ss_ltqyx_sft = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [11])
ss_ltqyx_jx = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [12])
ss_lfhys_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [13])
ss_lfhyx_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [14])
ss_dslys_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [15])
ss_dslyx_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [16])
ss_hmtys_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [17])
ss_hmtyx_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [18])
ss_qhys_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [19])
ss_qhyx_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [20])
ss_dygys_ld = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [21])
ss_dygys_bs = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [22])
ss_dygyx_bs = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [23])
ss_sfys_yy = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [24])
ss_sfyx_yy = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [25])
ss_qxyys_ld = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [26])
ss_qxyys_bs = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [27])
ss_qxyys_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [28])
ss_qxyys_yy = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [29])
ss_qxyyx_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [30])
ss_qxyyx_yy = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [31])
ss_ltqyx_bq = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [32])
ss_ltqyx_rh = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [33])
ss_nlh_rh = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [34])
ss_nlhyx_rh = load_np_data("破坏系数", "农业破坏系数1", index_col = False, usecols = [35])

sx_xhgq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [2])
sx_jagq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [3])
sx_jxgq1 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [4])
sx_xhgq1 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [5])
sx_jcgq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [6])
sx_jxgq2 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [7])
sx_291gq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [8])
sx_xhgq2 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [9])
sx_hmtgq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [10])
sx_853gq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [11])
sx_qlqgq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [12])
sx_yygq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [13])
sx_597gq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [14])
sx_ltqgq = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [15])
sx_rhgq1 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [16])
sx_rhgq2 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [17])
sx_rhgq3 = load_np_data("破坏系数", "农业破坏系数2", index_col = False, usecols = [18])
#回归水系数
#地表水回归

# dbhgsxs1=0.8
# dbhgsxs2=0.0
# dbhgsxs3=0.0
# dbhgsxs4=0.8
# dbhgsxs5=0.6
# dbhgsxs6=0.6
# dbhgsxs7=0.6
# dbhgsxs8=0.0
# dbhgsxs9=0.2
# dbhgsxs10=0.0
# dbhgsxs11=0.0
# dbhgsxs12=0.0
# dbhgsxs13=0.0
# dbhgsxs14=0.0
# dbhgsxs15=0.0
# dbhgsxs16=0.0
#
# #地下水回归
# dxhgsxs1=0.8
# dxhgsxs2=0.0
# dxhgsxs3=0.0
# dxhgsxs4=0.8
# dxhgsxs5=0.6
# dxhgsxs6=0.6
# dxhgsxs7=0.6
# dxhgsxs8=0.0
# dxhgsxs9=0.2
# dxhgsxs10=0.0
# dxhgsxs11=0.0
# dxhgsxs12=0.0
# dxhgsxs13=0.0
# dxhgsxs14=0.0
# dxhgsxs15=0.0
# dxhgsxs16=0.0
