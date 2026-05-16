import requests
response = requests.get("https://api.github.com/user", timeout=10)
print(response.status_code)