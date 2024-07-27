# Dental Stall Scraper

This project is a web scraping application built with FastAPI. It scrapes product data from the Dental Stall website and stores it in a JSON file. The application uses caching to avoid redundant data and supports proxy usage.

## Project Structure

The project has the following structure:

```plaintext
scraper/
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
   git clone https://github.com/codeffe/scraper.git
   cd scraper
   
2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install the required packages:

   ``` sh
   pip install -r requirements.txt
   ```
   
4. Create the necessary directories and files if they don't exist:

   ```sh
   mkdir -p images
   touch scraped_data.json cache.json
   Running the Application
   ```
5. Start the FastAPI server:

   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   
6. Access the API:

The API will be available at http://localhost:8000.

## API Endpoints

The FastAPI application has the following endpoint:

      Endpoint: /scrape
      Method: POST
      Headers: token: xyz

      Request Body: 
         {
           "pages": 1,
           "proxy": null
         }

      Response:
         {
           "scraped_products": [ ... ],
           "message": "Scraped X products"
         }

### Authentication
The application uses a static token for authentication. Ensure to include the header token: xyz in your requests.

### How it Works

Initialization: The Scraper class initializes with the number of pages to scrape, an optional proxy, and a cache instance.

Scraping Process: The scrape method fetches the specified pages from the Dental Stall website.
It parses product information including title, price, and image URL.
Images are downloaded and saved to the images/ directory.

Image Validation: Downloaded images are validated to ensure they are not corrupted.

Caching: The cache is used to store product prices to avoid redundant data scraping.

Saving Data: Scraped data is saved to scraped_data.json.
Cache is updated and saved to cache.json.

Notification: A message is logged indicating the number of products scraped and saved.

### Example Request

To scrape data from the Dental Stall website, you can use the following curl command:

```sh
curl -X POST "http://localhost:8000/scrape" -H "Content-Type: application/json" -H "token: xyz" -d '{"pages": 1, "proxy": null}'
```
This will initiate the scraping process for 1 page without using a proxy.

### License
This project is licensed under the MIT License.
