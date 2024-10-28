
import pandas as pd
import os
import shutil
from pathlib import Path
from slwork.add_code import *


g_year=None
g_xun=None
g_day=None
sk_name_list=[]

def file_exists(file_path):
    return os.path.exists(file_path)

def create_directory(directory):
    if os.path.exists(directory):
        # shutil.rmtree(directory)
        # print(f"'{directory}' 已删除。")
        # os.makedirs(directory)
        # print(f"'{directory}' 已创建。")
        pass
    else:
        os.makedirs(directory, exist_ok=True)
        print(f"'{directory}' 已创建。")


# 地级行政区
def create_folder_dj(df, folder_column, par_folder):
    if folder_column in df.columns:
        # 遍历每一行数据，创建对应的文件夹
        for folder_dj in df[folder_column].unique():
            if str(folder_dj) == 'nan':
                pass
            else:
                full_new_folder_path = os.path.join(par_folder, f'{folder_dj.strip()}')
                create_directory(full_new_folder_path)

    else:
        print(f"Column {folder_column} not found in the Excel")

# 四级区
def create_folder_sj(df, folder_column, par_column,xlsx_folder):
    if folder_column in df.columns:

        ii = 0
        for folder_sj in df[folder_column]:

            if str(folder_sj) == 'nan':
                pass
            else:
                par_folder = df.loc[ii, par_column].strip()
                sj_xlsx_folder = os.path.join(xlsx_folder, f'{str(par_folder)}')
                full_new_folder_path = os.path.join(sj_xlsx_folder.strip(), folder_sj.strip())
                create_directory(full_new_folder_path)

            ii = ii + 1

    else:
        print(f"Column {folder_column} not found in the Excel")

# 计算分区
def create_folder_js(df, folder_column, par_column,xlsx_folder):
    if folder_column in df.columns:

        ii = 0
        for folder_sj in df[folder_column]:

            if str(folder_sj) == 'nan':
                pass
            else:

                sec_folder = df.loc[ii, par_column]
                par_folder = df.loc[ii, '地级行政区']
                sj_xlsx_folder = os.path.join(xlsx_folder, f'{str(par_folder).strip()}', str(sec_folder).strip())

                full_new_folder_path = os.path.join(sj_xlsx_folder, folder_sj.strip())
                create_directory(full_new_folder_path)

            ii = ii + 1
    else:
        print(f"Column {folder_column} not found in the Excel")

# 遍历 path 文件夹，获取分区文件夹位置，判断文件夹的子文件夹里只有一个“输出”文件夹，或没有文件夹，则存为分区路径
# 但会有错误路径“输出”等文件夹，但没事会在使用的时候再次判断
def traverse_directory(path):
    save_folder_path = []
    for path in Path(path).rglob('*'):
        if path.is_dir() :
            # 获取所有子文件路径
            subfolders = list(path.iterdir())

            # 子文件中的文件夹计数
            sub_f_num=get_folder_num(subfolders)

            # 判断子文件夹中只有一个'输出'文件夹，或没有文件夹，就是需要获取的分区文件夹路径
            if (sub_f_num == 1 and subfolders[0].name == '输出') or (sub_f_num == 0):
                one_data = {
                    'name': path.name,
                    'path': path,
                }
                save_folder_path.append(one_data)
    return save_folder_path


# 遍历 folder_list 列表里的文件，返回文件夹个数
def get_folder_num(folder_list):
    folder_num=0
    for path in folder_list:
        if path.is_dir() :
            folder_num+=1
    return folder_num


# 1.创建分区文件夹
# 2.解析 计算分区径流分割系数.xlsx 文件，存成的文件路径为 data_base/xx_files
# 3.解析 计算分区径流分割系数.xlsx 文件，创建径流分割系数表、中小型水库打捆设计参数、创建回归水系数表
def create_fenqu_folder_jlxs_kr_hgxs(input_file_path,xlsx_folder_path):
    xlsx_folder=Path(xlsx_folder_path)
    input_file=Path(input_file_path)

    create_directory(xlsx_folder)

    df = pd.read_excel(input_file)

    create_folder_dj(df, '地级行政区', xlsx_folder)
    create_folder_sj(df, '四级区', '地级行政区',xlsx_folder)
    create_folder_js(df, '计算分区', '四级区',xlsx_folder)


    trans_excel_jlxs(input_file, '径流分割系数',df,xlsx_folder)  # 创建径流分割系数表
    trans_excel_kr(input_file, '中小型水库打捆设计参数',df,xlsx_folder)  # 创建库容表（中小型水库打捆设计参数）
    trans_excel_hgxs(input_file, '回归水系数',df,xlsx_folder)  # 创建回归水系数表


# 创建径流分割系数表
def trans_excel_jlxs(input_file, out_excel_name,df,xlsx_folder):
    '''径流分割系数表'''


    rows = df.shape[0]

    for ii in range(1, rows):
        xs = df.iloc[ii, 4]
        dj = df.iloc[ii, 0]
        sj = df.iloc[ii, 1]
        js = df.iloc[ii, 2]

        out_path = Path(xlsx_folder).joinpath(str(sj).strip()).joinpath(str(dj).strip()).joinpath(str(js).strip())

        np_to_exl(input_file, out_path,Path(f"{out_excel_name}.xlsx"),
                  [xs], cur_column=[df.columns[4]])

# 中小型水库打捆设计参数
def trans_excel_kr(input_file, out_excel_name,df,xlsx_folder):
    '''中小型水库打捆设计参数'''

    # data = pd.read_excel(input_file)

    rows = df.shape[0]

    for ii in range(1, rows):
        xl = df.iloc[ii, 5]
        xx = df.iloc[ii, 6]
        skr = df.iloc[ii, 7]

        dj = df.iloc[ii, 0]
        sj = df.iloc[ii, 1]
        js = df.iloc[ii, 2]


        out_path = Path(xlsx_folder).joinpath(str(sj).strip()).joinpath(str(dj).strip()).joinpath(str(js).strip())

        np_to_exl(input_file, out_path,Path(f"{out_excel_name}.xlsx"),
                  [[xl, xx, skr]], cur_column=[df.iloc[0, 5], df.iloc[0, 6], df.iloc[0, 7]])



def trans_excel_hgxs(input_file, out_excel_name,df,xlsx_folder):
    '''回归水系数'''

    # data = pd.read_excel(input_file)

    rows = df.shape[0]

    for i in range(1, rows):
        df_list = pd.DataFrame()
        dj = df.iloc[i, 0]
        sj = df.iloc[i, 1]
        js = df.iloc[i, 2]

        df_list = pd.concat([df_list, df.iloc[[i],
        [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]]],
                            axis=0,
                            ignore_index=True)
        df_list.columns = [df.iloc[0, 8], df.iloc[0, 9], df.iloc[0, 10], df.iloc[0, 11],
                           df.iloc[0, 12], df.iloc[0, 13], df.iloc[0, 14], df.iloc[0, 15],
                           df.iloc[0, 16], df.iloc[0, 17], df.iloc[0, 18], df.iloc[0, 19],
                           df.iloc[0, 20], df.iloc[0, 21], df.iloc[0, 22], df.iloc[0, 23],
                           df.iloc[0, 24]]

        # out_path = os.path.join(xlsx_folder, f'{str(sj).strip()}', str(dj).strip(), str(js).strip())
        out_path = Path(xlsx_folder).joinpath(str(sj).strip()).joinpath(str(dj).strip()).joinpath(str(js).strip())
        # out_file = Path(f"{out_path}/{out_excel_name}.xlsx")
        out_excel_file_one_file(df_list, Path(f"{out_excel_name}.xlsx"), out_path, input_file)




# 保存一个exl表
def out_excel_file_one_file(out_pd, out_file, save_folder_path,input_file):
        out_file_path = Path(save_folder_path).joinpath(out_file)
        is_file = file_exists(out_file_path)
        if is_file:
            is_update = check_exl_time(input_file, out_file_path)
            if is_update:
                with pd.ExcelWriter(out_file_path, engine='openpyxl',
                                    mode='w',  # 追加模式,不覆盖其他文件
                                    ) as writer:
                    out_pd.to_excel(writer, sheet_name='Sheet1', index=False)
                print(f"已更新'{out_file_path}'")
        else:
            with pd.ExcelWriter(out_file_path, engine='openpyxl',
                                mode='w',  # 追加模式,不覆盖其他文件
                                ) as writer:
                out_pd.to_excel(writer, sheet_name='Sheet1', index=False)
            print(f"已创建'{out_file_path}'")

# np转为pd，然后存为exl
def np_to_exl(input_file,save_folder_path, out_file, data, cur_column):
    new_df = pd.DataFrame(data, columns=cur_column)
    out_excel_file_one_file(new_df, out_file, save_folder_path, input_file)




def trans_excel_sr(input_file, out_excel_xs, out_excel_gs, out_excel_jc, out_excel_phxs, save_folder_path):
    '''sheet名:输入系列值。转换：基础数据，需水，地下水供水 '''

    data = pd.read_excel(Path(input_file), sheet_name="输入系列值")

    rows = data.shape[0]

    out_file_jc = Path(f"{out_excel_jc}.xlsx")
    out_file_xs = Path(f"{out_excel_xs}.xlsx")
    out_file_gs = Path(f"{out_excel_gs}.xlsx")
    out_file_phxs = Path(f"{out_excel_phxs}.xlsx")
    jc_list = []
    xs_list = []
    gs_list = []
    phxs_list = []
    for i in range(1, rows):
        # 转换4-7列，基础数据
        jc_list = chuli_col(3, 7, data, i, jc_list, 3, False)

        # 转换8-24列，需水
        xs_list = chuli_col(7, 24, data, i, xs_list, 3)

        # 转换25-41列，地下水供水
        gs_list = chuli_col(24, 41, data, i, gs_list, 3)

        # 转换42-44破坏系数
        phxs_list = chuli_col(41, 44, data, i, phxs_list, 3)

    out_same_exl(jc_list, out_file_jc, save_folder_path,input_file)
    out_same_exl(xs_list, out_file_xs, save_folder_path,input_file)
    out_same_exl(gs_list, out_file_gs, save_folder_path,input_file)
    out_same_exl(phxs_list, out_file_phxs, save_folder_path,input_file)


# 给所有分区创建一样的exl
def out_same_exl(out_list, out_file, save_folder_path,input_file):
    for item in save_folder_path:
        save_foler=item['path']
        df_all = pd.concat(out_list, ignore_index=True)
        out_excel_file_one_file(df_all,save_foler, out_file, input_file)


def chuli_col(start_col, end_col, data, i, data_list, start_col_num, is_iloc=True):
    col_arr = []
    col_name_arr = []
    for col_num in range(0, start_col_num):
        col_arr.append(col_num)
        col_name_arr.append(data.columns[col_num])
    for x in range(start_col, end_col):
        col_arr.append(x)
        if is_iloc:
            col_name_arr.append(data.iloc[0, x])
        else:
            col_name_arr.append(data.columns[x])
    df_list = pd.DataFrame()
    df_list = pd.concat([df_list, data.iloc[[i], col_arr]], axis=0, ignore_index=True)
    df_list.columns = col_name_arr
    data_list.append(df_list)
    return data_list

# 获取年旬天的pd，并初始化年旬天的全局变量
def get_nxt(fenqu_file_path, fenqu_name):

    global g_year
    if g_year is None:

        xushui_exl = load_pd_data(fenqu_file_path, fenqu_name, '需水', 'Sheet1', index_col=False, usecols=None)

        global g_xun
        global g_day

        g_year, g_xun, g_day=get_nxt_with_return(xushui_exl)



# 转换 径流系列.xlsx 生成‘本区径流.xlsx’
def trans_bqjl_excel(input_file, save_folder_path):

    df = pd.read_excel(input_file, sheet_name="Sheet1")

    for item in save_folder_path:
        # 条件筛选
        condition = (df.iloc[:, 2] == item['name']) & (df.iloc[:, 3] != '多年平均')
        # condition = (df.iloc[:, 2] == '克鲁伦河东方省') & (df.iloc[:, 3] != '多年平均')

        # 获取符合条件的行号
        row_indices = df.index[condition].tolist()

        a=df.loc[row_indices,:]
        # 截取列
        b=a.iloc[:,4:-1]

        all_num_list = []
        for index, row in b.iterrows():
            for i in row:
                all_num_list.append(i)
        c=np.array(all_num_list)
        c = c.reshape(c.shape[0], 1)
        new_df = pd.DataFrame(c)
        new_df = new_df.set_axis(['本区径流'], axis='columns')
        df_shuchu = pd.concat([g_year, g_xun, g_day, new_df], axis=1)  # 按列合并

        out_excel_file_one_file(df_shuchu,Path("本区径流.xlsx"),item['path'],input_file)


# 创建水库文件夹
def create_folder_sk(df, folder_column, par_folder):
    global sk_name_list
    for row in df[folder_column]:
        # 遍历每一行数据，创建对应的文件夹
        if str(row) != 'nan':
            full_new_folder_path =Path(par_folder).joinpath(row.strip())
            sk_name_list.append(row.strip())
            create_directory(full_new_folder_path)



# 第一种转换表 每一行按照水库名保存
def ter_sk_1(df,sheet_name,out_base_folder,input_file):
    for item  in sk_name_list:
        filter_row = df[(df['水库名称'] == item)]
        # 截取列
        b=filter_row.iloc[:,1:]
        c=np.array(b)
        # 有的水库没有数值
        if c.size!=0:
            new_df = pd.DataFrame(c.T)
            new_df = new_df.set_axis([sheet_name], axis='columns')

            out_path=Path(out_base_folder).joinpath(item)

            out_excel_file_one_file(new_df,f"{sheet_name}.xlsx",out_path,input_file)


# 第2种转换表 蒸发强度过程线 渗漏强度过程线
def ter_sk_2(start_col,end_col,df,sheet_name,out_base_folder,input_file):
    new_df=df.iloc[:, start_col:end_col]
    # 重置索引
    new_df = new_df.reset_index(drop=True)
    for item  in sk_name_list:
        filter_row = new_df[(new_df.iloc[:, 0] == item)]
        # # 截取列
        b=filter_row.iloc[:,1:]
        c=np.array(b)
        # 有的水库没有数值
        if c.size!=0:

            xun_np=data_yue_to_xun(c)
            data_df = pd.DataFrame(xun_np)
            data_df = data_df.set_axis([sheet_name], axis='columns')

            out_path=Path(out_base_folder).joinpath(item)

            out_excel_file_one_file(data_df,f"{sheet_name}.xlsx",out_path,input_file)



# 一列月的数据，每个月除以三，然后拼接成为3个数字，转换成为一列旬的数据
def data_yue_to_xun(yue_data_list):
    '''
    yue_data_list:12个月的数据列表
    '''
    xun_data_list=[]
    for one_data in yue_data_list[0]:
        new_xun_data=one_data/3
        for i in range(3):
            xun_data_list.append(new_xun_data)


    xun_data_list_np=np.array(xun_data_list)

    return xun_data_list_np


# 第3种转换表 水库特性
def ter_sk_3(start_col,end_col,df,sheet_name,out_base_folder,input_file):
    new_df=df.iloc[:, start_col:end_col]
    # 重置索引
    new_df = new_df.reset_index(drop=True)
    for item  in sk_name_list:
        filter_row = new_df[(new_df.iloc[:, 0] == item)]
        # # 截取列
        b=filter_row.iloc[:,1:]
        c=np.array(b)
        # 有的水库没有数值
        if c.size!=0:

            data_df = pd.DataFrame(c)
            data_df = data_df.set_axis(['死库容（万m3）',	'兴利库容（万m3）',
                                        '汛限水位（m）',	'汛限库容（万m3）'], axis='columns')

            out_path=Path(out_base_folder).joinpath(item)

            out_excel_file_one_file(data_df,f"{sheet_name}.xlsx",out_path,input_file)


