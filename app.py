"""
Flask Hello World Application

A simple web application that displays 'Hello, World!' in multiple languages.
Supports: English, German, French, and Croatian.
"""

from flask import Flask, render_template

# Initialize Flask application
app = Flask(__name__)

# Language configurations
LANGUAGES = {
    'en': {
        'name': 'English',
        'greeting': 'Hello, World!',
        'flag': '🇬🇧'
    },
    'de': {
        'name': 'Deutsch',
        'greeting': 'Hallo, Welt!',
        'flag': '🇩🇪'
    },
    'fr': {
        'name': 'Français',
        'greeting': 'Bonjour, le monde!',
        'flag': '🇫🇷'
    },
    'hr': {
        'name': 'Hrvatski',
        'greeting': 'Pozdrav, svijete!',
        'flag': '🇭🇷'
    }
}


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
                         languages=LANGUAGES)


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
                         languages=LANGUAGES)


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
                         languages=LANGUAGES)


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
                         languages=LANGUAGES)


if __name__ == '__main__':
    # Run the application on localhost:5000 in debug mode
    app.run(host='localhost', port=5000, debug=True)
