import streamlit as st
import pandas as pd
import random
import io

st.title("SEE R20 - Marks Distribution Generator")

st.markdown("""
This tool divides **Total Marks** into:
- **Part A**: 10 Questions × 1–2 Marks (Total = 10 Marks)
- **Part B**: 5 Questions × 1–8 Marks (Total = Input Marks - 10)
- Input via Excel. Download the result as a new Excel file.
- **Total Marks must be between 11 and 60**.
""")

def generate_part_a():
    # Generate 10 numbers of 1 or 2 such that their sum is exactly 10
    while True:
        values = [random.choice([1, 2]) for _ in range(10)]
        if sum(values) == 10:
            return values

def generate_part_b(total_b):
    attempts = 0
    while attempts < 1000:
        values = [random.randint(1, 8) for _ in range(5)]
        if sum(values) == total_b:
            return values
        attempts += 1
    return None

def generate_distribution(total_mark):
    if not (11 <= total_mark <= 60):
        return None, None

    part_a = generate_part_a()
    part_b_total = total_mark - 10
    part_b = generate_part_b(part_b_total)
    if part_b is None:
        return None, None
    return part_a, part_b

uploaded_file = st.file_uploader("📤 Upload Excel File (with column: Total Marks)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if 'Total Marks' not in df.columns:
        st.error("Excel file must have a column named 'Total Marks'")
    else:
        st.success("File uploaded successfully. Generating distributions...")

        results = []
        for idx, row in df.iterrows():
            total = row['Total Marks']
            part_a, part_b = generate_distribution(total)
            if part_a and part_b:
                results.append({
                    'Total Marks': total,
                    'Part A Distribution': str(part_a),
                    'Part B Distribution': str(part_b)
                })
            else:
                results.append({
                    'Total Marks': total,
                    'Part A Distribution': '❌ Invalid',
                    'Part B Distribution': '❌ Invalid'
                })

        result_df = pd.DataFrame(results)

        st.dataframe(result_df)

        # Prepare to export as Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, sheet_name='SEE Distribution')
        output.seek(0)

        st.download_button(
            label="📥 Download Distribution Excel",
            data=output,
            file_name="SEE_Mark_Distributions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

