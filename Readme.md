# Twitter Trends Scraper

A web application that scrapes trending topics from Twitter and displays them through a web interface.

## Features
- Scrapes top 5 trending topics from Twitter
- Stores trend data in MongoDB
- Displays trends with timestamps and IP addresses
- Web interface for running scraper
- Error handling and retry mechanisms

## Prerequisites
- Python 3.x
- Chrome browser
- MongoDB installed and running
- Twitter account

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd twitter-trends-scraper
```

2. Install dependencies:
```bash
pip install selenium flask pymongo requests
```

3. Install ChromeDriver:
   - Download ChromeDriver matching your Chrome version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/)
   - Add ChromeDriver to your system PATH

## Configuration

1. Open `scraper.py`
2. Replace credentials:
```python
username_input.send_keys("your_twitter_username")
password_input.send_keys("your_twitter_password")
```

3. Configure MongoDB (if using different connection):
```python
client = MongoClient('mongodb://localhost:27017/')
```

## Usage

1. Start MongoDB service

2. Run the application:
```bash
python scraper.py
```

3. Open browser and visit:
```
http://localhost:5000
```

4. Click "Click here to run the script" to fetch trends

## Project Structure
```
twitter-trends-scraper/
├── scraper.py        # Main application file
├── requirements.txt  # Python dependencies
└── README.md        # Documentation
```

## Error Handling
- Retries failed trend fetching attempts
- Provides fallback data if scraping fails
- Handles missing trends gracefully

## MongoDB Schema
```json
{
    "_id": "uuid",
    "nameoftrend1": "string",
    "nameoftrend2": "string",
    "nameoftrend3": "string",
    "nameoftrend4": "string",
    "nameoftrend5": "string",
    "datetime": "datetime",
    "ip_address": "string"
}
```

## Troubleshooting
- Ensure MongoDB is running
- Verify Twitter credentials
- Check ChromeDriver matches Chrome version
- Ensure stable internet connection

## License
MIT License
