import requests
import json

# Function to get the access token using OAuth 2.0
def get_access_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'client_id': client_id,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Raise error if something went wrong
    return response.json()['access_token']

# Function to list all apps in Intune
def list_apps(tenant_id, client_id, client_secret):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    url = "https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Apps:", response.json())
    else:
        print(f"Failed to list apps: {response.status_code}, {response.text}")

# Function to get details of a specific app
def get_app_details(tenant_id, client_id, client_secret, app_id):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    url = f"https://graph.microsoft.com/v1.0/deviceAppManagement/mobileApps/{app_id}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("App Details:", response.json())
    else:
        print(f"Failed to get app details: {response.status_code}, {response.text}")


