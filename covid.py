import streamlit as st
import pandas as pd
import requests
from my_decoder import MyDecoder

@st.cache
def load_data():
    response = requests.get("https://ckan.pf-sapporo.jp/api/action/datastore_search?resource_id=b83606f6-3aa2-4e0c-8a1a-509dd36be2ae&limit=300", verify=False)
    #print(response.content.decode('unicode-escape'))
    response_json = MyDecoder().decode(response.text)
    df = pd.json_normalize(response_json, record_path=["result", "records"])
    df["日付"] = df["日付"].map(lambda x: re.search(r'\d{4}-\d{2}-\d{2}', x).group())
    return df


df = load_data().copy() \
        .set_index("日付") \
        .drop(columns="_id")

st.write(df)
st.line_chart(df)
