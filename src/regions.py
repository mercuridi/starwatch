"""Script that creates a JSON file containing the 12 major regions and their lat/long coordinates"""

import pandas as pd

def main():
    """Driver function"""

    # lat/long pairs snatched from Wikipedia
    regions = {
        "region_name"   : [
            "Cymru Wales",
            "East Midlands",
            "East of England",
            "London",
            "North East & Cumbria",
            "North West",
            "Northern Ireland",
            "Scotland",
            "South East",
            "South West",
            "West Midlands",
            "Yorkshire & the Humber"
        ],
        "latitude"      : [
            +51.29, # Wales (actually Cardiff)
            +52.98, # East Midlands
            +52.24, # East of England
            +51.30, # London (actually City of London)
            +55.00, # North East & Cumbria
            +54.04, # North West
            +54.60, # Northern Ireland (actually Belfast)
            +55.57, # Scotland (actually Edinburgh)
            +51.30, # South East
            +50.96, # South West
            +52.28, # West Midlands
            +53.34  # Yorkshire & the Humber
        ],
        "longitude"     : [
            -03.11, # Wales (actually Cardiff)
            -00.75, # East Midlands
            +00.41, # East of England
            -00.05, # London (actually City of London)
            -01.87, # North East & Cumbria
            -02.45, # North West
            -05.93, # Northern Ireland (actually Belfast)
            -03.11, # Scotland (actually Edinburgh)
            -00.80, # South East
            -03.22, # South West
            -02.15, # West Midlands
            -01.12  # Yorkshire & the Humber
        ]
    }
    df = pd.DataFrame(data=regions)
    df.to_json(path_or_buf="data/regions.json")

if __name__ == "__main__":
    main()
