import os


API_URL = os.environ.get("API_URL")
assert API_URL, "icesi: undefined environment variable: API_URL"
if API_URL.endswith("/"):
    API_URL = API_URL[:-1]

WEBAPP_AUTH_PROTECTED = os.environ.get("WEBAPP_AUTH_PROTECTED", "true").lower() == "true"
WEBAPP_DEMO_MOCK = os.environ.get("WEBAPP_AUTH_PROTECTED", "false").lower() == "true"

print(f"icesi: environment: API_URL={API_URL} WEBAPP_AUTH_PROTECTED={WEBAPP_AUTH_PROTECTED} WEBAPP_DEMO_MOCK={WEBAPP_DEMO_MOCK}")
