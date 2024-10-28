from pathlib import Path


DATA_PATH = Path("./data_base")
RESULT_PATH = Path('./xx_result')
CACHE_PATH = Path("./xx_pkl")

for tpath in [RESULT_PATH, CACHE_PATH]:
    if tpath.exists():
        pass
    else:
        tpath.mkdir()

# 回归水系数
# 地表水回归
dbhgsxs1 = 0.8
dbhgsxs2 = 0.0
dbhgsxs3 = 0.0
dbhgsxs4 = 0.8
dbhgsxs5 = 0.6
dbhgsxs6 = 0.6
dbhgsxs7 = 0.6
dbhgsxs8 = 0.0
dbhgsxs9 = 0.2
dbhgsxs10 = 0.0
dbhgsxs11 = 0.0
dbhgsxs12 = 0.0
dbhgsxs13 = 0.0
dbhgsxs14 = 0.0
dbhgsxs15 = 0.0
dbhgsxs16 = 0.0

# 地下水回归
dxhgsxs1 = 0.8
dxhgsxs2 = 0.0
dxhgsxs3 = 0.0
dxhgsxs4 = 0.8
dxhgsxs5 = 0.6
dxhgsxs6 = 0.6
dxhgsxs7 = 0.6
dxhgsxs8 = 0.0
dxhgsxs9 = 0.2
dxhgsxs10 = 0.0
dxhgsxs11 = 0.0
dxhgsxs12 = 0.0
dxhgsxs13 = 0.0
dxhgsxs14 = 0.0
dxhgsxs15 = 0.0
dxhgsxs16 = 0.0

columns_arr = ['城镇生活', '农村生活', '牲畜', '三产', '火核电', '一般工业', '高耗水工业', '建筑业',
               '水田', '水浇地', '菜田', '林果地', '草场', '鱼塘', '城镇生态', '湿地']

BiaoTouHangYe = ['城镇生活', '农村生活', '牲畜', '三产',
                 '火核电', '一般工业', '高耗水工业', '建筑业',
                 '水田', '水浇地', '菜田', '林果地',
                 '草场', '鱼塘', '城镇生态', '湿地']

# Python 中 global 关键字可以定义一个变量为全局变量，但是这个仅限于在一个模块（py文件）中调用全局变量
# g_year = None
# g_xun = None
# g_day = None
#
