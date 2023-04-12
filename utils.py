import os
import random
import csv
import streamlit as st
from transformers import T5Config, T5ForConditionalGeneration, T5Tokenizer

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

# Define the function to generate questions

def generate_questions(folder_path, num_questions):
    # set output file path
    output_file_path = "generated_questions.csv"

    # open output file for writing
    with open(output_file_path, "w", newline="") as csvfile:
        fieldnames = ["file_name", "generated_question"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # loop through files in folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    random.shuffle(lines)
                    generated_questions = 0
                    for line in lines:
                        # split line into chunks of max length 512
                        line_chunks = [line[i:i+2048] for i in range(0, len(line), 2048)]
                        for chunk in line_chunks:
                            if chunk.strip() and not chunk.isspace():
                                questions = run_model(f"generate questions: {chunk}")
                                for question in questions:
                                    writer.writerow({"file_name": file_name, "generated_question": question})
                                    generated_questions += 1
                                    if generated_questions >= num_questions:
                                        break
                                if generated_questions >= num_questions:
                                    break
                            if generated_questions >= num_questions:
                                break
                        if generated_questions >= num_questions:
                            break


    return output_file_path


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
