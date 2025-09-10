import api_requests

url = "http://127.0.0.1:8000/upload/"
files = {"file": open("api_requests/David.jpg", "rb")}
response = api_requests.post(url, files=files)
print(response.json())