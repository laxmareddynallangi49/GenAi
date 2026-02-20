# def evaluate_loan(customer_row, requested_amount, requested_tenure):
#     """
#     Evaluate loan eligibility based on customer data.
    
#     Parameters:
#         customer_row: dict with customer info (from FAISS)
#         requested_amount: float, requested loan amount
#         requested_tenure: int, requested loan tenure in months
        
#     Returns:
#         status: "Approved" or "Rejected"
#         reason: string with reason for rejection (if any)
#     """

#     # Extract customer info
#     annual_income = customer_row.get("Annual_Income", 0)
#     credit_score = customer_row.get("Credit_Score", 0)
#     employment_years = customer_row.get("Years_of_Employment", 0)
    
#     loan_type = customer_row.get("Loan_Type", "").lower()
#     previous_status = customer_row.get("Previous_Loan_Status", "").lower()
    
#     # Basic rules (example)
#     if credit_score < 400:
#         return "Rejected", "Credit score is too low."
    
#     if requested_amount > 0.5 * annual_income:
#         return "Rejected", "Requested amount exceeds 50% of annual income."
    
#     if employment_years < 1:
#         return "Rejected", "Employment duration is too short."
    
#     if previous_status == "default":
#         return "Rejected", "Customer has previous defaulted loans."
    
#     if requested_tenure > 60:
#         return "Rejected", "Requested tenure exceeds maximum allowed (60 months)."
    
#     # If all rules passed
#     return "Approved", "Customer meets all eligibility criteria."


def evaluate_loan(customer_row, requested_amount, requested_tenure):
    annual_income = customer_row.get("Annual_Income", 0)
    credit_score = customer_row.get("Credit_Score", 0)
    employment_years = customer_row.get("Years_of_Employment", 0)
    previous_status = customer_row.get("Previous_Loan_Status", "").lower()


    if credit_score > 758:
        return "Accepted"
    if credit_score < 400:
        return "Rejected", "Credit score is too low."
    if requested_amount > 0.7 * annual_income:
        return "Rejected", "Requested amount exceeds 70% of annual income."
    if employment_years < 1 and customer_row.get("Employment", "").lower() not in ["student", "unemployed"]:
        return "Rejected", "Employment duration is too short."
    if previous_status == "defaulted":
        return "Rejected", "Customer has previous defaulted loans."
    if requested_tenure > 84:
        return "Rejected", "Requested tenure exceeds maximum allowed (84 months)."

    return "Approved", "Customer meets all eligibility criteria."