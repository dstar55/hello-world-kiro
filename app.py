"""
Flask Hello World Application

A simple web application that displays 'Hello, World!' on the homepage.
"""

from flask import Flask, render_template

# Initialize Flask application
app = Flask(__name__)


@app.route('/')
def index():
    """
    Homepage route handler.
    
    Returns:
        Rendered HTML template displaying 'Hello, World!'
    """
    return render_template('index.html')


if __name__ == '__main__':
    # Run the application on localhost:5000 in debug mode
    app.run(host='localhost', port=5000, debug=True)
