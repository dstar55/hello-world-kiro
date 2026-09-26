# Hello World - Kiro

A simple Python Flask web application that displays "Hello, World!" in multiple languages with **Google OAuth authentication** and **live currency conversion**.

## Features

- 🌍 **Multi-language support**: 8 languages (English, German, French, Croatian, Spanish, Turkish, Portuguese, Russian)
- 💱 **Live currency converter**: Real-time exchange rates for USD, EUR, GBP, TRY, RUB
- 🔐 **Google OAuth authentication**: Secure login with Gmail accounts
- 👥 **User management**: Superadmin approval workflow for new registrations
- 📊 **Admin dashboard**: Approve/reject users, manage accounts
- 🔒 **Private pages**: User dashboard and profile pages for authenticated users
- 📱 **Responsive design**: Works on all devices

## Supported Languages

- 🇬🇧 **English** - Hello, World! (Currency: GBP £)
- 🇩🇪 **German (Deutsch)** - Hallo, Welt! (Currency: EUR €)
- 🇫🇷 **French (Français)** - Bonjour, le monde! (Currency: EUR €)
- 🇭🇷 **Croatian (Hrvatski)** - Pozdrav, svijete! (Currency: EUR €)
- 🇪🇸 **Spanish (Español)** - ¡Hola, Mundo! (Currency: EUR €)
- 🇹🇷 **Turkish (Türkçe)** - Merhaba, Dünya! (Currency: TRY ₺)
- 🇵🇹 **Portuguese (Português)** - Olá, Mundo! (Currency: EUR €)
- 🇷🇺 **Russian (Русский)** - Привет, мир! (Currency: RUB ₽)
- 🇺🇸 **US Dollar** - USD $ (Base currency for conversions)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Cloud account (for OAuth credentials)
- Gmail account (for superadmin setup)

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

### 5. Configure Google OAuth

#### Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google+ API** (or Google Identity Services)
4. Go to **Credentials** → **Create Credentials** → **OAuth client ID**
5. Choose **Web application**
6. Add authorized redirect URIs:
   - For local development: `http://localhost:5000/auth/callback`
   - For production: `https://your-domain.com/auth/callback`
7. Copy the **Client ID** and **Client Secret**

#### Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```bash
   # Generate a secure secret key
   SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   
   # Paste your Google OAuth credentials
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   
   # Database URL (default is fine for local development)
   DATABASE_URL=sqlite:///data/users.db
   ```

**⚠️ Important**: Never commit the `.env` file to version control. It's already in `.gitignore`.

### 6. Set Up Superadmin Account

Before running the application for the first time, create a superadmin account:

```bash
python setup_superadmin.py
```

Follow the prompts to enter your Gmail address. This account will have admin privileges to approve new user registrations.

**Additional commands:**
```bash
# List all users in the database
python setup_superadmin.py --list

# Show help
python setup_superadmin.py --help
```

## Running the Application

### Local Development

1. Ensure your virtual environment is activated
2. Make sure you've completed the OAuth setup and superadmin configuration
3. Run the application:

```bash
python app.py
```

4. Open your web browser and navigate to:

```
http://localhost:5000
```

### Using Docker

Build and run the application using Docker:

```bash
# Build the image
docker build -t hello-world-kiro .

# Run the container
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e SECRET_KEY="your-secret-key" \
  -e GOOGLE_CLIENT_ID="your-client-id" \
  -e GOOGLE_CLIENT_SECRET="your-client-secret" \
  hello-world-kiro
```

Or use docker-compose (for production deployment):

```bash
cd deploy
docker-compose up -d
```

**Note**: Make sure to set environment variables in your deployment environment or create a `.env` file for docker-compose.

## User Authentication Flow

### For Regular Users

1. **Sign In**: Click "Sign in with Google" button
2. **Google OAuth**: Authenticate with your Gmail account
3. **Pending Approval**: After first login, your account will be in "pending" status
4. **Waiting Page**: You'll see a waiting page while the superadmin reviews your request
5. **Access Granted**: Once approved, you can access private pages (Dashboard, Profile)

### For Superadmin

1. **Sign In**: Log in with your Gmail account (set up via `setup_superadmin.py`)
2. **Admin Dashboard**: Access `/admin/dashboard` to manage users
3. **Approve/Reject**: Review pending registrations and approve or reject them
4. **User Management**: View all users, their status, and manage accounts

### Private Routes

**Available to all approved users:**
- `/dashboard` - User dashboard with quick links
- `/profile` - User profile showing account information

**Available to superadmin only:**
- `/admin/dashboard` - Admin panel to manage users
- `/admin/user/<id>/approve` - Approve a user (API)
- `/admin/user/<id>/reject` - Reject a user (API)
- `/admin/user/<id>/delete` - Delete a user (API)

**Public routes (no authentication required):**
- `/` - Homepage (English)
- `/de`, `/fr`, `/hr`, `/es`, `/tr`, `/pt`, `/ru` - Language-specific pages
- `/login` - Initiate Google OAuth login
- `/logout` - Log out current user

## Available Routes

The application supports multiple language routes:

- **English (default)**: `http://localhost:5000/`
- **German**: `http://localhost:5000/de`
- **French**: `http://localhost:5000/fr`
- **Croatian**: `http://localhost:5000/hr`
- **Spanish**: `http://localhost:5000/es`
- **Turkish**: `http://localhost:5000/tr`
- **Portuguese**: `http://localhost:5000/pt`
- **Russian**: `http://localhost:5000/ru`

You can also switch between languages using the language selector buttons on the page. The authentication header persists across all language pages.

## Currency Converter

The application includes a built-in currency converter with **live exchange rates** that supports the following currencies:

- **USD** - US Dollar ($)
- **EUR** - Euro (€)
- **GBP** - British Pound (£)
- **TRY** - Turkish Lira (₺)
- **RUB** - Russian Ruble (₽)

### Exchange Rate Source

Exchange rates are fetched in real-time from **[exchangerate-api.com](https://exchangerate-api.com)**, a free and reliable API that provides current foreign exchange rates from multiple sources.

**Features:**
- 🔄 **Live rates**: Updated automatically from multiple foreign exchange sources
- ⚡ **Smart caching**: Rates cached for 1 hour to improve performance
- 🛡️ **Fallback protection**: Uses static rates if API is unavailable
- 📊 **Transparent**: Shows whether rates are live or cached
- 🕐 **Rate timestamps**: Displays when rates were last updated

### How to Use

1. Enter the amount you want to convert in either input box
2. Select currencies from the dropdowns
3. **Real-time conversion**: The result updates automatically as you type (300ms debounce)
4. **Bidirectional**: You can type in either the "From" or "To" box
5. The converter displays:
   - Converted amount in real-time
   - Current exchange rate
   - Rate source (live/cached)

**Note**: No "Convert" button needed - conversion happens automatically!

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
├── app.py                 # Main Flask application with routes
├── models.py              # Database models (User model)
├── setup_superadmin.py    # Script to create/update superadmin users
├── templates/             # HTML templates directory
│   ├── index.html        # Homepage template (with auth header)
│   ├── dashboard.html    # User dashboard (private)
│   ├── profile.html      # User profile (private)
│   ├── admin_dashboard.html  # Admin panel (superadmin only)
│   ├── pending.html      # Pending approval page
│   └── error.html        # Error page template
├── data/                  # SQLite database directory (gitignored)
│   └── users.db          # User database (created automatically)
├── deploy/                # Deployment configuration
│   └── docker-compose.yml # Docker Compose for production
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example          # Example environment variables
├── .env                  # Your actual environment variables (gitignored)
├── .dockerignore         # Docker ignore rules
├── .gitignore            # Git ignore rules
├── .kiro/                # Kiro configuration
│   └── steering/         # Steering rules
├── LICENSE               # License file
└── README.md             # This file
```

## Technology Stack

- **Framework**: Flask 3.0+
- **Language**: Python 3.8+
- **Template Engine**: Jinja2 (built into Flask)
- **Authentication**: Google OAuth 2.0 (via Authlib)
- **Database**: SQLite (with Flask-SQLAlchemy ORM)
- **Session Management**: Flask-Login
- **Deployment**: Docker + Gunicorn

## Database Schema

### User Table

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| email | String(255) | User's Gmail address (unique, indexed) |
| name | String(255) | User's full name from Google |
| profile_picture | String(500) | URL to Google profile picture |
| role | String(50) | 'superadmin' or 'user' |
| status | String(50) | 'pending', 'approved', or 'rejected' |
| created_at | DateTime | Registration timestamp |
| updated_at | DateTime | Last update timestamp |

## Security Considerations

- **Environment Variables**: Never commit `.env` file - it contains sensitive credentials
- **Secret Key**: Generate a strong secret key for production: `python -c "import secrets; print(secrets.token_hex(32))"`
- **HTTPS**: Always use HTTPS in production (OAuth callback requires it for production domains)
- **Session Security**: Sessions are set to HTTPOnly and SameSite=Lax
- **Gmail Only**: Only Gmail addresses (`@gmail.com`) are allowed for authentication
- **Superadmin Protection**: Superadmin accounts cannot be deleted through the UI
- **Database**: SQLite is fine for small deployments; consider PostgreSQL for production scale

## Troubleshooting

### Google OAuth Errors

**Error: "redirect_uri_mismatch"**
- Make sure the redirect URI in Google Cloud Console matches exactly: `http://localhost:5000/auth/callback`
- For production, update it to your domain: `https://your-domain.com/auth/callback`

**Error: "Access blocked: This app's request is invalid"**
- Ensure Google+ API (or Google Identity Services) is enabled in Google Cloud Console
- Verify your OAuth consent screen is configured
- Check that your credentials are correctly set in `.env`

### Database Issues

**Error: "Unable to open database file"**
- Make sure the `data/` directory exists: `mkdir -p data`
- Check file permissions on the data directory
- Verify `DATABASE_URL` in `.env` points to a writable location

**Need to reset the database?**
```bash
# Backup existing database
mv data/users.db data/users.db.backup

# Database will be recreated on next app start
python app.py

# Don't forget to run setup_superadmin.py again!
python setup_superadmin.py
```

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

- The application runs in debug mode by default for local development
- Debug mode provides automatic reloading and detailed error messages
- Database tables are created automatically on first run
- Sessions persist for 7 days by default
- Exchange rates are cached for 1 hour to reduce API calls

**⚠️ Production Warnings**:
- Never run with `debug=True` in production!
- Always use HTTPS in production
- Set strong `SECRET_KEY` in production environment
- Consider using PostgreSQL instead of SQLite for production
- Set up proper OAuth consent screen verification with Google
- Configure `SESSION_COOKIE_SECURE=True` when using HTTPS

## Deployment to Production

1. **Set up environment variables** on your server (via GitHub Secrets or server env)
2. **Update Google OAuth redirect URI** to your production domain
3. **Run setup_superadmin.py** on the production server to create initial admin
4. **Use Docker** for consistent deployment:
   ```bash
   docker-compose -f deploy/docker-compose.yml up -d
   ```
5. **Database persistence**: Ensure the `data/` volume is backed up regularly

## License

See LICENSE file for details.
