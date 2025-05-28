import pandas as pd
import newspaper
from newspaper import Config
import requests
import re
from tqdm import tqdm
from colorama import init, Fore

import spacy
# Load the English language model
nlp = spacy.load("en_core_web_sm")

print(Fore.YELLOW + "Running full_content.py")

# Initialize colorama
init(autoreset=True)

# function to extract final URL
def find_final_url(url):
    try:
        response = requests.get(url)
        final_url = response.url
        return final_url
    except requests.exceptions.RequestException as e:
        return url

# function to get the article content from a URL
def get_article_content(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    article = newspaper.Article(url, config=config)
    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(Fore.RED + f"\nError fetching content for URL: {url}")
        print(Fore.RED + str(e))
        return ''
    
def filter_content(text):

    # Set the number of sentences for the main content
    num_sentences = 4
    # Process the text with spaCy
    doc = nlp(text)

    # Extract the sentences
    sentences = [sent.text for sent in doc.sents]
    # Get the first 'num_sentences' sentences as main content
    main_content = " ".join(sentences[:num_sentences])

    # Filter out the main content from the original text
    filtered_text = main_content
    # Filter out the main content from the original text
    filtered_text = "".join([str(sentence) for sentence in main_content])
    return filtered_text

input_file = r'dataset/raw/news_1.csv'
output_file = r'dataset/raw/news_with_full_content_2.csv'

# read the input CSV file into a pandas data frame
df = pd.read_csv(input_file)

# add a new column for the article content
df['raw_full_content'] = ''
df['spacy_full_content'] = ''
df['final_full_content']=''

# iterate over rows and get content for each URL
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Fetching article content"):
    url = row['URL']
    url = find_final_url(url)
    content = get_article_content(url)
    raw_content = content
    content = filter_content(content)

    # Perform multiple regex substitutions on the 'content' variable:
    # 1. Replace one or more consecutive whitespaces with a single space
    # 2. Remove any characters that are not alphanumeric or whitespaces
    # 3. Remove any characters that are not word characters, whitespaces, or periods
    # Finally, strip any leading or trailing spaces from the resulting string
    raw_content = re.sub(r'\s+', ' ', raw_content).strip()
    raw_content = re.sub(r'[^0-9a-zA-Z\s.?!]+', '', raw_content)

    content = re.sub(r'\s+', ' ', content).strip()
    content = re.sub(r'[^0-9a-zA-Z\s.?!]+', '', content)
    content = re.sub(r'[^\w\s.?!]', '', content)

    text = content
    df.loc[idx, 'raw_full_content'] = raw_content
    df.loc[idx, 'spacy_full_content'] = text
    

    larger_text = max([text, row['Description'], row['Content']], key=len)
    larger_text = re.sub(r'\d{4} chars$', '', larger_text)
    df.loc[idx, 'final_full_content'] = larger_text

# write the updated data frame to a new CSV file
df.to_csv(output_file, index=False)

print(Fore.GREEN + "\nAll full contents have been fetched, check dataset/raw/news_with_full_content_2.csv")