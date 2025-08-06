"""Module to quickly & easily get the current position of the ISS in lat/long"""
from calendar import timegm
from datetime import datetime, timezone

import requests
import ephem

def get_iss_lat_long_now() -> tuple[float, float]:
    """Returns the current lat/long of the ISS as a float tuple"""
    req = requests.get("http://api.open-notify.org/iss-now.json", timeout=15)
    if req.status_code == 200:
        pos = req.json()["iss_position"]
        return (pos["latitude"], pos["longitude"])
    raise RuntimeError(f"Error from ISS API: {req}")

def get_passes(lon, lat, n=1, alt=0):
    """
    Compute n number of passes of the ISS for a given location
    This code is from https://github.com/open-notify/Open-Notify-API/blob/master/iss.py
    It used to be hosted on a the Open Notify API but now is not so we calculate it locally instead
    To be clear, *the StarWatch team did not write this code!*
    StarWatch has adapted it to work in a useful way for the project
    Adaptations:
        - Updated TLE source from private redis to public API
        - Updated code overall from Python 2.x to 3.13
        - Updated outdated library references to modern ones
        - Added some basic error checking against bad inputs
    """
    if lat < -90 or lat > 90:
        raise ValueError(f"Latitude out of expected range: -90 < lat < 90. Got {lat}")
    if lon < -180 or lon > 180:
        raise ValueError(f"Longitude out of expected range: -180 < lon < 180. Got {lon}")

    # Get latest TLE from Ariss
    tle_req = requests.get("https://live.ariss.org/iss.txt", timeout=60)
    if tle_req.status_code == 200:
        tle_raw = tle_req.text
    else:
        raise RuntimeError("Failed to get the TLE required for ISS orbit calculation")
    print(tle_raw)
    tle = tle_raw.split("\n")
    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    # Set location
    location = ephem.Observer()
    location.lat = str(lat)
    location.long = str(lon)
    location.elevation = alt

    # Override refraction calculation
    location.pressure = 0
    location.horizon = '10:00'

    # Set time now
    now = datetime.now(timezone.utc)
    location.date = now

    # Predict passes
    passes = []
    for _ in range(n):
        tr, _, _, _, ts, _ = location.next_pass(iss)
        duration = int((ts - tr) * 60 * 60 * 24)
        year, month, day, hour, minute, second = tr.tuple()
        dt = datetime(year, month, day, hour, minute, int(second))

        if duration > 60:
            passes.append({"risetime": timegm(dt.timetuple()), "duration": duration})

        # Increase the time by more than a pass and less than an orbit
        location.date = tr + 25*ephem.minute

    # Return object
    obj = {"request": {
        "datetime": timegm(now.timetuple()),
        "latitude": lat,
        "longitude": lon,
        "altitude": alt,
        "passes": n,
        },
        "response": passes,
    }

    return obj


def present_iss_passes(passes_obj) -> list[tuple[str, int]]:
    """
    Converts the calculated ISS passes to human formats
    The further in the future the prediction, the less accurate!!!
    The orbit of the ISS decays chaotically and changes often
    """
    formatted_passes = []
    for iss_pass in passes_obj["response"]:
        formatted_passes.append((
            # string of the date and time of the pass in UTC
            str(datetime.fromtimestamp(iss_pass["risetime"], tz=timezone.utc)),
            # duration of overhead pass in seconds
            iss_pass["duration"]
        ))
    return formatted_passes

if __name__ == "__main__":
    print(get_passes(0, 0))
