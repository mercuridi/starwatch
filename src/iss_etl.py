"""Module to quickly & easily get the current position of the ISS in lat/long"""
import requests

def get_iss_lat_long() -> tuple[float, float]:
    """Returns the current lat/long of the ISS as a float tuple"""
    req = requests.get("http://api.open-notify.org/iss-now.json", timeout=15)
    if req.status_code == 200:
        pos = req.json()["iss_position"]
        return (pos["latitude"], pos["longitude"])
    raise RuntimeError(f"Error from ISS API: {req}")

if __name__ == "__main__":
    print(get_iss_lat_long())
