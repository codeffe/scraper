import requests
from bs4 import BeautifulSoup
import os
import json
import logging
from models import Product
from cache import Cache
from typing import Optional
from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Scraper:
    def __init__(self, pages: int, proxy: Optional[str], cache: Cache):
        self.pages = pages
        self.proxy = proxy
        self.session = requests.Session()
        self.scraped_data = []
        self.cache = cache
        self.image_dir = "images"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def scrape(self):
        for page in range(1, self.pages + 1):
            url = f"https://dentalstall.com/shop/page/{page}/" if page > 1 else "https://dentalstall.com/shop/"
            logging.info(f"Fetching {url}")
            try:
                response = self.session.get(url, proxies={"http": self.proxy, "https": self.proxy} if self.proxy else None)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                products = soup.select('.product')
                for product in products:
                    try:
                        self.parse_product(product)
                    except Exception as e:
                        logging.error(f"Error parsing product: {e}")
            except requests.RequestException as e:
                logging.error(f"Failed to fetch page {page}: {e}")
                if response.status_code == 500:
                    time.sleep(5)
                    continue
        return self.scraped_data

    def parse_product(self, product):
        title = product.select_one('.woo-loop-product__title a').text.strip()
        price_element = product.select_one('.price')
        price = (price_element.select_one('ins .woocommerce-Price-amount') or
                 price_element.select_one('.woocommerce-Price-amount')).text.strip()
        image_url = product.select_one('.mf-product-thumbnail img').get('data-lazy-src')
        logging.info(f"Image URL: {image_url}")
        image_path = self.download_image(image_url)
        product_data = Product(
            product_title=title,
            product_price=float(price.replace('₹', '').replace(',', '')),
            path_to_image=image_path
        )
        self.check_and_update_cache(product_data)

    def download_image(self, url):
        if not url:
            return ""
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'image' in content_type:
                    image_name = url.split("/")[-1]
                    image_path = os.path.join(self.image_dir, image_name)
                    with open(image_path, 'wb') as handler:
                        handler.write(response.content)
                    if self.is_valid_image(image_path):
                        logging.info(f"Image downloaded and saved to {image_path}")
                        return image_path
                    else:
                        logging.warning(f"Downloaded image is not valid: {image_path}")
                        os.remove(image_path)
                else:
                    logging.warning(f"URL does not point to an image: {url}")
            else:
                logging.warning(f"Failed to download image, status code: {response.status_code}")
            return ""
        except Exception as e:
            logging.error(f"Failed to download image {url}: {e}")
            return ""

    def is_valid_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            logging.error(f"Image verification failed for {image_path}: {e}")
            with open(image_path, 'rb') as f:
                logging.error(f"Content of the invalid image file: {f.read()[:100]}")  # Log first 100 bytes of the file content for debugging
            return False

    def save_data(self, file_path):
        with open(file_path, 'w') as f:
            json.dump([product.dict() for product in self.scraped_data], f, indent=4)
        self.cache.save_cache()

    def notify(self):
        logging.info(f"Scraped {len(self.scraped_data)} products and saved to JSON")

    def check_and_update_cache(self, product_data: Product):
        cached_price = self.cache.get_product_price(product_data.product_title)
        if cached_price is None or cached_price != product_data.product_price:
            self.scraped_data.append(product_data)
            self.cache.update_product(product_data.product_title, product_data.product_price)
            logging.info(f"Product added to scraped data: {product_data}")
        else:
            logging.info(f"Product already in cache: {product_data}")
