import json
import streamlit as st
import pandas as pd
import requests
import json

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
    response = requests.get("https://ckan.pf-sapporo.jp/api/action/datastore_search?resource_id=dcb6abdc-a73a-400d-abf0-82dffa5b5d40&limit=12", verify=False)
    response_json = MyDecoder().decode(response.text)
    df = pd.json_normalize(response_json, record_path=["result", "records"])
    df.set_index("月", inplace=True)
    df.drop(columns=["_id", "年"], inplace=True)
    return df

df = load_data().copy()

selected_targets = st.multiselect('select targets', sorted(df.columns))
view = df[selected_targets].copy()
st.line_chart(view)
