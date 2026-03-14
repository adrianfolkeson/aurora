"""
Aurora - Price Update API
Flask routes for manual price updates via web interface
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Product, Store, Price, PriceHistory
from price_system import update_price_manual, SwedishStoreScraper, AffiliateAPIManager
import logging
from datetime import datetime

price_api = Blueprint('price_api', __name__)

logger = logging.getLogger(__name__)


@price_api.route('/api/price/update/manual', methods=['POST'])
@login_required
def manual_price_update():
    """
    Manual price update endpoint
    POST data: {product_id, store_id, new_price, shipping}
    """
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    product_id = data.get('product_id')
    store_id = data.get('store_id')
    new_price = data.get('new_price')
    shipping = data.get('shipping', 0)

    if not all([product_id, store_id, new_price is not None]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        update_price_manual(product_id, store_id, new_price, shipping)
        return jsonify({'success': True, 'message': 'Price updated successfully'})
    except Exception as e:
        logger.error(f"Manual price update error: {e}")
        return jsonify({'error': str(e)}), 500


@price_api.route('/api/price/update/scrape', methods=['POST'])
@login_required
def scrape_price_update():
    """
    Scrape prices for a product
    POST data: {product_id}
    """
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400

    try:
        product = Product.query.get_or_404(product_id)
        scraper = SwedishStoreScraper()

        # Scrape all stores
        stores = Store.query.filter(Store.verified == True).all()
        results = {}

        for store in stores:
            scrape_method = getattr(scraper, f'scrape_{store.slug.lower()}', None)
            if scrape_method:
                price = scrape_method(product.name)
                if price:
                    update_price_manual(product.id, store.id, price, 0)
                    results[store.name] = f"{price} kr"

        return jsonify({
            'success': True,
            'product': product.name,
            'results': results,
            'message': f'Prices updated for {product.name}'
        })
    except Exception as e:
        logger.error(f"Scrape price update error: {e}")
        return jsonify({'error': str(e)}), 500


@price_api.route('/api/price/update/all', methods=['POST'])
@login_required
def update_all_prices():
    """
    Update all prices using specified approach
    POST data: {approach: 'scraper'|'api'|'hybrid'}
    """
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    approach = data.get('approach', 'scraper')

    try:
        from price_system import update_all_prices_automatically

        # Run in background
        import threading
        def update_in_background():
            update_all_prices_automatically(approach)

        thread = threading.Thread(target=update_in_background)
        thread.start()

        return jsonify({
            'success': True,
            'message': f'Price update started using {approach} approach'
        })
    except Exception as e:
        logger.error(f"Update all prices error: {e}")
        return jsonify({'error': str(e)}), 500


@price_api.route('/api/price/history/<int:product_id>', methods=['GET'])
def get_price_history(product_id):
    """
    Get price history for a product
    """
    try:
        from sqlalchemy import func

        product = Product.query.get_or_404(product_id)

        # Get price history
        history = db.session.query(
            PriceHistory.store_id,
            PriceHistory.price,
            PriceHistory.recorded_at,
            Store.name.label('store_name')
        ).join(Store, PriceHistory.store_id == Store.id
        ).filter(PriceHistory.product_id == product_id
        ).order_by(PriceHistory.recorded_at.desc()
        ).limit(50).all()

        return jsonify({
            'product': product.name,
            'history': [
                {
                    'store': row.store_name,
                    'price': row.price,
                    'date': row.recorded_at.isoformat()
                }
                for row in history
            ]
        })
    except Exception as e:
        logger.error(f"Price history error: {e}")
        return jsonify({'error': str(e)}), 500


@price_api.route('/api/price/status', methods=['GET'])
def price_update_status():
    """
    Get status of price updates
    Shows last update time, number of products, etc.
    """
    try:
        product_count = Product.query.count()
        store_count = Store.query.count()
        price_count = Price.query.count()

        # Get last update time
        last_price = Price.query.order_by(Price.last_updated.desc()).first()

        return jsonify({
            'products': product_count,
            'stores': store_count,
            'prices': price_count,
            'last_update': last_price.last_updated.isoformat() if last_price else None,
            'status': 'active'
        })
    except Exception as e:
        logger.error(f"Price status error: {e}")
        return jsonify({'error': str(e)}), 500
