"""
Aurora - Complete Price Update System
Implements all three approaches: Manual, Web Scraping, and Affiliate APIs
"""

# ============================================
# APPROACH 1: MANUAL PRICE UPDATES
# ============================================

def update_price_manual(product_id, store_id, new_price, shipping=0):
    """
    Manual price update through admin panel or direct function
    Usage: Call from admin panel or this script
    """
    from app import create_app, db
    from app.models import Price, PriceHistory
    from datetime import datetime

    app = create_app()
    with app.app_context():
        # Get existing price
        existing_price = Price.query.filter_by(
            product_id=product_id,
            store_id=store_id
        ).first()

        if existing_price:
            # Save to history before updating
            if existing_price.price != new_price:
                history = PriceHistory(
                    product_id=product_id,
                    store_id=store_id,
                    price=existing_price.price
                )
                db.session.add(history)

            existing_price.price = new_price
            existing_price.shipping = shipping
            existing_price.last_updated = datetime.utcnow()
        else:
            new_price = Price(
                product_id=product_id,
                store_id=store_id,
                price=new_price,
                shipping=shipping,
                stock_status='in_stock'
            )
            db.session.add(new_price)

        db.session.commit()
        print(f"✅ Price updated: Product {product_id}, Store {store_id}, New price: {new_price} kr")


# ============================================
# APPROACH 2: WEB SCRAPING (AUTOMATED)
# ============================================

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SwedishStoreScraper:
    """Scrapes prices from Swedish electronics stores"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
        })

    def scrape_elgiganten(self, search_query):
        """
        Scrape Elgiganten.se
        Note: Elgiganten has anti-scraping measures.
        Consider using their affiliate API instead.
        """
        try:
            search_url = "https://www.elgiganten.se/search"
            params = {'q': search_query}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Elgiganten price selectors (may change)
            price_selectors = [
                '.product-price',
                '.price-tag',
                '[data-test="product-price"]',
                '.product-price__amount'
            ]

            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    # Extract price (handle formats like "14 995 kr" or "14995:-")
                    import re
                    price_match = re.search(r'(\d+[.,]\d+)', price_text.replace(' ', ''))
                    if price_match:
                        price = float(price_match.group(1).replace(',', '.'))
                        logger.info(f"Elgiganten: {search_query} = {price} kr")
                        return price

            logger.warning(f"Elgiganten: Could not find price for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Elgiganten scraping error: {e}")
            return None

    def scrape_netonnet(self, search_query):
        """Scrape NetOnNet.se"""
        try:
            search_url = "https://www.netonnet.se/search"
            params = {'q': search_query}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # NetOnNet price selectors
            price_selectors = [
                '.price',
                '.product-price',
                '[data-price]'
            ]

            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    import re
                    price_match = re.search(r'(\d+[.,]\d+)', price_text)
                    if price_match:
                        price = float(price_match.group(1).replace(',', '.'))
                        logger.info(f"NetOnNet: {search_query} = {price} kr")
                        return price

            logger.warning(f"NetOnNet: Could not find price for {search_query}")
            return None

        except Exception as e:
            logger.error(f"NetOnNet scraping error: {e}")
            return None

    def scrape_komplett(self, search_query):
        """Scrape Komplett.se"""
        try:
            search_url = "https://www.komplett.se/search"
            params = {'q': search_query}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Komplett price selectors
            price_selectors = [
                '.product-price',
                '.price-tag',
                '[data-price]'
            ]

            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    import re
                    price_match = re.search(r'(\d+[.,]\d+)', price_text)
                    if price_match:
                        price = float(price_match.group(1).replace(',', '.'))
                        logger.info(f"Komplett: {search_query} = {price} kr")
                        return price

            logger.warning(f"Komplett: Could not find price for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Komplett scraping error: {e}")
            return None

    def scrape_webhallen(self, search_query):
        """Scrape Webhallen.se"""
        try:
            search_url = "https://www.webhallen.se/search"
            params = {'q': search_query}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Webhallen price selectors
            price_selectors = [
                '.price',
                '.product-price',
                '[data-price]'
            ]

            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    import re
                    price_match = re.search(r'(\d+[.,]\d+)', price_text)
                    if price_match:
                        price = float(price_match.group(1).replace(',', '.'))
                        logger.info(f"Webhallen: {search_query} = {price} kr")
                        return price

            logger.warning(f"Webhallen: Could not find price for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Webhallen scraping error: {e}")
            return None

    def scrape_all_stores(self, product_name):
        """
        Scrape all stores for a product
        Returns dict with store names as keys and prices as values
        """
        results = {}

        # Scrape each store
        results['Elgiganten'] = self.scrape_elgiganten(product_name)
        results['NetOnNet'] = self.scrape_netonnet(product_name)
        results['Komplett'] = self.scrape_komplett(product_name)
        results['Webhallen'] = self.scrape_webhallen(product_name)

        # Add delay between requests to be respectful
        time.sleep(random.uniform(1, 2))

        return results


# ============================================
# APPROACH 3: AFFILIATE APIs (PRODUCTION)
# ============================================

class AffiliateAPIManager:
    """
    Manages affiliate API connections to Swedish stores
    Most Swedish affiliate networks: Adtraction, Awin, Adtraction
    """

    def __init__(self):
        self.api_keys = {
            'adtraction': os.getenv('ATTRACTION_API_KEY'),
            'awin': os.getenv('AWIN_API_KEY'),
        }

    def fetch_from_adtraction(self, product_ean=None, product_id=None):
        """
        Fetch prices from Adtraction affiliate network
        Adtraction is the largest affiliate network in Scandinavia

        To get access:
        1. Apply at https://adtraction.com
        2. Get API credentials
        3. Set ATTRACTION_API_KEY environment variable
        """
        import os
        api_key = self.api_keys['adtraction']

        if not api_key:
            logger.warning("Adtraction API key not set. Set ATTRACTION_API_KEY environment variable.")
            return None

        try:
            # Adtraction API endpoint (example)
            api_url = "https://api.adtraction.com/v1/products/search"

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            params = {}
            if product_ean:
                params['ean'] = product_ean
            if product_id:
                params['product_id'] = product_id

            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Process API response
            results = []
            for offer in data.get('offers', []):
                results.append({
                    'store': offer.get('merchant_name'),
                    'price': float(offer.get('price', 0)),
                    'availability': offer.get('in_stock', False),
                    'affiliate_url': offer.get('tracking_url'),
                    'shipping': float(offer.get('shipping_cost', 0))
                })

            logger.info(f"Adtraction API: Found {len(results)} offers")
            return results

        except Exception as e:
            logger.error(f"Adtraction API error: {e}")
            return None

    def fetch_from_awin(self, merchant_id, product_id):
        """
        Fetch prices from Awin affiliate network
        Awin is another major affiliate network in Sweden
        """
        api_key = self.api_keys['awin']

        if not api_key:
            logger.warning("Awin API key not set. Set AWIN_API_KEY environment variable.")
            return None

        try:
            # Awin Product Search API
            api_url = "https://api.awin1.com/v2/merchants"

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Process API response
            results = []
            for offer in data.get('products', []):
                results.append({
                    'store': offer.get('merchant_name'),
                    'price': float(offer.get('price', 0)),
                    'affiliate_url': offer.get('deep_link'),
                    'availability': offer.get('in_stock', False)
                })

            logger.info(f"Awin API: Found {len(results)} offers")
            return results

        except Exception as e:
            logger.error(f"Awin API error: {e}")
            return None

    def simulate_api_prices(self, product_name):
        """
        Simulate API responses for testing/demonstration
        In production, replace this with actual API calls
        """
        logger.info(f"Simulating API prices for: {product_name}")

        # Simulate prices from different stores
        import random
        base_price = random.randint(5000, 15000)

        simulated_results = {
            'Elgiganten': base_price * random.uniform(1.0, 1.1),
            'NetOnNet': base_price * random.uniform(0.95, 1.05),
            'Komplett': base_price * random.uniform(0.98, 1.08),
            'Webhallen': base_price * random.uniform(0.97, 1.06),
        }

        # Round to nearest kr
        for store in simulated_results:
            simulated_results[store] = round(simulated_results[store], 0)

        return simulated_results


# ============================================
# AUTOMATED PRICE UPDATE SYSTEM
# ============================================

def update_all_prices_automatically(approach='scraper'):
    """
    Main function to update all prices using specified approach
    Options: 'scraper', 'api', 'hybrid'
    """
    from app import create_app, db
    from app.models import Product, Store, Price, PriceHistory
    import os

    app = create_app()

    with app.app_context():
        products = Product.query.all()
        stores = Store.query.filter(Store.verified == True).all()

        logger.info(f"Updating prices for {len(products)} products using {approach} approach")

        for product in products:
            logger.info(f"Processing: {product.name}")

            for store in stores:
                new_price = None
                shipping = 0

                if approach == 'scraper':
                    # Use web scraping
                    scraper = SwedishStoreScraper()
                    scrape_method = getattr(scraper, f'scrape_{store.slug.lower()}')
                    if scrape_method:
                        new_price = scrape_method(product.name)

                elif approach == 'api':
                    # Use affiliate APIs
                    api_manager = AffiliateAPIManager()
                    results = api_manager.fetch_from_adtraction(
                        product_ean=product.ean,
                        product_id=product.id
                    )
                    if results:
                        for result in results:
                            if result['store'].lower() in store.slug.lower():
                                new_price = result['price']
                                shipping = result.get('shipping', 0)
                                break

                elif approach == 'hybrid':
                    # Try API first, fall back to scraping
                    api_manager = AffiliateAPIManager()
                    api_results = api_manager.fetch_from_adtraction(product.id)

                    if api_results and len(api_results) > 0:
                        for result in api_results:
                            if result['store'].lower() in store.slug.lower():
                                new_price = result['price']
                                shipping = result.get('shipping', 0)
                                break
                    else:
                        # Fall back to scraping
                        scraper = SwedishStoreScraper()
                        scrape_method = getattr(scraper, f'scrape_{store.slug.lower()}')
                        if scrape_method:
                            new_price = scrape_method(product.name)

                # Apply price update
                if new_price:
                    update_price_manual(product.id, store.id, new_price, shipping)
                    logger.info(f"  {store.name}: {new_price} kr")

                # Be respectful - add delay
                time.sleep(random.uniform(0.5, 1.5))


# ============================================
# SCHEDULER FOR AUTOMATIC UPDATES
# ============================================

def schedule_price_updates():
    """
    Setup cron job for automatic price updates
    Run this once to schedule automatic updates
    """
    import subprocess
    import crontab

    # Get current crontab
    current_cron = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL).decode()

    # Add Aurora price update job (runs every 6 hours)
    aurora_job = f"0 */6 * * * cd {os.path.dirname(os.path.abspath(__file__))} && source venv/bin/activate && python price_scraper.py\n"

    if 'price_scraper.py' not in current_cron:
        # Add to crontab
        cron_command = f'(crontab -l 2>/dev/null; echo "{aurora_job}") | crontab -'
        subprocess.run(cron_command, shell=True)
        print("✅ Price update scheduler added to crontab")
        print("   Prices will update every 6 hours")
    else:
        print("ℹ️  Price scheduler already exists in crontab")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'update':
            approach = sys.argv[2] if len(sys.argv) > 2 else 'scraper'
            update_all_prices_automatically(approach)
            print("✅ Price update complete!")

        elif command == 'schedule':
            schedule_price_updates()

        elif command == 'test':
            # Test individual approaches
            print("Testing price update approaches...")

            # Test scraping
            print("\n1. Testing Web Scraping:")
            scraper = SwedishStoreScraper()
            results = scraper.scrape_all_stores("iPhone 15 Pro")
            for store, price in results.items():
                if price:
                    print(f"  {store}: {price} kr")
                else:
                    print(f"  {store}: Not found")

            # Test API
            print("\n2. Testing Affiliate API (simulated):")
            api_manager = AffiliateAPIManager()
            results = api_manager.simulate_api_prices("iPhone 15 Pro")
            for store, price in results.items():
                print(f"  {store}: {price} kr")

        else:
            print("Unknown command")
            print("Available commands:")
            print("  update [scraper/api/hybrid] - Update prices")
            print("  schedule - Setup cron job")
            print("  test - Test all approaches")
    else:
        print("Aurora Price Update System")
        print("=" * 40)
        print("Usage:")
        print("  python price_system.py update scraper  - Update prices using web scraping")
        print("  python price_system.py update api      - Update prices using affiliate APIs")
        print("  python price_system.py update hybrid   - Use API first, scraping as fallback")
        print("  python price_system.py schedule        - Setup automatic updates (cron)")
        print("  python price_system.py test            - Test all approaches")
