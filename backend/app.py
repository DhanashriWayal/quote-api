from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
from flask_swagger_ui import get_swaggerui_blueprint
import os

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Enable CORS for all routes (critical for frontend)
CORS(app)

# -------------------------------------------------
# Quote Database (Mock Data)
# -------------------------------------------------
QUOTES = [
    {"content": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House", "tags": ["programming"]},
    {"content": "First, solve the problem. Then, write the code.", "author": "John Johnson", "tags": ["programming"]},
    {"content": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "tags": ["technology"]},
    {"content": "The best error message is the one that never shows up.", "author": "Thomas Fuchs", "tags": ["programming"]},
    {"content": "Make it work, make it right, make it fast.", "author": "Kent Beck", "tags": ["programming"]},
]

# -------------------------------------------------
# Swagger UI Setup
# -------------------------------------------------
SWAGGER_URL = '/docs'  # URL for Swagger UI
API_URL = '/static/openapi.yaml'  # Path to OpenAPI spec

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Quote API - Random Quotes Generator"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve OpenAPI spec from static folder
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# -------------------------------------------------
# API Routes
# -------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Quote API is Live!",
        "endpoints": {
            "GET /random": "Get random quote (?tag=programming)",
            "GET /docs": "Interactive Swagger UI",
            "GET /health": "Health check"
        },
        "swagger_ui": f"{request.url_root[:-1]}{SWAGGER_URL}"
    })

@app.route("/random")
def random_quote():
    """Return a random quote with optional tag filtering."""
    tag = request.args.get("tag")
    
    # Filter quotes by tag (case-insensitive)
    filtered = [
        q for q in QUOTES
        if not tag or any(tag.lower() in t.lower() for t in q["tags"])
    ]
    
    if not filtered:
        return jsonify({"error": f"No quotes found for tag: '{tag}'"}), 404
    
    return jsonify(random.choice(filtered))

@app.route("/health")
def health():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "ok", "service": "quote-api"}), 200

# -------------------------------------------------
# Run App
# -------------------------------------------------
if __name__ == "__main__":
    # Only for local development
    app.run(host="0.0.0.0", port=8000, debug=False)