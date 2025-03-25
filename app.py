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

    # Vital signs
    if st.session_state.get("chk_bp"): selected.append("Abnormal BP")
    if st.session_state.get("chk_pulse_fast") or st.session_state.get("chk_pulse_slow"):
        selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"): selected.append("Abnormal Temperature")
    if st.session_state.get("chk_resp"): selected.append("Abnormal Respiration")

    # BMI
    if st.session_state.get("chk_bmi_25"): selected.append("BMI ≥ 25")
    if st.session_state.get("chk_bmi_28"): selected.append("BMI ≥ 27")

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
        else:
            selected.append("Abnormal kidney")

    # Thyroid
    if st.session_state.get("thyroid_main"):
        thyroid_items = []
        if st.session_state.get("chk_tsh"): thyroid_items.append("TSH")
        if st.session_state.get("chk_ft3"): thyroid_items.append("Free T3")
        if st.session_state.get("chk_ft4"): thyroid_items.append("Free T4")
        if thyroid_items:
            selected.append("Abnormal thyroid (" + ", ".join(thyroid_items) + ")")
        else:
            selected.append("Abnormal thyroid")

    # Tumor markers
    if st.session_state.get("chk_afp"): selected.append("Abnormal AFP")
    if st.session_state.get("chk_ca125"): selected.append("Abnormal CA-125")
    if st.session_state.get("chk_ca199"): selected.append("Abnormal CA 19-9")
    if st.session_state.get("chk_psa"): selected.append("Abnormal PSA")

    # UA
    if st.session_state.get("ua_main"):
        ua_items = []
        if st.session_state.get("chk_ua_wbc"): ua_items.append("WBC")
        if st.session_state.get("chk_ua_rbc"): ua_items.append("RBC")
        if st.session_state.get("chk_ua_protein"): ua_items.append("Protein")
        if st.session_state.get("chk_ua_glucose"): ua_items.append("Glucose")
        if ua_items:
            selected.append("Abnormal UA (" + ", ".join(ua_items) + ")")
        else:
            selected.append("Abnormal UA")

    # Vitamin D
    if st.session_state.get("chk_vitd"): selected.append("Abnormal vit D")

    # Stool
    if st.session_state.get("chk_stool"): selected.append("Abnormal Stool")

    # Pap smear
    if st.session_state.get("chk_pap"): selected.append("Abnormal Pap smear")

    # Radiology
    if st.session_state.get("chk_cxr"):
        cxr_detail = st.session_state.get("txt_cxr", "").strip()
        selected.append(f"Abnormal CXR ({cxr_detail})" if cxr_detail else "Abnormal CXR")

    if st.session_state.get("chk_us"):
        us_detail = st.session_state.get("txt_us", "").strip()
        selected.append(f"Abnormal US ({us_detail})" if us_detail else "Abnormal US")

    # ✅ Mammogram + BI-RADS
    if st.session_state.get("chk_mammo"):
        birads_list = []
        for k, label in {
            "chk_birads3": "BI-RADS 3",
            "chk_birads4a": "BI-RADS 4A",
            "chk_birads4b": "BI-RADS 4B",
            "chk_birads4c": "BI-RADS 4C",
            "chk_birads5": "BI-RADS 5"
        }.items():
            if st.session_state.get(k): birads_list.append(label)
        if birads_list:
            selected.extend(birads_list)
        else:
            selected.append("Abnormal Mammogram/US breast")

    st.session_state.selected_keywords = selected

# ✅ Clear Button
def clear_keywords():
    for k in list(st.session_state.keys()):
        if k.startswith("chk_") or k in [
            "cbc_main", "pe_input", "lft_main", "kidney_main", "thyroid_main",
            "ua_main", "txt_cxr", "txt_us",
            "chk_mammo", "chk_birads3", "chk_birads4a", "chk_birads4b", "chk_birads4c", "chk_birads5"
        ]:
            st.session_state[k] = False if k.startswith("chk_") or k.endswith("_main") else ""
    st.session_state.selected_keywords = []

# ✅ Show result box
update_keywords()
combined_text = "; ".join(st.session_state.selected_keywords)

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

# ✅ Section 1: Vital signs and PE
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

# ✅ Section 2: Lab results (คงเดิม)

# ✅ Section 3: Radiology results (มีส่วนที่เพิ่ม)
st.markdown(f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>3. ผลตรวจทางรังสีวิทยา</div>", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล (Radiology results)", expanded=False):
    col_cxr, col_us = st.columns([1, 1])
    with col_cxr:
        st.checkbox("Chest PA", key="chk_cxr", on_change=update_keywords)
        st.text_input("ระบุหรือไม่ระบุก็ได้", key="txt_cxr", on_change=update_keywords)
    with col_us:
        st.checkbox("Abdominal ultrasound", key="chk_us", on_change=update_keywords)
        st.text_input("จำเป็นต้องระบุอวัยวะ", key="txt_us", on_change=update_keywords)

    st.checkbox("Mammogram with ultrasound breast", key="chk_mammo", on_change=update_keywords)
    if st.session_state.get("chk_mammo"):
        st.markdown("เลือก BI-RADS:")
        st.checkbox("BI-RADS 3", key="chk_birads3", on_change=update_keywords)
        st.checkbox("BI-RADS 4A", key="chk_birads4a", on_change=update_keywords)
        st.checkbox("BI-RADS 4B", key="chk_birads4b", on_change=update_keywords)
        st.checkbox("BI-RADS 4C", key="chk_birads4c", on_change=update_keywords)
        st.checkbox("BI-RADS 5", key="chk_birads5", on_change=update_keywords)
