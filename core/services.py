import requests

def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "zoom": 18,
        "addressdetails": 1,
    }

    headers = {
        "User-Agent": "CivicCareApp/1.0 (contact: yourmail@example.com)"
    }

    r = requests.get(url, params=params, headers=headers, timeout=10)
    data = r.json()

    address = data.get("address", {})

    return {
        "state": address.get("state"),
        "district": address.get("county") or address.get("state_district") or address.get("city"),
        "location": address.get("suburb") or address.get("neighbourhood") or address.get("village"),
        "pincode": address.get("postcode"),
    }
