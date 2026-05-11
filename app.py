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

# ४. --- हेडर आणि लोगो ---
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
    
    tab1, tab2 = st.tabs(["🔐 लॉगिन (Login)", "📝 स्पर्धा नोंदणी अर्ज"])
    
    # --- टॅब १: लॉगिन ---
    with tab1:
        st.subheader("लॉगिन करा")
        login_id = st.text_input("युजर आयडी (उदा. FGL-101)")
        password = st.text_input("पासवर्ड", type="password")
        if st.button("लॉगिन करा", type="primary", use_container_width=True):
            st.success("लॉगिन यशस्वी!") # हे नंतर Google Sheet ला जोडू

    # --- टॅब २: रिअल रजिस्ट्रेशन फॉर्म (PDF नुसार) ---
    with tab2:
        st.markdown("<h4 style='text-align: center;'>नोंदणी अर्ज: फार्मर ग्रुप लीग (FGL) – २०२६</h4>", unsafe_allow_html=True)
        
        # गट नोंदणीची तपासणी (Validation)
        st.write("---")
        is_registered = st.radio("तुमचा शेतकरी गट अधिकृतरीत्या नोंदणीकृत (Registered) आहे का?", ["होय", "नाही"])
        
        if is_registered == "नाही":
            st.error("⚠️ क्षमस्व! स्पर्धेत भाग घेण्यासाठी आत्मा (ATMA) कार्यालयाशी संपर्क करून गट नोंदणी करणे अनिवार्य आहे. नोंदणी झाल्यानंतरच तुम्ही हा फॉर्म भरू शकता.")
        
        else:
            with st.form("reg_form", clear_on_submit=False):
                # PDF मधील अधिकृत मजकूर
                st.markdown("""
                **प्रति,** <br>
                **मा. जिल्हा अधीक्षक कृषी अधिकारी, वाशिम** <br>
                **विषय:** फार्मर ग्रुप लीग (FGL) - २०२६ स्पर्धेमध्ये सहभागी होणेबाबत...<br>
                **महोदय,**<br>
                वरील विषयानुसार अर्ज सादर करण्यात येतो की, आमचा शेतकरी गट आपल्या विभागामार्फत आयोजित फार्मर ग्रुप लीग (FGL) – २०२६ या स्पर्धेमध्ये सहभागी होण्यास इच्छुक आहे. आमच्या गटाची माहिती पुढीलप्रमाणे आहे:
                """, unsafe_allow_html=True)
                st.markdown("---")

                # अ) भौगोलिक माहिती (Demographic in English)
                st.write("📍 **Geographical Info (भौगोलिक माहिती)**")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    dist = st.selectbox("District", ["Washim"])
                with col_b:
                    taluka = st.selectbox("Taluka", ["Washim", "Malegaon", "Risod", "Mangrulpir", "Karanja", "Manora"])
                with col_c:
                    village = st.text_input("Village (इंग्रजीत नाव टाका)")

                # ब) गटाची माहिती
                st.write("👥 **गटाची माहिती**")
                group_name = st.text_input("शेतकरी गटाचे पूर्ण नाव")
                reg_no = st.text_input("गटाचा नोंदणी क्रमांक (Registration Number)")
                
                col1, col2 = st.columns(2)
                with col1:
                    # तारीख फॉरमॅट DD/MM/YYYY
                    est_date = st.date_input("स्थापना दिनांक", format="DD/MM/YYYY")
                    members = st.number_input("सदस्य संख्या (किमान १० आवश्यक)", min_value=10, step=1)
                with col2:
                    area = st.number_input("एकूण शेती क्षेत्र (हेक्टरमध्ये)", min_value=0.1, step=0.1)
                
                # मुख्य पिके - Multiple Selection (वाशिम खरीप पिके)
                crops = st.multiselect(
                    "मुख्य पिके (एकापेक्षा जास्त पिके निवडू शकता)", 
                    ["Soybean (सोयाबीन)", "Cotton (कापूस)", "Tur (तूर)", "Urad (उडीद)", "Moong (मूग)", "Sorghum (ज्वारी)", "Horticulture (फळबाग)", "Other (इतर)"]
                )

                # क) गट प्रमुख
                st.write("👤 **संपर्क व्यक्ती**")
                head_name = st.text_input("गट प्रमुखाचे (अध्यक्ष/सचिव) नाव")
                mobile = st.text_input("संपर्क क्रमांक (Mobile Number)", max_chars=10)

                # ड) पीडीएफ मधील घोषणापत्र (Declaration)
                st.markdown("---")
                declaration = st.checkbox("आम्ही आपले नियम व अटीच्या आधीन राहून स्पर्धेत सहभागी होत आहोत. तरी कृपया आमचा अर्ज मान्य करून आम्हाला फार्मर ग्रुप लीग (FGL) - २०२६ मध्ये सहभागी होण्याची संधी द्यावी ही नम्र विनंती.")

                # सबमिट बटण
                submitted = st.form_submit_button("अर्ज सादर करा (Submit Application)", use_container_width=True)
                
                if submitted:
                    if not declaration:
                        st.warning("कृपया नियम व अटी मान्य असल्याचा चेकबॉक्स (☑️) टिक करा.")
                    elif not reg_no:
                        st.error("गटाचा नोंदणी क्रमांक भरणे अनिवार्य आहे.")
                    elif len(mobile) != 10 or not mobile.isdigit():
                        st.error("कृपया अचूक १० अंकी संपर्क क्रमांक भरा.")
                    elif not group_name or not village or not crops:
                        st.error("कृपया सर्व माहिती पूर्ण भरा (गाव, गटाचे नाव, पिके).")
                    else:
                        st.success(f"'{group_name}' चा नोंदणी अर्ज यशस्वीरित्या सादर झाला आहे!")
                        # प्रोविजनल (Provisional) मेसेज
                        st.info(f"""
                        ✅ **नोंदणी यशस्वी!**
                        
                        **तुमचा तात्पुरता (Provisional) युजर आयडी:** FGL-{mobile[-4:]} 
                        **पासवर्ड:** {mobile}
                        
                        ⚠️ **महत्त्वाची सूचना:** हा अर्ज सध्या प्रलंबित (Pending) आहे. **मा. जिल्हा अधीक्षक कृषी अधिकारी, वाशिम** यांच्या मान्यतेनंतरच (Approval) तुमचा गट या स्पर्धेत अधिकृतरीत्या सहभागी होऊ शकेल. मंजुरी मिळाल्यावर तुम्ही लॉगिन करून काम सुरु करू शकता.
                        """)
