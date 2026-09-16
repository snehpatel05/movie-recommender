import requests
import urllib3

# Force IPv4 only
urllib3.util.connection.HAS_IPV6 = False

url = "https://api.themoviedb.org/3/movie/19995?api_key=2527986befbd07cd11a19af36746555b"

try:
    r = requests.get(url, timeout=10)
    print("STATUS:", r.status_code)
    print("BODY:", r.text[:300])
except requests.exceptions.RequestException as e:
    print("REQUEST FAILED:", e)