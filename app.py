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
    expectation_mapping = {
        "No major service escalations, standard response times": 1,
        "Client requires immediate responses OR hospitality service model": 2,
        "NPS below standard, high client expectations, or newly onboarded": 3
    }
    e_score = expectation_mapping.get(expectation, 1)
    
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
    elif 3 <= projects <= 5:
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
st.title("KWPMC REAP Calculator")

st.subheader("Choose Input Method")
input_method = st.radio("Select how you want to input data:", ("Manual Entry", "Upload Excel File"))

if input_method == "Upload Excel File":
    st.subheader("Upload Excel File for Bulk Assessment")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        required_columns = ["Revenue", "Expectation", "Amenities", "Projects"]
        if all(col in df.columns for col in required_columns):
            results = []
            for _, row in df.iterrows():
                result = assess_property_complexity(row["Revenue"], row["Expectation"], row["Amenities"], row["Projects"])
                results.append(result)
            
            results_df = pd.DataFrame(results)
            st.write("### Complexity Assessment Results")
            st.dataframe(results_df)
        else:
            st.error("Uploaded file must contain the columns: Revenue, Expectation, Amenities, Projects")
else:
    st.subheader("Enter Property Details Manually")
    revenue = st.number_input("Annual Revenue ($)", min_value=0, step=10000)
    expectation = st.selectbox("Expectation Level", [
        "No major service escalations, standard response times",
        "Client requires immediate responses OR hospitality service model",
        "NPS below standard, high client expectations, or newly onboarded"
    ])
    amenities = st.number_input("Number of Amenities", min_value=0, step=1)
    projects = st.number_input("Number of Projects", min_value=0, step=1)

    if st.button("Assess Complexity"):
        result = assess_property_complexity(revenue, expectation, amenities, projects)
        result_df = pd.DataFrame([result])
        st.write("### Complexity Assessment Result")
        st.dataframe(result_df)
