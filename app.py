import streamlit as st
import streamlit.components.v1 as components

# ✅ Wide layout + Theme session
st.set_page_config(layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []
if "metabolic_main" not in st.session_state:
    st.session_state.metabolic_main = False
if "tumor_main" not in st.session_state:
    st.session_state.tumor_main = False

# ✅ Theme toggle button
col1, col2, col3 = st.columns([10, 1, 2])
with col3:
    theme = st.radio("โหมด", ["🌞 Light", "🌙 Night"], horizontal=True, label_visibility="collapsed")
    st.session_state.theme_mode = "dark" if "Night" in theme else "light"

# ✅ Custom CSS
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
    st.markdown(custom_css, unsafe_allow_html=True)

# ✅ Update Keywords
def update_keywords():
    selected = []

    if st.session_state.get("chk_bp"): selected.append("Abnormal BP")
    if st.session_state.get("chk_pulse_fast") or st.session_state.get("chk_pulse_slow"):
        selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"): selected.append("Abnormal Temperature")
    if st.session_state.get("chk_resp"): selected.append("Abnormal Respiration")

    if st.session_state.get("chk_bmi_25"): selected.append("BMI ≥ 25")
    if st.session_state.get("chk_bmi_28"): selected.append("BMI ≥ 27")

    if st.session_state.get("cbc_main"):
        cbc_items = []
        for k, label in {
            "chk_hb": "Hb", "chk_hct": "Hct", "chk_rbc": "RBC", "chk_wbc": "WBC",
            "chk_plt": "PLT", "chk_neutro": "Neutrophils", "chk_lymph": "Lymphocytes",
            "chk_eos": "Eosinophils"
        }.items():
            if st.session_state.get(k): cbc_items.append(label)
        if cbc_items:
            selected.append("Abnormal CBC (" + ", ".join(cbc_items) + ")")

    sugar_items = []
    if st.session_state.get("chk_glu"): sugar_items.append("Glucose")
    if st.session_state.get("chk_hba1c"): sugar_items.append("HbA1C")
    if sugar_items:
        selected.append("Abnormal Sugar (" + ", ".join(sugar_items) + ")")

    lipid_items = []
    if st.session_state.get("chk_tc"): lipid_items.append("TC")
    if st.session_state.get("chk_trig"): lipid_items.append("Trig")
    if st.session_state.get("chk_hdl"): lipid_items.append("HDL")
    if st.session_state.get("chk_ldl"): lipid_items.append("LDL-C")
    if lipid_items:
        selected.append("Abnormal Lipid (" + ", ".join(lipid_items) + ")")

    if st.session_state.get("chk_uric"): selected.append("Abnormal Uric")
    if st.session_state.get("chk_urinecre"): selected.append("Abnormal Urine cre.")
    if st.session_state.get("chk_microalb"): selected.append("Abnormal Microalbumin")

    if st.session_state.get("lft_main"):
        lft_items = []
        for k, label in {
            "chk_ast": "AST", "chk_alt": "ALT", "chk_alp": "ALP", "chk_ggt": "GGT"
        }.items():
            if st.session_state.get(k): lft_items.append(label)
        if lft_items:
            selected.append("Abnormal LFT (" + ", ".join(lft_items) + ")")
        else:
            selected.append("Abnormal LFT")

    if st.session_state.get("pe_input"):
        selected.append(f"Abnormal PE ({st.session_state.pe_input})")

    if st.session_state.get("kidney_main"):
        kidney_items = []
        if st.session_state.get("chk_bun"): kidney_items.append("BUN")
        if st.session_state.get("chk_creatinine"): kidney_items.append("Creatinine")
        if st.session_state.get("chk_egfr"): kidney_items.append("eGFR")
        if kidney_items:
            selected.append("Abnormal kidney (" + ", ".join(kidney_items) + ")")
        else:
            selected.append("Abnormal kidney")

    if st.session_state.get("thyroid_main"):
        thyroid_items = []
        if st.session_state.get("chk_tsh"): thyroid_items.append("TSH")
        if st.session_state.get("chk_ft3"): thyroid_items.append("Free T3")
        if st.session_state.get("chk_ft4"): thyroid_items.append("Free T4")
        if thyroid_items:
            selected.append("Abnormal thyroid (" + ", ".join(thyroid_items) + ")")
        else:
            selected.append("Abnormal thyroid")

    if st.session_state.get("chk_afp"): selected.append("Abnormal AFP")
    if st.session_state.get("chk_ca125"): selected.append("Abnormal CA-125")
    if st.session_state.get("chk_ca199"): selected.append("Abnormal CA 19-9")
    if st.session_state.get("chk_psa"): selected.append("Abnormal PSA")

    st.session_state.selected_keywords = selected

# ✅ Clear Button
def clear_keywords():
    for k in list(st.session_state.keys()):
        if k.startswith("chk_") or k in ["cbc_main", "pe_input", "lft_main", "kidney_main", "thyroid_main", "metabolic_main", "tumor_main"]:
            st.session_state[k] = False if k.startswith("chk_") or k.endswith("_main") else ""
    st.session_state.selected_keywords = []

update_keywords()
combined_text = "; ".join(st.session_state.selected_keywords)

# ✅ กล่องแสดงผล + ปุ่มคัดลอก / ล้าง
bg_color = "#333" if st.session_state.theme_mode == "dark" else "#f0f2f6"
st.markdown(f"<div style='background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:20px;'>"
            "<h3>📝 ระบบช่วยเขียนข้อความ consult</h3>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 6, 2])
with c1:
    components.html(
        f"<button onclick=\"navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!');\""
        "style=\"padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer;\">"
        "📋 คัดลอกข้อความ</button>",
        height=60,
    )
with c2:
    st.text_area("รวมคำ consult", value=combined_text, height=80)
with c3:
    if st.button("🗑 ล้างข้อความ"):
        clear_keywords()

st.markdown("</div>", unsafe_allow_html=True)

# ✅ หัวข้อ 1: Vital Signs & BMI & PE
st.markdown(f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>1. ผล Vital signs และการตรวจร่างกาย</div>", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล (Vital signs และ PE)", expanded=False):
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

with st.expander("คลิกเพื่อเลือกข้อมูล (Lab results)", expanded=False):
    col_cbc, col_lft = st.columns(2)

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

    with col_lft:
        st.checkbox("การทำงานของตับ (Liver function test)", key="lft_main", on_change=update_keywords)
        if st.session_state.get("lft_main"):
            st.checkbox("AST (SGOT)", key="chk_ast", on_change=update_keywords)
            st.checkbox("ALT (SGPT)", key="chk_alt", on_change=update_keywords)
            st.checkbox("ALP", key="chk_alp", on_change=update_keywords)
            st.checkbox("GGT", key="chk_ggt", on_change=update_keywords)

    st.checkbox("ผลตรวจด้านเมตาบอลิซึม (Metabolic)", key="metabolic_main", on_change=update_keywords)
    if st.session_state.get("metabolic_main"):
        with st.expander("รายละเอียด Metabolic", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.checkbox("Glucose (Fasting/Non-Fasting)", key="chk_glu", on_change=update_keywords)
                st.checkbox("HbA1C", key="chk_hba1c", on_change=update_keywords)
                st.checkbox("Total Cholesterol", key="chk_tc", on_change=update_keywords)
            with col2:
                st.checkbox("Triglyceride", key="chk_trig", on_change=update_keywords)
                st.checkbox("HDL-C", key="chk_hdl", on_change=update_keywords)
                st.checkbox("LDL-C", key="chk_ldl", on_change=update_keywords)
            with col3:
                st.checkbox("Uric Acid", key="chk_uric", on_change=update_keywords)
                st.checkbox("Urine Creatinine", key="chk_urinecre", on_change=update_keywords)
                st.checkbox("Microalbumin", key="chk_microalb", on_change=update_keywords)

    st.checkbox("สารบ่งชี้มะเร็ง (Tumor markers)", key="tumor_main", on_change=update_keywords)
    if st.session_state.get("tumor_main"):
        with st.expander("รายละเอียด Tumor markers", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("AFP", key="chk_afp", on_change=update_keywords)
                st.checkbox("CA-125", key="chk_ca125", on_change=update_keywords)
            with col2:
                st.checkbox("CA 19-9", key="chk_ca199", on_change=update_keywords)
                st.checkbox("PSA", key="chk_psa", on_change=update_keywords)

    col_kidney, col_thyroid = st.columns(2)

    with col_kidney:
        st.checkbox("การทำงานของไต (Kidney function test)", key="kidney_main", on_change=update_keywords)
        if st.session_state.get("kidney_main"):
            st.checkbox("Blood urea nitrogen (BUN)", key="chk_bun", on_change=update_keywords)
            st.checkbox("Creatinine", key="chk_creatinine", on_change=update_keywords)
            st.checkbox("eGFR", key="chk_egfr", on_change=update_keywords)

    with col_thyroid:
        st.checkbox("การทำงานของต่อมไทรอยด์ (Thyroid function test)", key="thyroid_main", on_change=update_keywords)
        if st.session_state.get("thyroid_main"):
            st.checkbox("TSH", key="chk_tsh", on_change=update_keywords)
            st.checkbox("Free T3", key="chk_ft3", on_change=update_keywords)
            st.checkbox("Free T4", key="chk_ft4", on_change=update_keywords)
