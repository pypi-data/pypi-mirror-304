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
    response.raise_for_status()
    return response.json()['access_token']

# Function to create a device compliance policy in Intune
def create_compliance_policy(tenant_id, client_id, client_secret):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    url = "https://graph.microsoft.com/v1.0/deviceManagement/deviceCompliancePolicies"
    
    # Define your Windows 10 compliance policy configuration
    payload = {
        "@odata.type": "#microsoft.graph.windows10CompliancePolicy",
        "displayName": "Windows 10 Compliance Policy",
        "description": "Compliance policy for ensuring device security on Windows 10",
        "passwordRequired": True,
        "passwordMinimumLength": 8,
        "passwordMinutesOfInactivityBeforeLock": 15,
        "passwordExpirationDays": 90,
        "passwordPreviousPasswordBlockCount": 5,
        "osMinimumVersion": "10.0.19041.0",
        "storageRequireEncryption": True,
        "deviceThreatProtectionEnabled": True,
        "deviceThreatProtectionRequiredSecurityLevel": "high",
        "scheduledActionsForRule": [
            {
                "ruleName": "PasswordRequired",
                "scheduledActionConfigurations": [
                    {
                        "actionType": "block",
                        "gracePeriodHours": 72,
                        "notificationMessageCCList": []
                    }
                ]
            }
        ]
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print("Device Compliance Policy created successfully.")
    else:
        print(f"Failed to create device compliance policy: {response.status_code}, {response.text}")
        
def get_device_details(tenant_id, client_id, client_secret, device_id):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    url = f"https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/{device_id}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Device Details:", response.json())
    else:
        print(f"Failed to get device details: {response.status_code}, {response.text}")

# Function to list all managed devices in Intune
def list_managed_devices(tenant_id, client_id, client_secret):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    url = "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Managed Devices:", response.json())
    else:
        print(f"Failed to list managed devices: {response.status_code}, {response.text}")
        
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



