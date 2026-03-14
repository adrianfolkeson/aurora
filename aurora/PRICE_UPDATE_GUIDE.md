# 🔧 Price Update System - Complete Guide

## 📋 Three Approaches to Update Prices

### **Approach 1: Manual Price Updates** ✅ (Already Working)

**Best for:** Testing, initial setup, few products

**How to use:**
1. Go to http://127.0.0.1:5001/admin
2. Click "Products"
3. Edit a product
4. Update prices for each store
5. Save

**Or use Python:**
```python
from price_system import update_price_manual

# Update iPhone 15 Pro at Elgiganten to 12,499 kr
update_price_manual(
    product_id=1,
    store_id=1,
    new_price=12499,
    shipping=0
)
```

---

### **Approach 2: Web Scraping** 🕷️ (Automated)

**Best for:** Medium volume, no API access

**How to use:**

```bash
# Test scraping
python price_system.py test

# Update all products via scraping
python price_system.py update scraper

# Schedule automatic updates (every 6 hours)
python price_system.py schedule
```

**Supported Stores:**
- ✅ Elgiganten.se
- ✅ NetOnNet.se
- ✅ Komplett.se
- ✅ Webhallen.se

**Note:** Web scraping may break if stores change their HTML.

---

### **Approach 3: Affiliate APIs** 🌐 (Production Ready)

**Best for:** High volume, reliability, production

**Swedish Affiliate Networks:**

| Network | Website | Stores | Setup Difficulty |
|----------|---------|--------|-------------------|
| **Adtraction** | attraction.com | 200+ Swedish stores | Medium |
| **Awin** | awin.com | 100+ Swedish stores | Medium |
| **Adrecord** | adrecord.com | 50+ Swedish stores | Easy |

**How to Get Access:**

1. **Adtraction (Recommended)**
   - Go to https://adtraction.com
   - Apply as publisher
   - Wait for approval (1-3 days)
   - Get API credentials
   - Set environment variable:
     ```bash
     export ATTRACTION_API_KEY="your-key-here"
     ```

2. **Awin**
   - Go to https://publishers.awin.com
   - Sign up as publisher
   - Apply to Swedish advertisers
   - Get API access
   - Set environment variable:
     ```bash
     export AWIN_API_KEY="your-key-here"
     ```

3. **Adrecord (Easiest)**
   - Go to https://adrecord.com
   - Quick signup process
   - Instant access to many Swedish stores

**How to use:**

```bash
# Update using API
python price_system.py update api

# Hybrid approach (API first, scraping fallback)
python price_system.py update hybrid
```

---

## 🚀 Quick Start Examples

### **Example 1: Update One Product Manually**

```python
from app import create_app, db
from app.models import Product
from price_system import update_price_manual

app = create_app()
with app.app_context():
    # Find iPhone 15 Pro
    product = Product.query.filter_by(name='iPhone 15 Pro').first()

    # Update at Elgiganten
    store_id = 1  # Elgiganten
    update_price_manual(product.id, store_id, 12499)

    print(f"✅ Updated {product.name}")
```

### **Example 2: Scrape All Products**

```bash
cd aurora/aurora
source venv/bin/activate
python price_system.py update scraper
```

### **Example 3: Setup Automatic Updates**

```bash
# Schedule automatic updates (every 6 hours)
python price_system.py schedule

# Check it was added
crontab -l
```

---

## 🔧 Advanced Configuration

### **Custom Scraping Intervals**

Edit crontab to change update frequency:
```bash
crontab -e

# Examples:
# Every hour
0 * * * * python /path/to/price_scraper.py

# Every 30 minutes
*/30 * * * * python /path/to/price_scraper.py

# Every day at midnight
0 0 * * * python /path/to/price_scraper.py

# Every Monday at 9am
0 9 * * 1 python /path/to/price_scraper.py
```

### **Add Custom Stores**

Create custom scraper in `price_system.py`:

```python
def scrape_custom_store(self, search_query):
    """Scrape a custom store"""
    try:
        url = f"https://custom-store.se/search?q={search_query}"
        response = self.session.get(url, timeout=10)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find price element (inspect store website to get selector)
        price_elem = soup.find('span', class_='custom-price-class')

        if price_elem:
            import re
            price_text = price_elem.get_text()
            price_match = re.search(r'(\d+[.,]\d+)', price_text)
            if price_match:
                return float(price_match.group(1))

        return None
    except Exception as e:
        logger.error(f"Custom store error: {e}")
        return None
```

---

## 📊 Monitor Price Updates

### **View Price History**

All price changes are tracked in `PriceHistory` table:

```python
from app import create_app, db
from app.models import PriceHistory

app = create_app()
with app.app_context():
    # Get price history for a product
    history = PriceHistory.query.filter_by(product_id=1).order_by(PriceHistory.recorded_at.desc()).limit(10).all()

    for record in history:
        print(f"{record.recorded_at}: {record.price} kr")
```

### **Create Price Alert for Users**

Users can set price alerts and get notified when prices drop!

---

## 🎯 Production Checklist

- [x] Manual price updates (via admin panel)
- [x] Web scraping system (price_scraper.py)
- [x] Affiliate API integration (price_system.py)
- [x] Scheduling system (cron jobs)
- [ ] **Get API keys** (Apply to Adtraction/Awin)
- [ ] **Test in production** (Start with manual, then API)
- [ ] **Set up monitoring** (Check if scraper is working)
- [ ] **Add error handling** (Email alerts when scraper fails)

---

## 💡 Pro Tips

1. **Start with manual updates** for the first 100 products
2. **Apply for affiliate APIs** early (takes 1-3 days to get approved)
3. **Use hybrid approach** (API + scraping fallback)
4. **Schedule updates** during off-peak hours (night/morning)
5. **Monitor your scrapers** (stores may block you)
6. **Respect rate limits** (don't overload store servers)

---

## 🚨 Troubleshooting

**Scraping not working?**
- Stores may have blocked your IP
- HTML structure may have changed
- Try using API instead

**API not working?**
- Check your API key is correct
- Verify you have access to the products
- Check API documentation for changes

**Cron job not running?**
- Check crontab: `crontab -l`
- Check logs: `grep CRON /var/log/syslog`
- Test manually first: `python price_system.py update scraper`

---

## 📞 Support

**Affiliate Networks:**
- Adtraction: https://adtraction.com/contact
- Awin: https://publishers.awin.com/contact
- Adrecord: https://adrecord.com/kontakt

**Swedish Affiliate Forums:**
- https://www.affiliatese.nu (Swedish affiliate community)

---

**🎉 You now have a complete price update system!**

Choose the approach that best fits your needs:
- **Testing/Development** → Manual updates
- **Small/Medium sites** → Web scraping
- **Production/Enterprise** → Affiliate APIs
