import os
from colorama import init, Fore
from crawl import clean_text, prompt_user
from content import find_final_url, get_article_content, filter_content
from summarise import multi
import pandas as pd
from tqdm import tqdm
import re
from datetime import datetime, timedelta

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
    print(Fore.YELLOW + "Note: Processing limited to 10 articles for efficiency")
    
    # Create necessary directories
    create_directories()
    
    # Step 1: Crawl news articles
    print(Fore.YELLOW + "\nStep 1: Crawling News Articles")
    from crawl import newsapi
    
    # Get user input for news search
    query = prompt_user(Fore.YELLOW + "Enter the query you want to search for: ",
                       "Invalid query. Please try again.",
                       lambda x: len(x) > 0)
    
    # Get current date and date from one month ago
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    
    # Format dates as YYYY-MM-DD
    to_date_str = to_date.strftime('%Y-%m-%d')
    from_date_str = from_date.strftime('%Y-%m-%d')
    
    print(Fore.YELLOW + f"Searching articles from {from_date_str} to {to_date_str}")
    
    # Retrieve articles with a limit of 10
    print(Fore.YELLOW + "\nFetching articles from NewsAPI...")
    articles = newsapi.get_everything(q=query, from_param=from_date_str, to=to_date_str, 
                                    language='en', sort_by="popularity", page_size=10)
    
    # Process articles
    print(Fore.YELLOW + "\nProcessing article data...")
    news_data = []
    for article in tqdm(articles["articles"], desc="Cleaning articles"):
        news_data.append([
            article["url"],
            clean_text(article["title"]),
            clean_text(article["description"]),
            clean_text(article["content"])
        ])
    
    # Save initial data
    raw_file = "dataset/raw/news_1.csv"
    print(Fore.YELLOW + "\nSaving initial data...")
    pd.DataFrame(news_data, columns=["URL", "Title", "Description", "Content"]).to_csv(raw_file, index=False)
    print(Fore.GREEN + f"\nInitial articles saved to {raw_file}")
    print(Fore.GREEN + f"Number of articles: {len(news_data)}")
    
    # Step 2: Extract and process full content
    print(Fore.YELLOW + "\nStep 2: Extracting Full Content")
    print(Fore.YELLOW + "Loading CSV file...")
    df = pd.read_csv(raw_file)
    df['raw_full_content'] = ''
    df['spacy_full_content'] = ''
    df['final_full_content'] = ''
    
    print(Fore.YELLOW + "\nProcessing articles...")
    success_count = 0
    fail_count = 0
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing articles"):
        try:
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
            success_count += 1
        except Exception as e:
            print(Fore.RED + f"\nError processing article {idx + 1}: {str(e)}")
            fail_count += 1
    
    # Save processed content
    processed_file = "dataset/raw/news_with_full_content_2.csv"
    print(Fore.YELLOW + "\nSaving processed content...")
    df.to_csv(processed_file, index=False)
    print(Fore.GREEN + f"\nProcessed content saved to {processed_file}")
    print(Fore.GREEN + f"Successfully processed: {success_count} articles")
    print(Fore.RED + f"Failed to process: {fail_count} articles")
    
    # Step 3: Generate summaries
    print(Fore.YELLOW + "\nStep 3: Generating Summaries")
    output_dir = 'dataset/multi-summaries'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(Fore.GREEN + f"Created directory: {output_dir}")
    
    output_file = os.path.join(output_dir, 'summaries.txt')
    print(Fore.YELLOW + "\nGenerating summaries...")
    summary_count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for content in tqdm(df['final_full_content'], desc="Generating summaries"):
            if pd.notna(content) and content.strip():
                try:
                    summary = multi(content)
                    f.write(summary + "\n")
                    summary_count += 1
                except Exception as e:
                    print(Fore.RED + f"\nError generating summary: {str(e)}")
    
    print(Fore.GREEN + f"\nSummaries saved to {output_file}")
    print(Fore.GREEN + f"Generated {summary_count} summaries")
    print(Fore.GREEN + "\nPipeline completed successfully!")

if __name__ == "__main__":
    main()
