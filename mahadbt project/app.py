# import streamlit as st
# import pandas as pd
# import joblib

# # ===============================
# # LOAD SAVED FILES
# # ===============================

# rf = joblib.load("scholarship_model.pkl")
# encoders = joblib.load("encoders.pkl")
# columns = joblib.load("columns.pkl")

# st.title("🎓 Scholarship Eligibility Predictor")

# user_data = {}
# raw_inputs = {}   # ⭐ IMPORTANT → store original values

# # ===============================
# # INPUT FIELDS
# # ===============================

# for col in columns:

#     if col in encoders:   # categorical

#         options = list(encoders[col].classes_)
#         selected = st.selectbox(f"Select {col}", options)

#         raw_inputs[col] = selected   # ⭐ save original text

#         encoded_value = encoders[col].transform([selected])[0]
#         user_data[col] = encoded_value

#     else:  # numerical

#         value = st.number_input(f"Enter {col}", value=0.0)
#         user_data[col] = value


# # ===============================
# # PREDICT
# # ===============================

# # if st.button("Predict Eligibility"):

# #     user_df = pd.DataFrame([user_data])
# #     prediction = rf.predict(user_df)[0]

# #     prediction = rf.predict(user_df)[0]

# #     caste = str(raw_inputs.get("Caste Category")).strip().lower()
# #     religion = str(raw_inputs.get("Religion")).strip().lower()
    
# #     scholarship_name = None
# #     minority_religions = ["muslim", "jain", "sikh", "christian", "buddhist", "parsi"]
    
# #     if prediction.strip().lower() == "eligible":
    
# #         if caste == "sc" and religion in ["hindu", "buddhist"]:
# #             scholarship_name = "Govt. of India Post-Matric Scholarship"

# #         elif caste == "st":
# #             scholarship_name = "Post Matric Scholarship Scheme (GOI)"
    
# #         elif caste == "obc" and religion == "hindu":
# #             scholarship_name = "Post Matric Scholarship to OBC Students"
    
# #         elif caste == "vjnt" and religion == "hindu":
# #             scholarship_name = "Post Matric Scholarship to VJNT Students"
    
# #         elif caste == "sbc" and religion == "hindu":
# #             scholarship_name = "Post Matric Scholarship to SBC Students"
    
# #         elif caste in ["open", "ews"] and religion == "hindu":
# #             scholarship_name = "Rajarshi Chhatrapati Shahu Maharaj EBC Scheme"
    
# #         elif caste == "open" and religion in minority_religions:
# #             scholarship_name = "State Minority Scholarship Part II"
    
# #         else:
# #             scholarship_name = "No Matching Scholarship"
# #             st.success("✅ The Applicant is ELIGIBLE")
# #             st.info(f"🎓 Scholarship: {scholarship_name}")

# #     else:
# #         st.error("❌ The Applicant is NOT ELIGIBLE")



# if st.button("Predict Eligibility"):

#     user_df = pd.DataFrame([user_data])
#     prediction = rf.predict(user_df)[0]

#     caste = str(raw_inputs.get("Caste Category")).strip().lower()
#     religion = str(raw_inputs.get("Religion")).strip().lower()

#     scholarship_name = None
#     minority_religions = ["muslim", "jain", "sikh", "christian", "buddhist", "parsi"]

#     if prediction.strip().lower() == "eligible":

#         if caste == "sc" and religion in ["hindu", "buddhist"]:
#             scholarship_name = "Govt. of India Post-Matric Scholarship"

#         elif caste == "st":
#             scholarship_name = "Post Matric Scholarship Scheme (GOI)"

#         elif caste == "obc" and religion == "hindu":
#             scholarship_name = "Post Matric Scholarship to OBC Students"

#         elif caste == "vjnt" and religion == "hindu":
#             scholarship_name = "Post Matric Scholarship to VJNT Students"

#         elif caste == "sbc" and religion == "hindu":
#             scholarship_name = "Post Matric Scholarship to SBC Students"

#         elif caste in ["open", "ews"] and religion == "hindu":
#             scholarship_name = "Rajarshi Chhatrapati Shahu Maharaj EBC Scheme"

#         elif caste == "open" and religion in minority_religions:
#             scholarship_name = "State Minority Scholarship Part II"

#         else:
#             scholarship_name = "No Matching Scholarship"

#         # ⭐ ALWAYS SHOW RESULT FOR ELIGIBLE
#         st.success("✅ The Applicant is ELIGIBLE")
#         st.info(f"🎓 Scholarship: {scholarship_name}")

#     else:
#         st.error("❌ The Applicant is NOT ELIGIBLE")


import streamlit as st
import pandas as pd
import joblib

# ===============================
# LOAD SAVED FILES
# ===============================
# Ensure these files exist in your directory
try:
    rf = joblib.load("scholarship_model.pkl")
    encoders = joblib.load("encoders.pkl")
    columns = joblib.load("columns.pkl")
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

st.title("🎓 Scholarship Eligibility Predictor")

user_data = {}
raw_inputs = {}   # Store original values for scholarship mapping logic

# ===============================
# INPUT FIELDS
# ===============================
for col in columns:
    if col in encoders:   # categorical columns
        options = list(encoders[col].classes_)
        selected = st.selectbox(f"Select {col}", options)
        
        raw_inputs[col] = selected   # Save original text for logic
        
        # Transform using the saved label encoder
        encoded_value = encoders[col].transform([selected])[0]
        user_data[col] = encoded_value
    else:  # numerical columns
        value = st.number_input(f"Enter {col}", value=0.0)
        user_data[col] = value

# ===============================
# PREDICT LOGIC
# ===============================
if st.button("Predict Eligibility"):
    # Create DataFrame for model prediction
    user_df = pd.DataFrame([user_data])
    
    # Get raw prediction from model
    prediction_raw = rf.predict(user_df)[0]
    
    # Normalize inputs for comparison logic
    # NOTE: Ensure 'Caste' matches the exact column name in your 'columns' list
    caste = str(raw_inputs.get("Caste", "")).strip().lower() 
    religion = str(raw_inputs.get("Religion", "")).strip().lower()

    scholarship_name = "No Matching Scholarship"
    minority_religions = ["muslim", "jain", "sikh", "christian", "buddhist", "parsi"]

    # Handle both string and numeric prediction outputs
    is_eligible = False
    if isinstance(prediction_raw, str):
        if prediction_raw.strip().lower() == "eligible":
            is_eligible = True
    elif prediction_raw == 1: # Assuming 1 is the encoded value for 'Eligible'
        is_eligible = True

    if is_eligible:
        # Scholarship Mapping Logic based on Caste and Religion
        if caste == "sc" and religion in ["hindu", "buddhist"]:
            scholarship_name = "Govt. of India Post-Matric Scholarship"

        elif caste == "st":
            scholarship_name = "Post Matric Scholarship Scheme (GOI)"

        elif caste == "obc": # Most OBC scholarships in MahaDBT are for Hindu/Others
            scholarship_name = "Post Matric Scholarship to OBC Students"

        elif caste == "vjnt":
            scholarship_name = "Post Matric Scholarship to VJNT Students"

        elif caste == "sbc":
            scholarship_name = "Post Matric Scholarship to SBC Students"

        elif caste in ["open", "ews"] and religion == "hindu":
            scholarship_name = "Rajarshi Chhatrapati Shahu Maharaj EBC Scheme"

        elif (caste in ["open", "ews"]) and (religion in minority_religions):
            scholarship_name = "State Minority Scholarship Part II"

        # Show Success Results
        st.success("✅ The Applicant is ELIGIBLE")
        st.info(f"**Recommended Scholarship:** {scholarship_name}")
    else:
        st.error("❌ The Applicant is NOT ELIGIBLE for any scholarship based on the provided details.")