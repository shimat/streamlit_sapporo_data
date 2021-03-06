import json
import re
import streamlit as st
import pandas as pd
import requests

class MyDecoder(json.JSONDecoder):
    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                if '.' in o:
                    return float(o)
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


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

st.title("札幌市内の新型コロナウイルス(COVID-19)陽性患者数")
st.write(df)
st.line_chart(df)

"(出典: DATA-SMART CITY SAPPORO https://data.pf-sapporo.jp/)"
