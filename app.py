import streamlit as st
import streamlit.components.v1 as components

# ✅ ตั้งค่า layout แบบ Wide
st.set_page_config(layout="wide")

# ✅ นำฟอนต์ที่รองรับภาษาไทย (Sarabun) จาก Google Fonts มาใช้งาน
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
    body, .block-container {
        font-family: 'Sarabun', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# ✅ ปุ่มสลับ Theme
col1, col2, col3 = st.columns([10, 1, 2])
with col3:
    theme = st.radio("โหมด", ["🌞 Light", "🌙 Night"], horizontal=True, label_visibility="collapsed")
    st.session_state.theme_mode = "dark" if "Night" in theme else "light"

# ✅ Custom CSS สำหรับโหมด Dark
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

# ✅ ฟังก์ชันอัพเดท Keywords
def update_keywords():
    selected = []

    # Vital signs
    if st.session_state.get("chk_bp"):
        selected.append("Abnormal BP")
    if st.session_state.get("chk_bp_fu1month"):
        selected.append("Abnormal BP F/U 1 month")
    if st.session_state.get("chk_pulse_abnormal"):
        selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"):
        selected.append("Fever")
    if st.session_state.get("chk_resp"):
        selected.append("Abnormal Respiration")

    # CBC
    if st.session_state.get("cbc_main"):
        selected.append("Abnormal CBC")
    if st.session_state.get("chk_anemia"):
        selected.append("Anemia")

    # Sugar
    sugar_items = []
    if st.session_state.get("chk_glu"):
        sugar_items.append("Glucose")
    if st.session_state.get("chk_hba1c"):
        sugar_items.append("HbA1C")
    if sugar_items:
        selected.append("Abnormal Sugar (" + ", ".join(sugar_items) + ")")

    # Lipid
    if st.session_state.get("chk_lipid"):
        selected.append("Abnormal Lipid")

    # Metabolic
    if st.session_state.get("chk_uric"):
        selected.append("Abnormal Uric")
    if st.session_state.get("chk_urinecre"):
        selected.append("Abnormal Urine cre.")
    if st.session_state.get("chk_microalb"):
        selected.append("Abnormal Microalbumin")

    # LFT
    if st.session_state.get("lft_main"):
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
            
    # เพิ่ม: การตรวจสมรรถภาพการได้ยิน
    if st.session_state.get("chk_audiometry"):
        audiometry_detail = st.session_state.get("txt_audiometry", "").strip()
        if audiometry_detail:
            selected.append("Abnormal Audiometry (" + audiometry_detail + ")")
        else:
            selected.append("Abnormal Audiometry")
            
    # เพิ่ม: การตรวจตา/การตรวจตาทางอาชีวอนามัย
    if st.session_state.get("chk_vision"):
        vision_detail = st.session_state.get("txt_vision", "").strip()
        if vision_detail:
            selected.append("Abnormal Vision (" + vision_detail + ")")
        else:
            selected.append("Abnormal Vision")
            
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
    
    # -------------------------------
    # F/U Options: เพิ่ม keyword เมื่อเลือก F/U 3 เดือน หรือ F/U 6 เดือน
    keys_for_fu = [
        "chk_bp", "chk_bp_fu1month", "chk_pulse_abnormal", "chk_temp", "chk_resp",
        "cbc_main", "chk_anemia", "chk_hb", "chk_hct",
        "chk_rbc", "chk_wbc", "chk_plt", "chk_neutro", "chk_lymph", "chk_eos",
        "chk_glu", "chk_hba1c", "chk_tc", "chk_trig", "chk_hdl", "chk_ldl",
        "chk_uric", "chk_urinecre", "chk_microalb", "lft_main", "chk_ast", "chk_alt",
        "chk_alp", "chk_ggt", "chk_bun", "chk_creatinine", "chk_egfr",
        "ua_main", "chk_ua_wbc", "chk_ua_rbc", "chk_ua_protein", "chk_ua_glucose",
        "thyroid_main", "chk_tsh", "chk_ft3", "chk_ft4", "chk_vitd",
        "chk_afp", "chk_ca125", "chk_ca199", "chk_psa", "chk_stool", "chk_pap",
        "chk_cxr", "chk_us", "chk_mammo", "chk_12lead", "chk_est", "chk_other_investigation",
        "chk_consult"
    ]
    if any(st.session_state.get(key) for key in keys_for_fu):
        if st.session_state.get("chk_fu3"):
            selected.append("F/U 3 mo.")
        if st.session_state.get("chk_fu6"):
            selected.append("F/U 6 mo.")

    st.session_state.selected_keywords = selected

# ✅ ฟังก์ชันสำหรับล้างข้อมูล Keywords
def clear_keywords():
    for k in list(st.session_state.keys()):
        if k.startswith("chk_") or k in [
            "cbc_main", "pe_input", "lft_main", "kidney_main", "thyroid_main",
            "ua_main", "txt_cxr", "txt_us",
            "txt_12lead", "txt_est", "txt_other_investigation", "txt_consult", "radio_birads",
            "txt_audiometry", "txt_vision"
        ]:
            st.session_state[k] = False if k.startswith("chk_") or k.endswith("_main") else ""
    st.session_state.selected_keywords = []

# ✅ แสดงผลลัพธ์ของ consult
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

# ==================================================================
# ✅ F/U Options (แทรกบรรทัดใหม่ก่อน Section 1)
fu_keys = [
    "chk_bp", "chk_bp_fu1month", "chk_pulse_abnormal", "chk_temp", "chk_resp",
    "cbc_main", "chk_anemia", "chk_hb", "chk_hct",
    "chk_rbc", "chk_wbc", "chk_plt", "chk_neutro", "chk_lymph", "chk_eos",
    "chk_glu", "chk_hba1c", "chk_tc", "chk_trig", "chk_hdl", "chk_ldl",
    "chk_uric", "chk_urinecre", "chk_microalb", "lft_main", "chk_ast", "chk_alt",
    "chk_alp", "chk_ggt", "chk_bun", "chk_creatinine", "chk_egfr",
    "ua_main", "chk_ua_wbc", "chk_ua_rbc", "chk_ua_protein", "chk_ua_glucose",
    "thyroid_main", "chk_tsh", "chk_ft3", "chk_ft4", "chk_vitd",
    "chk_afp", "chk_ca125", "chk_ca199", "chk_psa", "chk_stool", "chk_pap",
    "chk_cxr", "chk_us", "chk_mammo", "chk_12lead", "chk_est", "chk_other_investigation",
    "chk_consult"
]
any_section_selected = any(st.session_state.get(key) for key in fu_keys)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-weight:bold; font-size:16px;'>ตัวเลือก F/U</div>", unsafe_allow_html=True
)
col_fu1, col_fu2 = st.columns(2)
with col_fu1:
    st.checkbox("F/U 3 เดือน", key="chk_fu3", disabled=not any_section_selected, on_change=update_keywords)
with col_fu2:
    st.checkbox("F/U 6 เดือน", key="chk_fu6", disabled=not any_section_selected, on_change=update_keywords)

# ==================================================================
# ✅ Section 1: Vital signs and PE
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; "
    "padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "1. ผล Vital signs และการตรวจร่างกาย</div>",
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Vital signs และ PE)", expanded=False):
    col_vs, col_pe = st.columns(2)

    with col_vs:
        st.checkbox("SBP ≥ 160 หรือ DBP ≥ 100", key="chk_bp", on_change=update_keywords)
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

        st.checkbox("BP 140-159/90-99", key="chk_bp_fu1month", on_change=update_keywords)
        st.checkbox("ชีพจรผิดปกติ", key="chk_pulse_abnormal", on_change=update_keywords)
        st.checkbox("ไข้ (≥ 37.5 °C)", key="chk_temp", on_change=update_keywords)
        st.checkbox("การหายใจผิดปกติ", key="chk_resp", on_change=update_keywords)

    with col_pe:
        st.markdown("**โปรดระบุเมื่อการตรวจร่างกายผิดปกติ**")
        st.text_input("", key="pe_input", on_change=update_keywords)

# ==================================================================
# ส่วนที่เหลือของ code (Section 2-5) ยังคงเหมือนเดิม
# ==================================================================

# ✅ Section 2: Lab results
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; "
    "padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "2. ผลการตรวจทางห้องปฏิบัติการ</div>",
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Lab results)", expanded=False):
    col_cbc, col_met, col_lft = st.columns(3)

    with col_cbc:
        st.checkbox("ความสมบูรณ์ของเม็ดเลือด (CBC)", key="cbc_main", on_change=update_keywords)
        st.checkbox("ซีด (Anemia)", key="chk_anemia", on_change=update_keywords)

    with col_met:
        st.markdown("🔹 Metabolic")
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
        st.checkbox("ไขมันในเลือด (Cholesterol,Triglyceride,HDL,LDL)", key="chk_lipid", on_change=update_keywords)
        st.checkbox("Uric Acid", key="chk_uric", on_change=update_keywords)
        st.checkbox("Urine Creatinine", key="chk_urinecre", on_change=update_keywords)
        st.checkbox("Microalbumin", key="chk_microalb", on_change=update_keywords)

    with col_lft:
        st.checkbox("การทำงานของตับ (Liver function test): AST,ALT,ALP,GGT", key="lft_main", on_change=update_keywords)

    col_kidney, col_thyroid, col_other = st.columns(3)

    with col_kidney:
        st.checkbox("การทำงานของไต (Kidney function test)", key="kidney_main", on_change=update_keywords)
        if st.session_state.get("kidney_main"):
            st.checkbox("Blood urea nitrogen (BUN)", key="chk_bun", on_change=update_keywords)
            st.checkbox("Creatinine", key="chk_creatinine", on_change=update_keywords)
            st.checkbox("eGFR", key="chk_egfr", on_change=update_keywords)
        st.checkbox("การตรวจปัสสาวะ (Urinalysis: UA)", key="ua_main", on_change=update_keywords)

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
    # จัดให้อยู่ในแถวเดียวกัน โดยแบ่งเป็น 2 คอลัมน์
    col_audiometry, col_vision = st.columns(2)
    with col_audiometry:
        st.checkbox("การตรวจสมรรถภาพการได้ยิน", key="chk_audiometry", on_change=update_keywords)
        st.text_input("ระบุหรือไม่ระบุก็ได้", key="txt_audiometry", on_change=update_keywords)
    with col_vision:
        st.checkbox("การตรวจตา/การตรวจตาทางอาชีวอนามัย", key="chk_vision", on_change=update_keywords)
        st.text_input("ระบุหรือไม่ระบุก็ได้", key="txt_vision", on_change=update_keywords)

# ✅ Section 5: Consult
st.markdown(
    f"<div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>"
    "5. ปัญหาสุขภาพอื่น ๆ นอกเหนือรายการตรวจ</div>",
    unsafe_allow_html=True
)

with st.expander("คลิกเพื่อเลือกข้อมูล (Consult)", expanded=False):
    st.checkbox("Consult", key="chk_consult", on_change=update_keywords)
    st.text_input("จำเป็นต้องระบุ", key="txt_consult", on_change=update_keywords)
