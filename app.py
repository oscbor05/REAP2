import streamlit as st
import pandas as pd

def assess_property_complexity(r_score, e_score, a_score, p_score):
    """
    Assess the complexity of a property based on user-input scores.
    """
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

st.subheader("Enter Scores for Each Category (1-3 Scale)")
r_score = st.slider("Revenue Score", 1, 3, 1)
e_score = st.slider("Expectation Score", 1, 3, 1)
a_score = st.slider("Amenities Score", 1, 3, 1)
p_score = st.slider("Projects Score", 1, 3, 1)

if st.button("Assess Complexity"):
    result = assess_property_complexity(r_score, e_score, a_score, p_score)
    result_df = pd.DataFrame([result])
    st.dataframe(result_df)
