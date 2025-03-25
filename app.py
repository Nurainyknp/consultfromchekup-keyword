import streamlit as st
import streamlit.components.v1 as components

# ✅ Wide layout + Theme session
st.set_page_config(layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

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

    # 🔹 Vital signs
    if st.session_state.get("chk_bp"): selected.append("Abnormal BP")
    if st.session_state.get("chk_pulse_fast") or st.session_state.get("chk_pulse_slow"):
        selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"): selected.append("Abnormal Temperature")
    if st.session_state.get("chk_resp"): selected.append("Abnormal Respiration")

    # 🔹 BMI
    if st.session_state.get("chk_bmi_25"): selected.append("BMI ≥ 25")
    if st.session_state.get("chk_bmi_28"): selected.append("BMI ≥ 27")

    # 🔹 CBC
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

    # 🔹 Sugar
    sugar_items = []
    if st.session_state.get("chk_glu"): sugar_items.append("Glucose")
    if st.session_state.get("chk_hba1c"): sugar_items.append("HbA1C")
    if sugar_items:
        selected.append("Abnormal Sugar (" + ", ".join(sugar_items) + ")")

    # 🔹 Lipid
    lipid_items = []
    if st.session_state.get("chk_tc"): lipid_items.append("TC")
    if st.session_state.get("chk_trig"): lipid_items.append("Trig")
    if st.session_state.get("chk_hdl"): lipid_items.append("HDL")
    if st.session_state.get("chk_ldl"): lipid_items.append("LDL-C")
    if lipid_items:
        selected.append("Abnormal Lipid (" + ", ".join(lipid_items) + ")")

    # 🔹 Metabolic
    if st.session_state.get("chk_uric"): selected.append("Abnormal Uric")
    if st.session_state.get("chk_urinecre"): selected.append("Abnormal Urine cre.")
    if st.session_state.get("chk_microalb"): selected.append("Abnormal Microalbumin")

    # 🔹 Liver Function Test (LFT)
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
    # 🔹 Kidney Function Test
    if st.session_state.get("kidney_main"):
        kidney_items = []
        if st.session_state.get("chk_bun"): kidney_items.append("BUN")
        if st.session_state.get("chk_creatinine"): kidney_items.append("Creatinine")
        if st.session_state.get("chk_egfr"): kidney_items.append("eGFR")
        if kidney_items:
            selected.append("Abnormal kidney (" + ", ".join(kidney_items) + ")")

    # 🔹 Thyroid Function Test
    if st.session_state.get("thyroid_main"):
        thyroid_items = []
        if st.session_state.get("chk_tsh"): thyroid_items.append("TSH")
        if st.session_state.get("chk_t3"): thyroid_items.append("Free T3")
        if st.session_state.get("chk_t4"): thyroid_items.append("Free T4")
        if thyroid_items:
            selected.append("Abnormal thyroid (" + ", ".join(thyroid_items) + ")")

    # 🔹 PE (Physical Examination)
    if st.session_state.get("pe_input"):
        selected.append(f"Abnormal PE ({st.session_state.pe_input})")

    st.session_state.selected_keywords = selected

# ✅ Clear all selections
def clear_keywords():
    for k in list(st.session_state.keys()):
        if k.startswith("chk_") or k.endswith("_main") or k == "pe_input":
            st.session_state[k] = False if k != "pe_input" else ""
    st.session_state.selected_keywords = []

# ✅ Trigger update & show result
update_keywords()
combined_text = "; ".join(st.session_state.selected_keywords)

st.text_area("รวมคำ consult", value=combined_text, height=80)
if st.button("🗑 ล้างข้อความ"):
    clear_keywords()
# ✅ หัวข้อ 2: Lab results
with st.expander("2. ผลการตรวจทางห้องปฏิบัติการ", expanded=True):
    col1, col2, col3 = st.columns(3)

    # 🔹 Kidney function test
    with col1:
        st.checkbox("การทำงานของไต (Kidney function test)", key="kidney_main", on_change=update_keywords)
        if st.session_state.get("kidney_main"):
            st.checkbox("Blood urea nitrogen (BUN)", key="chk_bun", on_change=update_keywords)
            st.checkbox("Creatinine", key="chk_creatinine", on_change=update_keywords)
            st.checkbox("eGFR", key="chk_egfr", on_change=update_keywords)

    # 🔹 Thyroid function test
    with col2:
        st.checkbox("การทำงานของต่อมไทรอยด์ (Thyroid function test)", key="thyroid_main", on_change=update_keywords)
        if st.session_state.get("thyroid_main"):
            st.checkbox("TSH", key="chk_tsh", on_change=update_keywords)
            st.checkbox("Free T3", key="chk_t3", on_change=update_keywords)
            st.checkbox("Free T4", key="chk_t4", on_change=update_keywords)

    # 🔹 Liver function test (LFT)
    with col3:
        st.checkbox("การทำงานของตับ (Liver function test)", key="lft_main", on_change=update_keywords)
        if st.session_state.get("lft_main"):
            st.checkbox("AST (SGOT)", key="chk_ast", on_change=update_keywords)
            st.checkbox("ALT (SGPT)", key="chk_alt", on_change=update_keywords)
            st.checkbox("ALP", key="chk_alp", on_change=update_keywords)
            st.checkbox("GGT", key="chk_ggt", on_change=update_keywords)

    # ✅ แถวล่าง: CBC + Metabolic
    col_cbc, col_met, _ = st.columns([1.5, 1.5, 1])

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
