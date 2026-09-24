"""
Flask Hello World Application

A simple web application that displays 'Hello, World!' in multiple languages.
Supports: English, German, French, Croatian, Spanish, Turkish, and Portuguese.
Includes a currency converter with live exchange rates from exchangeratesapi.io.
"""

from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta

# Initialize Flask application
app = Flask(__name__)

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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
                         currencies=get_all_currencies())


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
