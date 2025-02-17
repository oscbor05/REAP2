import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Check for required dependencies
missing_dependencies = []
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
    # Assign Revenue Alpha Code
    if revenue < 750000:
        revenue_code = "L"
    elif 750000 <= revenue <= 1100000:
        revenue_code = "M"
    else:
        revenue_code = "H"
    
    # Assign Expectation Score
    expectation_mapping = {
        "Standard": 1,
        "Elevated": 2,
        "High-Touch": 3
    }
    e_score = expectation_mapping.get(expectation, 1)
    
    # Assign Amenities Score (Allow 0 for no amenities)
    if amenities == 0:
        a_score = 0
    elif 1 <= amenities <= 3:
        a_score = 1
    elif 4 <= amenities <= 5:
        a_score = 2
    else:
        a_score = 3
    
    # Assign Projects Score (Allow 0 for no projects)
    if projects == 0:
        p_score = 0
    elif 1 <= projects <= 2:
        p_score = 1
    elif 3 <= projects <= 5:
        p_score = 2
    else:
        p_score = 3
    
    # Total Complexity Score
    total_score = e_score + a_score + p_score
    
    # Assign Complexity Classification with exact numeric score
    complexity_score = str(total_score)
    final_classification = f"{revenue_code}{complexity_score}"
    
    return {
        "Revenue Code": revenue_code,
        "Total Score": total_score,
        "Complexity Classification": final_classification
    }

# Streamlit App
st.title("KWPMC REAP Calculator")

st.subheader("Choose Input Method")
input_method = st.radio("Select how you want to input data:", ("Manual Entry", "Upload Excel File"))

def plot_complexity_chart(results_df):
    """ Generate and display an XY chart mapping properties by revenue and complexity score. """
    revenue_mapping = {"L": 500000, "M": 925000, "H": 1500000}
    
    results_df["Revenue Numeric"] = results_df["Revenue Code"].map(revenue_mapping)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(results_df["Revenue Numeric"], results_df["Total Score"], color='blue')
    
    for i, row in results_df.iterrows():
        plt.text(row["Revenue Numeric"], row["Total Score"], row["Property Name"], fontsize=9, ha='right')
    
    plt.xlabel("Revenue ($)")
    plt.ylabel("Operational Management Intensity (1-9)")
    plt.title("Property Complexity Mapping")
    plt.xticks([500000, 925000, 1500000], labels=["L ($500K)", "M ($925K)", "H ($1.5M+)"])
    plt.yticks(range(1, 10))
    plt.grid(True)
    st.pyplot(plt)

if input_method == "Upload Excel File":
    st.subheader("Upload Excel File for Bulk Assessment")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            
            required_columns = ["Property Name", "Revenue", "Expectation", "Amenities Count", "Projects Count"]
            if all(col in df.columns for col in required_columns):
                results = []
                complexity_counts = {}
                for _, row in df.iterrows():
                    result = assess_property_complexity(row["Revenue"], row["Expectation"], row["Amenities Count"], row["Projects Count"])
                    result["Property Name"] = row["Property Name"]
                    results.append(result)
                    complexity_counts[result["Complexity Classification"]] = complexity_counts.get(result["Complexity Classification"], 0) + 1
                
                results_df = pd.DataFrame(results)
                st.write("### Complexity Assessment Results by Property")
                st.dataframe(results_df)
                
                # Generate and display the complexity chart
                plot_complexity_chart(results_df)
                
                # Calculate the most frequent complexity classification
                avg_complexity = max(complexity_counts, key=complexity_counts.get)
                st.write(f"### Most Common Complexity Classification for Portfolio: {avg_complexity}")
                
            else:
                st.error("Uploaded file must contain the columns: Property Name, Revenue, Expectation, Amenities Count, Projects Count")
        except Exception as e:
            st.error(f"Error processing file: {e}")
else:
    st.subheader("Enter Property Details Manually")
    property_name = st.text_input("Property Name")
    revenue = st.number_input("Annual Revenue ($)", min_value=0, step=10000)
    expectation = st.selectbox("Expectation Level", [
        "Standard",
        "Elevated",
        "High-Touch"
    ])
    amenities = st.number_input("Number of Amenities", min_value=0, step=1)
    projects = st.number_input("Number of Projects", min_value=0, step=1)

    if st.button("Assess Complexity"):
        result = assess_property_complexity(revenue, expectation, amenities, projects)
        result["Property Name"] = property_name
        result_df = pd.DataFrame([result])
        st.write("### Complexity Assessment Result")
        st.dataframe(result_df)
