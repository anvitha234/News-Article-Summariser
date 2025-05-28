from transformers import PegasusForConditionalGeneration, AutoTokenizer
from tqdm import tqdm
import csv
import numpy as np
import os
from colorama import init, Fore
import re

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
input_dir = r'dataset/topics'
output_dir = r'dataset/multi-summaries'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through all csv files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        # Construct the output filename
        output_filename = os.path.splitext(filename)[0] + '.txt'
        # Open the input CSV file
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as csvfile:
            # create a reader object
            reader = csv.reader(csvfile)
            # read the first row, which contains the column names
            column_names = next(reader)
            # find the index of the "full_content" column
            full_content_index = column_names.index("final_full_content")
            # read the column you want into a list
            my_docs = []
            for row in reader:
                my_docs.append(row[full_content_index])
            # convert the list into a numpy array
            docs = np.array(my_docs)
        
        # Generate summary for each document and export the result summary in a txt file with the same name as the input CSV file
        with open(os.path.join(output_dir, output_filename), "w") as f:
            for doc in tqdm(docs, desc=f"Summarising articles for {output_filename}"):
                text = doc
                summary = multi(text)
                f.write(summary + "\n")
        print(Fore.GREEN + "Summary generation completed, file {}. Check {} for results.\n".format(filename, output_filename))