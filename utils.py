import os
import random
import csv
import streamlit as st
from transformers import T5Config, T5ForConditionalGeneration, T5Tokenizer
import sentencepiece
import torch
import pandas as pd

# Define the T5 model and tokenizer
model_name = "allenai/t5-small-squad2-question-generation"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Define the function to run the T5 model
def run_model(input_string, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt")
    res = model.generate(input_ids, **generator_args)
    output = tokenizer.batch_decode(res, skip_special_tokens=True)
    return output



def generate_questions(folder_path, num_questions):
    # create an empty list to hold the generated questions
    generated_questions = []
    

    # loop through files in folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as f:
                lines = f.readlines()
                random.shuffle(lines)
                generated_questions_count = 0
                for line in lines:
                    # split line into chunks of max length 2048
                    line_chunks = [line[i:i+2048] for i in range(0, len(line), 2048)]
                    for chunk in line_chunks:
                        if chunk.strip() and not chunk.isspace():
                            questions = run_model(f"generate questions: {chunk}")
                            for question in questions:
                                generated_questions.append({"file_name": file_name, "generated_question": question})
                                generated_questions_count += 1
                                if generated_questions_count >= num_questions:
                                    break
                            if generated_questions_count >= num_questions:
                                break
                        if generated_questions_count >= num_questions:
                            break
                    if generated_questions_count >= num_questions:
                        break

    # convert the list of generated questions to a Pandas DataFrame
    df = pd.DataFrame(generated_questions)

    return df


#
# # Define the Streamlit app
# def main():
#     st.title("Question Generation App")
#
#     # Get the folder path and number of questions to generate from the user
#     folder_path = st.text_input("Enter the folder path:")
#     num_questions = st.number_input("Enter the number of questions to generate:", value=3)
#
#     # Generate the questions and download the output file
#     if st.button("Generate Questions"):
#         with st.spinner("Generating Questions..."):
#             output_file_path = generate_questions(folder_path, num_questions)
#             st.success("Questions Generated!")
#             st.download_button(
#                 label="Download Questions",
#                 data=open(output_file_path, "rb").read(),
#                 file_name=output_file_path,
#                 mime="text/csv"
#             )
#
# # Run the Streamlit app
# if __name__ == "__main__":
#     main()
