import csv
import re
import sys
from colorama import init, Fore
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
news_api_key = os.getenv('NEWS_API')

# Initialize colorama
init(autoreset=True)

print(Fore.YELLOW + "Running news_crawl.py")

# Initialize NewsApiClient with API key
newsapi = NewsApiClient(api_key=news_api_key)

def clean_text(text):
    """Clean the text by replacing newlines with spaces, removing extra spaces and symbols."""
    if text is not None:
        text = text.replace("\n", " ")
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^0-9a-zA-Z\s]+', '', text)
    return text

def prompt_user(prompt_message, error_message, validation_func):
    """Prompt the user for input, validate the input and return it."""
    while True:
        user_input = input(prompt_message)
        if validation_func(user_input):
            return user_input
        else:
            print(Fore.RED + error_message, file=sys.stderr)

# Get current date and date from one month ago
to_date = datetime.now()
from_date = to_date - timedelta(days=30)

# Format dates as YYYY-MM-DD
to_date_str = to_date.strftime('%Y-%m-%d')
from_date_str = from_date.strftime('%Y-%m-%d')

print(Fore.YELLOW + f"Searching news from {from_date_str} to {to_date_str}")

# Prompt user only for query
query = prompt_user(Fore.YELLOW + "Enter the query you want to search for: ",
                    "Invalid query. Please try again.",
                    lambda x: len(x) > 0)

print(Fore.YELLOW + "\nFetching articles from NewsAPI...")

# Retrieve articles from NewsAPI with a limit of 10 articles
# Using English language by default
articles = newsapi.get_everything(q=query, from_param=from_date_str, to=to_date_str, 
                                language='en', sort_by="popularity", page_size=10)

# Create list of lists containing cleaned article data
print(Fore.YELLOW + "\nProcessing article data...")
indian_news_more = []
for article in tqdm(articles["articles"], desc="Cleaning articles"):
    indian_news_more.append([
        article["url"],
        clean_text(article["title"]),
        clean_text(article["description"]),
        clean_text(article["content"])
    ])

output_dir = r'dataset/raw'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(Fore.GREEN + f"Created directory: {output_dir}")

# Write data to CSV file
print(Fore.YELLOW + "\nSaving articles to CSV...")
with open("dataset/raw/news_1.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Title", "Description", "Content"])
    writer.writerows(indian_news_more)

# Log success or error message
if len(indian_news_more) > 0:
    print(Fore.GREEN + f"\nSUCCESS: {len(indian_news_more)} articles retrieved and written to file dataset/raw/news_1.csv")
    print(Fore.GREEN + f"Date range: {from_date_str} to {to_date_str}")
    print(Fore.GREEN + f"Query: {query}")
else:
    print(Fore.RED + "\nERROR: No articles retrieved.")