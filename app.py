import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to assess property complexity
def assess_property_complexity(property_name, revenue, onboarding_status, nps_score, hospitality_service, financial_acumen, special_assessments, solvency, investment_accounts, cash_accounts, amenities, projects):
    """ Assesses the complexity of a property. """
    revenue_code = "L" if revenue < 750000 else "M" if revenue <= 1100000 else "H"
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

st.title("KWPMC REAP Calculator")
st.subheader("Choose Input Method")
input_method = st.radio("Select how you want to input data:", ("Manual Entry", "Upload Excel File"))

def plot_complexity_chart(results_df):
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
    st.subheader("Upload Property Data")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
        df.rename(columns={
            "property_name": "property_name",
            "revenue": "revenue",
            "onboarding_status": "onboarding_status",
            "nps_score": "nps_score",
            "hospitality_service": "hospitality_service",
            "financial_acumen": "financial_acumen",
            "special_assessments": "special_assessments",
            "solvency": "solvency",
            "investment_accounts": "investment_accounts",
            "cash_accounts": "cash_accounts",
            "amenities_count": "amenities",
            "projects_count": "projects"
        }, inplace=True)
        results = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            try:
                result = assess_property_complexity(**row_dict)
                results.append(result)
            except TypeError as e:
                st.error(f"Error processing row: {row_dict}")
                st.error(f"TypeError: {e}")
        if results:
            results_df = pd.DataFrame(results)
            st.write("### Complexity Assessment Results")
            st.dataframe(results_df)
            plot_complexity_chart(results_df)
