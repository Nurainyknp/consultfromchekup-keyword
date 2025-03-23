import streamlit as st

# ตัวแปร session สำหรับเก็บข้อความ
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# ฟังก์ชันเพิ่ม keyword
def add_keyword(keyword):
    if keyword not in st.session_state.selected_keywords:
        st.session_state.selected_keywords.append(keyword)

# ฟังก์ชันล้างข้อความ
def clear_keywords():
    st.session_state.selected_keywords = []

# 🔘 ปุ่ม Keyword Copy และ ช่องข้อความ + ปุ่ม Clear
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.button("📋 Keyword copy", on_click=lambda: st.toast("กด Ctrl+C เพื่อคัดลอก"))

with col2:
    st.text_area("รวมคำ consult", value="; ".join(st.session_state.selected_keywords), height=80)

with col3:
    st.button("🗑 Clear", on_click=clear_keywords)

# 🔽 หัวข้อหลัก (Expander)
with st.expander("1. ผล Vital sign และการตรวจร่างกาย"):
    st.button("BP สูง", on_click=lambda: add_keyword("ความดันโลหิตสูง"))
    st.button("หัวใจเต้นเร็ว", on_click=lambda: add_keyword("หัวใจเต้นเร็วกว่าปกติ"))
    
with st.expander("2. สิ่งส่งตรวจห้องปฏิบัติการ"):
    st.button("LDL สูง", on_click=lambda: add_keyword("ภาวะไขมันในเลือดผิดปกติ (LDL)"))
    st.button("FBS สูง", on_click=lambda: add_keyword("ระดับน้ำตาลในเลือดสูง (FBS)"))

with st.expander("3. การตรวจเครื่องมือต่าง ๆ"):

with st.expander("4. การตรวจสุขภาพทางอาชีวอนามัย"):

with st.expander("5. การตรวจอื่น ๆ"):

with st.expander("6. ประวัติสุขภาพ"):


    
