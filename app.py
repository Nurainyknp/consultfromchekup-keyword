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

# ================================
# 🔘 ส่วนบน: ปุ่ม + ช่อง + ล้าง
# ================================
st.markdown("### 📝 ระบบช่วยเขียนข้อความ consult")

col1, col2, col3 = st.columns([2, 6, 2])

# ✅ ปุ่มคัดลอกข้อความ (HTML + JS)
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

# ✅ ช่องแสดงข้อความ
with col2:
    st.text_area("รวมคำ consult", value=combined_text, height=80)

# ✅ ปุ่มล้างข้อความ (HTML)
with col3:
    st.markdown(
        """
        <button onclick="window.location.reload();"
                style="padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#f44336; color:white; border:none; cursor:pointer;">
            🗑 ล้างข้อความ
        </button>
        """,
        unsafe_allow_html=True,
    )

# ================================
# 🔽 หัวข้อหลัก (Expander)
# ================================

with st.expander("1. ผล Vital sign และการตรวจร่างกาย"):
    col1, col2 = st.columns(2)
    with col1:
        st.button("BP สูง", on_click=lambda: add_keyword("ความดันโลหิตสูง"))
        st.button("HR เร็ว", on_click=lambda: add_keyword("หัวใจเต้นเร็ว")
        )
    with col2:
        st.button("BMI สูง", on_click=lambda: add_keyword("ภาวะน้ำหนักเกิน"))

with st.expander("2. สิ่งส่งตรวจห้องปฏิบัติการ"):
    col1, col2 = st.columns(2)
    with col1:
        st.button("LDL สูง", on_click=lambda: add_keyword("ภาวะไขมันในเลือดผิดปกติ (LDL)"))
        st.button("FBS สูง", on_click=lambda: add_keyword("ระดับน้ำตาลในเลือดสูง (FBS)"))
    with col2:
        st.button("HbA1c สูง", on_click=lambda: add_keyword("ภาวะเบาหวาน (HbA1c สูง)"))

