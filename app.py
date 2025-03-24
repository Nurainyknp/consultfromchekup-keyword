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

# 🔘 ปุ่ม "คัดลอกข้อความ" + ช่องข้อความ + ปุ่ม Clear
col1, col2, col3 = st.columns([1.5, 6, 1])
with col1:
    if st.button("📋 คัดลอกข้อความ"):
        # เรียก JavaScript สั่งคัดลอกไป clipboard
        components.html(
            f"""
            <script>
            navigator.clipboard.writeText("{combined_text}");
            alert("คัดลอกข้อความเรียบร้อยแล้ว!");
            </script>
            """,
            height=0,
        )

with col2:
    st.text_area("รวมคำ consult", value=combined_text, height=80)

with col3:
    st.button("🗑 ล้างข้อความ", on_click=clear_keywords)

# 🔽 ตัวอย่างหัวข้อ
with st.expander("1. ผล Vital sign และการตรวจร่างกาย"):
    st.button("BP สูง", on_click=lambda: add_keyword("ความดันโลหิตสูง"))
    st.button("HR เร็ว", on_click=lambda: add_keyword("หัวใจเต้นเร็ว"))
