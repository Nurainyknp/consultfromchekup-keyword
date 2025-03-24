import streamlit as st
import streamlit.components.v1 as components

# -------------------------------
# ใช้ session_state เก็บ keyword
# -------------------------------
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# เพิ่ม keyword
def add_keyword(keyword):
    if keyword not in st.session_state.selected_keywords:
        st.session_state.selected_keywords.append(keyword)

# ล้างข้อความ
def clear_keywords():
    st.session_state.selected_keywords = []

# -------------------------------
# แสดงข้อความรวม
# -------------------------------
combined_text = "; ".join(st.session_state.selected_keywords)

st.markdown("### 📝 ระบบช่วยเขียนข้อความ consult")

col1, col2, col3 = st.columns([2, 6, 2])

# 🔘 ปุ่มคัดลอกข้อความ
with col1:
    components.html(
        f"""
        <button onclick="navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!');"
                style="padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer;">
            📋 คัดลอกข้อความ
        </button>
        """,
        height=60,
    )

# 💬 กล่องแสดงข้อความรวม
with col2:
    st.text_area("รวมคำ consult", value=combined_text, height=80)

# 🗑 ปุ่มล้างข้อความ (ทำงานจริง)
with col3:
    if st.button("🗑 ล้างข้อความ"):
        clear_keywords()

# -------------------------------
# Header style function
# -------------------------------
def section_header(title):
    st.markdown(
        f"""
        <div style='background-color:#E0E0E0; padding:8px; border-radius:5px; font-weight:bold; font-size:18px; margin-top:20px;'>
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# หัวข้อ 1: Vital signs & PE
# -------------------------------
section_header("1. ผล Vital signs และการตรวจร่างกาย")

with st.expander("คลิกเพื่อเลือกข้อมูล"):
    col_vs, col_pe = st.columns(2)

    # ฝั่งซ้าย: Vital Signs
    with col_vs:
        st.markdown("**🔹 Vital signs**")
        st.button("BP สูง", on_click=lambda: add_keyword("Abnormal BP"))
        st.button("ชีพจรเร็ว", on_click=lambda: add_keyword("Abnormal Pulse"))
        st.button("ชีพจรช้า", on_click=lambda: add_keyword("Abnormal Pulse"))
        st.button("อุณหภูมิร่างกายผิดปกติ", on_click=lambda: add_keyword("Abnormal Temperature"))
        st.button("การหายใจผิดปกติ", on_click=lambda: add_keyword("Abnormal Respiration"))

    # ฝั่งขวา: การตรวจร่างกาย (PE)
    with col_pe:
        st.markdown("**🔹 การตรวจร่างกาย (PE)**")
        pe_input = st.text_input("พิมพ์ผลตรวจร่างกาย", placeholder="พิมพ์ภาษาไทยหรืออังกฤษ")

        if st.button("➕ เพิ่ม PE"):
            if pe_input.strip():
                keyword_pe = f"Abnormal PE ({pe_input.strip()})"
                if keyword_pe not in st.session_state.selected_keywords:
                    st.session_state.selected_keywords.append(keyword_pe)
