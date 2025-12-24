import requests

API_KEY = "10480544922acc8365d639806165098a2"
url = f"https://api.themoviedb.org/3/movie/155?api_key={API_KEY}&language=en-US"

try:
    response = requests.get(url, timeout=10)
    print("STATUS:", response.status_code)
    print("DATA:", response.json())
except Exception as e:
    print("Python request failed:", e)
