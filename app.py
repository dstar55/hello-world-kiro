"""
Flask Hello World Application

A simple web application that displays 'Hello, World!' in multiple languages.
Supports: English, German, French, Croatian, Spanish, Turkish, Portuguese, and Russian.
Includes a currency converter with live exchange rates from exchangerate-api.com.
Includes Google OAuth authentication with superadmin approval workflow.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import requests
from datetime import datetime, timedelta
import os
import json
from functools import wraps
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from authlib.integrations.flask_client import OAuth
from models import db, User

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data/users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration - 7 day persistent sessions
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Google OAuth configuration
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_DISCOVERY_URL'] = 'https://accounts.google.com/.well-known/openid-configuration'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Create tables on first request
@app.before_request
def create_tables():
    """Create database tables if they don't exist."""
    if not hasattr(app, '_tables_created'):
        with app.app_context():
            # Create data directory if it doesn't exist
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else 'data', exist_ok=True)
            db.create_all()
            app._tables_created = True


# ============================================================================
# Authentication Decorators
# ============================================================================

def approved_required(f):
    """
    Decorator to require that user is logged in AND approved.
    Redirects to pending page if user is authenticated but not approved.
    Redirects to login if user is not authenticated.
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.is_rejected():
            # User is rejected, log them out and show error
            logout_user()
            return render_template('error.html',
                                 error_title='Access Denied',
                                 error_message='Your registration request has been rejected. Please contact the administrator.',
                                 languages=LANGUAGES,
                                 current_lang='en'), 403
        
        if current_user.is_pending():
            # User is pending approval
            return redirect(url_for('pending_approval'))
        
        if not current_user.is_approved():
            # User has some other status
            return render_template('error.html',
                                 error_title='Access Denied',
                                 error_message='You do not have permission to access this page.',
                                 languages=LANGUAGES,
                                 current_lang='en'), 403
        
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator to require that user is logged in, approved, AND is a superadmin.
    Combines approved_required with superadmin check.
    """
    @wraps(f)
    @approved_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_superadmin():
            return render_template('error.html',
                                 error_title='Admin Access Required',
                                 error_message='You must be a superadmin to access this page.',
                                 languages=LANGUAGES,
                                 current_lang='en'), 403
        
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# Helper Functions
# ============================================================================

# Language configurations with currency data
LANGUAGES = {
    'en': {
        'name': 'English',
        'greeting': 'Hello, World!',
        'flag': '🇬🇧',
        'currency': 'GBP',
        'currency_symbol': '£',
        'currency_name': 'British Pound'
    },
    'de': {
        'name': 'Deutsch',
        'greeting': 'Hallo, Welt!',
        'flag': '🇩🇪',
        'currency': 'EUR',
        'currency_symbol': '€',
        'currency_name': 'Euro'
    },
    'fr': {
        'name': 'Français',
        'greeting': 'Bonjour, le monde!',
        'flag': '🇫🇷',
        'currency': 'EUR',
        'currency_symbol': '€',
        'currency_name': 'Euro'
    },
    'hr': {
        'name': 'Hrvatski',
        'greeting': 'Pozdrav, svijete!',
        'flag': '🇭🇷',
        'currency': 'EUR',
        'currency_symbol': '€',
        'currency_name': 'Euro'
    },
    'es': {
        'name': 'Español',
        'greeting': '¡Hola, Mundo!',
        'flag': '🇪🇸',
        'currency': 'EUR',
        'currency_symbol': '€',
        'currency_name': 'Euro'
    },
    'tr': {
        'name': 'Türkçe',
        'greeting': 'Merhaba, Dünya!',
        'flag': '🇹🇷',
        'currency': 'TRY',
        'currency_symbol': '₺',
        'currency_name': 'Turkish Lira'
    },
    'pt': {
        'name': 'Português',
        'greeting': 'Olá, Mundo!',
        'flag': '🇵🇹',
        'currency': 'EUR',
        'currency_symbol': '€',
        'currency_name': 'Euro'
    },
    'ru': {
        'name': 'Русский',
        'greeting': 'Привет, мир!',
        'flag': '🇷🇺',
        'currency': 'RUB',
        'currency_symbol': '₽',
        'currency_name': 'Russian Ruble'
    }
}

# Exchange rates cache
EXCHANGE_RATES_CACHE = {
    'rates': None,
    'last_updated': None,
    'cache_duration': timedelta(hours=1)  # Cache for 1 hour
}

# Fallback exchange rates (base: USD) - used if API is unavailable
FALLBACK_EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'TRY': 34.15,
}


def fetch_exchange_rates():
    """
    Fetch live exchange rates from exchangerate-api.com (free v4 API).
    Uses caching to avoid excessive API calls.
    Falls back to static rates if API is unavailable.
    
    Returns:
        dict: Exchange rates with USD as base currency
    """
    # Check if we have cached rates that are still valid
    if EXCHANGE_RATES_CACHE['rates'] and EXCHANGE_RATES_CACHE['last_updated']:
        time_since_update = datetime.now() - EXCHANGE_RATES_CACHE['last_updated']
        if time_since_update < EXCHANGE_RATES_CACHE['cache_duration']:
            return EXCHANGE_RATES_CACHE['rates']
    
    try:
        # Fetch latest rates with USD as base currency from exchangerate-api.com (free)
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract rates - USD is already the base
        rates = data.get('rates', {})
        
        # Update cache
        EXCHANGE_RATES_CACHE['rates'] = rates
        EXCHANGE_RATES_CACHE['last_updated'] = datetime.now()
        
        print(f"✓ Successfully fetched live exchange rates at {datetime.now()}")
        print(f"  Rates from: {data.get('provider', 'exchangerate-api.com')}")
        print(f"  Last updated: {data.get('date', 'unknown')}")
        return rates
        
    except requests.exceptions.RequestException as e:
        print(f"⚠ Warning: Could not fetch live rates from API: {e}")
        print("  Using fallback static rates instead")
        
        # If API fails and we have no cached rates, use fallback
        if EXCHANGE_RATES_CACHE['rates'] is None:
            EXCHANGE_RATES_CACHE['rates'] = FALLBACK_EXCHANGE_RATES
            EXCHANGE_RATES_CACHE['last_updated'] = datetime.now()
        
        return EXCHANGE_RATES_CACHE['rates']
    except Exception as e:
        print(f"⚠ Unexpected error fetching exchange rates: {e}")
        
        # Use fallback rates
        if EXCHANGE_RATES_CACHE['rates'] is None:
            EXCHANGE_RATES_CACHE['rates'] = FALLBACK_EXCHANGE_RATES
            EXCHANGE_RATES_CACHE['last_updated'] = datetime.now()
        
        return EXCHANGE_RATES_CACHE['rates']


def get_all_currencies():
    """Get unique list of all currencies from languages, including USD."""
    currencies = {}
    
    # Add USD first
    currencies['USD'] = {
        'code': 'USD',
        'symbol': '$',
        'name': 'US Dollar'
    }
    
    # Add currencies from languages
    for lang_code, lang_data in LANGUAGES.items():
        currency = lang_data['currency']
        if currency not in currencies:
            currencies[currency] = {
                'code': currency,
                'symbol': lang_data['currency_symbol'],
                'name': lang_data['currency_name']
            }
    
    return currencies


# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/login')
def login():
    """Initiate Google OAuth login flow."""
    # Store the page user was trying to access
    next_page = request.args.get('next')
    if next_page:
        session['next_url'] = next_page
    
    # Build redirect URI
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth/callback')
def auth_callback():
    """Handle Google OAuth callback."""
    try:
        # Get authorization token
        token = google.authorize_access_token()
        
        # Get user info from Google
        resp = google.get('https://openidconnect.googleapis.com/v1/userinfo')
        user_info = resp.json()
        
        # Extract user details
        email = user_info.get('email')
        name = user_info.get('name')
        picture = user_info.get('picture')
        
        # Validate email domain - only Gmail addresses allowed
        if not email or not email.endswith('@gmail.com'):
            return render_template('error.html',
                                 error_title='Invalid Email Domain',
                                 error_message='Only Gmail addresses are allowed. Please sign in with a Gmail account.',
                                 languages=LANGUAGES,
                                 current_lang='en')
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user with pending status
            user = User(
                email=email,
                name=name,
                profile_picture=picture,
                role='user',
                status='pending'
            )
            db.session.add(user)
            db.session.commit()
            print(f"✓ New user created: {email} (status: pending)")
        else:
            # Update user info
            user.name = name
            user.profile_picture = picture
            db.session.commit()
            print(f"✓ User login: {email} (status: {user.status})")
        
        # Log in the user (even if pending)
        login_user(user, remember=True, duration=timedelta(days=7))
        session.permanent = True
        
        # Redirect to original destination or home
        next_url = session.pop('next_url', None)
        if next_url:
            return redirect(next_url)
        
        # If user is pending, redirect to pending page
        if user.is_pending():
            return redirect(url_for('pending_approval'))
        
        # If user is rejected, show error
        if user.is_rejected():
            logout_user()
            return render_template('error.html',
                                 error_title='Access Denied',
                                 error_message='Your registration request has been rejected. Please contact the administrator.',
                                 languages=LANGUAGES,
                                 current_lang='en')
        
        # Approved users go to dashboard
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        print(f"✗ OAuth error: {e}")
        return render_template('error.html',
                             error_title='Authentication Error',
                             error_message=f'An error occurred during authentication: {str(e)}',
                             languages=LANGUAGES,
                             current_lang='en')


@app.route('/logout')
def logout():
    """Log out the current user."""
    logout_user()
    return redirect(url_for('index'))


@app.route('/pending')
def pending_approval():
    """Page shown to users awaiting approval."""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if not current_user.is_pending():
        # User is not pending, redirect appropriately
        if current_user.is_approved():
            return redirect(url_for('dashboard'))
        elif current_user.is_rejected():
            logout_user()
            return render_template('error.html',
                                 error_title='Access Denied',
                                 error_message='Your registration request has been rejected.',
                                 languages=LANGUAGES,
                                 current_lang='en')
    
    return render_template('pending.html',
                         user=current_user,
                         languages=LANGUAGES,
                         current_lang='en')


# ============================================================================
# Private User Pages
# ============================================================================

@app.route('/dashboard')
@approved_required
def dashboard():
    """User dashboard - accessible to approved users."""
    return render_template('dashboard.html',
                         user=current_user,
                         languages=LANGUAGES,
                         current_lang='en')


@app.route('/profile')
@approved_required
def profile():
    """User profile page - accessible to approved users."""
    return render_template('profile.html',
                         user=current_user,
                         languages=LANGUAGES,
                         current_lang='en')


# ============================================================================
# Admin Pages
# ============================================================================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard - shows all users and pending approvals."""
    # Get all users, sorted by status (pending first) then by creation date
    all_users = User.query.order_by(
        db.case(
            (User.status == 'pending', 0),
            (User.status == 'approved', 1),
            (User.status == 'rejected', 2),
            else_=3
        ),
        User.created_at.desc()
    ).all()
    
    # Count users by status
    pending_count = User.query.filter_by(status='pending').count()
    approved_count = User.query.filter_by(status='approved').count()
    rejected_count = User.query.filter_by(status='rejected').count()
    
    return render_template('admin_dashboard.html',
                         users=all_users,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count,
                         languages=LANGUAGES,
                         current_lang='en')


@app.route('/admin/user/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(user_id):
    """Approve a pending user."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot modify your own status'}), 400
    
    user.status = 'approved'
    db.session.commit()
    
    print(f"✓ User approved: {user.email} by {current_user.email}")
    
    return jsonify({
        'success': True,
        'message': f'User {user.email} has been approved',
        'user': user.to_dict()
    })


@app.route('/admin/user/<int:user_id>/reject', methods=['POST'])
@admin_required
def reject_user(user_id):
    """Reject a pending user."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot modify your own status'}), 400
    
    user.status = 'rejected'
    db.session.commit()
    
    print(f"✓ User rejected: {user.email} by {current_user.email}")
    
    return jsonify({
        'success': True,
        'message': f'User {user.email} has been rejected',
        'user': user.to_dict()
    })


@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot delete yourself'}), 400
    
    if user.is_superadmin():
        return jsonify({'success': False, 'error': 'Cannot delete a superadmin'}), 400
    
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    print(f"✓ User deleted: {email} by {current_user.email}")
    
    return jsonify({
        'success': True,
        'message': f'User {email} has been deleted'
    })


# ============================================================================
# Main Language Routes
# ============================================================================


@app.route('/')
def index():
    """
    Homepage route handler - English version.
    
    Returns:
        Rendered HTML template displaying 'Hello, World!' in English
    """
    return render_template('index.html', 
                         current_lang='en',
                         greeting=LANGUAGES['en']['greeting'],
                         lang_name=LANGUAGES['en']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/de')
def german():
    """
    German language route handler.
    
    Returns:
        Rendered HTML template displaying 'Hallo, Welt!' in German
    """
    return render_template('index.html',
                         current_lang='de',
                         greeting=LANGUAGES['de']['greeting'],
                         lang_name=LANGUAGES['de']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/fr')
def french():
    """
    French language route handler.
    
    Returns:
        Rendered HTML template displaying 'Bonjour, le monde!' in French
    """
    return render_template('index.html',
                         current_lang='fr',
                         greeting=LANGUAGES['fr']['greeting'],
                         lang_name=LANGUAGES['fr']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/hr')
def croatian():
    """
    Croatian language route handler.
    
    Returns:
        Rendered HTML template displaying 'Pozdrav, svijete!' in Croatian
    """
    return render_template('index.html',
                         current_lang='hr',
                         greeting=LANGUAGES['hr']['greeting'],
                         lang_name=LANGUAGES['hr']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/es')
def spanish():
    """
    Spanish language route handler.
    
    Returns:
        Rendered HTML template displaying '¡Hola, Mundo!' in Spanish
    """
    return render_template('index.html',
                         current_lang='es',
                         greeting=LANGUAGES['es']['greeting'],
                         lang_name=LANGUAGES['es']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/tr')
def turkish():
    """
    Turkish language route handler.
    
    Returns:
        Rendered HTML template displaying 'Merhaba, Dünya!' in Turkish
    """
    return render_template('index.html',
                         current_lang='tr',
                         greeting=LANGUAGES['tr']['greeting'],
                         lang_name=LANGUAGES['tr']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/pt')
def portuguese():
    """
    Portuguese language route handler.
    
    Returns:
        Rendered HTML template displaying 'Olá, Mundo!' in Portuguese
    """
    return render_template('index.html',
                         current_lang='pt',
                         greeting=LANGUAGES['pt']['greeting'],
                         lang_name=LANGUAGES['pt']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/ru')
def russian():
    """
    Russian language route handler.
    
    Returns:
        Rendered HTML template displaying 'Привет, мир!' in Russian
    """
    return render_template('index.html',
                         current_lang='ru',
                         greeting=LANGUAGES['ru']['greeting'],
                         lang_name=LANGUAGES['ru']['name'],
                         languages=LANGUAGES,
                         currencies=get_all_currencies(),
                         current_user=current_user)


@app.route('/api/convert', methods=['POST'])
def convert_currency():
    """
    API endpoint for currency conversion using live exchange rates.
    
    Expects JSON payload with:
    - amount: float
    - from_currency: string (currency code)
    - to_currency: string (currency code)
    
    Returns:
        JSON with converted amount, exchange rate, and rate source info
    """
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_currency = data.get('from_currency', 'USD')
        to_currency = data.get('to_currency', 'EUR')
        
        # Fetch live exchange rates
        exchange_rates = fetch_exchange_rates()
        
        # Validate currencies
        if from_currency not in exchange_rates or to_currency not in exchange_rates:
            return jsonify({'error': 'Invalid currency code'}), 400
        
        # Convert to USD first, then to target currency
        amount_in_usd = amount / exchange_rates[from_currency]
        converted_amount = amount_in_usd * exchange_rates[to_currency]
        
        # Calculate exchange rate
        exchange_rate = exchange_rates[to_currency] / exchange_rates[from_currency]
        
        # Determine if using live or cached rates
        time_since_update = datetime.now() - EXCHANGE_RATES_CACHE['last_updated']
        is_cached = time_since_update < EXCHANGE_RATES_CACHE['cache_duration']
        
        return jsonify({
            'success': True,
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 2),
            'exchange_rate': round(exchange_rate, 4),
            'rate_source': 'cached' if is_cached else 'live',
            'last_updated': EXCHANGE_RATES_CACHE['last_updated'].isoformat() if EXCHANGE_RATES_CACHE['last_updated'] else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the application on localhost:5000 in debug mode
    app.run(host='localhost', port=5000, debug=True)
