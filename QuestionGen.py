# import streamlit as st
# from utils import generate_questions

# st.title("Question Generation App")

# # Get the folder path and number of questions to generate from the user
# folder_path = st.text_input("Enter the folder path:")
# num_questions = st.number_input("Enter the number of questions to generate:", value=3)

# # Generate the questions and download the output file
# if st.button("Generate Questions"):
#     with st.spinner("Generating Questions..."):
#         df = generate_questions(folder_path, num_questions)
#         st.success("Questions Generated!")
#         st.dataframe(df)
#         output_text = df.to_csv(sep="\t", index=False)

import os
import streamlit as st
from utils import generate_questions

st.title("Question Generation App")

# Get the zip file and number of questions to generate from the user
zip_file = st.file_uploader("Upload a zip file containing text files:", type="zip")
num_questions = st.number_input("Enter the number of questions to generate:", value=3)

# Generate the questions and download the output file
if st.button("Generate Questions"):
    if zip_file is not None:
        with st.spinner("Generating Questions..."):
            df = generate_questions(zip_file, num_questions)
            st.success("Questions Generated!")
            st.dataframe(df)
            output_text = df.to_csv(sep="\t", index=False)
    else:
        st.warning("Please upload a zip file containing text files.")
        #clipboard.copy(output_text)
        #st.info("The generated questions have been copied to the clipboard as tab-separated text.")

