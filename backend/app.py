from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import random
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Quote Database
QUOTES = [
    {"content": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House", "tags": ["programming"]},
    {"content": "First, solve the problem. Then, write the code.", "author": "John Johnson", "tags": ["programming"]},
    {"content": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "tags": ["technology"]},
    {"content": "The best error message is the one that never shows up.", "author": "Thomas Fuchs", "tags": ["programming"]},
    {"content": "Make it work, make it right, make it fast.", "author": "Kent Beck", "tags": ["programming"]},
]

# Embedded OpenAPI YAML (no file needed!)
OPENAPI_YAML = """
openapi: 3.0.3
info:
  title: Quote API
  version: 1.0.0
  description: Random programming & tech quotes
servers:
  - url: https://quote-api.onrender.com
paths:
  /random:
    get:
      summary: Get random quote
      parameters:
        - name: tag
          in: query
          schema: {type: string}
      responses:
        '200': {description: Quote}
  /health:
    get:
      summary: Health check
      responses:
        '200': {description: OK}
"""

# Swagger UI Setup (uses embedded YAML)
SWAGGER_URL = '/docs'
API_URL = '/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Quote API"}
)
app.register_blueprint(swaggerui_blueprint)

# Serve embedded YAML
@app.route('/openapi.yaml')
def serve_openapi():
    return Response(OPENAPI_YAML, mimetype='text/yaml')

# Routes
@app.route("/")
def home():
    return jsonify({
        "message": "Quote API Live!",
        "endpoints": ["/random", "/docs", "/health"]
    })

@app.route("/random")
def random_quote():
    tag = request.args.get("tag")
    filtered = [q for q in QUOTES if not tag or any(tag.lower() in t.lower() for t in q["tags"])]
    if not filtered:
        return jsonify({"error": "No quotes for tag"}), 404
    return jsonify(random.choice(filtered))

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "quote-api"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)