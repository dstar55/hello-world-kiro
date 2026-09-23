"""
Flask Hello World Application

A simple web application that displays 'Hello, World!' in multiple languages.
Supports: English, German, French, Croatian, Spanish, Turkish, and Portuguese.
Includes a currency converter for each country's currency.
"""

from flask import Flask, render_template, jsonify, request

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
    }
}

# Exchange rates (base: USD)
# In production, these should be fetched from an API like exchangerate-api.com
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'TRY': 34.15,
}

def get_all_currencies():
    """Get unique list of all currencies from languages."""
    currencies = {}
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


@app.route('/api/convert', methods=['POST'])
def convert_currency():
    """
    API endpoint for currency conversion.
    
    Expects JSON payload with:
    - amount: float
    - from_currency: string (currency code)
    - to_currency: string (currency code)
    
    Returns:
        JSON with converted amount and exchange rate
    """
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_currency = data.get('from_currency', 'USD')
        to_currency = data.get('to_currency', 'EUR')
        
        # Validate currencies
        if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
            return jsonify({'error': 'Invalid currency code'}), 400
        
        # Convert to USD first, then to target currency
        amount_in_usd = amount / EXCHANGE_RATES[from_currency]
        converted_amount = amount_in_usd * EXCHANGE_RATES[to_currency]
        
        # Calculate exchange rate
        exchange_rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
        
        return jsonify({
            'success': True,
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 2),
            'exchange_rate': round(exchange_rate, 4)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the application on localhost:5000 in debug mode
    app.run(host='localhost', port=5000, debug=True)
