import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://backend:8000/partners")

st.set_page_config(page_title="U3 Partner Registry", page_icon="🤝")

st.title("🤝 U3 Partner Registry")

st.sidebar("Settings")
sb = st.sidebar.radio("CRUD Operations", ["Add Partner", "Delete Partner"]
if sb = "Add Partner":

    st.markdown("Enter the partner details below to register them in the **U3-Core** system.")
    
    with st.form("partner_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            middle_name = st.text_input("Middle Name (Optional)")
            last_name = st.text_input("Last Name")
            
        with col2:
            gender = st.selectbox("Gender", options=["M", "F"]")
            
            loyalty = st.selectbox("Loyalty Rank", options=["Universel", "Unlimited", "Limited"])
            
            age = st.number_input("Age", min_value=18)
    
        submit = st.form_submit_button("Register Partner")
    
    if submit:
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
                st.success(f"Partner Registered! UnityID: {result['partner']['UnityId']}")
                st.json(result)
            else:
                st.error(f"API Error {response.status_code}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Could not connect to backend at {API_URL}")
            st.info("Check if your backend container is running and the network name is correct.")

if sb = "Delete Partner":
    st.markdown("Enter the UnityID of a partner to delete them")
    UnityId = st.text_input("Unity Id")
    API_URL += str(UnityId)
    with st.spinner("Deleting..."):
        response = requests.delete(API_URL)
        if response.status_code == 200 and not reponse:
            st.success(f"Partner with {UnityId} as a UnityId Was **Deleted**)
        else:
            st.error("Somthing is wrong with the DataBase or partner does not exist")
            
