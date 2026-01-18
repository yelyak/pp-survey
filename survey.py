import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import random
import time
import base64
import json

# --- FIREBASE INITIALIZATION ---
# --- FIREBASE INITIALIZATION ---
if not firebase_admin._apps:
    if "FIREBASE_BASE64" in st.secrets:
        # Added .strip() to remove any invisible spaces from the paste
        base64_string = st.secrets["FIREBASE_BASE64"].strip() 
        
        decoded_bytes = base64.b64decode(base64_string)
        # .decode("utf-8") ensures it reads as standard text
        firebase_secrets = json.loads(decoded_bytes.decode("utf-8"))
        cred = credentials.Certificate(firebase_secrets)
    else:
        cred = credentials.Certificate("serviceAccountKey.json")
    
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ppsurveyyy-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

# --- 2. THE SURVEY UI ---
st.set_page_config(page_icon="ppsurveyfav.png")
st.image("name.png", caption="Kayley Kwok Y10J")
st.title(">personal project survey 👽")

with st.form("my_form"):
    with st.container(border=True):
        p_name = st.text_input("What is your name?")
        age = st.slider("How old are you?", 0, 80, 20)
        demog = st.radio("Are you a...", ["Primary Student ✏️", "Secondary Student 📚", "Uni Student 🎓","Teacher 📖", "Non-teacher Adult ⌚️"])
        
        st.text("What do you think of this game concept?")
        concept = st.select_slider(
        "Input your answer :)",
            options=[
                "great!! 🍇",
                "good idea",
                "alright, depending on execution",
                "...why?",
                "not needed/terrible",
            ],
        )
        conc2 = st.text_input("Please explain your answer.",key="conc")

        st.text("How does it look?")
        aesthetics = st.feedback("faces")
        aes2 = st.text_input("Please explain your answer.", key="aes2")

        st.text("How educational is this game?")
        edu = st.feedback("stars")
        edu2 = st.text_input("Please explain your answer.",key="edu2")

    with st.container(border=True):
        st.markdown("Make your own star!")
        col1, col2 = st.columns(2)

        with col1:
            p_color = st.color_picker("Star Color", "#1b2e56")
        with col2:
            p_size = st.slider("Size", 5, 50, 20)
        
    submitted = st.form_submit_button("Launch!")

    if submitted:
        # Create the data packet
        planet_data = {
            "name": p_name,
            "color": p_color,
            "size": p_size,
            "x": (random.random() - 0.5) * 8000,
            "y": (random.random() - 0.5) * 8000,
            "timestamp": int(time.time() * 1000),
            
            #to fire base
            "age": age,
            "demographic": demog,
            "concept": concept,
            "c_explanation": conc2,
            "aesthetics": aesthetics,
            "a_explanation": aes2,
            "edu": edu,
            "e_explanation": edu2
        }

        # Push to Firebase
        db.reference('planets').push(planet_data)
        st.success(f"Planet {p_name} is now in orbit!")