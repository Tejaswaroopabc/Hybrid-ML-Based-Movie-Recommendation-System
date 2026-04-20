import requests

API_KEY = "30627522cfe8fdf8166fd84f89a9b95b"

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
response = requests.get(url, timeout=10)

print(response.status_code)