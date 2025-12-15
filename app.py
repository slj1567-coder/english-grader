import streamlit as st
import google.generativeai as genai

# 設定頁面
st.set_page_config(page_title="無錫中考英語作文批改", page_icon="📝")
st.title("📝 無錫中考英語作文批改 App (線上版)")

# --- 從 Streamlit Secrets 讀取 API Key ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ 未配置 API Key，请在 Streamlit 后台设置 Secrets。")
    st.stop()

# --- 介面布局 ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_area("作文题目", height=100, placeholder="例如：My Dream")
with col2:
    essay_content = st.text_area("学生作文", height=300, placeholder="粘贴作文内容...")

if st.button("🚀 开始智能批改", type="primary"):
    if not essay_content:
        st.warning("请先粘贴作文！")
    else:
        status_box = st.empty()
        status_box.info("正在连接 AI 老师 (Gemini 2.0 Flash)...")
        
        try:
            # 指定 Gemini 2.0 Flash 模型
            model = genai.GenerativeModel("gemini-2.0-flash")
            
            prompt = f"""
            你是一位无锡初中英语教师。请批改以下作文。
            题目：{topic}
            内容：{essay_content}
            要求：给出得分(满分20)、中文点评、纠错、润色和范文。
            """
            
            response = model.generate_content(prompt)
            status_box.empty()
            # 新版 SDK 通常用 .text 或 .candidates[0].content.parts
            if hasattr(response, "text") and response.text:
                st.markdown(response.text)
            else:
                # 保底處理，避免物件格式變動時報錯
                st.write(response)
            
        except Exception as e:
            status_box.empty()
            st.error(f"发生错误: {e}")
