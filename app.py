import streamlit as st
import streamlit.components.v1 as components

# ✅ เปิด wide layout
st.set_page_config(layout="wide")

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

# รวมข้อความ
combined_text = "; ".join(st.session_state.selected_keywords)

# -------------------------------
# ส่วนบน: กล่องรวมข้อความ + ปุ่ม
# -------------------------------
with st.container():
    st.markdown("""
        <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; margin-bottom:20px;">
            <h3 style="margin-top:0;">📝 ระบบช่วยเขียนข้อความ consult</h3>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 6, 2])

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

    with col2:
        st.text_area("รวมคำ consult", value=combined_text, height=80)

    with col3:
        if st.button("🗑 ล้างข้อความ"):
            clear_keywords()

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# หัวข้อ 1: Vital Signs & PE
# -------------------------------
st.markdown("""
    <div style='background-color:#E0E0E0; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>
        1. ผล Vital signs และการตรวจร่างกาย
    </div>
""", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล", expanded=True):
    with st.container():
        col_vs, col_pe = st.columns(2)

        # 🔹 ฝั่งซ้าย: Vital Signs
        with col_vs:
            st.markdown("""
                <div style="background-color:#ffffff; border:1px solid #ddd; border-radius:8px; padding:10px;">
                <strong>🔹 Vital signs</strong><br><br>
            """, unsafe_allow_html=True)

            # ปุ่มแถวบนแนวนอน
            row1 = st.columns([1.2, 1.2, 1.1])
            with row1[0]:
                st.button("BP สูง", on_click=lambda: add_keyword("Abnormal BP"))
            with row1[1]:
                st.button("ชีพจรเร็ว", on_click=lambda: add_keyword("Abnormal Pulse"))
            with row1[2]:
                st.button("ชีพจรช้า", on_click=lambda: add_keyword("Abnormal Pulse"))

            # ปุ่มแถวล่างแนวนอน
            row2 = st.columns([1, 1])
            with row2[0]:
                st.button("อุณหภูมิร่างกายผิดปกติ", on_click=lambda: add_keyword("Abnormal Temperature"))
            with row2[1]:
                st.button("การหายใจผิดปกติ", on_click=lambda: add_keyword("Abnormal Respiration"))

            st.markdown("</div>", unsafe_allow_html=True)

        # 🔹 ฝั่งขวา: การตรวจร่างกาย (PE)
        with col_pe:
            st.markdown("""
                <div style="background-color:#ffffff; border:1px solid #ddd; border-radius:8px; padding:10px;">
                <strong>🔹 การตรวจร่างกาย (PE)</strong><br><br>
            """, unsafe_allow_html=True)

            pe_input = st.text_input("พิมพ์ผลตรวจร่างกาย", placeholder="พิมพ์ภาษาไทยหรืออังกฤษ")

            if st.button("➕ เพิ่ม PE"):
                if pe_input.strip():
                    keyword_pe = f"Abnormal PE ({pe_input.strip()})"
                    if keyword_pe not in st.session_state.selected_keywords:
                        st.session_state.selected_keywords.append(keyword_pe)

            st.markdown("</div>", unsafe_allow_html=True)
