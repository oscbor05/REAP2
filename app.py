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

def assess_property_complexity(property_name, revenue, onboarding_status, nps_score, hospitality_service, financial_acumen, special_assessments, solvency, investment_accounts, cash_accounts, amenities, projects):
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
    
    # Assign Expectation Score - Operational Factors (Max 3 points each, Total Max 6)
    expectation_score_operational = 0
    expectation_score_operational += 1 if nps_score >= 30 else 3
    expectation_score_operational += 1 if onboarding_status == "Not onboarded / More than 90 days" else 3
    expectation_score_operational += 3 if hospitality_service == "Yes" else 1
    expectation_score_operational = min(expectation_score_operational, 6)  # Cap at 6
    
    # Assign Expectation Score - Financial Factors (Max 3 points each, Total Max 6)
    expectation_score_financial = 0
    expectation_score_financial += 1 if financial_acumen == "Strong" else 2 if financial_acumen == "Moderate" else 3
    expectation_score_financial += 1 if special_assessments == "No" else 3
    expectation_score_financial += 1 if solvency == "Yes" else 3
    expectation_score_financial += 1 if investment_accounts == "No" else 3
    expectation_score_financial += 1 if cash_accounts <= 2 else 2 if cash_accounts <= 5 else 3
    expectation_score_financial = min(expectation_score_financial, 6)  # Cap at 6
    
    # Total Expectation Score (Capped at 6)
    expectation_score = min(expectation_score_operational + expectation_score_financial, 6)
    
    # Determine Expectation Level
    if expectation_score <= 2:
        expectation_level = "Standard"
    elif expectation_score <= 4:
        expectation_level = "Elevated"
    else:
        expectation_level = "High-Touch"
    
    # Assign Amenities Score (Max 3 points)
    if amenities <= 3:
        a_score = 1
    elif 4 <= amenities <= 5:
        a_score = 2
    else:
        a_score = 3
    
    # Assign Projects Score (Max 3 points)
    if projects <= 2:
        p_score = 1
    elif 3 <= projects <= 5:
        p_score = 2
    else:
        p_score = 3
    
    # Total Complexity Score (Capped at 9)
    total_score = min(expectation_score + a_score + p_score, 9)
    
    # Assign Complexity Classification
    final_classification = f"{revenue_code}{total_score}"
    
    return {
        "Property Name": property_name,
        "Revenue Code": revenue_code,
        "Expectation Level": expectation_level,
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

if input_method == "Manual Entry":
    st.subheader("Enter Property Details Manually")
    property_name = st.text_input("Property Name")
    revenue = st.number_input("Annual Revenue ($)", min_value=0, step=10000)
    onboarding_status = st.selectbox("Onboarding Status", ["Not onboarded / More than 90 days", "New Client (Onboarded within 90 days)"])
    nps_score = st.number_input("Most Recent NPS Score", min_value=-100, max_value=100, step=1)
    hospitality_service = st.selectbox("Is this a Hospitality-Driven Property?", ["No", "Yes"])
    amenities = st.number_input("Number of Amenities", min_value=0, step=1)
    projects = st.number_input("Number of Projects", min_value=0, step=1)
    
    if st.button("Assess Complexity"):
        result = assess_property_complexity(property_name, revenue, onboarding_status, nps_score, hospitality_service, "Strong", "No", "Yes", "No", 1, amenities, projects)
        result_df = pd.DataFrame([result])
        st.write("### Complexity Assessment Result")
        st.dataframe(result_df)
        
        # Generate and display the complexity chart for a single property
        plot_complexity_chart(result_df)

if input_method == "Upload Excel File":
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        
        results = [assess_property_complexity(*row) for _, row in df.iterrows()]
        results_df = pd.DataFrame(results)
        st.write("### Bulk Complexity Assessment Results")
        st.dataframe(results_df)
        
        # Generate and display the complexity chart for all properties
        plot_complexity_chart(results_df)
