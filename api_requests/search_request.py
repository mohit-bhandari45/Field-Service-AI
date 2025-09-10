import requests

url = "http://127.0.0.1:8000/api/search/"
files = {"file": open("api_requests/image_1.jpg", "rb")}
params = {"top_k": 3}  # optional, overrides default

response = requests.post(url, files=files, params=params)

print("Response:", response.json())