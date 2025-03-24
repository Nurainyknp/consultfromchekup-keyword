import streamlit as st
import streamlit.components.v1 as components

# ✅ เปิด wide mode
st.set_page_config(page_title="Consult Keyword Generator", layout="wide")

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

# -------------------------------
# Header
# -------------------------------
st.markdown("<h2 style='color:#005B9A;'>📝 ระบบช่วยเขียนข้อความ consult</h2>", unsafe_allow_html=True)

# ===============================
# 🔘 Top Bar (Copy + Text + Clear)
# ===============================
with st.container():
    col1, col2, col3 = st.columns([2, 7, 2])

    with col1:
        components.html(
            f"""
            <button onclick="navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!');"
                    style="padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer; width:100%;">
                📋 คัดลอกข้อความ
            </button>
            """,
            height=60,
        )

    with col2:
        st.text_area("รวมคำ consult", value=combined_text, height=80)

    with col3:
        if st.button("🗑 ล้างข้อความ"):
            clear_keywords()

# ===============================
# 🔲 ฟังก์ชันสร้าง Card Box สำหรับหัวข้อ
# ===============================
def card_container(title):
    st.markdown(
        f"""
        <div style='background-color:#F3F6FA; padding:20px 25px; border-radius:12px; margin-top:25px; border-left:5px solid #0D47A1'>
            <h4 style='font-weight:bold; color:#0D47A1;'>{title}</h4>
        """,
        unsafe_allow_html=True,
    )

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# 🩺 หัวข้อ 1: Vital Signs & PE
# ===============================
card_container("1. ผล Vital signs และการตรวจร่างกาย")

with st.expander("คลิกเพื่อเลือกข้อมูล", expanded=False):
    col_vs, col_pe = st.columns(2)

    # ฝั่งซ้าย: Vital Signs
    with col_vs:
        st.markdown("**🔹 Vital signs**")
        st.button("BP สูง", on_click=lambda: add_keyword("Abnormal BP"))
        st.button("ชีพจรเร็ว", on_click=lambda: add_keyword("Abnormal Pulse"))
        st.button("ชีพจรช้า", on_click=lambda: add_keyword("Abnormal Pulse"))
        st.button("อุณหภูมิร่างกายผิดปกติ", on_click=lambda: add_keyword("Abnormal Temperature"))
        st.button("การหายใจผิดปกติ", on_click=lambda: add_keyword("Abnormal Respiration"))

    # ฝั่งขวา: PE
    with col_pe:
        st.markdown("**🔹 การตรวจร่างกาย (PE)**")
        pe_input = st.text_input("พิมพ์ผลตรวจร่างกาย", placeholder="พิมพ์ภาษาไทยหรืออังกฤษ")

        if st.button("➕ เพิ่ม PE"):
            if pe_input.strip():
                keyword_pe = f"Abnormal PE ({pe_input.strip()})"
                if keyword_pe not in st.session_state.selected_keywords:
                    st.session_state.selected_keywords.append(keyword_pe)

card_end()
