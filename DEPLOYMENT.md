# Aurora Deployment Guide

## 🚀 Deploy Your Price Comparison Website

### **Option 1: Railway (Recommended - Easiest)**

**Pros:**
- Free tier available
- Automatic SSL/HTTPS
- Easy database setup
- GitHub integration

**Steps:**

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   ```
   a. Go to https://railway.app/new
   b. Select "Deploy from GitHub repo"
   c. Choose your aurora repository
   d. Railway will auto-detect Flask
   ```

3. **Configure Environment Variables**
   ```bash
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://...
   ```

4. **Deploy!**
   - Railway builds and deploys automatically
   - You'll get a URL like `aurora.up.railway.app`

---

### **Option 2: Render (Great Free Tier)**

**Steps:**

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   ```
   a. Click "New +" → "Web Service"
   b. Connect your GitHub repo
   c. Configure:
      - Runtime: Python 3
      - Build Command: pip install -r requirements.txt
      - Start Command: python app.py
   ```

3. **Add Environment Variables**
   ```
   SECRET_KEY=generate-a-random-key
   DATABASE_URL=render-postgres-url
   ```

4. **Deploy**
   - Automatic deployment from GitHub
   - Free SSL certificate included

---

### **Option 3: Vercel + Python (Best Performance)**

**Steps:**

1. **Create vercel.json** in project root:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

2. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

---

### **Option 4: DigitalOcean (Full Control)**

**For production apps with high traffic**

**Docker Setup:**

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

2. **Create docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - DATABASE_URL=postgresql://...
       depends_on:
         - db

     db:
       image: postgres:15
       environment:
         POSTGRES_PASSWORD: yourpassword
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

3. **Deploy to DigitalOcean:**
   ```bash
   docker-compose up -d
   ```

---

## 🔄 Automatic Price Updates

### **Using GitHub Actions (Free)**

Create `.github/workflows/price-update.yml`:

```yaml
name: Update Prices
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:      # Manual trigger

jobs:
  update-prices:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd aurora/aurora
          pip install -r requirements.txt
          pip install requests beautifulsoup4 lxml

      - name: Run price scraper
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
        run: |
          cd aurora/aurora
          python price_scraper.py
```

---

### **Using Cron Jobs (VPS/Server)**

Add to crontab:
```bash
crontab -e

# Update prices every 6 hours
0 */6 * * * cd /path/to/aurora/aurora && source venv/bin/activate && python price_scraper.py
```

---

## 📊 Monitoring

**Recommended Tools:**
- **Uptime Robot** - Free uptime monitoring
- **Sentry** - Error tracking (free tier available)
- **Google Analytics** - Visitor analytics

---

## 🔒 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (automatic on Railway/Render)
- [ ] Set up database backups
- [ ] Rate limiting on API endpoints
- [ ] CSRF protection enabled
- [ ] Strong password policy

---

## 💰 Cost Estimates

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| Railway | $5/month credit | $5-20/month |
| Render | Free (limited) | $7/month+ |
| Vercel | Free (hobby) | $20/month+ |
| DigitalOcean | $0 (first month) | $4-12/month |

---

## 🎯 Quick Deploy (Railway)

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Go to https://railway.app/new
# 3. Click "Deploy from GitHub repo"
# 4. Select your aurora repository
# 5. Add environment variables
# 6. Click "Deploy"
```

That's it! Your site will be online in ~2 minutes. 🚀
