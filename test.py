import requests
import json

# Define the URL of your API
base_url = "http://127.0.0.1:5000"

# Function to create a new user account
def create_account(username, password, email):
    register_url = f"{base_url}/createUser"
    data = {
        "username": username,
        "password": password,
        "email": email
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(register_url, json=data, headers=headers)
    return response

# Function to log in and obtain access and refresh tokens
def login(username, password):
    login_url = f"{base_url}/login"
    data = {
        "username": username,
        "password": password
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(login_url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Login failed with status code", response.status_code)
        return None

# Function to call the protected endpoint
def call_protected_endpoint(access_token):
    protected_url = f"{base_url}/protected"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(protected_url, headers=headers)
    return response

if __name__ == "__main__":
    # User registration
    create_account_response = create_account("user1", "password1", "user1@example.com")
    print("Create Account Response:", create_account_response.status_code)
    print(create_account_response.text)
    # User login
    login_response = login("user1", "password1")
    print(login_response)
    if login_response and "access_token" in login_response:
        access_token = login_response["access_token"]
        # Call the protected endpoint with the access token
        protected_response = call_protected_endpoint(access_token)
        
        if protected_response.status_code == 200:
            print("Protected Endpoint Response:", protected_response.text)
        else:
            print("Protected endpoint access failed with status code", protected_response.status_code)
    else:
        print("Access token not obtained. Check login credentials.")
