"""
Aurora Price Comparison - Database Models
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    
    parent = db.relationship('Category', remote_side=[id], backref='children')
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    @property
    def product_count(self):
        return self.products.count()
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    affiliate_network = db.Column(db.String(50), nullable=True)
    affiliate_params = db.Column(db.Text, nullable=True)
    return_policy = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prices = db.relationship('Price', backref='store', lazy='dynamic')
    clicks = db.relationship('Click', backref='store', lazy='dynamic')
    
    def get_affiliate_link(self, product_url):
        if not self.affiliate_params:
            return product_url
        return f"{product_url}?ref=aurora&utm_source=aurora&utm_medium=affiliate"
    
    def __repr__(self):
        return f'<Store {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    ean = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    specs_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prices = db.relationship('Price', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    price_history = db.relationship('PriceHistory', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    clicks = db.relationship('Click', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def lowest_price(self):
        price = self.prices.filter(Price.stock_status == 'in_stock').order_by(Price.price.asc()).first()
        return price
    
    @property
    def lowest_price_ever(self):
        history = self.price_history.order_by(PriceHistory.price.asc()).first()
        return history.price if history else None
    
    @property
    def store_count(self):
        return self.prices.count()
    
    @property
    def avg_rating(self):
        stores = self.prices.join(Store).with_entities(func.avg(Store.rating)).scalar()
        return round(stores, 1) if stores else 0
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Price(db.Model):
    __tablename__ = 'prices'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    shipping = db.Column(db.Float, default=0.0)
    stock_status = db.Column(db.String(20), default='in_stock')
    affiliate_link = db.Column(db.String(500), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def total_price(self):
        return self.price + self.shipping
    
    def get_tracked_link(self, user_id=None):
        if self.affiliate_link:
            base = self.affiliate_link
            if user_id:
                return f"{base}&aurora_ref={user_id}"
            return base
        return self.store.url
    
    def __repr__(self):
        return f'<Price {self.product_id} - {self.store_id}: {self.price}>'


class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    store = db.relationship('Store', backref=db.backref('price_history', lazy='dynamic'))
    
    def __repr__(self):
        return f'<PriceHistory {self.product_id} - {self.price}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    price_alerts = db.relationship('PriceAlert', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    clicks = db.relationship('Click', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>'


class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_favorite'),)
    
    def __repr__(self):
        return f'<Favorite user={self.user_id} product={self.product_id}>'


class PriceAlert(db.Model):
    __tablename__ = 'price_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_notified = db.Column(db.DateTime, nullable=True)
    
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<PriceAlert user={self.user_id} product={self.product_id}>'


class Click(db.Model):
    __tablename__ = 'clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    referrer = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Click product={self.product_id} store={self.store_id}>'


class PageView(db.Model):
    __tablename__ = 'page_views'
    
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    referrer = db.Column(db.String(500), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PageView {self.path}>'
