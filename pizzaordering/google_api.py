from urllib.parse import urlencode
import requests
import json
import datetime


class GoogleAPI(object):
    def __init__(self):
        self.data_type = "json"
        self.google_api_key = "*********"
        self.end_point_for_nearby = f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        self.end_point_for_distance = f"https://maps.googleapis.com/maps/api/distancematrix/{self.data_type}"
        self.end_point_for_geocoding = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        self.end_point_for_place_detail = f"https://maps.googleapis.com/maps/api/place/details/{self.data_type}"

    def extract_locations(self, coors):
        lat = coors["lat"]
        lng = coors["lng"]

        return f"{lat},{lng}"

    def distance_calculation(self, origin, destinations):
        # extract orgin coordinates
        _origrin = self.extract_locations(origin)

        # extract destination coordinates
        _destinations = None
        _destination_coors = []

        for destination in destinations:
            _loca = self.extract_locations(destination)

            _destination_coors.append(_loca)

        _destinations = "|".join(_destination_coors)

        print(_destinations)

        params = {
            "origins": _origrin,
            "destinations": _destinations,
            "key": self.google_api_key
        }

        url_params = urlencode(params)
        print(url_params)

        distance_api_url = f"{self.end_point_for_distance}?{url_params}"

        response = requests.get(distance_api_url)

        if response.status_code in range(200, 299):
            # print(response.text)
            return response.json()

        else:
            return {}

    def extract_coors_from_address(self, address):
        if len(address) > 0:
            params = {
                "address": address,
                "key": self.google_api_key
            }

            url_params = urlencode(params)
            address_api_url = f"{self.end_point_for_geocoding}?{url_params}"

            response = requests.get(address_api_url)

            if response.status_code in range(200, 299):
                data = None
                res_data = json.loads(response.text)
                formated_address = None
                location = []
                is_results = len(res_data["results"]) > 0

                if (is_results):
                    formated_address = res_data["results"][0]["formatted_address"]
                    location = res_data["results"][0]["geometry"]["location"]

                data = {
                    "address": formated_address,
                    "location": location,
                    "message": "Not found, Please enter a valid address!" if is_results is False else ""
                }

                return data

            else:
                return {}

        else:
            return {}

    def place_detail(self, places):
        place_ids = [place["place_id"] for place in places]

        data = []

        for place_id in place_ids:
            params = {
                "place_id": place_id,
                "key": self.google_api_key
            }

            url_params = urlencode(params)
            places_api_url = f"{self.end_point_for_place_detail}?{url_params}"

            response = requests.get(places_api_url)

            if response.status_code in range(200, 299):
                _weekday = datetime.datetime.today().weekday()

                returned_data = json.loads(response.text)["result"]
                returned_data = {
                    "phone_number": returned_data["formatted_phone_number"],
                    "opening_hour": returned_data["opening_hours"]["weekday_text"][_weekday]
                }

                data.append(returned_data)

            else:
                return []

        return data

    def get_nearby_place(self, radius, _type, keyword, location):
        lat = location["lat"]
        lng = location["lng"]
        _location = f"{lat},{lng}"

        params = {
            "location": _location,
            "radius": radius,
            "type": _type,
            "keyword": keyword,
            "key": self.google_api_key
        }

        url_params = urlencode(params)
        places_api_url = f"{self.end_point_for_nearby}?{url_params}"

        response = requests.get(places_api_url)

        if response.status_code in range(200, 299):
            copy_data = json.loads(response.text).copy()

            found_res = copy_data["results"]

            for i in range(len(found_res)):
                if not found_res[i]["opening_hours"]["open_now"]:
                    found_res[i] = "_"

            found_res = [res for res in found_res if res != "_"]

            not_found_msg = "There is no restaurant nearby available."
            res_counter = len(found_res)
            be_v = "is" if len(found_res) == 1 else "are"
            _s = "" if len(found_res) == 1 else "s"
            found_msg = f"There {be_v} {res_counter} location{_s} nearby."

            data = {
                "available_location": found_res if len(found_res) > 0 else [],
                "message": found_msg if len(found_res) > 0 else not_found_msg,
            }

            return data

        else:
            return {}
