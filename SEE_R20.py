import streamlit as st
import pandas as pd
import random
import io

st.title("SEE R20 - CO-wise Mark Distribution Generator")

st.markdown("""
This tool generates CO-wise mark distributions for SEE exams based on input total marks.

- **Part A**: 10 Questions × 1–2 marks each (Max: 20)
- **Part B**: 5 Questions × 1–8 marks each (Max: 40)
- Total Marks can be between **1 and 60**
- Outputs a formatted Excel sheet with Q-CO mapping as column headers
""")

# Question headers
part_a_headers = ['Q1 CO1 2M', 'Q2 CO1 2M', 'Q3 CO2 2M', 'Q4 CO2 2M',
                  'Q5 CO3 2M', 'Q6 CO3 2M', 'Q7 CO4 2M', 'Q8 CO4 2M',
                  'Q9 CO5 2M', 'Q10 CO5 2M']

part_b_headers = ['Q1 CO1 8M', 'Q2 CO2 8M', 'Q3 CO3 8M', 'Q4 CO4 8M', 'Q5 CO5 8M']

def try_generate_marks(target_sum, count, max_mark):
    if target_sum == 0:
        return [""] * count
    for _ in range(500):
        values = [random.randint(1, max_mark) for _ in range(count)]
        if sum(values) == target_sum:
            return values
    return None

def generate_flexible_distribution(total):
    for _ in range(1000):
        part_a_total = random.randint(0, min(20, total))
        part_b_total = total - part_a_total

        part_a = try_generate_marks(part_a_total, 10, 2)
        part_b = try_generate_marks(part_b_total, 5, 8)

        if part_a is not None and part_b is not None:
            return part_a, part_b
    # fallback to blanks if distribution not possible
    return [""] * 10, [""] * 5

uploaded_file = st.file_uploader("📤 Upload Excel File (must include column: 'Total Marks')", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
