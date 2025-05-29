# News Article Summarizer

A Python-based news article processing pipeline that fetches, processes, and summarizes news articles using NLP techniques.

## Features

- Fetches news articles using NewsAPI
- Extracts and processes article content
- Generates summaries using the Pegasus model
- Supports multiple articles processing
- Progress tracking and error handling

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd News-Extractor-Summarizer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your NewsAPI key:
```
NEWS_API=your_api_key_here
```

## Usage

1. Download the Pegasus model:
```bash
python download_model.py
```

2. Run the pipeline:
```bash
python main.py
```

Or run individual components:
```bash
python crawl.py      # Fetch articles
python content.py    # Process content
python summarise.py  # Generate summaries
```

## Project Structure

```
News-Extractor-Summarizer/
├── crawl.py         # Article fetching
├── content.py       # Content processing
├── summarise.py     # Summary generation
├── main.py          # Main pipeline
├── download_model.py # Model downloader
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

## Dependencies

- newsapi-python
- transformers
- pandas
- numpy
- colorama
- tqdm
- python-dotenv

## License

MIT License 