import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from openpyxl import Workbook

st.set_page_config(page_title="🎓 Student Data & Analysis App 📊", page_icon="📚")

st.title("🎓 Student Data Management & Analysis App 📈📚✨")

# Excel file setup
file_path = 'student_data.xlsx'
if not os.path.exists(file_path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Roll Number", "Class", "Marks"])
    wb.save(file_path)

# Data Entry Form
with st.form("student_form"):
    st.subheader("📝 Add New Student Data")
    name = st.text_input("👦 Student Name")
    roll = st.text_input("🔢 Roll Number")
    s_class = st.selectbox("🏫 Class", ["5th", "6th", "7th", "8th", "9th", "10th"])
    marks = st.number_input("📊 Marks (out of 100)", min_value=0, max_value=100)

    submit = st.form_submit_button("💾 Save Data")

    if submit:
        if name and roll:
            df = pd.read_excel(file_path)
            new_data = {"Name": name, "Roll Number": roll, "Class": s_class, "Marks": marks}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(file_path, index=False)
            st.success("✅ Data Saved Successfully! 🎉")
        else:
            st.error("⚠️ Please fill in all fields!")

# Load Data
df = pd.read_excel(file_path)

# Show All Data
if st.button("📂 Show All Student Data"):
    st.subheader("📜 Student Records")
    st.dataframe(df)

# Filter by Class
st.subheader("🔎 Filter Data by Class")
class_filter = st.multiselect("Choose Class", df['Class'].unique())
if class_filter:
    filtered_data = df[df['Class'].isin(class_filter)]
    st.write(filtered_data)
else:
    filtered_data = df

# Data Analysis Section
st.subheader("📈 Data Analysis & Visualization")

# Marks Distribution Plot
if st.checkbox("🎯 Show Marks Distribution"):
    fig, ax = plt.subplots()
    sns.histplot(filtered_data['Marks'], bins=10, kde=True, color='skyblue')
    plt.xlabel("Marks")
    plt.ylabel("Number of Students")
    plt.title("Marks Distribution 🎯")
    st.pyplot(fig)

# Bar Chart Class vs Average Marks
if st.checkbox("🏫 Show Average Marks by Class"):
    class_avg = filtered_data.groupby('Class')['Marks'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=class_avg, x='Class', y='Marks', palette='viridis')
    plt.title("📊 Average Marks per Class")
    st.pyplot(fig)

# Pie Chart - Pass/Fail
if st.checkbox("✅📉 Show Pass/Fail Pie Chart"):
    filtered_data['Result'] = filtered_data['Marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
    result_count = filtered_data['Result'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(result_count, labels=result_count.index, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    plt.title("Pass vs Fail Ratio 🎯")
    st.pyplot(fig)

# General Stats
if st.checkbox("📊 Show General Stats"):
    st.write("✅ Total Students:", len(filtered_data))
    st.write("✅ Average Marks:", round(filtered_data['Marks'].mean(), 2))
    st.write("✅ Highest Marks:", filtered_data['Marks'].max())
    st.write("✅ Lowest Marks:", filtered_data['Marks'].min())

st.markdown("---")
st.markdown("📌 *App created for student data management & analysis with love ❤️ by Ammara*")
# Hidden credit line for Ammara
st.markdown('<p style="color:white; font-size:8px;">This app is created by Ammara</p>', unsafe_allow_html=True)

