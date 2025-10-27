from flask import Flask, jsonify, request, send_from_directory
import random
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)
CORS(app)
# -------------------------------------------------
# Built-in quote database (mock data)
# -------------------------------------------------
QUOTES = [
    {"content": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House", "tags": ["programming"]},
    {"content": "First, solve the problem. Then, write the code.", "author": "John Johnson", "tags": ["programming"]},
    {"content": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "tags": ["technology"]},
    {"content": "The best error message is the one that never shows up.", "author": "Thomas Fuchs", "tags": ["programming"]},
    {"content": "Make it work, make it right, make it fast.", "author": "Kent Beck", "tags": ["programming"]},
]

# -------------------------------------------------
# Swagger UI Setup (Fixed!)
# -------------------------------------------------
SWAGGER_URL = '/docs'
API_URL = '/static/openapi.yaml'  # Serve from static folder

# Register Swagger blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Quote API",
        'url': API_URL,
        'spec_url': API_URL,
        'static_url_path': '/swagger-ui/static'
    }
)
app.register_blueprint(swaggerui_blueprint)

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
        "message": "Quote API Live!",
        "endpoints": {
            "GET /random": "Random quote (?tag=programming)",
            "GET /docs": "Swagger UI Documentation",
            "GET /health": "Health check"
        }
    })

@app.route("/random")
def random_quote():
    """Get a random quote with optional tag filter."""
    tag = request.args.get("tag")
    filtered_quotes = [
        q for q in QUOTES
        if not tag or any(tag.lower() in str(t).lower() for t in q["tags"])
    ]
    
    if not filtered_quotes:
        return jsonify({"error": f"No quotes found for tag: {tag}"}), 404
    
    quote = random.choice(filtered_quotes)
    return jsonify(quote)

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "quote-api"}), 200

# -------------------------------------------------
# Run the app
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)