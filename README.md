# News Article Processing Pipeline

This project implements a complete pipeline for processing news articles, including crawling, content extraction, and summarization.

## Features

- News article crawling using NewsAPI
- Full content extraction from article URLs
- Text cleaning and processing
- Article summarization using the Pegasus model

## Prerequisites

- Python 3.7+
- NewsAPI key (get one at https://newsapi.org/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-article-pipeline.git
cd news-article-pipeline
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your NewsAPI key:
```
NEWS_API=your_newsapi_key_here
```

## Usage

Run the main pipeline:
```bash
python main.py
```

The script will:
1. Prompt for search criteria (query, date range, language)
2. Crawl news articles
3. Extract and process full content
4. Generate summaries

## Project Structure

- `main.py`: Main pipeline orchestration
- `crawl.py`: News article crawling functionality
- `content.py`: Content extraction and processing
- `summarise.py`: Article summarization using Pegasus model

## Output

The pipeline generates the following outputs:
- `dataset/raw/news_1.csv`: Initial crawled articles
- `dataset/raw/news_with_full_content_2.csv`: Processed articles with full content
- `dataset/multi-summaries/summaries.txt`: Generated summaries

## License

[Your chosen license]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 