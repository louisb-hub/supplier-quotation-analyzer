
import pandas as pd

# ==========================================
# STEP 1: LOAD THE RFQ AND SUPPLIER QUOTATIONS
# ==========================================
rfq_data = pd.read_excel("RFQ_2026_014.xlsx", skiprows=7)

supplier_a = pd.read_excel("Quotation A.xlsx", skiprows=6)
supplier_b = pd.read_excel("Quotation B.xlsx", skiprows=6)
supplier_c = pd.read_excel("Quotation C.xlsx", skiprows=6)
supplier_d = pd.read_excel("Quotation D.xlsx", skiprows=6)


# ==========================================
# STEP 2: MATCH EACH QUOTATION WITH THE RFQ
# ==========================================
comparison_a = rfq_data.merge(supplier_a, how="left", on="Item Code")
comparison_b = rfq_data.merge(supplier_b, how="left", on="Item Code")
comparison_c = rfq_data.merge(supplier_c, how="left", on="Item Code")
comparison_d = rfq_data.merge(supplier_d, how="left", on="Item Code")


# ==========================================
# STEP 3: CHECK WHETHER THE QUOTED QUANTITY IS SUFFICIENT
# ==========================================
comparison_a["Quantity Available"] = (
    comparison_a["Quoted Quantity"] >= comparison_a["Quantity"])

comparison_b["Quantity Available"] = (
    comparison_b["Quoted Quantity"] >= comparison_b["Quantity"])

comparison_c["Quantity Available"] = (
    comparison_c["Quoted Quantity"] >= comparison_c["Quantity"])

comparison_d["Quantity Available"] = (
    comparison_d["Quoted Quantity"] >= comparison_d["Quantity"])



# ==========================================
# STEP 4: IDENTIFY ITEMS NOT QUOTED BY EACH SUPPLIER
# ==========================================
missing_row_a = comparison_a[
    comparison_a["Quoted Quantity"].isna()][["Item Code", "Product", "Quoted Quantity"]]

missing_row_b = comparison_b[
    comparison_b["Quoted Quantity"].isna()][["Item Code", "Product", "Quoted Quantity"]]

missing_row_c = comparison_c[
    comparison_c["Quoted Quantity"].isna()][["Item Code", "Product", "Quoted Quantity"]]

missing_row_d = comparison_d[
    comparison_d["Quoted Quantity"].isna()][["Item Code", "Product", "Quoted Quantity"]]


# ==========================================
# STEP 5: IDENTIFY SPECIFICATION NONCOMPLIANCE
# ==========================================
no_meet_requirements_a = comparison_a[
    comparison_a["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
]

no_meet_requirements_b = comparison_b[
    comparison_b["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
]

no_meet_requirements_c = comparison_c[
    comparison_c["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
]

no_meet_requirements_d = comparison_d[
    comparison_d["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
]


# ==========================================
# STEP 6: CALCULATE THE QUOTED PRODUCT TOTAL
# ==========================================
comparison_a["Quoted Total"] = (
    comparison_a["Quoted Quantity"] * comparison_a["Unit Price"]
)
comparison_b["Quoted Total"] = (
    comparison_b["Quoted Quantity"] * comparison_b["Unit Price"]
)
comparison_c["Quoted Total"] = (
    comparison_c["Quoted Quantity"] * comparison_c["Unit Price"]
)
comparison_d["Quoted Total"] = (
    comparison_d["Quoted Quantity"] * comparison_d["Unit Price"]
)


# ==========================================
# STEP 7: DETERMINE ELIGIBILITY FOR EACH ITEM
# ==========================================
comparison_a["Eligible"] = (
    comparison_a["Quoted Quantity"].notna()
    & comparison_a["Quantity Available"]
    & ~comparison_a["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
)

comparison_b["Eligible"] = (
    comparison_b["Quoted Quantity"].notna()
    & comparison_b["Quantity Available"]
    & ~comparison_b["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
)

comparison_c["Eligible"] = (
    comparison_c["Quoted Quantity"].notna()
    & comparison_c["Quantity Available"]
    & ~comparison_c["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
)

comparison_d["Eligible"] = (
    comparison_d["Quoted Quantity"].notna()
    & comparison_d["Quantity Available"]
    & ~comparison_d["Specification Compliance"].str.contains(
        "No", case=False, na=False
    )
)


# ==========================================
# STEP 8: VERIFY SUPPLIER D'S CHAIR QUOTATION
# ==========================================
# print(
#     comparison_d[comparison_d["Item Code"] == "FN-001"][
#         [
#             "Item Code",
#             "Quantity",
#             "Quoted Quantity",
#             "Quantity Available",
#             "Specification Compliance",
#             "Eligible",
#         ]
#     ]
# )

print(comparison_a[["Item Code", "Eligible"]])
print(comparison_b[["Item Code", "Eligible"]])
print(comparison_c[["Item Code", "Eligible"]])
print(comparison_d[["Item Code", "Eligible"]])

def supplier_report():
    print("Supplier summary")
