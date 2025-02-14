import streamlit as st
import pandas as pd

def assess_property_complexity(revenue, expectation, amenities, projects):
    """
    Assess the complexity of a property based on user inputs.
    """
    if revenue < 750000:
        r_score = 1
    elif 750000 <= revenue <= 1100000:
        r_score = 2
    else:
        r_score = 3
    
    e_score = min(max(expectation, 1), 3)
    a_score = min(max(amenities, 1), 3)
    p_score = min(max(projects, 1), 3)
    
    total_score = r_score + e_score + a_score + p_score
    
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

revenue = st.number_input("Annual Revenue ($)", min_value=0, step=10000)
expectation = st.slider("Expectation Level (1-3)", 1, 3, 2)
amenities = st.slider("Amenities Level (1-3)", 1, 3, 2)
projects = st.slider("Projects Level (1-3)", 1, 3, 2)

if st.button("Assess Complexity"):
    result = assess_property_complexity(revenue, expectation, amenities, projects)
    result_df = pd.DataFrame([result])
    st.dataframe(result_df)
