import os
from colorama import init, Fore
from crawl import clean_text, prompt_user
from content import find_final_url, get_article_content, filter_content
from summarise import multi
import pandas as pd
from tqdm import tqdm
import re

# Initialize colorama
init(autoreset=True)

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['dataset/raw', 'dataset/topics', 'dataset/multi-summaries']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(Fore.GREEN + f"Created directory: {directory}")

def main():
    print(Fore.YELLOW + "Starting News Article Processing Pipeline")
    
    # Create necessary directories
    create_directories()
    
    # Step 1: Crawl news articles
    print(Fore.YELLOW + "\nStep 1: Crawling News Articles")
    from crawl import newsapi
    
    # Get user input for news search
    query = prompt_user(Fore.YELLOW + "Enter the query you want to search for: ",
                       "Invalid query. Please try again.",
                       lambda x: len(x) > 0)
    
    from_date_str = prompt_user(Fore.YELLOW + "Enter the starting date for the search (YYYY-MM-DD): ",
                               "Invalid date format. Please enter in YYYY-MM-DD format.",
                               lambda x: re.match(r'\d{4}-\d{2}-\d{2}', x) is not None)
    
    to_date_str = prompt_user(Fore.YELLOW + "Enter the ending date for the search (YYYY-MM-DD): ",
                             "Invalid date format. Please enter in YYYY-MM-DD format.",
                             lambda x: re.match(r'\d{4}-\d{2}-\d{2}', x) is not None)
    
    language = prompt_user(Fore.YELLOW + "Enter the language you want to search in (e.g. 'en', 'fr', 'es'): ",
                          "Invalid language. Please try again.",
                          lambda x: len(x) == 2)
    
    # Retrieve articles
    articles = newsapi.get_everything(q=query, from_param=from_date_str, to=to_date_str, 
                                    language=language, sort_by="popularity")
    
    # Process articles
    news_data = [[article["url"], clean_text(article["title"]), 
                 clean_text(article["description"]), clean_text(article["content"])] 
                 for article in articles["articles"]]
    
    # Save initial data
    raw_file = "dataset/raw/news_1.csv"
    pd.DataFrame(news_data, columns=["URL", "Title", "Description", "Content"]).to_csv(raw_file, index=False)
    print(Fore.GREEN + f"\nInitial articles saved to {raw_file}")
    
    # Step 2: Extract and process full content
    print(Fore.YELLOW + "\nStep 2: Extracting Full Content")
    df = pd.read_csv(raw_file)
    df['raw_full_content'] = ''
    df['spacy_full_content'] = ''
    df['final_full_content'] = ''
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing articles"):
        url = find_final_url(row['URL'])
        content = get_article_content(url)
        raw_content = content
        content = filter_content(content)
        
        # Clean content
        raw_content = re.sub(r'\s+', ' ', raw_content).strip()
        raw_content = re.sub(r'[^0-9a-zA-Z\s.?!]+', '', raw_content)
        
        content = re.sub(r'\s+', ' ', content).strip()
        content = re.sub(r'[^0-9a-zA-Z\s.?!]+', '', content)
        content = re.sub(r'[^\w\s.?!]', '', content)
        
        df.loc[idx, 'raw_full_content'] = raw_content
        df.loc[idx, 'spacy_full_content'] = content
        
        larger_text = max([content, row['Description'], row['Content']], key=len)
        larger_text = re.sub(r'\d{4} chars$', '', larger_text)
        df.loc[idx, 'final_full_content'] = larger_text
    
    # Save processed content
    processed_file = "dataset/raw/news_with_full_content_2.csv"
    df.to_csv(processed_file, index=False)
    print(Fore.GREEN + f"\nProcessed content saved to {processed_file}")
    
    # Step 3: Generate summaries
    print(Fore.YELLOW + "\nStep 3: Generating Summaries")
    output_dir = 'dataset/multi-summaries'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, 'summaries.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for content in tqdm(df['final_full_content'], desc="Generating summaries"):
            if pd.notna(content) and content.strip():
                summary = multi(content)
                f.write(summary + "\n")
    
    print(Fore.GREEN + f"\nSummaries saved to {output_file}")
    print(Fore.GREEN + "\nPipeline completed successfully!")

if __name__ == "__main__":
    main()
