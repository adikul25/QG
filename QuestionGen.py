import os
import streamlit as st
from utils import generate_questions, generate_file_questions

st.title("Question Generation App")



# Get the file or folder path and number of questions to generate from the user
path_choice = st.selectbox("Select path type:", options=["File", "Folder"])
if path_choice == "File":
    input_path = st.file_uploader("Upload a text file:", type=["txt"])
else:
    input_path = st.file_uploader("Upload a text file:", type=["zip"])

num_questions = st.number_input("Enter the number of questions to generate:", value=3)

# Generate the questions and download the output file
if st.button("Generate Questions"):
    if input_path:
        with st.spinner("Generating Questions..."):
            if path_choice == "File":
                df = generate_file_questions(input_path, num_questions)
            else:
                df = generate_questions(input_path, num_questions)
            st.success("Questions Generated!")
            st.dataframe(df)
            output_text = df.to_csv(sep="\t", index=False)
    else:
        st.warning("Please input a file or folder path.")


