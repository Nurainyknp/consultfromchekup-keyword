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
        selected.append("BMI ≥ 25.0-26.99")
    if st.session_state.get("chk_bmi_28"): 
        selected.append("BMI ≥ 27")

    # CBC (แสดง keyword เป็น "Abnormal CBC")
    if st.session_state.get("cbc_main"):
        selected.append("Abnormal CBC")

    # Sugar
    sugar_items = []
    if st.session_state.get("chk_glu"): 
        sugar_items.append("Glucose")
    if st.session_state.get("chk_hba1c"): 
        sugar_items.append("HbA1C")
    if sugar_items:
        selected.append("Abnormal Sugar (" + ", ".join(sugar_items) + ")")

    # Lipid
    lipid_items = []
    if st.session_state.get("chk_tc"): 
        lipid_items.append("TC")
    if st.session_state.get("chk_trig"): 
        lipid_items.append("Trig")
    if st.session_state.get("chk_hdl"): 
        lipid_items.append("HDL")
    if st.session_state.get("chk_ldl"): 
        lipid_items.append("LDL-C")
    if lipid_items:
        selected.append("Abnormal Lipid (" + ", ".join(lipid_items) + ")")

    # Metabolic
    if st.session_state.get("chk_uric"): 
        selected.append("Abnormal Uric")
    if st.session_state.get("chk_urinecre"): 
        selected.append("Abnormal Urine cre.")
    if st.session_state.get("chk_microalb"): 
        selected.append("Abnormal Microalbumin")

    # LFT
    if st.session_state.get("lft_main"):
        lft_items = []
        for k, label in {
            "chk_ast": "AST", "chk_alt": "ALT", "chk_alp": "ALP", "chk_ggt": "GGT"
        }.items():
            if st.session_state.get(k): 
                lft_items.append(label)
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
        if st.session_state.get("chk_bun"): 
            kidney_items.append("BUN")
        if st.session_state.get("chk_creatinine"): 
            kidney_items.append("Creatinine")
        if st.session_state.get("chk_egfr"): 
            kidney_items.append("eGFR")
        if kidney_items:
            selected.append("Abnormal kidney (" + ", ".join(kidney_items) + ")")
        else:
            selected.append("Abnormal kidney")

    # Thyroid
    if st.session_state.get("thyroid_main"):
        thyroid_items = []
        if st.session_state.get("chk_tsh"): 
            thyroid_items.append("TSH")
        if st.session_state.get("chk_ft3"): 
            thyroid_items.append("Free T3")
        if st.session_state.get("chk_ft4"): 
            thyroid_items.append("Free T4")
        if thyroid_items:
            selected.append("Abnormal thyroid (" + ", ".join(thyroid_items) + ")")
        else:
            selected.append("Abnormal thyroid")

    # Tumor markers
    if st.session_state.get("chk_afp"): 
        selected.append("Abnormal AFP")
    if st.session_state.get("chk_ca125"): 
        selected.append("Abnormal CA-125")
    if st.session_state.get("chk_ca199"): 
        selected.append("Abnormal CA 19-9")
    if st.session_state.get("chk_psa"): 
        selected.append("Abnormal PSA")

    # UA
    if st.session_state.get("ua_main"):
        ua_items = []
        if st.session_state.get("chk_ua_wbc"): 
            ua_items.append("WBC")
        if st.session_state.get("chk_ua_rbc"): 
            ua_items.append("RBC")
        if st.session_state.get("chk_ua_protein"): 
            ua_items.append("Protein")
        if st.session_state.get("chk_ua_glucose"): 
            ua_items.append("Glucose")
        if ua_items:
            selected.append("Abnormal UA (" + ", ".join(ua_items) + ")")
        else:
            selected.append("Abnormal UA")

    # Vitamin D
    if st.session_state.get("chk_vitd"): 
        selected.append("Abnormal vit D")

    # Stool
    if st.session_state.get("chk_stool"): 
        selected.append("Abnormal Stool")

    # Pap smear
    if st.session_state.get("chk_pap"): 
        selected.append("Abnormal Pap smear")

    # Radiology: CXR and US
    if st.session_state.get("chk_cxr"):
        cxr_detail = st.session_state.get("txt_cxr", "").strip()
        selected.append(f"Abnormal CXR ({cxr_detail})" if cxr_detail else "Abnormal CXR")
    if st.session_state.get("chk_us"):
        us_detail = st.session_state.get("txt_us", "").strip()
        selected.append(f"Abnormal US ({us_detail})" if us_detail else "Abnormal US")
    
    # Radiology additional: Mammogram with ultrasound breast
    if st.session_state.get("chk_mammo"):
        if st.session_state.get("radio_birads"):
            selected.append(st.session_state.radio_birads)

    # -------------------------------
    # Section 4: Other investigations
    if st.session_state.get("chk_12lead"):
        text = st.session_state.get("txt_12lead", "").strip()
        if text:
            selected.append("12-lead EKG (" + text + ")")
        else:
            selected.append("Abnormal EKG")
            
    if st.session_state.get("chk_est"):
        text = st.session_state.get("txt_est", "").strip()
        if text:
            selected.append("Abnormal EST (" + text + ")")
        else:
            selected.append("Abnormal EST")
            
    if st.session_state.get("chk_other_investigation"):
        text = st.session_state.get("txt_other_investigation", "").strip()
        if text:
            selected.append("Abnormal(" + text + ")")
        else:
            selected.append("Abnormal")

    # -------------------------------
    # Section 5: Consult
    if st.session_state.get("chk_consult"):
        text = st.session_state.get("txt_consult", "").strip()
        if text:
            selected.append("Consult (" + text + ")")
        else:
            selected.append("Consult")

    st.session_state.selected_keywords = selected

# ✅ Clear Button
def clear_keywords():
    for k in list(st.session_state.keys()):
        if k.startswith("chk_") or k in [
            "cbc_main", "pe_input", "lft_main", "kidney_main", "thyroid_main",
            "ua_main", "txt_cxr", "txt_us",
            "txt_12lead", "txt_est", "txt_other_investigation", "txt_consult", "radio_birads"
        ]:
            st.session_state[k] = False if k.startswith("chk_") or k.endswith("_main") else ""
    st.session_state.selected_keywords = []

# ✅ Show result box
update_keywords()
combined_text = "; ".join(st.session_state.selected_keywords)

bg_color = "#333" if st.session_state.theme_mode == "dark" else "#f0f2f6"
st.markdown(
    f"<div style='background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:20px;'>"
    "<h3>📝 ระบบช่วยเขียนข้อความ consult</h3>", 
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns([2, 6, 2])
with c1:
    # ปุ่มคัดลอกข้อความ ทำการคัดลอกทันทีโดยไม่มี alert pop-up
    components.html(
        f"<button onclick=\"navigator.clipboard.writeText('{combined_text}');\""
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
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "1. ผล Vital signs และการตรวจร่างกาย</div>", 
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Vital signs และ PE)", expanded=False):
    col_vs, col_bmi, col_pe = st.columns(3)

    with col_vs:
        # เปลี่ยน label BP เป็น "SBP ≥ 140 หรือ DBP ≥ 90"
        st.checkbox("SBP ≥ 140 หรือ DBP ≥ 90", key="chk_bp", on_change=update_keywords)
        if st.session_state.get("chk_bp"):
            st.markdown(
                '''
                <style>
                .blinking {
                  animation: blinker 1s linear infinite;
                }
                @keyframes blinker {
                  50% { opacity: 0; }
                }
                </style>
                <span class="blinking" style="color: red; font-weight: bold; font-size: 24px;">ส่งทันที</span>
                ''',
                unsafe_allow_html=True
            )
        st.checkbox("ชีพจรเร็ว", key="chk_pulse_fast", on_change=update_keywords)
        st.checkbox("ชีพจรช้า", key="chk_pulse_slow", on_change=update_keywords)
        st.checkbox("อุณหภูมิร่างกายผิดปกติ", key="chk_temp", on_change=update_keywords)
        st.checkbox("การหายใจผิดปกติ", key="chk_resp", on_change=update_keywords)

    with col_bmi:
        col_bmi_1, col_bmi_2 = st.columns([1, 1])
        with col_bmi_1:
            disable_bmi25 = st.session_state.get("chk_bmi_28", False)
            st.checkbox("BMI ≥ 25.0-26.99", key="chk_bmi_25", on_change=update_keywords, disabled=disable_bmi25)
        with col_bmi_2:
            disable_bmi28 = st.session_state.get("chk_bmi_25", False)
            st.checkbox("BMI ≥ 27", key="chk_bmi_28", on_change=update_keywords, disabled=disable_bmi28)
            if st.session_state.get("chk_bmi_28"):
                st.markdown(
                    '''
                    <style>
                    .blinking {
                      animation: blinker 1s linear infinite;
                    }
                    @keyframes blinker {
                      50% { opacity: 0; }
                    }
                    </style>
                    <span class="blinking" style="color: red; font-weight: bold; font-size: 24px;">ส่งทันที</span>
                    ''',
                    unsafe_allow_html=True
                )

    with col_pe:
        st.markdown("**โปรดระบุเมื่อการตรวจร่างกายผิดปกติ**")
        st.text_input("", key="pe_input", on_change=update_keywords)

# ✅ Section 2: Lab results
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "2. ผลการตรวจทางห้องปฏิบัติการ</div>", 
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Lab results)", expanded=False):
    col_cbc, col_met, col_lft = st.columns(3)

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

    with col_met:
        st.markdown("🔹 Metabolic")
        # Glucose checkbox
        st.checkbox("Glucose (Fasting/Non-Fasting)", key="chk_glu", on_change=update_keywords)
        if st.session_state.get("chk_glu"):
            st.markdown(
                '''
                <span style="color: red; font-weight: bold; font-size: 24px;">ถ้า≥ 126</span>
                <span class="blinking" style="color: red; font-weight: bold; font-size: 24px; margin-left: 10px;">ส่งทันที</span>
                <style>
                .blinking {
                  animation: blinker 1s linear infinite;
                }
                @keyframes blinker {
                  50% { opacity: 0; }
                }
                </style>
                ''',
                unsafe_allow_html=True
            )
        st.checkbox("HbA1C", key="chk_hba1c", on_change=update_keywords)
        st.checkbox("Total Cholesterol", key="chk_tc", on_change=update_keywords)
        st.checkbox("Triglyceride", key="chk_trig", on_change=update_keywords)
        st.checkbox("HDL-C", key="chk_hdl", on_change=update_keywords)
        st.checkbox("LDL-C", key="chk_ldl", on_change=update_keywords)
        if st.session_state.get("chk_ldl"):
            st.markdown(
                '''
                <span style="color: red; font-weight: bold; font-size: 24px;">ถ้า≥ 190</span>
                <span class="blinking" style="color: red; font-weight: bold; font-size: 24px; margin-left: 10px;">ส่งทันที</span>
                <style>
                .blinking {
                  animation: blinker 1s linear infinite;
                }
                @keyframes blinker {
                  50% { opacity: 0; }
                }
                </style>
                ''',
                unsafe_allow_html=True
            )
        st.checkbox("Uric Acid", key="chk_uric", on_change=update_keywords)
        st.checkbox("Urine Creatinine", key="chk_urinecre", on_change=update_keywords)
        st.checkbox("Microalbumin", key="chk_microalb", on_change=update_keywords)

    with col_lft:
        st.checkbox("การทำงานของตับ (Liver function test)", key="lft_main", on_change=update_keywords)
        if st.session_state.get("lft_main"):
            st.checkbox("AST (SGOT)", key="chk_ast", on_change=update_keywords)
            st.checkbox("ALT (SGPT)", key="chk_alt", on_change=update_keywords)
            st.checkbox("ALP", key="chk_alp", on_change=update_keywords)
            st.checkbox("GGT", key="chk_ggt", on_change=update_keywords)

    col_kidney, col_thyroid, col_other = st.columns(3)

    with col_kidney:
        st.checkbox("การทำงานของไต (Kidney function test)", key="kidney_main", on_change=update_keywords)
        if st.session_state.get("kidney_main"):
            st.checkbox("Blood urea nitrogen (BUN)", key="chk_bun", on_change=update_keywords)
            st.checkbox("Creatinine", key="chk_creatinine", on_change=update_keywords)
            st.checkbox("eGFR", key="chk_egfr", on_change=update_keywords)
        st.checkbox("การตรวจปัสสาวะ (Urinalysis: UA)", key="ua_main", on_change=update_keywords)
        if st.session_state.get("ua_main"):
            st.checkbox("White blood cell (WBC)", key="chk_ua_wbc", on_change=update_keywords)
            st.checkbox("Red blood cell (RBC)", key="chk_ua_rbc", on_change=update_keywords)
            st.checkbox("Protein", key="chk_ua_protein", on_change=update_keywords)
            st.checkbox("Glucose", key="chk_ua_glucose", on_change=update_keywords)

    with col_thyroid:
        st.checkbox("การทำงานของต่อมไทรอยด์ (Thyroid function test)", key="thyroid_main", on_change=update_keywords)
        if st.session_state.get("thyroid_main"):
            st.checkbox("TSH", key="chk_tsh", on_change=update_keywords)
            st.checkbox("Free T3", key="chk_ft3", on_change=update_keywords)
            st.checkbox("Free T4", key="chk_ft4", on_change=update_keywords)
        st.checkbox("วิตามินดี (Vitamin D total)", key="chk_vitd", on_change=update_keywords)

    with col_other:
        st.markdown("🔹 สารบ่งชี้มะเร็ง (Tumor markers)")
        st.checkbox("AFP", key="chk_afp", on_change=update_keywords)
        st.checkbox("CA-125", key="chk_ca125", on_change=update_keywords)
        st.checkbox("CA 19-9", key="chk_ca199", on_change=update_keywords)
        st.checkbox("PSA", key="chk_psa", on_change=update_keywords)
        st.checkbox("การตรวจอุจจาระ", key="chk_stool", on_change=update_keywords)
        st.checkbox("Pap smear", key="chk_pap", on_change=update_keywords)

# ✅ Section 3: Radiology results
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "3. ผลตรวจทางรังสีวิทยา</div>", 
    unsafe_allow_html=True
)

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
        st.radio("เลือก BI-RADS", 
                 ["BI-RADS 3", "BI-RADS 4A", "BI-RADS 4B", "BI-RADS 4C", "BI-RADS 5"],
                 key="radio_birads", on_change=update_keywords)

# ✅ Section 4: Other investigations
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "4. การตรวจอื่น ๆ</div>", 
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Other investigations)", expanded=False):
    col_12lead, col_est, col_other_invest = st.columns(3)
    
    with col_12lead:
        st.checkbox("12-lead EKG", key="chk_12lead", on_change=update_keywords)
        st.text_input("ระบุหรือไม่ระบุก็ได้", key="txt_12lead", on_change=update_keywords)
    
    with col_est:
        st.checkbox("Exercise stress test (EST)", key="chk_est", on_change=update_keywords)
        st.text_input("ระบุหรือไม่ระบุก็ได้", key="txt_est", on_change=update_keywords)
    
    with col_other_invest:
        st.checkbox("ผลผิดปกติอื่น ๆ", key="chk_other_investigation", on_change=update_keywords)
        st.text_input("จำเป็นต้องระบุ", key="txt_other_investigation", on_change=update_keywords)

# ✅ Section 5: Consult
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "5. ปัญหาสุขภาพอื่น ๆ นอกเหนือรายการตรวจ</div>", 
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Consult)", expanded=False):
    st.checkbox("Consult", key="chk_consult", on_change=update_keywords)
    st.text_input("จำเป็นต้องระบุ", key="txt_consult", on_change=update_keywords)
