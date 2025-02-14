import streamlit as st
import pandas as pd

# Check for required dependencies
missing_dependencies = []
try:
    import matplotlib.pyplot as plt
except ImportError:
    missing_dependencies.append("matplotlib")

try:
    import openpyxl
except ImportError:
    missing_dependencies.append("openpyxl")

if missing_dependencies:
    st.error(f"Missing dependencies: {', '.join(missing_dependencies)}. Install them using `pip install {' '.join(missing_dependencies)}`.")
    st.stop()

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
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            
            required_columns = ["Property Name", "Revenue", "Expectation", "Amenities", "Projects"]
            if all(col in df.columns for col in required_columns):
                results = []
                total_scores = []
                for _, row in df.iterrows():
                    result = assess_property_complexity(row["Revenue"], row["Expectation"], row["Amenities"], row["Projects"])
                    result["Property Name"] = row["Property Name"]
                    results.append(result)
                    total_scores.append(result["Total Score"])
                
                results_df = pd.DataFrame(results)
                st.write("### Complexity Assessment Results by Property")
                st.dataframe(results_df)
                
                # Aggregate Portfolio Score
                avg_score = sum(total_scores) / len(total_scores) if total_scores else 0
                st.write(f"### Aggregate Portfolio Complexity Score: {avg_score:.2f}")
                
            else:
                st.error("Uploaded file must contain the columns: Property Name, Revenue, Expectation, Amenities, Projects")
        except Exception as e:
            st.error(f"Error processing file: {e}")
else:
    st.subheader("Enter Property Details Manually")
    property_name = st.text_input("Property Name")
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
        result["Property Name"] = property_name
        result_df = pd.DataFrame([result])
        st.write("### Complexity Assessment Result")
        st.dataframe(result_df)
