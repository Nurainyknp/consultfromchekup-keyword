import streamlit as st
import streamlit.components.v1 as components

# ใช้ session_state เก็บ keyword
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# เพิ่ม keyword
def add_keyword(keyword):
    if keyword not in st.session_state.selected_keywords:
        st.session_state.selected_keywords.append(keyword)

# ล้างข้อความ
def clear_keywords():
    st.session_state.selected_keywords = []

# 💬 แสดงข้อความรวม
combined_text = "; ".join(st.session_state.selected_keywords)

# 🔘 Layout 3 ส่วน
col1, col2, col3 = st.columns([2, 6, 1])

# 🔘 ปุ่ม HTML ที่คัดลอกจริงๆ
with col1:
    components.html(
        f"""
        <button onclick="navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!')" 
                style="padding:0.5em 1em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer;">
            📋 คัดลอกข้อความ
        </button>
        """,
        height=40,
    )

# ช่องแสดงข้อความ
with col2:
    st.text_area("รวมคำ consult", value=combined_text, height=80)

# ปุ่ม Clear
with col3:
    st.button("🗑 ล้างข้อความ", on_click=clear_keywords)

# 🔽 หัวข้อหลัก (Expander)
with st.expander("1. ผล Vital sign และการตรวจร่างกาย"):
    st.button("BP สูง", on_click=lambda: add_keyword("ความดันโลหิตสูง"))
    st.button("หัวใจเต้นเร็ว", on_click=lambda: add_keyword("หัวใจเต้นเร็วกว่าปกติ"))
    
with st.expander("2. สิ่งส่งตรวจห้องปฏิบัติการ"):
    st.button("LDL สูง", on_click=lambda: add_keyword("ภาวะไขมันในเลือดผิดปกติ (LDL)"))
    st.button("FBS สูง", on_click=lambda: add_keyword("ระดับน้ำตาลในเลือดสูง (FBS)"))
