import streamlit as st
from streamlit_gsheets import GSheetsConnection # ही लायब्ररी कनेक्शनसाठी लागेल

# १. कनेक्शन प्रस्थापित करणे
conn = st.connection("gsheets", type=GSheetsConnection)

# २. डेमो ग्राफिक डेटा वाचणे (Demographic_data शीटमधून)
@st.cache_data(ttl=600) # १० मिनिटे डेटा कॅशमध्ये राहील
def get_village_data():
    return conn.read(worksheet="Demographic_data")

df_demo = get_village_data()

# --- नोंदणी फॉर्ममध्ये बदलांचे लॉजिक ---
with tab2:
    st.markdown("<h4 style='text-align: center;'>नोंदणी अर्ज: FGL-२०२६</h4>", unsafe_allow_html=True)
    
    with st.form("reg_form", clear_on_submit=True):
        # अ) भौगोलिक माहिती (एक्सेल शीटवरून ऑटोमॅटिक)
        st.write("📍 **Geographical Info**")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            dist = st.selectbox("District", df_demo['District'].unique())
        with col_b:
            # निवडलेल्या जिल्ह्यानुसार तालुके फिल्टर करणे
            filtered_taluka = df_demo[df_demo['District'] == dist]['Taluka'].unique()
            selected_taluka = st.selectbox("Taluka", filtered_taluka)
        with col_c:
            # निवडलेल्या तालुक्यानुसार गावे फिल्टर करणे
            filtered_villages = df_demo[df_demo['Taluka'] == selected_taluka]['Village'].unique()
            selected_village = st.selectbox("Village", filtered_villages)

        # ... (गटाची इतर माहिती आधीप्रमाणेच राहील) ...

        submitted = st.form_submit_button("अर्ज सादर करा")
        
        if submitted:
            # ३. डेटा शीटमध्ये लिहिणे (Append Data)
            new_data = {
                "Registration_ID": f"FGL-{mobile[-4:]}",
                "Group_Name": group_name,
                "District": dist,
                "Taluka": selected_taluka,
                "Village": selected_village,
                "Mobile_No": mobile,
                "Password": mobile,
                "Approval_Status": "Pending", # सुरुवातीला प्रलंबित
                "Is_Password_Changed": "FALSE"
            }
            
            # Google Sheet मध्ये डेटा अपडेट करणे
            try:
                conn.create(worksheet="Registration", data=[new_data])
                st.balloons()
                st.success("अर्ज यशस्वीरित्या सादर! मा. DSAO यांच्या मंजुरीनंतर लॉगिन करता येईल.")
            except Exception as e:
                st.error("डेटा सेव्ह करताना त्रुटी आली. कृपया इंटरनेट तपासा.")
