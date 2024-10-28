
import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path("./data_base")
exl_file = DATA_PATH / "水库特征曲线.xlsx"

#水库蒸发和渗漏
# skzf = load_pd_data("水库特征曲线", "蒸发", index_col = False, usecols = None)
skzf = pd.read_excel(
    exl_file, sheet_name='蒸发', index_col=False, usecols=None
)
zf_bjssk=skzf['笔架山水库']
zf_hcgsk=skzf['寒葱沟水库']


sksl =pd.read_excel(
    exl_file, sheet_name='渗漏', index_col=False, usecols=None
)
sl_bjssk=sksl['笔架山水库']
sl_hcgsk=sksl['寒葱沟水库']

hcgsk = pd.read_excel(
    exl_file, sheet_name='寒葱沟水库', index_col=False, usecols=None
)
hcgsk = hcgsk.fillna(0)#将缺失值填充为0
m_hcgsk=hcgsk['面积']
v_hcgsk=hcgsk['库容']