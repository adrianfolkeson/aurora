# Aurora - Price Comparison Website

A full-featured affiliate marketing price comparison platform built with Flask.

![Aurora](https://img.shields.io/badge/Aurora-Price%20Comparison-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)

## Features

- 🏷️ **Price Comparison** - Compare prices across multiple stores
- 🔍 **Smart Search** - Autocomplete, spelling correction, relevance ranking
- ❤️ **Favorites** - Save products for later
- 🔔 **Price Alerts** - Get notified when prices drop
- 📊 **Admin Panel** - Full product, store, and user management
- 📱 **Responsive Design** - Works on mobile, tablet, and desktop
- 🔐 **User Authentication** - Register, login, and manage account
- 📈 **Affiliate Tracking** - Track clicks and conversions

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Database**: SQLite (easily scalable to PostgreSQL)
- **Frontend**: HTML, CSS (Aurora theme), Vanilla JavaScript
- **Deployment**: Ready for Vercel, Railway, or any WSGI server

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/aurora.git
cd aurora

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open http://localhost:5000 in your browser.

## Admin Login

- **Email**: admin@aurora.se
- **Password**: admin123

## Project Structure

```
aurora/
├── app/
│   ├── routes/          # All Flask routes
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JS, images
│   ├── models.py        # Database models
│   └── extensions.py    # Flask extensions
├── instance/            # SQLite database
├── app.py               # Main application entry
├── requirements.txt     # Python dependencies
└── SPEC.md             # Project specification
```

## Routes

| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/category/<slug>` | Category page |
| `/product/<slug>` | Product detail with price comparison |
| `/search` | Search results |
| `/favorites` | Saved products |
| `/price-alerts` | Price alerts |
| `/stores` | All stores |
| `/store/<slug>` | Store detail |
| `/admin/*` | Admin panel |
| `/api/*` | REST API endpoints |

## Screenshots

The website features:
- Modern Aurora blue theme (#0ea5e9)
- Hero section with search
- Category cards
- Product grids with filters
- Price comparison tables
- Price history charts

## License

MIT License - Feel free to use for your own projects!

---

Built with ❤️ using Flask
