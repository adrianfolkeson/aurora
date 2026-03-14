"""
Aurora Price Comparison - API Routes
"""
from flask import Blueprint, jsonify, request
from app import db
from app.models import Product, Store, Price, Category, Click
from sqlalchemy import func
import datetime

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/products')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'products': [p.to_dict() for p in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': page
    })

@api.route('/product/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    prices = Price.query.filter_by(product_id=product_id).join(Store).all()
    return jsonify({
        'product': product.to_dict(),
        'prices': [{
            'store': p.store.name,
            'price': p.price,
            'shipping': p.shipping,
            'total': p.total_price,
            'stock': p.stock_status
        } for p in prices]
    })

@api.route('/stores')
def get_stores():
    stores = Store.query.order_by(Store.name).all()
    return jsonify({'stores': [s.to_dict() for s in stores]})

@api.route('/categories')
def get_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify({'categories': [c.to_dict() for c in categories]})

@api.route('/track-click', methods=['POST'])
def track_click():
    data = request.get_json()
    product_id = data.get('product_id')
    store_id = data.get('store_id')
    
    if not product_id or not store_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    click = Click(
        product_id=product_id,
        store_id=store_id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(click)
    db.session.commit()
    
    return jsonify({'success': True})

@api.route('/stats/clicks')
def get_click_stats():
    days = request.args.get('days', 30, type=int)
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    
    clicks = db.session.query(
        func.date(Click.clicked_at),
        func.count(Click.id)
    ).filter(Click.clicked_at >= start_date).group_by(func.date(Click.clicked_at)).all()
    
    return jsonify({
        'clicks': [{'date': str(c[0]), 'count': c[1]} for c in clicks]
    })

# Add to_dict methods to models
Product.to_dict = lambda self: {
    'id': self.id,
    'name': self.name,
    'slug': self.slug,
    'brand': self.brand,
    'image_url': self.image_url,
    'lowest_price': self.lowest_price.price if self.lowest_price else None
}

Store.to_dict = lambda self: {
    'id': self.id,
    'name': self.name,
    'slug': self.slug,
    'logo': self.logo,
    'rating': self.rating,
    'verified': self.verified
}

Category.to_dict = lambda self: {
    'id': self.id,
    'name': self.name,
    'slug': self.slug,
    'product_count': self.product_count
}
