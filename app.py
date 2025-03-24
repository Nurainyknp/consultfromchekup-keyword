import streamlit as st
import streamlit.components.v1 as components

# ===============================
# ✅ Wide layout + Theme session
# ===============================
st.set_page_config(layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# ===============================
# ✅ Theme toggle button (top right)
# ===============================
col_theme_left, col_theme_spacer, col_theme_right = st.columns([10, 1, 2])
with col_theme_right:
    selected = st.radio("โหมด", ["🌞 Light", "🌙 Night"], horizontal=True, label_visibility="collapsed")
    st.session_state.theme_mode = "dark" if "Night" in selected else "light"

# ===============================
# ✅ Custom CSS per theme
# ===============================
if st.session_state.theme_mode == "dark":
    custom_css = """
        <style>
            body, .block-container {
                background-color: #1e1e1e !important;
                color: white !important;
            }
            .stTextArea textarea, .stTextInput input {
                background-color: #2c2c2c !important;
                color: white !important;
            }
            .stButton > button {
                background-color: #444 !important;
                color: white !important;
            }
            .stRadio > div {
                color: white !important;
            }
        </style>
    """
else:
    custom_css = """
        <style>
            body, .block-container {
                background-color: white !important;
                color: black !important;
            }
        </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)

# ===============================
# ✅ Functions
# ===============================
def add_keyword(keyword):
    if keyword not in st.session_state.selected_keywords:
        st.session_state.selected_keywords.append(keyword)

def clear_keywords():
    st.session_state.selected_keywords = []

# ===============================
# ✅ Consult keyword box + buttons
# ===============================
combined_text = "; ".join(st.session_state.selected_keywords)

with st.container():
    bg_color = "#333" if st.session_state.theme_mode == "dark" else "#f0f2f6"
    st.markdown(f"""
        <div style="background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:20px;">
            <h3 style="margin-top:0;">📝 ระบบช่วยเขียนข้อความ consult</h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 6, 2])

    with col1:
        components.html(
            f"""
            <button onclick=\"navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!');\"
                    style=\"padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer;\">
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

# ===============================
# ✅ Section: Vital signs and PE
# ===============================
st.markdown(f"""
    <div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; 
                padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>
        1. ผล Vital signs และการตรวจร่างกาย
    </div>
""", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล", expanded=True):
    with st.container():
        col_vs, col_pe = st.columns(2)

        # 🔹 ฝั่งซ้าย: Vital Signs
        with col_vs:
            box_color = "#2c2c2c" if st.session_state.theme_mode == "dark" else "#ffffff"
            st.markdown(f"""
                <div style="background-color:{box_color}; border:1px solid #888; border-radius:8px; padding:10px;">
                <strong>🔹 Vital signs</strong>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            row1 = st.columns([1, 0.05, 1, 0.05, 1])
            with row1[0]:
                st.button("BP สูง", on_click=lambda: add_keyword("Abnormal BP"))
            with row1[2]:
                st.button("ชีพจรเร็ว", on_click=lambda: add_keyword("Abnormal Pulse"))
            with row1[4]:
                st.button("ชีพจรช้า", on_click=lambda: add_keyword("Abnormal Pulse"))

            row2 = st.columns([1, 0.05, 1])
            with row2[0]:
                st.button("อุณหภูมิร่างกายผิดปกติ", on_click=lambda: add_keyword("Abnormal Temperature"))
            with row2[2]:
                st.button("การหายใจผิดปกติ", on_click=lambda: add_keyword("Abnormal Respiration"))

            st.markdown("</div>", unsafe_allow_html=True)

        # 🔹 ฝั่งขวา: การตรวจร่างกาย (PE)
        with col_pe:
            box_color = "#2c2c2c" if st.session_state.theme_mode == "dark" else "#ffffff"
            st.markdown(f"""
                <div style="background-color:{box_color}; border:1px solid #888; border-radius:8px; padding:10px;">
                <strong>🔹 การตรวจร่างกาย (PE)</strong><br><br>
            """, unsafe_allow_html=True)

            pe_input = st.text_input("พิมพ์ผลตรวจร่างกาย", placeholder="พิมพ์ภาษาไทยหรืออังกฤษ")

            if st.button("➕ เพิ่ม PE"):
                if pe_input.strip():
                    keyword_pe = f"Abnormal PE ({pe_input.strip()})"
                    if keyword_pe not in st.session_state.selected_keywords:
                        st.session_state.selected_keywords.append(keyword_pe)

            st.markdown("</div>", unsafe_allow_html=True)
