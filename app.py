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
    theme_options = ["Light", "Night"]
    icon_map = {"Light": "🌞", "Night": "🌙"}
    theme_label = st.radio("โหมด", theme_options, horizontal=True, label_visibility="collapsed")
    theme = f"{icon_map[theme_label]} {theme_label}"
    st.session_state.theme_mode = "dark" if theme_label == "Night" else "light"

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

    # Vital signs
    if st.session_state.get("chk_bp"): selected.append("Abnormal BP")
    if st.session_state.get("chk_pulse_fast") or st.session_state.get("chk_pulse_slow"):
        selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"): selected.append("Abnormal Temperature")
    if st.session_state.get("chk_resp"): selected.append("Abnormal Respiration")

    # BMI
    if st.session_state.get("chk_bmi_25"): selected.append("BMI ≥ 25")
    if st.session_state.get("chk_bmi_28"): selected.append("BMI ≥ 28")

    # CBC
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

    # Metabolic
    if st.session_state.get("chk_uric"): selected.append("Abnormal Uric")
    if st.session_state.get("chk_urinecre"): selected.append("Abnormal Urine cre.")
    if st.session_state.get("chk_microalb"): selected.append("Abnormal Microalbumin")

    # LFT
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

    # PE
    if st.session_state.get("pe_input"):
        selected.append(f"Abnormal PE ({st.session_state.pe_input})")

    # Kidney
    if st.session_state.get("kidney_main"):
        kidney_items = []
        if st.session_state.get("chk_bun"): kidney_items.append("BUN")
        if st.session_state.get("chk_creatinine"): kidney_items.append("Creatinine")
        if st.session_state.get("chk_egfr"): kidney_items.append("eGFR")
        if kidney_items:
            selected.append("Abnormal kidney (" + ", ".join(kidney_items) + ")")

    # Thyroid
    if st.session_state.get("thyroid_main"):
        thyroid_items = []
        if st.session_state.get("chk_tsh"): thyroid_items.append("TSH")
        if st.session_state.get("chk_ft3"): thyroid_items.append("Free T3")
        if st.session_state.get("chk_ft4"): thyroid_items.append("Free T4")
        if thyroid_items:
            selected.append("Abnormal thyroid (" + ", ".join(thyroid_items) + ")")

    st.session_state.selected_keywords = selected

# ✅ Clear

def clear_keywords():
    for k in list(st.session_state.keys()):
        if k.startswith("chk_") or k in ["cbc_main", "pe_input", "lft_main", "kidney_main", "thyroid_main"]:
            st.session_state[k] = False if k.startswith("chk_") or k.endswith("_main") else ""
    st.session_state.selected_keywords = []
