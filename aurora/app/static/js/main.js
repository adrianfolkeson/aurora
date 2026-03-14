// Aurora Price Comparison - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Search autocomplete
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('search-suggestions');
    
    if (searchInput && suggestionsBox) {
        let debounceTimer;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const query = this.value.trim();
            
            if (query.length < 2) {
                suggestionsBox.classList.remove('show');
                return;
            }
            
            debounceTimer = setTimeout(async function() {
                try {
                    const response = await fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`);
                    const results = await response.json();
                    
                    if (results.length > 0) {
                        suggestionsBox.innerHTML = results.map(item => `
                            <a href="/product/${item.slug}" class="suggestion-item">
                                <img src="${item.image || 'https://via.placeholder.com/40'}" alt="${item.name}">
                                <div>
                                    <strong>${item.name}</strong>
                                    ${item.brand ? `<small>${item.brand}</small>` : ''}
                                    ${item.price ? `<span>${item.price} kr</span>` : ''}
                                </div>
                            </a>
                        `).join('');
                        suggestionsBox.classList.add('show');
                    } else {
                        suggestionsBox.classList.remove('show');
                    }
                } catch (error) {
                    console.error('Search error:', error);
                }
            }, 300);
        });
        
        // Close suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.classList.remove('show');
            }
        });
        
        // Handle form submission
        searchInput.closest('form')?.addEventListener('submit', function(e) {
            if (suggestionsBox.classList.contains('show')) {
                e.preventDefault();
                const firstSuggestion = suggestionsBox.querySelector('a');
                if (firstSuggestion) {
                    window.location.href = firstSuggestion.href;
                }
            }
        });
    }
    
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }
    
    // Alert close buttons
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
    
    // Price alert form validation
    const priceAlertForm = document.querySelector('.price-alert-form');
    if (priceAlertForm) {
        priceAlertForm.addEventListener('submit', function(e) {
            const targetPrice = parseFloat(this.querySelector('input[name="target_price"]').value);
            if (!targetPrice || targetPrice <= 0) {
                e.preventDefault();
                alert('Ange ett giltigt målpris');
            }
        });
    }
    
    // Filter form auto-submit (optional - comment out if not wanted)
    // const filterForm = document.getElementById('filter-form');
    // if (filterForm) {
    //     filterForm.querySelectorAll('input, select').forEach(input => {
    //         input.addEventListener('change', () => filterForm.submit());
    //     });
    // }
    
    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Track outbound clicks
    document.querySelectorAll('a[target="_blank"]').forEach(link => {
        link.addEventListener('click', function() {
            const priceId = this.dataset.priceId;
            if (priceId) {
                fetch('/api/track-click', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ price_id: priceId })
                }).catch(console.error);
            }
        });
    });
});

// Format price with Swedish locale
function formatPrice(price) {
    return new Intl.NumberFormat('sv-SE', {
        style: 'currency',
        currency: 'SEK',
        minimumFractionDigits: 0
    }).format(price);
}

// Export for use in other scripts
window.Aurora = {
    formatPrice
};
