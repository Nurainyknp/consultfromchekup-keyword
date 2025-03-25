import streamlit as st
import streamlit.components.v1 as components

# ✅ Wide layout + Theme session
st.set_page_config(layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# ✅ Theme toggle button (top right)
col_theme_left, col_theme_spacer, col_theme_right = st.columns([10, 1, 2])
with col_theme_right:
    selected = st.radio("โหมด", ["🌞 Light", "🌙 Night"], horizontal=True, label_visibility="collapsed")
    st.session_state.theme_mode = "dark" if "Night" in selected else "light"

# ✅ Custom CSS per theme
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
    custom_css = ""

st.markdown(custom_css, unsafe_allow_html=True)

# ✅ Function: update consult keywords
def update_keywords():
    selected = []

    # Vital signs
    if st.session_state.get("chk_bp"):
        selected.append("Abnormal BP")
    if st.session_state.get("chk_pulse_fast") or st.session_state.get("chk_pulse_slow"):
        selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"):
        selected.append("Abnormal Temperature")
    if st.session_state.get("chk_resp"):
        selected.append("Abnormal Respiration")

    # BMI
    if st.session_state.get("chk_bmi_25"):
        selected.append("BMI ≥ 25")
    if st.session_state.get("chk_bmi_28"):
        selected.append("BMI ≥ 28")

    # CBC
    if st.session_state.get("cbc_main"):
        cbc_items = []
        if st.session_state.get("chk_hb"): cbc_items.append("Hb")
        if st.session_state.get("chk_hct"): cbc_items.append("Hct")
        if st.session_state.get("chk_rbc"): cbc_items.append("RBC")
        if st.session_state.get("chk_wbc"): cbc_items.append("WBC")
        if st.session_state.get("chk_plt"): cbc_items.append("PLT")
        if st.session_state.get("chk_neutro"): cbc_items.append("Neutrophils")
        if st.session_state.get("chk_lymph"): cbc_items.append("Lymphocytes")
        if st.session_state.get("chk_eos"): cbc_items.append("Eosinophils")
        if cbc_items:
            selected.append("Abnormal CBC (" + ", ".join(cbc_items) + ")")

    # Sugar
    sugar_items = []
    if st.session_state.get("chk_glu"): sugar_items.append("Glucose")
    if st.session_state.get("chk_hba1c"): sugar_items.append("HbA1C")
    if sugar_items:
        selected.append("Abnormal Sugar (" + ", ".join(sugar_items) + ")")

    # Lipid
    lipid_items = []
    if st.session_state.get("chk_tc"): lipid_items.append("TC")
    if st.session_state.get("chk_trig"): lipid_items.append("Trig")
    if st.session_state.get("chk_hdl"): lipid_items.append("HDL")
    if st.session_state.get("chk_ldl"): lipid_items.append("LDL-C")
    if lipid_items:
        selected.append("Abnormal Lipid (" + ", ".join(lipid_items) + ")")

    # Metabolic (Uric, Urine, Microalbumin)
    if st.session_state.get("chk_uric"):
        selected.append("Abnormal Uric")
    if st.session_state.get("chk_urinecre"):
        selected.append("Abnormal Urine cre.")
    if st.session_state.get("chk_microalb"):
        selected.append("Abnormal Microalbumin")

    # PE
    if st.session_state.get("pe_input"):
        selected.append(f"Abnormal PE ({st.session_state.pe_input})")

    st.session_state.selected_keywords = selected

# ✅ Clear all
def clear_keywords():
    st.session_state.selected_keywords = []
    for key in list(st.session_state.keys()):
        if key.startswith("chk_") or key in ["cbc_main", "pe_input"]:
            st.session_state[key] = False if key.startswith("chk_") or key == "cbc_main" else ""
# ✅ แสดง consult keyword box
update_keywords()
combined_text = "; ".join(st.session_state.selected_keywords)

with st.container():
    bg_color = "#333" if st.session_state.theme_mode == "dark" else "#f0f2f6"
    st.markdown(f"<div style='background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:20px;'>"
                "<h3 style='margin-top:0;'>📝 ระบบช่วยเขียนข้อความ consult</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        components.html(
            f"<button onclick=\"navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!');\""
            "style=\"padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer;\">"
            "📋 คัดลอกข้อความ</button>",
            height=60,
        )
    with col2:
        st.text_area("รวมคำ consult", value=combined_text, height=80)
    with col3:
        if st.button("🗑 ล้างข้อความ"):
            clear_keywords()

    st.markdown("</div>", unsafe_allow_html=True)

# ✅ หัวข้อ 1: Vital signs, BMI, PE
st.markdown(f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>1. ผล Vital signs และการตรวจร่างกาย</div>", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล (Vital signs และ PE)", expanded=True):
    col_vs, col_bmi, col_pe = st.columns(3)

    with col_vs:
        st.checkbox("BP สูง", key="chk_bp", on_change=update_keywords)
        st.checkbox("ชีพจรเร็ว", key="chk_pulse_fast", on_change=update_keywords)
        st.checkbox("ชีพจรช้า", key="chk_pulse_slow", on_change=update_keywords)
        st.checkbox("อุณหภูมิร่างกายผิดปกติ", key="chk_temp", on_change=update_keywords)
        st.checkbox("การหายใจผิดปกติ", key="chk_resp", on_change=update_keywords)

    with col_bmi:
        st.checkbox("BMI ≥ 25", key="chk_bmi_25", on_change=update_keywords)
        st.checkbox("BMI ≥ 28", key="chk_bmi_28", on_change=update_keywords)

    with col_pe:
        st.text_input("พิมพ์ผลตรวจร่างกาย", key="pe_input", on_change=update_keywords)
# ✅ หัวข้อ 2: Lab results
st.markdown(f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>2. ผลการตรวจทางห้องปฏิบัติการ</div>", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล (Lab results)", expanded=True):
    col_cbc, col_met, col_liver = st.columns(3)

    # 🔹 CBC
    with col_cbc:
        st.checkbox("ความสมบูรณ์ของเม็ดเลือด (CBC)", key="cbc_main", on_change=update_keywords)
        if st.session_state.get("cbc_main"):
            st.checkbox("Hemoglobin (Hb)", key="chk_hb", on_change=update_keywords)
            st.checkbox("Hematocrit (Hct)", key="chk_hct", on_change=update_keywords)
            st.checkbox("Red blood cell (RBC)", key="chk_rbc", on_change=update_keywords)
            st.checkbox("White blood cell (WBC)", key="chk_wbc", on_change=update_keywords)
            st.checkbox("Platelet count (PLT)", key="chk_plt", on_change=update_keywords)
            st.checkbox("Neutrophil", key="chk_neutro", on_change=update_keywords)
            st.checkbox("Lymphocytes", key="chk_lymph", on_change=update_keywords)
            st.checkbox("Eosinophils", key="chk_eos", on_change=update_keywords)

    # 🔹 Metabolic
    with col_met:
        st.markdown("🔹 Metabolic")
        st.checkbox("Glucose (Fasting/Non-Fasting)", key="chk_glu", on_change=update_keywords)
        st.checkbox("HbA1C", key="chk_hba1c", on_change=update_keywords)
        st.checkbox("Total Cholesterol", key="chk_tc", on_change=update_keywords)
        st.checkbox("Triglyceride", key="chk_trig", on_change=update_keywords)
        st.checkbox("HDL-C", key="chk_hdl", on_change=update_keywords)
        st.checkbox("LDL-C", key="chk_ldl", on_change=update_keywords)
        st.checkbox("Uric Acid", key="chk_uric", on_change=update_keywords)
        st.checkbox("Urine Creatinine", key="chk_urinecre", on_change=update_keywords)
        st.checkbox("Microalbumin", key="chk_microalb", on_change=update_keywords)

    # 🔹 Liver Function (placeholder)
    with col_liver:
        st.markdown("🔹 การทำงานของตับ (Liver function test)")
    # 🔹 กลุ่มล่าง: Kidney / Thyroid / Tumor
    col_kidney, col_thyroid, col_tumor = st.columns(3)

    with col_kidney:
        st.markdown("🔹 การทำงานของไตและเกลือแร่")
        # เพิ่มกล่องติ๊กในอนาคต เช่น:
        # st.checkbox("Creatinine", key="chk_creatinine", on_change=update_keywords)

    with col_thyroid:
        st.markdown("🔹 การทำงานของต่อมไทรอยด์")
        # st.checkbox("TSH", key="chk_tsh", on_change=update_keywords)

    with col_tumor:
        st.markdown("🔹 สารบ่งชี้มะเร็ง (Tumor markers)")
        # st.checkbox("CEA", key="chk_cea", on_change=update_keywords)
