"""
Aurora Price Comparison - Admin Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Category, Product, Store, Price, PriceHistory, User, Click, PageView, Favorite, PriceAlert
from sqlalchemy import func
import datetime

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_stores = Store.query.count()
    total_users = User.query.count()
    total_clicks = Click.query.count()
    total_page_views = PageView.query.count()
    today_clicks = Click.query.filter(Click.clicked_at >= datetime.datetime.utcnow().replace(hour=0, minute=0, second=0)).count()
    today_views = PageView.query.filter(PageView.viewed_at >= datetime.datetime.utcnow().replace(hour=0, minute=0, second=0)).count()
    recent_clicks = Click.query.order_by(Click.clicked_at.desc()).limit(10).all()
    top_products = db.session.query(Product, func.count(Click.id).label('clicks')).join(Click).group_by(Product.id).order_by(func.count(Click.id).desc()).limit(10).all()
    return render_template('admin/dashboard.html', total_products=total_products, total_stores=total_stores, total_users=total_users, total_clicks=total_clicks, total_page_views=total_page_views, today_clicks=today_clicks, today_views=today_views, recent_clicks=recent_clicks, top_products=top_products)

@admin.route('/products')
@login_required
@admin_required
def products():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    search = request.args.get('search', '')
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/products.html', products=products, search=search)

@admin.route('/product/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        brand = request.form.get('brand')
        category_id = request.form.get('category_id', type=int)
        ean = request.form.get('ean')
        image_url = request.form.get('image_url')
        description = request.form.get('description')
        slug = name.lower().replace(' ', '-')
        product = Product(name=name, brand=brand, category_id=category_id, ean=ean, image_url=image_url, description=description, slug=slug)
        db.session.add(product)
        db.session.commit()
        flash(f'Product "{name}" created', 'success')
        return redirect(url_for('admin.products'))
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/product_edit.html', product=None, categories=categories)

@admin.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.brand = request.form.get('brand')
        product.category_id = request.form.get('category_id', type=int)
        product.ean = request.form.get('ean')
        product.image_url = request.form.get('image_url')
        product.description = request.form.get('description')
        product.slug = product.name.lower().replace(' ', '-')
        db.session.commit()
        flash(f'Product "{product.name}" updated', 'success')
        return redirect(url_for('admin.products'))
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/product_edit.html', product=product, categories=categories)

@admin.route('/product/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted', 'success')
    return redirect(url_for('admin.products'))

@admin.route('/stores')
@login_required
@admin_required
def stores():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    stores = Store.query.order_by(Store.name).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/stores.html', stores=stores)

@admin.route('/store/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_store():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        logo = request.form.get('logo')
        rating = request.form.get('rating', type=float, default=0.0)
        affiliate_network = request.form.get('affiliate_network')
        affiliate_params = request.form.get('affiliate_params')
        return_policy = request.form.get('return_policy')
        verified = 'verified' in request.form
        slug = name.lower().replace(' ', '-')
        store = Store(name=name, url=url, logo=logo, rating=rating, affiliate_network=affiliate_network, affiliate_params=affiliate_params, return_policy=return_policy, verified=verified, slug=slug)
        db.session.add(store)
        db.session.commit()
        flash(f'Store "{name}" created', 'success')
        return redirect(url_for('admin.stores'))
    return render_template('admin/store_edit.html', store=None)

@admin.route('/store/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_store(id):
    store = Store.query.get_or_404(id)
    if request.method == 'POST':
        store.name = request.form.get('name')
        store.url = request.form.get('url')
        store.logo = request.form.get('logo')
        store.rating = request.form.get('rating', type=float)
        store.affiliate_network = request.form.get('affiliate_network')
        store.affiliate_params = request.form.get('affiliate_params')
        store.return_policy = request.form.get('return_policy')
        store.verified = 'verified' in request.form
        store.slug = store.name.lower().replace(' ', '-')
        db.session.commit()
        flash(f'Store "{store.name}" updated', 'success')
        return redirect(url_for('admin.stores'))
    return render_template('admin/store_edit.html', store=store)

@admin.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories)

@admin.route('/category/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    name = request.form.get('name')
    parent_id = request.form.get('parent_id', type=int)
    icon = request.form.get('icon')
    slug = name.lower().replace(' ', '-')
    category = Category(name=name, parent_id=parent_id if parent_id else None, icon=icon, slug=slug)
    db.session.add(category)
    db.session.commit()
    flash(f'Category "{name}" created', 'success')
    return redirect(url_for('admin.categories'))

@admin.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/users.html', users=users)

@admin.route('/analytics')
@login_required
@admin_required
def analytics():
    days = request.args.get('days', 30, type=int)
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    daily_views = db.session.query(func.date(PageView.viewed_at), func.count(PageView.id)).filter(PageView.viewed_at >= start_date).group_by(func.date(PageView.viewed_at)).all()
    daily_clicks = db.session.query(func.date(Click.clicked_at), func.count(Click.id)).filter(Click.clicked_at >= start_date).group_by(func.date(Click.clicked_at)).all()
    top_referrers = db.session.query(PageView.referrer, func.count(PageView.id)).filter(PageView.referrer != None).group_by(PageView.referrer).order_by(func.count(PageView.id).desc()).limit(10).all()
    return render_template('admin/analytics.html', daily_views=daily_views, daily_clicks=daily_clicks, top_referrers=top_referrers, days=days)

@admin.route('/price-history/add/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def add_price_history(product_id):
    product = Product.query.get_or_404(product_id)
    store_id = request.form.get('store_id', type=int)
    price = request.form.get('price', type=float)
    if store_id and price:
        history = PriceHistory(product_id=product_id, store_id=store_id, price=price)
        db.session.add(history)
        db.session.commit()
        flash('Price history added', 'success')
    return redirect(url_for('admin.products'))
