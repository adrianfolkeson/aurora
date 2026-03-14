"""
Aurora - Sample Data Creator
Populates the database with sample categories, stores, and products
"""
from app import create_app, db
from app.models import Category, Store, Product, Price, User
from datetime import datetime

def create_sample_data():
    app = create_app()

    with app.app_context():
        print("🗑️  Clearing existing data...")
        Price.query.delete()
        Product.query.delete()
        Store.query.delete()
        Category.query.delete()
        db.session.commit()

        print("📁 Creating categories...")
        categories = [
            Category(name='Datorer', slug='datorer', icon='pc-display', parent_id=None),
            Category(name='Mobiltelefoner', slug='mobiltelefoner', icon='phone', parent_id=None),
            Category(name='Laptops', slug='laptops', icon='laptop', parent_id=None),
            Category(name='Surfplattor', slug='surfplattor', icon='tablet', parent_id=None),
            Category(name='Headset', slug='headset', icon='headset', parent_id=None),
        ]

        for category in categories:
            db.session.add(category)
        db.session.commit()

        # Add parent relationships
        for cat in categories:
            print(f"  - {cat.name}")

        print("\n🏪 Creating stores...")
        stores = [
            Store(
                name='Elgiganten',
                slug='elgiganten',
                url='https://www.elgiganten.se',
                rating=4.2,
                verified=True,
                logo='https://www.elgiganten.se/favicon.ico'
            ),
            Store(
                name='NetOnNet',
                slug='netonnet',
                url='https://www.netonnet.se',
                rating=4.0,
                verified=True,
                logo='https://www.netonnet.se/favicon.ico'
            ),
            Store(
                name='Komplett',
                slug='komplett',
                url='https://www.komplett.se',
                rating=4.3,
                verified=True,
                logo='https://www.komplett.se/favicon.ico'
            ),
            Store(
                name='Webhallen',
                slug='webhallen',
                url='https://www.webhallen.se',
                rating=4.1,
                verified=True,
                logo='https://www.webhallen.se/favicon.ico'
            ),
        ]

        for store in stores:
            db.session.add(store)
        db.session.commit()

        for store in stores:
            print(f"  - {store.name}")

        print("\n📱 Creating products...")
        products = [
            # Datorer
            Product(
                name='Apple MacBook Air M2',
                slug='apple-macbook-air-m2',
                brand='Apple',
                category_id=categories[2].id,  # Laptops
                description='13.6", M2-chip, 8GB RAM, 256GB SSD, Midnight',
                image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400'
            ),
            Product(
                name='Dell XPS 13',
                slug='dell-xps-13',
                brand='Dell',
                category_id=categories[2].id,  # Laptops
                description='13.4", Intel Core i7, 16GB RAM, 512GB SSD',
                image_url='https://images.unsplash.com/photo-1593642632823-8f7853e85ee4?w=400'
            ),
            Product(
                name='HP Pavilion 15',
                slug='hp-pavilion-15',
                brand='HP',
                category_id=categories[2].id,  # Laptops
                description='15.6", Intel Core i5, 8GB RAM, 256GB SSD',
                image_url='https://images.unsplash.com/photo-1588872657578-3efd9243d8f9?w=400'
            ),

            # Mobiltelefoner
            Product(
                name='iPhone 15 Pro',
                slug='iphone-15-pro',
                brand='Apple',
                category_id=categories[1].id,  # Mobiltelefoner
                description='6.1", A17 Pro, 256GB, Titanium Blue',
                image_url='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400'
            ),
            Product(
                name='Samsung Galaxy S24 Ultra',
                slug='samsung-galaxy-s24-ultra',
                brand='Samsung',
                category_id=categories[1].id,  # Mobiltelefoner
                description='6.8", Snapdragon 8 Gen 3, 256GB, Titanium Gray',
                image_url='https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400'
            ),
            Product(
                name='Google Pixel 8 Pro',
                slug='google-pixel-8-pro',
                brand='Google',
                category_id=categories[1].id,  # Mobiltelefoner
                description='6.7", Tensor G3, 128GB, Porcelain',
                image_url='https://images.unsplash.com/photo-1598327105666-5b89351aff70?w=400'
            ),

            # Surfplattor
            Product(
                name='iPad Pro 12.9"',
                slug='ipad-pro-12-9',
                brand='Apple',
                category_id=categories[3].id,  # Surfplattor
                description='12.9", M2-chip, 256GB, Wi-Fi',
                image_url='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400'
            ),
            Product(
                name='Samsung Galaxy Tab S9',
                slug='samsung-galaxy-tab-s9',
                brand='Samsung',
                category_id=categories[3].id,  # Surfplattor
                description='11", Snapdragon 8 Gen 2, 128GB',
                image_url='https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400'
            ),

            # Headset
            Product(
                name='Sony WH-1000XM5',
                slug='sony-wh-1000xm5',
                brand='Sony',
                category_id=categories[4].id,  # Headset
                description='Noise cancelling, Bluetooth, 30h battery',
                image_url='https://images.unsplash.com/photo-1613040809024-b4ef7ba99bc3?w=400'
            ),
            Product(
                name='Bose QuietComfort 45',
                slug='bose-quietcomfort-45',
                brand='Bose',
                category_id=categories[4].id,  # Headset
                description='Noise cancelling, Bluetooth, 24h battery',
                image_url='https://images.unsplash.com/photo-1545127398-14699f92334bf?w=400'
            ),
        ]

        for product in products:
            db.session.add(product)
        db.session.commit()

        print(f"  Created {len(products)} products")

        print("\n💰 Creating prices...")
        prices = [
            # MacBook Air M2
            Price(product_id=products[0].id, store_id=stores[0].id, price=14495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[0].id, store_id=stores[1].id, price=13995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[0].id, store_id=stores[2].id, price=14290, shipping=0, stock_status='in_stock'),
            Price(product_id=products[0].id, store_id=stores[3].id, price=14199, shipping=0, stock_status='in_stock'),

            # Dell XPS 13
            Price(product_id=products[1].id, store_id=stores[0].id, price=13995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[1].id, store_id=stores[1].id, price=13495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[1].id, store_id=stores[2].id, price=13790, shipping=0, stock_status='in_stock'),
            Price(product_id=products[1].id, store_id=stores[3].id, price=13599, shipping=0, stock_status='in_stock'),

            # HP Pavilion 15
            Price(product_id=products[2].id, store_id=stores[0].id, price=7995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[2].id, store_id=stores[1].id, price=7495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[2].id, store_id=stores[2].id, price=7790, shipping=0, stock_status='in_stock'),
            Price(product_id=products[2].id, store_id=stores[3].id, price=7699, shipping=0, stock_status='in_stock'),

            # iPhone 15 Pro
            Price(product_id=products[3].id, store_id=stores[0].id, price=12495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[3].id, store_id=stores[1].id, price=11995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[3].id, store_id=stores[2].id, price=12290, shipping=0, stock_status='in_stock'),
            Price(product_id=products[3].id, store_id=stores[3].id, price=12199, shipping=0, stock_status='in_stock'),

            # Samsung Galaxy S24 Ultra
            Price(product_id=products[4].id, store_id=stores[0].id, price=13995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[4].id, store_id=stores[1].id, price=13495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[4].id, store_id=stores[2].id, price=13790, shipping=0, stock_status='in_stock'),
            Price(product_id=products[4].id, store_id=stores[3].id, price=13699, shipping=0, stock_status='in_stock'),

            # Google Pixel 8 Pro
            Price(product_id=products[5].id, store_id=stores[0].id, price=9995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[5].id, store_id=stores[1].id, price=9495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[5].id, store_id=stores[2].id, price=9790, shipping=0, stock_status='in_stock'),
            Price(product_id=products[5].id, store_id=stores[3].id, price=9699, shipping=0, stock_status='in_stock'),

            # iPad Pro
            Price(product_id=products[6].id, store_id=stores[0].id, price=15495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[6].id, store_id=stores[1].id, price=14995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[6].id, store_id=stores[2].id, price=15290, shipping=0, stock_status='in_stock'),
            Price(product_id=products[6].id, store_id=stores[3].id, price=15199, shipping=0, stock_status='in_stock'),

            # Samsung Galaxy Tab S9
            Price(product_id=products[7].id, store_id=stores[0].id, price=7995, shipping=0, stock_status='in_stock'),
            Price(product_id=products[7].id, store_id=stores[1].id, price=7495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[7].id, store_id=stores[2].id, price=7790, shipping=0, stock_status='in_stock'),
            Price(product_id=products[7].id, store_id=stores[3].id, price=7699, shipping=0, stock_status='in_stock'),

            # Sony WH-1000XM5
            Price(product_id=products[8].id, store_id=stores[0].id, price=4495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[8].id, store_id=stores[1].id, price=4195, shipping=0, stock_status='in_stock'),
            Price(product_id=products[8].id, store_id=stores[2].id, price=4390, shipping=0, stock_status='in_stock'),
            Price(product_id=products[8].id, store_id=stores[3].id, price=4299, shipping=0, stock_status='in_stock'),

            # Bose QuietComfort 45
            Price(product_id=products[9].id, store_id=stores[0].id, price=3495, shipping=0, stock_status='in_stock'),
            Price(product_id=products[9].id, store_id=stores[1].id, price=3195, shipping=0, stock_status='in_stock'),
            Price(product_id=products[9].id, store_id=stores[2].id, price=3390, shipping=0, stock_status='in_stock'),
            Price(product_id=products[9].id, store_id=stores[3].id, price=3299, shipping=0, stock_status='in_stock'),
        ]

        for price in prices:
            db.session.add(price)
        db.session.commit()

        print(f"  Created {len(prices)} prices")

        print("\n✅ Sample data created successfully!")
        print(f"\n📊 Summary:")
        print(f"  - {len(categories)} categories")
        print(f"  - {len(stores)} stores")
        print(f"  - {len(products)} products")
        print(f"  - {len(prices)} prices")

        return True

if __name__ == '__main__':
    create_sample_data()
