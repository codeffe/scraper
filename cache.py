import json
import os

class Cache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4)

    def get_product_price(self, product_title):
        return self.cache.get(product_title)

    def update_product(self, product_title, product_price):
        self.cache[product_title] = product_price
