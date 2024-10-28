
import pickle as cpickle
from pathlib import Path
import os
import pandas as pd
import numpy as np

# DATA_PATH = Path("./data_base")
CACHE_PATH = Path("./xx_pkl")

"""
所有涉及文件路径处理，修改为使用 pathlib 模块。
参考： https://www.osgeo.cn/python-tutorial/file-pathlib.html
及相关资料。

    from pathlib import Path

对于原始XLSX与其对应的Pickle文件，涉及更新的问题。
添加文件修改时间判断，若原始文件有更新，则生成新的Pickle文件。
"""


# 判断exl文件的修改时间，是否有更新
def check_exl_time(exl_name, pkl_name):
    exl_path = Path(exl_name)
    pkl_path = Path(pkl_name)

    # 获取文件最后修改时间
    e_last_modified_time = os.path.getmtime(exl_path)

    p_last_modified_time = os.path.getmtime(pkl_path)

    if e_last_modified_time > p_last_modified_time:
        # exl有更新，需要更新pkl文件
        return True
    else:
        return False


# todo 别ctrl+alt+L 调整代码格式，np.array(pd.read_excel( 就会变成两行，然后运行映射代码出错


# 保存get_data1的文件
def cache_pd_data(exl_file, tmp_file, sname, index_col=False, usecols=None):
    # 如果index_col=None 就是不传递index_col参数

    if index_col:

        data = pd.read_excel(
            exl_file, sheet_name=sname, index_col=index_col, usecols=usecols
        )
        # data = pd.read_excel(
        #     exl_file, sheet_name=sname, index_col=index_col, usecols=usecols
        # )
    else:
        data = pd.read_excel(exl_file, sname, usecols=usecols)

        # data = pd.read_excel(exl_file, sheet_name=sname, usecols=usecols)
        # data = pd.read_excel(exl_file, sheet_name=sname, usecols=usecols)

    cpickle.dump(data, open(tmp_file, "wb"))
    # cpickle.dump(data, open(tmp_file, "wb"))

    return data


def load_pd_data(f_path,fenqu_name,fname, sname, index_col=False, usecols=None ):

    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)
    tmp_file = CACHE_PATH / f"xx_get_data1_{fenqu_name}_{fname}_{index_col}_{usecols}.pkl"

    exl_file = Path(f'{f_path}/{fname}.xlsx')
    # exl_file = Path(fname)
    # exl_file = DATA_PATH / f"{fname}.xlsx"

    if tmp_file.exists():
        # 如果文件已存在，判断exl文件是否有更新，如果更新了就再修改一遍pkl文件
        if check_exl_time(exl_file, tmp_file):
            data = cache_pd_data(
                exl_file, tmp_file, sname, index_col=index_col, usecols=usecols
            )

        else:
            # exl文件没有更新，就直接获取文件数据
            data = cpickle.load(open(tmp_file, "rb"))
    else:
        data = cache_pd_data(
            exl_file, tmp_file, sname, index_col=index_col, usecols=usecols
        )

    return data





# 保存get_data2的文件
def cache_np_data(exl_file, tmp_file, sname, index_col=False, usecols=None):
    # 如果index_col=None 就是不传递index_col参数
    if index_col:
        data = np.array(
            pd.read_excel(
                exl_file, sheet_name=sname, index_col=index_col, usecols=usecols
            )
        )

    else:
        data = np.array(pd.read_excel(exl_file, sheet_name=sname, usecols=usecols))

    cpickle.dump(data, open(tmp_file, "wb"))


def load_np_data(f_path,fenqu_name,fname, sname, index_col=False, usecols=None ):
    # fpath = DATA_PATH

    tmp_file = CACHE_PATH / f"xx_get_data1_{fenqu_name}_{fname}_{index_col}_{usecols}.pkl"

    # exl_file = Path(f"{fpath}/{fname}.xlsx")
    # 调用的文件路径改为参数
    exl_file = Path(f'{f_path}/{fname}.xlsx')

    if tmp_file.exists():
        # 如果文件已存在，判断exl文件是否有更新，如果更新了就再修改一遍pkl文件
        if check_exl_time(exl_file, tmp_file):
            data = cache_np_data(
                exl_file, tmp_file, sname, index_col=index_col, usecols=usecols
            )

        else:
            # exl文件没有更新，就直接获取文件数据
            data = cpickle.load(open(tmp_file, "rb"))
    else:
        data = cache_np_data(
            exl_file, tmp_file, sname, index_col=index_col, usecols=usecols
        )

    return data



# ls_ltqyx_rh=np.array(pd.read_excel(file_path + '地表需水过程线.xlsx', sheet_name='天然来水',index_col=False,usecols=[33]))
# ls_ltqyx_rh = get_data2("地表需水过程线", "天然来水", index_col = False, usecols = [33])

def tester2():

    xlsx_file = Path('../data_base/水库需水.xlsx')
    if xlsx_file.exists():
        pass
    else:
        print('No file')
    sname = '笔架山水库'
    usecols = None
    data = pd.read_excel(xlsx_file, sheet_name=sname, usecols=usecols)
    # return data
    print(data)


def save_frame(data, sig):
    with pd.ExcelWriter(f'{sig}.xlsx') as writer:
        data.to_excel(writer, sheet_name='sheet')


def get_nxt_with_return(df):

    # 年
    g_year = df.iloc[:, 0]
    # 旬
    g_xun = df.iloc[:, 1]
    # 天
    g_day = df.iloc[:, 2]

    return g_year, g_xun, g_day

if __name__ == '__main__':
    tester2()