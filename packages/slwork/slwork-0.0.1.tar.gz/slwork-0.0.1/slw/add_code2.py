from slw_const import RESULT_PATH
import pandas as pd


def save_w_sheetname(data, sig,sheet_name):
    with pd.ExcelWriter(RESULT_PATH / f'{sig}.xlsx', encoding='utf-8') as writer:
        data.to_excel(writer, sheet_name=sheet_name)

def save_w_startcol(data, sig,sheet_name,startcol,startrow):
    with pd.ExcelWriter(RESULT_PATH / f'{sig}.xlsx', encoding='utf-8') as writer:
        data.to_excel(writer, sheet_name=sheet_name, startcol=startcol, startrow=startrow)



if __name__ == '__main__':
    data = {'姓名': ['数字', 'Nick', 'John', 'Alice'], 'Age': [28, 32, 25, 40],
            'City': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']}
    df = pd.DataFrame(data)
    save_w_sheetname(df,'xx_test','1')