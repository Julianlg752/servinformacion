import requests
import urllib
import os


def get_lat_lon(address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json?address="
    endpoint += urllib.parse.quote(address)
    endpoint += "&components=country:CO"
    endpoint += "&key="+os.getenv('GOOGLE_KEY')
    # print(endpoint)
    response = requests.get(endpoint)
    if response.status_code != 200:
        print("Can't Compleate Request")
    json_response = response.json()
    response_dict = {}
    # print(json_response.get("results"))
    if json_response["status"] == "ZERO_RESULTS":
        response_dict = {"error": "No se encontro la direccion"}

    elif json_response["status"] == "INVALID_REQUEST":
        response_dict = {"error": "No se encontro latitud o longitud"}

    elif json_response["status"] == "OK":
        # TODO: remove check len of the result
        results = json_response["results"][0]
        geom = results['geometry']['location']
        response_dict = {
                "direccion": results["formatted_address"],
                "lat": "{:5.10f}".format(geom['lat']),
                "lon": "{:5.10f}".format(geom['lng'])
                }

    return response_dict
    # print(json.dumps(json_response, indent=4))

# https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
