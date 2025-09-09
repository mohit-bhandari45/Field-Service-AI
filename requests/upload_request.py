import requests

url = "http://127.0.0.1:8000/upload/"
files = {"file": open("David.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())