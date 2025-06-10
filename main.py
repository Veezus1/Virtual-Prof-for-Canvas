from flask import Flask, request, jsonify, render_template_string
import jwt
import requests
import json
from jwt import PyJWKClient

app = Flask(__name__)

CANVAS_ISSUER = "https://canvas.instructure.com"
CLIENT_ID = "YOUR_CLIENT_ID"
DEPLOYMENT_ID = "YOUR_DEPLOYMENT_ID"
#JWK_URL = "https://canvas.instructure.com/api/lti/security/jwks"
JWK_URL = "http://localhost:8000/.well-known/jwks.json"

@app.route("/", methods=["GET"])
def index():
    return "<h2>AI Virtual Professor LTI Tool (Manual Flask Version)</h2>"

@app.route("/lti/launch", methods=["POST"])
def lti_launch():
    id_token = request.form.get("id_token")
    if not id_token:
        return "Missing id_token", 400

    try:
        # Fetch Canvas public keys
        jwks_client = PyJWKClient(JWK_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)

        # Decode and verify JWT
        decoded = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=CANVAS_ISSUER
        )

        user_name = decoded.get("name", "Student")
        context = decoded.get("https://purl.imsglobal.org/spec/lti/claim/context", {})
        course_id = context.get("id", "unknown")

        return render_template_string("""
        <html>
        <body>
            <h1>Welcome {{ user_name }}!</h1>
            <p>You are now connected to the AI Virtual Professor for course: {{ course_id }}</p>
        </body>
        </html>
        """, user_name=user_name, course_id=course_id)

    except Exception as e:
        return f"JWT validation error: {str(e)}", 400

@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    with open("./keys/jwk.json") as f:
        jwk = json.load(f)
    return jsonify(jwk)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
