import streamlit as st

# १. पेजची प्राथमिक सेटिंग (हे नेहमी कोडच्या सर्वात वर असावे)
st.set_page_config(page_title="FGL Washim 2026", page_icon="🌱", layout="centered")

# २. सेशन स्टेट्स (युजरची माहिती लक्षात ठेवण्यासाठी)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'must_change_password' not in st.session_state:
    st.session_state.must_change_password = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""

# ३. --- हेडर आणि लोगो डिझाईन ---
# ३ कॉलम तयार केले जेणेकरून ३ लोगो एका ओळीत दिसतील
col1, col2, col3 = st.columns([1, 1.5, 1])

with col1:
    # st.image("agri_logo.png", use_container_width=True)  # जेव्हा फोटो GitHub वर टाकाल तेव्हा या ओळीपुढची # काढून टाका.
    st.markdown("<h4 style='text-align: center; color: green;'>कृषी विभाग</h4>", unsafe_allow_html=True)

with col2:
    # st.image("fgl_logo.png", use_container_width=True)
    st.markdown("<h3 style='text-align: center; color: darkgreen;'>FGL २०२६</h3>", unsafe_allow_html=True)

with col3:
    # st.image("atma_logo.png", use_container_width=True)
    st.markdown("<h4 style='text-align: center; color: orange;'>ATMA वाशिम</h4>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #2e7b32;'>फार्मर ग्रुप लीग - वाशिम २०२६</h2>", unsafe_allow_html=True)
st.markdown("---")

# ४. --- मुख्य लॉजिक (लॉगिन आणि नोंदणी) ---

# जर युजर लॉगिन नसेल आणि पासवर्ड बदलायची वेळ नसेल, तर वेलकम पेज दाखवा
if not st.session_state.logged_in and not st.session_state.must_change_password:
    
    # दोन सुंदर टॅब तयार करणे
    tab1, tab2 = st.tabs(["🔐 लॉगिन (Login)", "📝 नवीन गट नोंदणी (Register)"])
    
    # --- टॅब १: लॉगिन ---
    with tab1:
        st.subheader("तुमच्या खात्यात प्रवेश करा")
        login_id = st.text_input("युजर आयडी (उदा. FGL-001 किंवा AAO-101)")
        password = st.text_input("पासवर्ड", type="password")
        
        if st.button("लॉगिन करा", type="primary", use_container_width=True):
            # (येथे आपण भविष्यात Google Sheet जोडणार आहोत. सध्या हे डेमो लॉजिक आहे.)
            
            # जर पासवर्ड १० अंकी मोबाईल नंबर असेल (म्हणजेच First Login)
            if len(password) == 10 and password.isdigit(): 
                st.session_state.must_change_password = True
                st.session_state.user_id = login_id
                st.rerun()
            
            # जर जुना युजर असेल ज्याने आधीच पासवर्ड बदलला आहे (डेमो पासवर्ड: 1234)
            elif password == "1234": 
                st.session_state.logged_in = True
                st.session_state.user_id = login_id
                st.rerun()
            else:
                st.error("चुकीचा आयडी किंवा पासवर्ड!")

    # --- टॅब २: नवीन गट नोंदणी ---
    with tab2:
        st.subheader("नवीन शेतकरी गट नोंदणी")
        st.info("नोंदणी २० मे २०२६ पर्यंतच खुली आहे. त्वरित नोंदणी करा!")
        
        new_group_name = st.text_input("गटाचे नाव")
        new_mobile = st.text_input("गट प्रमुखाचा मोबाईल नंबर (हाच तुमचा डिफॉल्ट पासवर्ड असेल)", max_chars=10)
        
        if st.button("नोंदणी पूर्ण करा", type="primary", use_container_width=True):
            if new_group_name and len(new_mobile) == 10 and new_mobile.isdigit():
                st.success(f"अभिनंदन! '{new_group_name}' ची नोंदणी यशस्वी झाली.")
                st.markdown("""
                **तुमचा युजर आयडी:** `FGL-101` *(हा आयडी सिस्टीमने तयार केला आहे. कृपया लिहून ठेवा)* **तुमचा पासवर्ड:** `तुमचा मोबाईल नंबर`
                """)
                st.warning("कृपया आता 'लॉगिन' टॅबवर जा, तुमचा आयडी व मोबाईल नंबर टाकून लॉगिन करा आणि लगेच तुमचा पासवर्ड बदला.")
            else:
                st.error("कृपया गटाचे नाव आणि अचूक १० अंकी मोबाईल नंबर भरा.")

# ५. --- सक्तीचा पासवर्ड बदल (Force Password Change) ---
elif st.session_state.must_change_password:
    st.markdown(f"<h3 style='text-align: center;'>स्वागत आहे {st.session_state.user_id}!</h3>", unsafe_allow_html=True)
    st.warning("सुरक्षेच्या कारणास्तव, सिस्टीम वापरण्यापूर्वी कृपया तुमचा नवीन पासवर्ड सेट करा.")
    
    new_pass1 = st.text_input("नवीन पासवर्ड तयार करा", type="password")
    new_pass2 = st.text_input("नवीन पासवर्ड पुन्हा टाका (Confirm)", type="password")
    
    if st.button("पासवर्ड सेव्ह करा", type="primary"):
        if new_pass1 == new_pass2 and len(new_pass1) >= 4:
            st.success("पासवर्ड यशस्वीरित्या बदलला! आता तुम्ही मुख्य डॅशबोर्ड वापरू शकता.")
            # (भविष्यात इथे आपण Google Sheet मध्ये TRUE अपडेट करू)
            st.session_state.must_change_password = False
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("पासवर्ड जुळत नाहीत किंवा ४ अक्षरांपेक्षा लहान आहेत. कृपया पुन्हा प्रयत्न करा.")

# ६. --- मुख्य डॅशबोर्ड (लॉगिन झाल्यावर दिसणारे पेज) ---
elif st.session_state.logged_in:
    st.success("लॉगिन यशस्वी!")
    st.header("डॅशबोर्ड: फार्मर ग्रुप लीग २०२६")
    st.write(f"**युजर आयडी:** {st.session_state.user_id}")
    st.write("येथे तुमची प्रलंबित कामे, तपासणी किंवा नवीन ऍक्टिव्हिटी भरण्याचा फॉर्म दिसेल...")
    
    # लॉगआउट बटण
    if st.button("लॉगआउट (Logout)"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.rerun()
