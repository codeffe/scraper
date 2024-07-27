# Dental Stall Scraper

This project is a web scraping application built with FastAPI. It scrapes product data from the Dental Stall website and stores it in a JSON file. The application uses caching to avoid redundant data and supports proxy usage.

## Project Structure

The project has the following structure:

```plaintext
dental-stall-scraper/
├── main.py # Entry point for the FastAPI application
├── cache.py # Cache management
├── models.py # Data models
├── scraper.py # Web scraper logic
├── utils.py # Utility functions, including authentication
├── images/ # Directory to store downloaded images
├── scraped_data.json # Output file for scraped data
└── cache.json # Cache file for storing product prices
```

## Requirements

- Python 3.8+
- FastAPI
- Requests
- BeautifulSoup4
- PIL (Pillow)
- Uvicorn

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/dental-stall-scraper.git
   cd dental-stall-scraper
   
2. Create and activate a virtual environment:

```sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required packages:

sh
Copy code
pip install -r requirements.txt
Create the necessary directories and files if they don't exist:

sh
Copy code
mkdir -p images
touch scraped_data.json cache.json
Running the Application
Start the FastAPI server:

sh
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000
Access the API:

The API will be available at http://localhost:8000.



### requirements.txt

To ensure all dependencies are captured, you can create a `requirements.txt` file with the following content:

