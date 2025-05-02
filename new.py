import pandas as pd
import streamlit as st
import random

# 讀取 CSV（Big5 編碼）
df = pd.read_csv("112迄今各里人口數按年齡分.csv", encoding="big5")

# 區分"區"與"里"
unique_areas = sorted(df[df["區域別"] != "總計"]["區域別"].unique().tolist())
districts = [area for area in unique_areas if area.endswith("區")]
villages = [area for area in unique_areas if not area.endswith("區")]

st.title("人口年齡分佈比較折線圖")

# 行政區選擇
st.header("請選擇要比較的行政區 (可多選，最多8個)")

selected_districts = st.multiselect("區", districts)
selected_villages = st.multiselect("里", villages)

selected_areas = selected_districts + selected_villages

if len(selected_areas) > 8:
    st.warning("最多只能選擇8個行政區！")
else:
    if selected_areas:
        st.subheader("人口年齡分佈比較圖表")

        # 準備年齡軸
        labels = []
        datasets = {}

        for area in selected_areas:
            area_data = df[(df["區域別"] == area) & (df["性別"] == "計")]

            if not area_data.empty:
                age_columns = [col for col in area_data.columns if "歲數量" in col or "100歲以上" in col]
                if not labels:
                    labels = [col.replace("歲數量", "").replace("100歲以上", "100+") for col in age_columns]

                population_data = area_data[age_columns].values.flatten().tolist()

                datasets[area] = population_data

        # 畫圖
        import plotly.graph_objects as go

        fig = go.Figure()

        for area, population in datasets.items():
            fig.add_trace(go.Scatter(
                x=labels,
                y=population,
                mode='lines',
                name=area,
                line=dict(width=2)
            ))

        fig.update_layout(
            title="行政區年齡分佈比較",
            xaxis_title="年齡",
            yaxis_title="人口數",
            width=800,
            height=500
        )

        st.plotly_chart(fig)

