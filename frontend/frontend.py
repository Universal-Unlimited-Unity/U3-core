import streamlit as st
import requests
import os

# Use the environment variable or default to the backend service name for Docker
API_URL = os.getenv("API_URL", "http://backend:8000/partners")

st.set_page_config(page_title="U3 Partner Registry", page_icon="🤝")

st.title("🤝 U3 Partner Registry")
st.markdown("Enter the partner details below to register them in the **U3-Core** system.")

with st.form("partner_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        last_name = st.text_input("Last Name")
        
    with col2:
        # Matches U3Gender Enum
        gender = st.selectbox("Gender", options=["M", "F"], format_func=lambda x: "Male" if x == "M" else "Female")
        
        # Matches U3Rank Enum
        loyalty = st.selectbox("Loyalty Rank", options=["Universel", "Unlimited", "Limited"])
        
        # Matches Age Field(ge=18)
        age = st.number_input("Age", min_value=18, max_value=120, value=25)

    submit = st.form_submit_button("Register Partner")

if submit:
    # Construct payload to match U3PartnerModel exactly
    payload = {
        "Gender": gender,
        "Loyalty": loyalty,
        "FirstName": first_name,
        "MiddleName": middle_name if middle_name else None,
        "LastName": last_name,
        "Age": age,
        "UnityId": None 
    }

    try:
        with st.spinner("Sending data to U3-Core..."):
            response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Partner Registered! UnityID: {result['partner']['UnityId']}")
            st.json(result)
        else:
            st.error(f"❌ API Error {response.status_code}")
            st.write(response.text)
            
    except Exception as e:
        st.error(f"Could not connect to backend at {API_URL}")
        st.info("Check if your backend container is running and the network name is correct.")