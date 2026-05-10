import streamlit as st

# ॲपचे नाव आणि डिझाईन
st.set_page_config(page_title="FGL Washim 2026", page_icon="🌱", layout="centered")

# सेशन स्टेट (Session State) मध्ये लॉगिन माहिती सेव्ह ठेवण्यासाठी
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'must_change_password' not in st.session_state:
    st.session_state.must_change_password = False

# --- मुख्य डिझाईन ---
st.title("🌱 फार्मर ग्रुप लीग (FGL) - वाशिम २०२६")
st.markdown("---")

# १. लॉगिन पेज
if not st.session_state.logged_in and not st.session_state.must_change_password:
    st.subheader("लॉगिन करा (Login)")
    
    login_type = st.radio("तुम्ही कोण आहात?", ["शेतकरी गट (Farmer Group)", "तपासणी अधिकारी (Officer)"])
    
    if login_type == "तपासणी अधिकारी (Officer)":
        user_id = st.text_input("तुमचा आयडी टाका (उदा. AAO-101)")
    else:
        user_id = st.text_input("गटाचा नोंदणी क्रमांक टाका (Registration ID)")
        
    password = st.text_input("पासवर्ड (सुरुवातीला तुमचा मोबाईल नंबर)", type="password")
    
    if st.button("लॉगिन करा"):
        # येथे आपण भविष्यात Google Sheet मधील डेटा तपासून बघू.
        # सध्या डेमोसाठी आपण असे समजू की लॉगिन यशस्वी झाले आणि हा 'First Login' आहे.
        
        st.session_state.logged_in = True
        st.session_state.must_change_password = True # आपण त्यांना पासवर्ड बदलायला लावणार आहोत
        st.rerun()

# २. सक्तीचा पासवर्ड बदल (Force Password Change Page)
elif st.session_state.must_change_password:
    st.warning("सुरक्षेच्या कारणास्तव, कृपया तुमचा डिफॉल्ट पासवर्ड (मोबाईल नंबर) बदलून नवीन पासवर्ड सेट करा.")
    
    new_pass1 = st.text_input("नवीन पासवर्ड तयार करा", type="password")
    new_pass2 = st.text_input("नवीन पासवर्ड पुन्हा टाका (Confirm)", type="password")
    
    if st.button("पासवर्ड सेव्ह करा"):
        if new_pass1 == new_pass2 and len(new_pass1) >= 4:
            st.success("पासवर्ड यशस्वीरित्या बदलला! आता तुम्ही डॅशबोर्ड वापरू शकता.")
            # येथे आपण Google Sheet मध्ये 'Is_Password_Changed' = TRUE आणि नवीन पासवर्ड अपडेट करू.
            st.session_state.must_change_password = False
            st.rerun()
        else:
            st.error("दोन्ही पासवर्ड जुळत नाहीत किंवा खूप लहान आहेत. कृपया पुन्हा तपासा.")

# ३. डॅशबोर्ड (लॉगिन झाल्यानंतरचे पान)
elif st.session_state.logged_in and not st.session_state.must_change_password:
    st.success("लॉगिन यशस्वी!")
    st.subheader("तुमचा डॅशबोर्ड")
    st.write("येथे लवकरच तुमची माहिती आणि फॉर्म दिसेल...")
    
    if st.button("लॉगआउट (Logout)"):
        st.session_state.logged_in = False
        st.rerun()