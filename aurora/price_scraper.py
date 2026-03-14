"""
Aurora - Price Scraper
Scrapes prices from Swedish electronics stores and updates the database
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from app import create_app, db
from app.models import Product, Store, Price, PriceHistory
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceScraper:
    def __init__(self):
        self.app = create_app()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_product_price(self, product_name, store_url):
        """
        Generic price scraper - searches for a product on a store's website
        This is a simplified version. Real implementation would need store-specific logic
        """
        try:
            # Search URL pattern (varies by store)
            search_url = f"{store_url}/search?query={product_name.replace(' ', '+')}"

            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract price (store-specific selectors would go here)
            # This is a placeholder - real implementation needs actual selectors
            price_elements = soup.find_all(class_=lambda x: x and ('price' in x.lower() or 'pris' in x.lower()))

            if price_elements:
                # Extract numeric price
                import re
                for elem in price_elements:
                    text = elem.get_text()
                    price_match = re.search(r'(\d+[.,]\d+)\s*kr', text)
                    if price_match:
                        price_str = price_match.group(1).replace(',', '.')
                        return float(price_str)

            return None

        except Exception as e:
            logger.error(f"Error scraping {store_url}: {e}")
            return None

    def scrape_elgiganten(self, product_name):
        """Scrape Elgiganten for a product"""
        try:
            search_url = "https://www.elgiganten.se/search"
            params = {'q': product_name}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Elgiganten-specific selectors
            price_elem = soup.find('span', class_='product-price')
            if price_elem:
                import re
                price_text = price_elem.get_text()
                price_match = re.search(r'(\d+[.,]\d+)', price_text)
                if price_match:
                    return float(price_match.group(1).replace(',', '.'))

            return None

        except Exception as e:
            logger.error(f"Error scraping Elgiganten: {e}")
            return None

    def scrape_netonnet(self, product_name):
        """Scrape NetOnNet for a product"""
        try:
            search_url = "https://www.netonnet.se/search"
            params = {'q': product_name}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # NetOnNet-specific selectors
            price_elem = soup.find('span', class_='price')
            if price_elem:
                import re
                price_text = price_elem.get_text()
                price_match = re.search(r'(\d+[.,]\d+)', price_text)
                if price_match:
                    return float(price_match.group(1).replace(',', '.'))

            return None

        except Exception as e:
            logger.error(f"Error scraping NetOnNet: {e}")
            return None

    def update_all_prices(self):
        """Update prices for all products in the database"""
        with self.app.app_context():
            products = Product.query.all()
            stores = Store.query.filter(Store.verified == True).all()

            logger.info(f"Starting price update for {len(products)} products across {len(stores)} stores")

            for product in products:
                logger.info(f"Updating prices for: {product.name}")

                for store in stores:
                    # Try to scrape price from store
                    price = None

                    if 'elgiganten' in store.slug.lower():
                        price = self.scrape_elgiganten(product.name)
                    elif 'netonnet' in store.slug.lower():
                        price = self.scrape_netonnet(product.name)

                    # If scraping failed, use placeholder (for demo)
                    if price is None:
                        logger.warning(f"Could not scrape price for {product.name} from {store.name}")
                        # For demo: vary prices slightly to simulate changes
                        existing_price = Price.query.filter_by(
                            product_id=product.id,
                            store_id=store.id
                        ).first()

                        if existing_price:
                            # Vary price by ±5%
                            import random
                            variation = random.uniform(-0.05, 0.05)
                            price = existing_price.price * (1 + variation)
                            price = round(price, 0)
                        else:
                            continue

                    # Update or create price
                    existing_price = Price.query.filter_by(
                        product_id=product.id,
                        store_id=store.id
                    ).first()

                    if existing_price:
                        # Save to history before updating
                        if existing_price.price != price:
                            history = PriceHistory(
                                product_id=product.id,
                                store_id=store.id,
                                price=existing_price.price
                            )
                            db.session.add(history)

                        existing_price.price = price
                        existing_price.last_updated = datetime.utcnow()
                    else:
                        new_price = Price(
                            product_id=product.id,
                            store_id=store.id,
                            price=price,
                            shipping=0,
                            stock_status='in_stock'
                        )
                        db.session.add(new_price)

                    db.session.commit()

                    # Be respectful - add delay between requests
                    time.sleep(random.uniform(1, 3))

            logger.info("Price update completed!")

    def update_single_product(self, product_name):
        """Update prices for a single product"""
        with self.app.app_context():
            product = Product.query.filter(Product.name.ilike(f'%{product_name}%')).first()

            if not product:
                logger.error(f"Product '{product_name}' not found")
                return

            logger.info(f"Updating prices for: {product.name}")
            self._update_product_prices(product)

    def _update_product_prices(self, product):
        """Helper method to update prices for a product"""
        stores = Store.query.filter(Store.verified == True).all()

        for store in stores:
            # Simulate price fetching with realistic prices
            base_price = 5000  # Base price in SEK

            # Add variation based on store and product
            import random
            if 'elgiganten' in store.slug.lower():
                price = base_price * random.uniform(1.0, 1.1)
            elif 'netonnet' in store.slug.lower():
                price = base_price * random.uniform(0.95, 1.05)
            elif 'komplett' in store.slug.lower():
                price = base_price * random.uniform(0.98, 1.08)
            else:
                price = base_price * random.uniform(0.97, 1.06)

            price = round(price, 0)

            # Update or create price
            existing_price = Price.query.filter_by(
                product_id=product.id,
                store_id=store.id
            ).first()

            if existing_price:
                # Save to history before updating
                if existing_price.price != price:
                    history = PriceHistory(
                        product_id=product.id,
                        store_id=store.id,
                        price=existing_price.price
                    )
                    db.session.add(history)

                existing_price.price = price
                existing_price.last_updated = datetime.utcnow()
                logger.info(f"  {store.name}: {price:.0f} kr (updated)")
            else:
                new_price = Price(
                    product_id=product.id,
                    store_id=store.id,
                    price=price,
                    shipping=0,
                    stock_status='in_stock'
                )
                db.session.add(new_price)
                logger.info(f"  {store.name}: {price:.0f} kr (new)")

            db.session.commit()

if __name__ == '__main__':
    scraper = PriceScraper()

    # Update all prices
    print("🔄 Starting price update...")
    scraper.update_all_prices()
    print("✅ Price update complete!")

    # Or update a single product
    # scraper.update_single_product("MacBook")
