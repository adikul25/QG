import os
import random
import csv
import streamlit as st
from transformers import T5Config, T5ForConditionalGeneration, T5Tokenizer
import torch
import zipfile
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



def generate_questions(file, num_questions):
    # create an empty list to hold the generated questions
    generated_questions = []

    with zipfile.ZipFile(file, 'r') as zip_ref:
        # loop through files in zip file
        for file_name in zip_ref.namelist():
            if file_name.endswith(".txt"):
                with zip_ref.open(file_name) as f:
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


def generate_file_questions(file, num_questions):

    max_length = 128
    # initialize generated_questions
    generated_questions = []
    # read file contents
    lines = file.read().decode("utf-8").split("\n")
    num_lines = len(lines)
    batch_size = 100
    num_batches = (num_lines + batch_size - 1) // batch_size

    # shuffle lines
    random.shuffle(lines)

    for i in range(num_batches):
        start = i * batch_size
        end = min((i + 1) * batch_size, num_lines)
        batch_lines = lines[start:end]

        for line in batch_lines:
            line = line.strip()
            if not line:
                continue
            if len(line) > 1024:
                # split line into multiple lines of maximum length 1024
                split_lines = [line[j:j+512] for j in range(0, len(line), 1024)]
                for split_line in split_lines:
                    questions = run_model(f"generate questions: {split_line}",
                                          num_return_sequences=1,
                                          max_length=max_length)
                    generated_questions.extend(questions)
                    if len(generated_questions) >= num_questions:
                        break
                if len(generated_questions) >= num_questions:
                    break
            else:
                questions = run_model(f"generate questions: {line}",
                                      num_return_sequences=1,
                                      max_length=max_length)
                generated_questions.extend(questions)
                if len(generated_questions) >= num_questions:
                    break

        if len(generated_questions) >= num_questions:
            break

    # convert the list of generated questions to a Pandas DataFrame
    df = pd.DataFrame(generated_questions, columns=["generated_question"])

    return df.head(num_questions)
