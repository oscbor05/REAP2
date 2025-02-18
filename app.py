import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to assess property complexity
def assess_property_complexity(property_name, revenue, onboarding_status, nps_score, hospitality_service, financial_acumen, special_assessments, solvency, investment_accounts, cash_accounts, amenities, projects):
    """ Assesses the complexity of a property. """
    # Revenue Code Assignment
    revenue_code = "L" if revenue < 750000 else "M" if revenue <= 1100000 else "H"
    
    # Expectation Scores
    expectation_score_operational = sum([
        1 if nps_score >= 30 else 3,
        1 if onboarding_status == "Not onboarded / More than 90 days" else 3,
        3 if hospitality_service == "Yes" else 1
    ])
    expectation_score_operational = min(expectation_score_operational, 6)
    
    expectation_score_financial = sum([
        1 if financial_acumen == "Strong" else 2 if financial_acumen == "Moderate" else 3,
        1 if special_assessments == "No" else 3,
        1 if solvency == "Yes" else 3,
        1 if investment_accounts == "No" else 3,
        1 if cash_accounts <= 2 else 2 if cash_accounts <= 5 else 3
    ])
    expectation_score_financial = min(expectation_score_financial, 6)
    
    expectation_score = min(expectation_score_operational + expectation_score_financial, 6)
    expectation_level = "Standard" if expectation_score <= 2 else "Elevated" if expectation_score <= 4 else "High-Touch"
    
    # Amenities & Projects Score
    a_score = 1 if amenities <= 3 else 2 if amenities <= 5 else 3
    p_score = 1 if projects <= 2 else 2 if projects <= 5 else 3
    
    total_score = min(expectation_score + a_score + p_score, 9)
    final_classification = f"{revenue_code}{total_score}"
    
    return {
        "Property Name": property_name,
        "Revenue Code": revenue_code,
        "Expectation Level": expectation_level,
        "Total Score": total_score,
        "Complexity Classification": final_classification
    }

# Streamlit App Title
st.title("KWPMC REAP Calculator")

# Input Selection
st.subheader("Choose Input Method")
input_method = st.radio("Select how you want to input data:", ("Manual Entry", "Upload Excel File"))

def plot_complexity_chart(results_df):
    """Generate and display an XY chart mapping properties by revenue and complexity score."""
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
    with st.form("manual_entry_form"):
        property_name = st.text_input("Property Name")
        revenue = st.number_input("Annual Revenue ($)", min_value=0, step=10000)
        onboarding_status = st.selectbox("Onboarding Status", ["Not onboarded / More than 90 days", "New Client (Onboarded within 90 days)"])
        nps_score = st.number_input("Most Recent NPS Score", min_value=-100, max_value=100, step=1)
        hospitality_service = st.selectbox("Is this a Hospitality-Driven Property?", ["No", "Yes"])
        financial_acumen = st.selectbox("Financial Acumen of Management", ["Strong", "Moderate", "Weak"])
        special_assessments = st.selectbox("Special Assessments in Last 12 Months?", ["No", "Yes"])
        solvency = st.selectbox("Is the Association Solvent?", ["Yes", "No"])
        investment_accounts = st.selectbox("Are There Investment Accounts to Track?", ["No", "Yes"])
        cash_accounts = st.number_input("Number of Cash Accounts", min_value=1, step=1)
        amenities = st.number_input("Number of Amenities", min_value=0, step=1)
        projects = st.number_input("Number of Projects", min_value=0, step=1)
        submit_manual = st.form_submit_button("Assess Complexity")
    
    if submit_manual:
        result = assess_property_complexity(property_name, revenue, onboarding_status, nps_score, hospitality_service, financial_acumen, special_assessments, solvency, investment_accounts, cash_accounts, amenities, projects)
        result_df = pd.DataFrame([result])
        st.write("### Complexity Assessment Result")
        st.dataframe(result_df)
        plot_complexity_chart(result_df)

elif input_method == "Upload Excel File":
    st.subheader("Upload Property Data")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        results = [assess_property_complexity(**row) for _, row in df.iterrows()]
        results_df = pd.DataFrame(results)
        st.write("### Complexity Assessment Results")
        st.dataframe(results_df)
        plot_complexity_chart(results_df)
