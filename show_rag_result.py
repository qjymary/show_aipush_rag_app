import streamlit as st
import pandas as pd

# 读取数据
@st.cache_data
def load_data(path):
    return pd.read_excel(path)

st.title("用户对话与RAG结果可视化")

# 上传或指定文件
uploaded_file = st.file_uploader("上传结果文件（xlsx）", type=["xlsx"])
if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.stop()

# remote_id筛选
remote_ids = df['remote_id'].unique()
selected_id = st.selectbox("选择remote_id", remote_ids)

user_df = df[df['remote_id'] == selected_id].sort_values(by='create_time')

st.subheader("对话详情")

for idx, row in user_df.iterrows():
    # 用户消息
    with st.chat_message("user"):
        st.markdown(f"**[{row['create_time']}] 用户：** {row['query']}")
        st.markdown(f"<span style='color:gray;font-size:12px;'>RAG召回：</span>", unsafe_allow_html=True)
        st.markdown(f"{row['召回结果']}", unsafe_allow_html=True)
    # 助手回复
    with st.chat_message("assistant"):
        st.markdown(f"<span style='color:gray;font-size:12px;'>**RAG回复：**</span>", unsafe_allow_html=True)
        st.write(row['messages提取'])
        st.markdown(f"<span style='color:gray;font-size:12px;'>**原始助手回复：**</span>", unsafe_allow_html=True)
        st.write(row['原始助手回复'])
        st.markdown(f"LLM输出")
        st.write(row['输出结果'])