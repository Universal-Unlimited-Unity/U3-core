import streamlit as st
import requests
import os
import pandas as pd
API_URL = os.getenv("API_URL", "http://backend:8000/partners")

st.set_page_config(page_title="U3 Partner Registry", page_icon="🤝")

st.title("🤝 U3 Partner Registry")

st.sidebar.title("Settings")
sb = st.sidebar.radio("CRUD Operations", ["Add Partner", "Delete Partner", "Show Partner", "Update Partner"])
if sb == "Add Partner":

    st.markdown("Enter the partner details below to register them in the **U3-Core** system.")
    
    with st.form("Add Partner"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            middle_name = st.text_input("Middle Name (Optional)")
            last_name = st.text_input("Last Name")
            
        with col2:
            gender = st.selectbox("Gender", options=["M", "F"])
            
            loyalty = st.selectbox("Loyalty Rank", options=["Universel", "Unlimited", "Limited"])
            
            age = st.number_input("Age", min_value=18)
    
        submit = st.form_submit_button("Register Partner")
    
    if submit:
        if not all([first_name, last_name, gender, loyalty, age]):
            st.warning("Please Enter Values in the Required Fields")
        else:
            payload = {
                "Gender": gender,
                "Loyalty": loyalty,
                "FirstName": first_name.title(),
                "MiddleName": middle_name.title() if middle_name else None,
                "LastName": last_name.title(),
                "Age": age,
                "UnityId": None 
            }
        
            try:
                with st.spinner("Sending data to U3-Core..."):
                    response = requests.post(API_URL, json=payload)
                    result = response.json()
                if response.status_code == 200:
                    st.success(f"Partner Registered!")
                    with st.spinner("Loading Partners's Info..."):
                        st.dataframe([result])
                else:
                    st.error(f"API Error {response.status_code}")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Could not connect to backend at {API_URL}")
                st.info("Check if your backend container is running and the network name is correct.")

if sb == "Delete Partner":
    st.markdown("Enter the UnityID of a partner to delete them")
    with st.form("Delete Partner"):

        UnityId = st.text_input("Unity Id")
        submit = st.form_submit_button("Delete")
        if submit:
            if not UnityId:
                st.warning("Please Enter The UnityId")
            else: 
                if UnityId.title() != "All":
                    try:
                        with st.spinner("Deleting..."):
                            p = requests.get(f"{API_URL}/{UnityId}")
                            response = requests.delete(f"{API_URL}/{UnityId}")
        
                            if response.status_code == 200:
                                if response.json() == 0:
                                    st.toast(f"Partner with {UnityId} as a UnityId Was **Deleted**", icon="✅")
                                    st.write("This is the Partner that was deleted")
                                    st.dataframe([p.json()])
                                else:
                                    st.error("Partner Not Found")
                
                    except Exception as e:
                        st.error(f"Somthing went wrong in the backend: {response.text}")
                else:
                    st.error("You can't delete all partners at once")
                    

if sb == "Show Partner":
    st.markdown("Enter the UnityId of a Partner to search for it or all to search for all Partners")
    with st.form("Show Partner Infos"):
        UnityId = st.text_input("UnityId")
        submit = st.form_submit_button("Search")
        if submit:
            if UnityId:
                try:
                    if UnityId.lower() == "all":
                        msg = "There you go! All partners"
                    else:
                        msg = "Partner Found!"
                    with st.spinner("Searching..."):
                        response = requests.get(f"{API_URL}/{UnityId}")
                    if response.status_code == 200:
                        st.success(msg)
                        result = response.json()
                        with st.spinner("Loading Partners's Info..."):
                            st.dataframe(result)
                    elif response.status_code == 404 and UnityId.lower() == "all":
                        st.info("The Partners's relational is **empty**")
                    elif response.status_code == 404:
                        st.error("Partner Not Found")
                except Exception as e:
                    sr.error(f"Somthing went wrong in the backend: {response.text}")
            else:
                st.warning("Please Enter the UnityId")
                    

if sb == "Update Partner":
    st.markdown("Enter the UnityId of the partner to update their infos. If you don't want to update a field, leave it empty.")

    with st.form("Update Partner"):
        UnityId = st.text_input("UnityId")
        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("First Name")
            middle_name = st.text_input("Middle Name")
            last_name = st.text_input("Last Name")

        with col2:
            gender = st.selectbox("Gender", options=["", "M", "F"])
            loyalty = st.selectbox("Loyalty Rank", options=["","Universel", "Unlimited", "Limited"])
            age = st.number_input("Age", min_value=18)

        submit = st.form_submit_button("Update Partner")

    if submit:
        if not UnityId:
            st.warning("Please Enter UnityId")
        else:
            payload = {
                "Gender": gender if gender else None,
                "Loyalty": loyalty if loyalty else None,
                "FirstName": first_name.title() if first_name else None,
                "MiddleName": middle_name.title() if middle_name else None,
                "LastName": last_name.title() if last_name else None,
                "Age": age if age else None,
            }

            try:
                with st.spinner("Searching and updating partner..."):
                    response = requests.patch(f"{API_URL}/{UnityId}", json=payload)

                if response.status_code == 200:
                    result = response.json()
                    st.success("Partner updated successfully!")
                    st.dataframe([result])
                elif response.status_code == 404:
                    st.error("Partner Not Found")
                else:
                    st.error(f"Error : {response.text}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")