# News Article Summarizer

Hey! This is my NLP lab project that fetches news articles and creates summaries.

## How to Run

1. First, install the required packages:
```bash
pip install -r requirements.txt
```

2. Download the model (this might take a few minutes):
```bash
python download_model.py
```

3. Create a file named `.env` in the project folder and add your NewsAPI key: (Sign up on https://newsapi.org/ to generate an api key)
```
NEWS_API=your_api_key_here
```

4. Run the program:
```bash
python main.py
```

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