import requests

API_KEY = "YOUR API KEY"

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
response = requests.get(url, timeout=10)

print(response.status_code)
