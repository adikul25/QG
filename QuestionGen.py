import streamlit as st
from utils import generate_questions

st.title("Question Generation App")

# Get the folder path and number of questions to generate from the user
folder_path = st.text_input("Enter the folder path:")
num_questions = st.number_input("Enter the number of questions to generate:", value=3)

# Generate the questions and download the output file
if st.button("Generate Questions"):
    with st.spinner("Generating Questions..."):
        df = generate_questions(folder_path, num_questions)
        st.success("Questions Generated!")
        st.dataframe(df)
        output_text = df.to_csv(sep="\t", index=False)
