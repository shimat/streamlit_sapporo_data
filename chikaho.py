import streamlit as st
import pandas as pd
import requests
from my_decoder import MyDecoder

@st.cache
def load_data():
    response = requests.get("https://ckan.pf-sapporo.jp/api/action/datastore_search?resource_id=5678d107-d9a4-4f81-8f57-092aac11db5e&limit=100", verify=False)
    response_json = MyDecoder().decode(response.text)
    df = pd.json_normalize(response_json, record_path=["result", "records"])
    return df


df = load_data().copy()
#"""
df_pt = df[df['アレイ'].isin(['J1'])].set_index('日時')[['大通り→札幌', '札幌→大通り']]
print(df_pt)
st.write(df_pt)
st.line_chart(df_pt)
#"""

"""
import streamlit.components.v1 as components
from pivottablejs import pivot_ui

#df_pt = df.pivot_table(index=['日時', 'アレイ'], columns=['大通り→札幌', '札幌→大通り'], values='合計')
df.drop(columns=["_id", "補正"], inplace=True)
df_pt = df.set_index(['日時', 'アレイ']).unstack(['アレイ'])
print(df_pt)
st.write(df_pt)
r = pivot_ui(df)
with open(r.src, encoding="utf-8") as t:
    components.html(t.read(), width=800, height=600, scrolling=True)
"""