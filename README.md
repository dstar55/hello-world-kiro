# Hello World - Kiro

A simple Python Flask web application that displays "Hello, World!" in multiple languages.

## Supported Languages

- 🇬🇧 **English** - Hello, World!
- 🇩🇪 **German (Deutsch)** - Hallo, Welt!
- 🇫🇷 **French (Français)** - Bonjour, le monde!
- 🇭🇷 **Croatian (Hrvatski)** - Pozdrav, svijete!

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

You can also switch between languages using the language selector buttons on the page.

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

- **Multi-language support**: English, German, French, and Croatian
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
