import os
import sys
import requests

CLIENT_ID = os.environ.get("CENTRAL_CLIENT_ID")
CLIENT_SECRET = os.environ.get("CENTRAL_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("CENTRAL_REFRESH_TOKEN")
API_URL = os.environ.get("CENTRAL_API_URL")
GROUP_NAME = os.environ.get("CENTRAL_GROUP_NAME")

TEMPLATE_FILE = "templates/gateway_group.cfg"

def get_access_token():
    """Fetches a fresh access token using the stored refresh token."""
    token_url = f"{API_URL}/oauth2/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to refresh token: {response.text}")
        sys.exit(1)

def upload_template(access_token):
    """Pushes the updated configuration template to Aruba Central."""
    # Note: Use 'ArubaGateway' for gateways or 'ArubaCX' / 'ArubaSwitch' for switches
    endpoint = f"{API_URL}/configuration/v1/groups/{GROUP_NAME}/templates"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    with open(TEMPLATE_FILE, "rb") as f:
        files = {"template": ("gateway_group.cfg", f, "text/plain")}
        response = requests.post(endpoint, headers=headers, files=files)

    if response.status_code in [200, 201]:
        print(f"Successfully deployed template to Aruba Central group: {GROUP_NAME}")
    else:
        print(f"Deployment failed ({response.status_code}): {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    token = get_access_token()
    upload_template(token)
