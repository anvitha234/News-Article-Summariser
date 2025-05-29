from transformers import PegasusForConditionalGeneration, AutoTokenizer
from tqdm import tqdm
import csv
import numpy as np
import os
from colorama import init, Fore
import re
import pandas as pd

# Initialize colorama
init(autoreset=True)

print(Fore.YELLOW + "Running multi_summ.py")

# Load the tokenizer and model
print('Loading tokenizer')
tokenizer = AutoTokenizer.from_pretrained('cache_dir/transformers/google/xsum')
print('Loading model')
model = PegasusForConditionalGeneration.from_pretrained('cache_dir/transformers/google/xsum')
print('Model and Tokenizer loaded')

def multi(text):
    text = text.strip()  # Remove leading/trailing whitespaces
    # Ensure input text is formatted as a single string with sentences/paragraphs separated by newlines
    text = text.replace("\n", " ")
    text = re.sub(r'[^\w\s\.]', '', text)
    # Step 3: Tokenize and encode the input text
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    # Check if token count exceeds the model's maximum limit
    if tokens.shape[1] > model.config.max_position_embeddings:
        print("Input text is too long. Please shorten it.")
        exit(1)

    # Step 4: Generate summaries
    summary_ids = model.generate(tokens, max_length=150, num_beams=4, temperature=1.0)
    summaries = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    if not summaries.endswith('.'):
        # If not, add a period at the end of the line
        summaries += '.'
    return summaries

# Set the input and output directories
input_file = r'dataset/raw/news_with_full_content_2.csv'
output_dir = r'dataset/multi-summaries'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(Fore.GREEN + f"Created directory: {output_dir}")

# Check if input file exists
if not os.path.exists(input_file):
    print(Fore.RED + f"Input file not found: {input_file}")
    print(Fore.YELLOW + "Please ensure you have run content.py first to process the articles.")
    exit(1)

# Process the input file
print(Fore.YELLOW + f"Processing file: {input_file}")
with open(input_file, 'r', encoding='utf-8') as csvfile:
    # create a reader object
    reader = csv.reader(csvfile)
    # read the first row, which contains the column names
    column_names = next(reader)
    # find the index of the "final_full_content" column
    full_content_index = column_names.index("final_full_content")
    # read the column you want into a list
    my_docs = []
    for row in reader:
        my_docs.append(row[full_content_index])
    # convert the list into a numpy array
    docs = np.array(my_docs)

# Generate summary for each document and export the result summary in a txt file
output_filename = "summaries.txt"
with open(os.path.join(output_dir, output_filename), "w", encoding='utf-8') as f:
    for doc in tqdm(docs, desc="Generating summaries"):
        if pd.notna(doc) and doc.strip():
            try:
                summary = multi(doc)
                f.write(summary + "\n")
            except Exception as e:
                print(Fore.RED + f"Error generating summary: {str(e)}")
                continue

print(Fore.GREEN + f"\nSummary generation completed! Check {os.path.join(output_dir, output_filename)} for results.")