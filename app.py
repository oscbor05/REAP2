import streamlit as st
import pandas as pd

def assess_property_complexity(revenue, expectation, amenities, projects):
    """
    Assess the complexity of a property based on user inputs and predefined scoring system.
    """
    # Assign Revenue Score
    if revenue < 750000:
        r_score = 1
    elif 750000 <= revenue <= 1100000:
        r_score = 2
    else:
        r_score = 3
    
    # Assign Expectation Score
    if expectation == "No major service escalations, standard response times":
        e_score = 1
    elif expectation == "Client requires immediate responses OR hospitality service model":
        e_score = 2
    else:
        e_score = 3
    
    # Assign Amenities Score
    if amenities <= 3:
        a_score = 1
    elif 4 <= amenities <= 5:
        a_score = 2
    else:
        a_score = 3
    
    # Assign Projects Score
    if projects <= 2:
        p_score = 1
    elif 3 <= projects <= 5 or (projects > 5 and projects <= 20):
        p_score = 2
    else:
        p_score = 3
    
    # Total Complexity Score
    total_score = r_score + e_score + a_score + p_score
    
    # Alphanumeric Classification
    if total_score <= 5:
        complexity = "L3 (Low Complexity)"
    elif 6 <= total_score <= 8:
        complexity = "M6 (Medium Complexity)"
    else:
        complexity = "H9 (High Complexity)"
    
    return {
        "Revenue Score": r_score,
        "Expectation Score": e_score,
        "Amenities Score": a_score,
        "Projects Score": p_score,
        "Total Score": total_score,
        "Complexity Classification": complexity
    }

# Streamlit App
st.title("Property Complexity Assessment Tool")

# User Inputs
revenue = st.number_input("Annual Revenue ($)", min_value=0, step=10000)
expectation = st.selectbox("Expectation Level", [
    "No major service escalations, standard response times",
    "Client requires immediate responses OR hospitality service model",
    "NPS below standard, high client expectations, or newly onboarded"
])
amenities = st.number_input("Number of Amenities", min_value=1, step=1)
projects = st.number_input("Number of Projects", min_value=0, step=1)

if st.button("Assess Complexity"):
    result = assess_property_complexity(revenue, expectation, amenities, projects)
    result_df = pd.DataFrame([result])
    st.dataframe(result_df)
