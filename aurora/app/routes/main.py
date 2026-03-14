"""
Aurora Price Comparison - Main Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, or_
from app import db
from app.models import Category, Product, Store, Price, PriceHistory, Favorite, PriceAlert, Click, PageView
import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    track_page_view(request.path)
    categories = Category.query.filter(Category.parent_id == None).order_by(Category.name).limit(12).all()
    trending_products = get_trending_products(limit=8)
    recent_drops = get_recent_price_drops(limit=8)
    featured_stores = Store.query.filter(Store.verified == True).order_by(Store.rating.desc()).limit(10).all()
    all_categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', categories=categories, trending_products=trending_products, recent_drops=recent_drops, featured_stores=featured_stores, all_categories=all_categories)

@main.route('/category/<slug>')
def category(slug):
    track_page_view(request.path)
    category = Category.query.filter_by(slug=slug).first_or_404()
    subcategories = Category.query.filter_by(parent_id=category.id).all()
    page = request.args.get('page', 1, type=int)
    per_page = 24
    query = Product.query.filter_by(category_id=category.id)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price:
        query = query.join(Price).filter(Price.price >= min_price)
    if max_price:
        query = query.join(Price).filter(Price.price <= max_price)
    sort = request.args.get('sort', 'popular')
    if sort == 'price_asc':
        query = query.join(Price).order_by(Price.price.asc())
    elif sort == 'price_desc':
        query = query.join(Price).order_by(Price.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    brands = db.session.query(Product.brand).filter(Product.category_id == category.id, Product.brand != None).distinct().all()
    brands = [b[0] for b in brands if b[0]]
    price_range = db.session.query(func.min(Price.price), func.max(Price.price)).join(Product).filter(Product.category_id == category.id).first()
    return render_template('category.html', category=category, subcategories=subcategories, products=products, brands=brands, price_range=price_range, sort=sort)

@main.route('/product/<slug>')
def product(slug):
    track_page_view(request.path)
    product = Product.query.filter_by(slug=slug).first_or_404()
    prices = Price.query.filter_by(product_id=product.id).join(Store).order_by((Price.price + Price.shipping).asc()).all()
    price_history = PriceHistory.query.filter_by(product_id=product.id).order_by(PriceHistory.recorded_at.desc()).limit(30).all()
    similar_products = Product.query.filter(Product.category_id == product.category_id, Product.id != product.id).limit(4).all()
    is_favorited = False
    if current_user.is_authenticated:
        favorite = Favorite.query.filter_by(user_id=current_user.id, product_id=product.id).first()
        is_favorited = favorite is not None
    has_alert = False
    if current_user.is_authenticated:
        alert = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product.id, active=True).first()
        has_alert = alert is not None
    return render_template('product.html', product=product, prices=prices, price_history=price_history, similar_products=similar_products, is_favorited=is_favorited, has_alert=has_alert)

@main.route('/search')
def search():
    track_page_view(request.path)
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    per_page = 24
    search_query = Product.query.filter(or_(Product.name.ilike(f'%{query}%'), Product.brand.ilike(f'%{query}%'), Product.description.ilike(f'%{query}%')))
    sort = request.args.get('sort', 'relevance')
    if sort == 'price_asc':
        search_query = search_query.join(Price).order_by(Price.price.asc())
    elif sort == 'price_desc':
        search_query = search_query.join(Price).order_by(Price.price.desc())
    else:
        search_query = search_query.order_by(Product.name.asc())
    results = search_query.paginate(page=page, per_page=per_page, error_out=False)
    categories = Category.query.order_by(Category.name).all()
    return render_template('search.html', query=query, results=results, categories=categories, sort=sort)

@main.route('/api/autocomplete')
def autocomplete():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).limit(10).all()
    results = []
    for p in products:
        lowest = p.lowest_price
        results.append({'id': p.id, 'name': p.name, 'brand': p.brand, 'slug': p.slug, 'price': lowest.price if lowest else None, 'image': p.image_url})
    return jsonify(results)

@main.route('/favorites')
@login_required
def favorites():
    track_page_view(request.path)
    favorites = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.created_at.desc()).all()
    return render_template('favorites.html', favorites=favorites)

@main.route('/favorite/toggle/<int:product_id>', methods=['POST'])
@login_required
def toggle_favorite(product_id):
    product = Product.query.get_or_404(product_id)
    existing = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        favorite = Favorite(user_id=current_user.id, product_id=product_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added'})

@main.route('/price-alerts')
@login_required
def price_alerts():
    track_page_view(request.path)
    alerts = PriceAlert.query.filter_by(user_id=current_user.id).order_by(PriceAlert.created_at.desc()).all()
    return render_template('price_alerts.html', alerts=alerts)

@main.route('/price-alert/create', methods=['POST'])
@login_required
def create_price_alert():
    product_id = request.form.get('product_id', type=int)
    target_price = request.form.get('target_price', type=float)
    if not product_id or not target_price:
        flash('Invalid request', 'error')
        return redirect(url_for('main.index'))
    product = Product.query.get_or_404(product_id)
    existing = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product_id, active=True).first()
    if existing:
        existing.target_price = target_price
        flash(f'Price alert updated for {product.name}', 'success')
    else:
        alert = PriceAlert(user_id=current_user.id, product_id=product_id, target_price=target_price)
        db.session.add(alert)
        flash(f'Price alert created for {product.name}', 'success')
    db.session.commit()
    return redirect(url_for('main.product', slug=product.slug))

@main.route('/price-alert/delete/<int:alert_id>', methods=['POST'])
@login_required
def delete_price_alert(alert_id):
    alert = PriceAlert.query.filter_by(id=alert_id, user_id=current_user.id).first_or_404()
    db.session.delete(alert)
    db.session.commit()
    flash('Price alert deleted', 'success')
    return redirect(url_for('main.price_alerts'))

@main.route('/click/<int:price_id>')
def click(price_id):
    price = Price.query.get_or_404(price_id)
    click = Click(product_id=price.product_id, store_id=price.store_id, user_id=current_user.id if current_user.is_authenticated else None, referrer=request.referrer, ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'))
    db.session.add(click)
    db.session.commit()
    tracked_link = price.get_tracked_link(user_id=current_user.id if current_user.is_authenticated else None)
    return redirect(tracked_link)

@main.route('/stores')
def stores():
    track_page_view(request.path)
    page = request.args.get('page', 1, type=int)
    per_page = 20
    stores = Store.query.order_by(Store.name).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('stores.html', stores=stores)

@main.route('/store/<slug>')
def store(slug):
    track_page_view(request.path)
    store = Store.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 24
    products = Price.query.filter_by(store_id=store.id).join(Product).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('store.html', store=store, products=products)

@main.route('/deals')
def deals():
    track_page_view(request.path)
    page = request.args.get('page', 1, type=int)
    per_page = 24
    products = Product.query.join(Price).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('deals.html', products=products)

def track_page_view(path):
    try:
        view = PageView(path=path, user_id=current_user.id if current_user.is_authenticated else None, ip_address=request.remote_addr, referrer=request.referrer, user_agent=request.headers.get('User-Agent'))
        db.session.add(view)
        db.session.commit()
    except:
        pass

def get_trending_products(limit=8):
    week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    trending = db.session.query(Product, func.count(Click.id).label('clicks')).join(Click).filter(Click.clicked_at >= week_ago).group_by(Product.id).order_by(func.count(Click.id).desc()).limit(limit).all()
    return [t[0] for t in trending]

def get_recent_price_drops(limit=8):
    products = Product.query.join(Price).limit(limit).all()
    return products
