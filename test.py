import requests

# Define the URL of the protected endpoint
protected_endpoint_url = "http://127.0.0.1:5000/protected"

# Replace with your actual access token obtained during login
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzg4ODgyNiwianRpIjoiZTZhZWMxMjAtNDFkMS00MjUyLWE4OGQtMmI1ZjlkYTM4ZDg2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ikpvc2VwaCIsIm5iZiI6MTY5Nzg4ODgyNiwiZXhwIjoxNjk3ODkwNjI2fQ.ysR59eEz-pXnm2O8t0RsbWxsiGEJ3db12YiEkT4J7Uc"

# Set the headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make a GET request to the protected endpoint with the headers
response = requests.get(protected_endpoint_url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # The request was successful
    data = response.json()
    print("Response Data:", data)
else:
    print(f"Request failed with status code {response.status_code}")
    # Handle the error as needed
