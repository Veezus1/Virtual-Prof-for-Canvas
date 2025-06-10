import jwt
import json
from datetime import datetime, timedelta

# Load private key (PEM)
with open("./keys/private.key", "r") as f:
    private_key = f.read()

# Token header
headers = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "test-key"
}

# Token payload
payload = {
    "iss": "https://canvas.instructure.com",
    "aud": "test-client",
    "exp": int((datetime.utcnow() + timedelta(minutes=5)).timestamp()),
    "iat": int(datetime.utcnow().timestamp()),
    "nonce": "mock-nonce",
    "name": "Test Student",
    "https://purl.imsglobal.org/spec/lti/claim/context": {
        "id": "test-course-123"
    }
}

# Sign the token
token = jwt.encode(
    payload,
    private_key,
    algorithm="RS256",
    headers=headers
)

print("\n👇 COPY THIS TOKEN INTO lti_test_launch.html 👇\n")
print(token)

