# Aurora Price Comparison - Affiliate Marketing Website

## Project Overview
**Project Name:** Aurora - Price Comparison & Affiliate Marketing Platform
**Type:** Web Application (Flask + SQLite)
**Core Functionality:** A professional price comparison website where users can compare product prices from multiple retailers, track price history, set price alerts, and earn affiliate commissions.
**Target Users:** Swedish consumers looking for the best deals, and affiliate marketers earning commissions.

---

## UI/UX Specification

### Layout Structure

#### Header (Sticky)
- Logo: "Aurora" with aurora borealis-inspired gradient icon
- Search bar (prominent, centered)
- Category navigation dropdown
- User account menu (login/register or profile)
- Favorites/Price alerts icon with badge

#### Homepage
- Hero section with large search bar
- Popular categories grid (8 categories)
- Trending products carousel
- Latest deals section
- Featured brands
- Recent price drops

#### Category Page
- Breadcrumb navigation
- Filter sidebar (left, sticky on desktop)
- Product grid (right, responsive 2-4 columns)
- Pagination or infinite scroll

#### Product Detail Page
- Product images (gallery)
- Product name, brand, description
- Specifications table
- **Price comparison table** (core feature)
- Price history chart
- User reviews
- Similar products carousel

#### User Dashboard
- Saved products/favorites
- Price alerts management
- Click statistics
- Affiliate earnings (if applicable)

#### Admin Panel
- Product management (CRUD)
- Store management
- Price feed management
- Product matching tools
- Statistics dashboard
- User management

### Visual Design

#### Color Palette
```css
:root {
  /* Primary - Aurora inspired */
  --primary: #0f172a;        /* Deep navy */
  --primary-light: #1e293b;
  --accent: #06b6d4;         /* Cyan aurora */
  --accent-green: #10b981;   /* Success/savings */
  --accent-red: #ef4444;     /* Price increase/warning */
  
  /* Neutrals */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  
  /* Borders */
  --border: #e2e8f0;
  --border-hover: #cbd5e1;
  
  /* Trust signals */
  --verified: #10b981;
  --rating: #f59e0b;
}
```

#### Typography
- **Headings:** "Outfit" (Google Fonts) - modern, clean
- **Body:** "Inter" (Google Fonts) - highly readable
- **Monospace (prices):** "JetBrains Mono"

#### Spacing System (8px grid)
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px, 3xl: 64px

### Components

**Product Card:**
- Product image (lazy loaded)
- Product name (2 lines max, ellipsis)
- Brand badge
- **Lowest price** (prominent)
- Store count badge
- Rating stars
- Favorite button (heart icon)

**Price Table Row:**
- Store logo
- Product price (large)
- Shipping cost
- Stock status
- "See Price" button (affiliate link)

### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

---

## Functionality Specification

### Core Features

1. **Product Database** - Products with multiple prices from different stores
2. **Store Management** - Stores with logos, ratings, affiliate config
3. **Price Tracking** - Current prices, price history, lowest ever
4. **Search System** - Full-text search with autocomplete
5. **User System** - Registration, login, favorites, price alerts
6. **Affiliate System** - Link generation, click tracking, redirects
7. **Admin Panel** - Full CRUD, statistics, user management
8. **SEO Features** - Meta tags, Schema.org, sitemap, programmatic pages

---

## Acceptance Criteria

- [ ] Header is sticky with all elements
- [ ] Homepage has prominent search bar
- [ ] Product cards show: image, name, lowest price, store count, rating
- [ ] Price comparison table shows all stores
- [ ] Filters work and update product grid
- [ ] Mobile responsive
- [ ] Admin panel has all management features
- [ ] Search returns relevant results
- [ ] Affiliate links track clicks
- [ ] User can register, login, manage favorites
- [ ] Price alerts can be set
- [ ] SEO meta tags present

---

## Database Schema

- categories (id, name, slug, parent_id, icon)
- products (id, name, slug, brand, category_id, ean, image_url, description, specs_json, created_at)
- stores (id, name, slug, logo, url, rating, affiliate_network, affiliate_params, return_policy, verified, created_at)
- prices (id, product_id, store_id, price, shipping, stock_status, affiliate_link, last_updated)
- price_history (id, product_id, store_id, price, recorded_at)
- users (id, email, password_hash, name, role, created_at)
- favorites (id, user_id, product_id, created_at)
- price_alerts (id, user_id, product_id, target_price, active, created_at)
- clicks (id, product_id, store_id, user_id, referrer, ip_address, user_agent, clicked_at)

