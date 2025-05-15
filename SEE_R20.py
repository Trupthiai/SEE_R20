import streamlit as st
import pandas as pd
import random
import io

st.title("SEE R20 - Marks Distribution Generator (CO-wise Format)")

st.markdown("""
**Features:**
- Part A: 10 Questions × 2 Marks = 20 Marks (CO1–CO5 × 2)
- Part B: 5 Questions × 8 Marks = 40 Marks (CO1–CO5)
- Accepts input Excel file with column `Total Marks` (1–60)
- Returns formatted Excel with CO-mapped questions and mark distribution
""")

# Labels
part_a_cols = ['Q1 CO1 2M', 'Q2 CO1 2M', 'Q3 CO2 2M', 'Q4 CO2 2M',
               'Q5 CO3 2M', 'Q6 CO3 2M', 'Q7 CO4 2M', 'Q8 CO4 2M',
               'Q9 CO5 2M', 'Q10 CO5 2M']
part_b_cols = ['Q1 CO1 8M', 'Q2 CO2 8M', 'Q3 CO3 8M', 'Q4 CO4 8M', 'Q5 CO5 8M']

def generate_part_a(total_a):
    # Generate distribution of 10 values between 1–2 that sum to total_a
    attempts = 0
    while attempts < 1000:
        values = [random.choice([1, 2]) for _ in range(10)]
        if sum(values) == total_a:
            return values
        attempts += 1
    return ['-'] * 10

def generate_part_b(total_b):
    attempts = 0
    while attempts < 1000:
        values = [random.randint(1, 8) for _ in range(5)]
        if sum(values) == total_b:
            return values
        attempts += 1
    return ['-'] * 5

uploaded_file = st.file_uploader("📤 Upload Excel File (with column: Total Marks)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if 'Total Marks' not in df.columns:
        st.error("❌ Excel file must have a column named 'Total Marks'")
    else:
        st.success("✅ File uploaded. Generating mark distributions...")

        output_rows = []
        for idx, row in df.iterrows():
            total = int(row['Total Marks'])

            part_a_total = min(total, 20)
            part_b_total = max(0, total - 20)

            part_a = generate_part_a(part_a_total) if part_a_total > 0 else ['-'] * 10
            part_b = generate_part_b(part_b_total) if part_b_total > 0 else ['-'] * 5

            full_row = part_a + part_b
            output_rows.append(full_row)

        output_df = pd.DataFrame(output_rows, columns=part_a_cols + part_b_cols)
        output_df.insert(0, 'Total Marks', df['Total Marks'])

        st.dataframe(output_df)

        # Export Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            output_df.to_excel(writer, index=False, sheet_name='SEE_Distribution_CO')
        output.seek(0)

        st.download_button(
            label="📥 Download CO-wise Distribution Excel",
            data=output,
            file_name="SEE_Mark_Distributions_CO.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
