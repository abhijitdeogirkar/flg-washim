import streamlit as st
import datetime

# १. पेज सेटिंग
st.set_page_config(page_title="FGL Washim 2026", page_icon="🌱", layout="centered")

# २. मोबाईलवर लोगो एकाच ओळीत दिसण्यासाठी CSS
st.markdown("""
    <style>
    .logo-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
    }
    .logo-container img {
        max-width: 80px;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# ३. सेशन स्टेट्स
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'must_change_password' not in st.session_state:
    st.session_state.must_change_password = False

# ४. --- हेडर आणि लोगो (मोबाईल फ्रेंडली) ---
# टीप: फोटो नावे तुमच्या GitHub वरील नावांप्रमाणे असावीत.
st.markdown(f"""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/तुमचा_युजरनेम/fgl-washim/main/agri_logo.png">
        <img src="https://raw.githubusercontent.com/तुमचा_युजरनेम/fgl-washim/main/fgl_logo.png">
        <img src="https://raw.githubusercontent.com/तुमचा_युजरनेम/fgl-washim/main/atma_logo.png">
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #2e7b32;'>फार्मर ग्रुप लीग - वाशिम २०२६</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>कृषी विभाग, जिल्हा परिषद वाशिम</h5>", unsafe_allow_html=True)
st.markdown("---")

# ५. मुख्य लॉगिन आणि नोंदणी टॅब
if not st.session_state.logged_in and not st.session_state.must_change_password:
    
    tab1, tab2 = st.tabs(["🔐 लॉगिन (Login)", "📝 नवीन नोंदणी (Registration)"])
    
    # --- टॅब १: लॉगिन ---
    with tab1:
        login_id = st.text_input("युजर आयडी (उदा. FGL-101)")
        password = st.text_input("पासवर्ड", type="password")
        if st.button("लॉगिन करा", type="primary", use_container_width=True):
            # लॉगिन लॉजिक (भविष्यात Google Sheets शी जोडले जाईल)
            st.success("लॉगिन यशस्वी!")

    # --- टॅब २: रिअल रजिस्ट्रेशन फॉर्म ---
    with tab2:
        st.subheader("स्पर्धा नोंदणी अर्ज (FGL-2026)")
        
        with st.form("reg_form", clear_on_submit=True):
            # अ) भौगोलिक माहिती (Demographic)
            st.write("📍 **भौगोलिक माहिती**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                dist = st.selectbox("जिल्हा", ["वाशिम"])
            with col_b:
                taluka = st.selectbox("तालुका निवडा", ["वाशिम", "मालेगाव", "रिसोड", "मंगरूळपीर", "कारंजा", "मानोरा"])
            with col_c:
                # येथे तुमच्या 'Demographic_data' मधून त्या तालुक्यातील गावे येतील
                village = st.text_input("गाव")

            st.write("👥 **गटाची माहिती**")
            group_name = st.text_input("शेतकरी गटाचे पूर्ण नाव")
            
            col1, col2 = st.columns(2)
            with col1:
                est_date = st.date_input("गटाची स्थापना दिनांक", min_value=datetime.date(1990, 1, 1))
                members = st.number_input("सदस्य संख्या", min_value=1, step=1)
            with col2:
                area = st.number_input("एकूण शेती क्षेत्र (हेक्टरमध्ये)", min_value=0.1, step=0.1)
                crops = st.text_input("मुख्य पिके")

            st.write("👤 **संपर्क व्यक्ती (गट प्रमुख)**")
            head_name = st.text_input("गट प्रमुखाचे नाव")
            mobile = st.text_input("मोबाईल क्रमांक (हाच लॉगिन पासवर्ड राहील)", max_chars=10)

            submitted = st.form_submit_button("अर्ज सादर करा (Submit)", use_container_width=True)
            
            if submitted:
                if group_name and len(mobile) == 10:
                    # येथे आपण डेटा Google Sheet मध्ये सेव्ह करू
                    st.balloons()
                    st.success(f"'{group_name}' चा नोंदणी अर्ज यशस्वीरित्या स्वीकारला आहे!")
                    st.info(f"**तुमचा लॉगिन आयडी:** FGL-{mobile[-3:]} (नमुना) \n\n **पासवर्ड:** {mobile}")
                else:
                    st.error("कृपया सर्व माहिती अचूक भरा. मोबाईल नंबर १० अंकी असावा.")

# पासवर्ड बदलणे आणि डॅशबोर्डचे लॉजिक आधीप्रमाणेच राहील...
