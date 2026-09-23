# Hello World - Kiro

A simple Python Flask web application that displays "Hello, World!" in multiple languages.

## Supported Languages

- 🇬🇧 **English** - Hello, World! (Currency: GBP £)
- 🇩🇪 **German (Deutsch)** - Hallo, Welt! (Currency: EUR €)
- 🇫🇷 **French (Français)** - Bonjour, le monde! (Currency: EUR €)
- 🇭🇷 **Croatian (Hrvatski)** - Pozdrav, svijete! (Currency: EUR €)
- 🇪🇸 **Spanish (Español)** - ¡Hola, Mundo! (Currency: EUR €)
- 🇹🇷 **Turkish (Türkçe)** - Merhaba, Dünya! (Currency: TRY ₺)
- 🇵🇹 **Portuguese (Português)** - Olá, Mundo! (Currency: EUR €)
- 🇺🇸 **US Dollar** - USD $ (Base currency for conversions)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository (if not already done)

```bash
git clone https://github.com/dstar55/hello-world-kiro.git
cd hello-world-kiro
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

1. Ensure your virtual environment is activated
2. Run the application:

```bash
python app.py
```

3. Open your web browser and navigate to:

```
http://localhost:5000
```

You should see "Hello, World!" displayed on the page with a beautiful gradient background.

## Available Routes

The application supports multiple language routes:

- **English (default)**: `http://localhost:5000/`
- **German**: `http://localhost:5000/de`
- **French**: `http://localhost:5000/fr`
- **Croatian**: `http://localhost:5000/hr`
- **Spanish**: `http://localhost:5000/es`
- **Turkish**: `http://localhost:5000/tr`
- **Portuguese**: `http://localhost:5000/pt`

You can also switch between languages using the language selector buttons on the page.

## Currency Converter

The application includes a built-in currency converter with **live exchange rates** that supports the following currencies:

- **USD** - US Dollar ($)
- **EUR** - Euro (€)
- **GBP** - British Pound (£)
- **TRY** - Turkish Lira (₺)

### Exchange Rate Source

Exchange rates are fetched in real-time from **[exchangerate-api.com](https://exchangerate-api.com)**, a free and reliable API that provides current foreign exchange rates from multiple sources.

**Features:**
- 🔄 **Live rates**: Updated automatically from multiple foreign exchange sources
- ⚡ **Smart caching**: Rates cached for 1 hour to improve performance
- 🛡️ **Fallback protection**: Uses static rates if API is unavailable
- 📊 **Transparent**: Shows whether rates are live or cached
- 🕐 **Rate timestamps**: Displays when rates were last updated

### How to Use

1. Enter the amount you want to convert
2. Select the source currency from the "From" dropdown
3. Select the target currency from the "To" dropdown
4. Click the "Convert" button to see the result
5. The converter displays:
   - Converted amount with currency symbols
   - Current exchange rate
   - Rate source (live/cached)
   - Last update timestamp

### Technical Details

- **API Endpoint**: `https://api.exchangerate-api.com/v4/latest/USD`
- **Update Frequency**: Updated multiple times per day
- **Cache Duration**: 1 hour (configurable)
- **Base Currency**: USD (all conversions use USD as intermediate)
- **Error Handling**: Automatic fallback to static rates if API is unavailable
- **No API Key Required**: Uses the free v4 API endpoint

## Stopping the Application

Press `Ctrl+C` in the terminal where the application is running.

## Project Structure

```
hello-world-kiro/
├── app.py              # Main Flask application
├── templates/          # HTML templates directory
│   └── index.html     # Homepage template
├── requirements.txt    # Python dependencies
├── .kiro/             # Kiro configuration
│   └── steering/      # Steering rules
├── .gitignore         # Git ignore rules
├── LICENSE            # License file
└── README.md          # This file
```

## Technology Stack

- **Framework**: Flask 3.0+
- **Language**: Python 3.8+
- **Template Engine**: Jinja2 (built into Flask)

## Features

- **Multi-language support**: English, German, French, Croatian, Spanish, Turkish, and Portuguese
- **Live currency converter**: Convert between USD, EUR, GBP, and TRY with real-time exchange rates
- **Exchange rate API**: Powered by [exchangerate-api.com](https://exchangerate-api.com) with multi-source data
- **Smart caching**: Rates cached for 1 hour to optimize performance
- **Automatic fallback**: Uses static rates if API is unavailable
- **Language switcher**: Easy navigation between language versions with flag emojis
- **Clean Flask structure**: Route-based language implementation
- **Responsive design**: Works on desktop, tablet, and mobile devices
- **Modern styling**: Beautiful gradient background with centered card layout
- **Debug mode**: Enabled for development with auto-reload

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can change it by modifying the last line in `app.py`:

```python
app.run(host='localhost', port=5001, debug=True)  # Change to any available port
```

### Module Not Found Error

Make sure you've activated the virtual environment and installed dependencies:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Permission Denied

On some systems, you may need to use `python3` instead of `python`:

```bash
python3 -m venv venv
python3 app.py
```

## Development Notes

- The application runs in debug mode by default, which provides:
  - Automatic reloading when code changes
  - Detailed error messages
  - Interactive debugger

**⚠️ Warning**: Never run with `debug=True` in production!

## License

See LICENSE file for details.
