import streamlit as st
from streamlit_option_menu import option_menu
import warnings
import numpy as np
import cv2
import sqlite3
import io
import database as db
from utils import readNumberPlate
import pandas as pd
import base64 

logo_path = "logo1.jpeg"

with st.sidebar:
    st.image(logo_path, width=200)
    st.title("GATE GUARD")
    st.write("Welcome to the Gate Guard")
    st.write(" Choose an option from the menu below to get started:")

    selected = option_menu('Gate Guard',
                          
                          ['About us',
                           'Show Logs',
                           'Register New Vehicle',
                           'Show Registered Vehicles'],
                          icons=['info-circle', 'file-earmark-text', 'car-front', 'clipboard-check'],
                          default_index=0)
    
if (selected == 'About us'):
    
    st.title("Welcome to Gate Guard")
    st.write("At Gate Guard, our mission is to revolutionize security by offering innovative solutions through computer vision. "
             "Our Platform  designed to enhance security and streamline access control. By leveraging state-of-the-art image processing techniques,"
             " Gate Guard can accurately detect and read vehicle number plates from user-submitted images..")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display uploaded imageif st.button("Add New Registered Vehicle"):
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        #st.image(image, caption='Uploaded Image', use_column_width=True)
        col1, col2 = st.columns([5,8])
        col1.header('Input Image')
        col1.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Detect number plate and display result
        if st.button('Detect Number Plate'):
            plate_text,score,img = readNumberPlate(image)
            col2.header('License Plate Detected')
            col2.image(img,caption='Detected Image', use_column_width=True)
            if plate_text:
                
                owner = db.check_registered_vehicle(plate_text)
                if owner:
                    st.success(f"Access granted to {owner[0]} for {plate_text}")
                    db.log_access(plate_text,owner[0])
                else:
                    st.write(plate_text)
                    st.warning(" Number Plate Not Registered")
            else:
                st.warning("Number Plate not detected")
    
    # Closing note
    st.write("Thank you for choosing Gate guard. We are committed to advancing security through technology and computer vision. "
            "Feel free to explore our features and take advantage of the insights we provide.")

if (selected == 'Show Logs'):
    
    # page title
    st.title('Logs')
    content = "Show Logs feature of the Gate Guard project provides a comprehensive and user-friendly way to review all recorded entries at the gate.Users can easily view these logs in a structured DataFrame format, ensuring all details are readily accessible and clearly displayed. Additionally, for convenience and further analysis, users can download the logs directly to their local machine."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
    
    
    # getting the input data from the user
    col1, col2, col3= st.columns([1,3,1])
    
    logs = db.get_access_logs()

    # Convert logs to DataFrame
    log_df = pd.DataFrame(logs, columns=["Number Plate", "Owner", "Time Stamp"])

    # Display DataFrame
    with col2:
        st.dataframe(log_df)  # Adjust the height as needed

    # Center align the DataFrame
        st.markdown(
            f'<style>div[data-testid="stDataFrameOutput"] div.css-1druufi.e1jpfar1 {{margin: auto;}}</style>',
            unsafe_allow_html=True)
    def download_csv():
        csv = log_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="access_logs.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

    download_csv()
    if st.button("Delete All Logs"):
        db.del_logs()

if (selected == 'Register New Vehicle'):
    
    # page title
    st.title('Register new Vehicle')
    
    content = "The Register New Vehicles feature of the Gate Guard project allows users to easily add new vehicles to the system’s database. By entering the necessary details such as the vehicle’s license plate number and the owner’s name, this feature ensures that new entries are quickly and accurately recorded"
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
    # getting the input data from the user

    with st.form("add_vehicle_form"):
        plate_number = st.text_input("License Plate Number")
        owner_name = st.text_input("Owner Name")
        submitted = st.form_submit_button("Submit")
        
        # Handling form submission
        if submitted:
            if plate_number and owner_name:
                db.add_registered_vehicle(plate_number, owner_name)
                st.success(f"Added {plate_number} for {owner_name}")
            else:
                st.error("Both fields are required")
    

if (selected == "Show Registered Vehicles"):
    st.title("Registered Vehicles")
    content="The Show All Registered Vehicles feature of the Gate Guard project provides a comprehensive overview of all vehicles currently registered in the system. This feature displays a list of registered vehicles, including their license plate numbers and owner names."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
    logs = db.get_registered_vehicles()
    col1, col2= st.columns(2)
    with col1:
        st.header("Plate Number")
    with col2:
        st.header("Owner")
    for log in logs:
        with col1:
            st.write(log[0])
        with col2:
            st.write(log[1])