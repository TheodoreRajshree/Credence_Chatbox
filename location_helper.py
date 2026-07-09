from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="gps_tracker")

def get_address(lat, lon):
    try:
        location = geolocator.reverse(
            (lat, lon),
            language="en"
        )

        if location:
            return location.address

    except Exception:
        pass

    return ""


def add_address(data):

    if isinstance(data, list):

        for item in data:

            lat = item.get("latitude")
            lon = item.get("longitude")

            if lat is not None and lon is not None:

                item["address"] = get_address(lat, lon)

    elif isinstance(data, dict):

        lat = data.get("latitude")
        lon = data.get("longitude")

        if lat is not None and lon is not None:

            data["address"] = get_address(lat, lon)

    return data