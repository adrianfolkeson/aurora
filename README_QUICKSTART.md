# 🎉 Aurora - Quick Start Guide

## ✅ What's Been Done

1. **Account Setup**
   - ✅ Email: du.vet.adde.17@gmail.com
   - ✅ Name: Adrian
   - ✅ Role: Admin (full access)

2. **Sample Data Created**
   - ✅ 5 Categories (Datorer, Mobiltelefoner, Laptops, Surfplattor, Headset)
   - ✅ 4 Stores (Elgiganten, NetOnNet, Komplett, Webhallen)
   - ✅ 10 Products (MacBooks, iPhones, Samsung, Sony, etc.)
   - ✅ 40 Prices across all stores

3. **Tools Created**
   - ✅ Price scraper (price_scraper.py)
   - ✅ Sample data script (create_sample_data.py)
   - ✅ Deployment guide (DEPLOYMENT.md)

4. **Everything Pushed to GitHub**
   - ✅ Repository: https://github.com/adrianfolkeson/aurora

---

## 🚀 Your Website is Ready!

**Access it now:** http://127.0.0.1:5001

**Admin Panel:** http://127.0.0.1:5001/admin

**Login:**
- Email: **du.vet.adde.17@gmail.com**
- Password: *(your created password)*

---

## 📝 How to Use Your Website

### **Adding Products (Manual)**

1. Go to http://127.0.0.1:5001/admin
2. Click "Categories" → Add new category
3. Click "Stores" → Add new store
4. Click "Products" → Add new product with prices

### **Updating Prices (Automatic)**

Run the price scraper:
```bash
cd aurora/aurora
source venv/bin/activate
python price_scraper.py
```

### **Schedule Automatic Updates (Cron)**

```bash
# Open crontab
crontab -e

# Add this line (updates every 6 hours)
0 */6 * * * cd /Users/adrianfolkeson/Projekt/aurora/aurora && source venv/bin/activate && python price_scraper.py
```

---

## 🌍 Deploy Online (Free Options)

### **Easiest: Railway (5 minutes)**

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select "aurora" repository
4. Add environment variables:
   - SECRET_KEY: `(generate random key)`
   - DATABASE_URL: `(Railway will provide this)`
5. Click "Deploy"

**Your site will be live in 2 minutes!**

### **Alternative: Render**

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`

---

## 🛠️ Maintenance

### **Update Prices Manually**
```bash
cd aurora/aurora
source venv/bin/activate
python price_scraper.py
```

### **Restart the Server**
```bash
# Stop: Ctrl+C
# Start:
cd aurora/aurora
source venv/bin/activate
python app.py
```

### **Backup Your Database**
```bash
cp instance/aurora.db instance/aurora.db.backup
```

---

## 📚 Next Steps

1. **Add More Products**
   - Use admin panel or create_sample_data.py

2. **Customize Design**
   - Edit: `app/static/css/style.css`
   - Edit: `app/templates/base.html`

3. **Connect Real Stores**
   - Update price_scraper.py with actual store APIs
   - Or use affiliate networks (Adtraction, Awin, etc.)

4. **Deploy Online**
   - Follow DEPLOYMENT.md guide
   - Railway recommended for easiest setup

---

## 🔧 Troubleshooting

**Port 5000 in use?**
```bash
# Use port 5001 instead:
python -c "from app import create_app; app = create_app(); app.run(port=5001)"
```

**Database errors?**
```bash
# Recreate database:
rm instance/aurora.db
python create_sample_data.py
```

**Price scraper not working?**
- Stores may have blocked scraping
- Update selectors in price_scraper.py
- Or use affiliate APIs instead

---

## 📊 Your Repository

**GitHub:** https://github.com/adrianfolkeson/aurora

**All changes are saved and pushed!**

---

## 🎯 Quick Commands

```bash
# Start server
cd aurora/aurora && source venv/bin/activate && python app.py

# Update prices
cd aurora/aurora && source venv/bin/activate && python price_scraper.py

# Create sample data
cd aurora/aurora && source venv/bin/activate && python create_sample_data.py

# Check database
cd aurora/aurora && source venv/bin/activate && python -c "from app import create_app, db; from app.models import Product, Store; app = create_app(); with app.app_context(): print(f'Products: {Product.query.count()}, Stores: {Store.query.count()}')"
```

---

## 🎉 Enjoy Your Price Comparison Website!

You now have a fully functional affiliate marketing site ready to deploy!

**Need help?** Check DEPLOYMENT.md or ask me! 😊
