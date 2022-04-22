import requests
import json
import time


class Currency:

    def __init__(self, url):
        with open("curr.json", 'r+') as f:
            data = json.load(f)
            next_update = data["time_next_update_unix"]
            if int(time.time()) > next_update:
                data = requests.get(url).json()
                print("new request")
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            self.currencies = data['conversion_rates']

    def convert(self, base_currency, to_currency, value):
        if base_currency != "USD":
            value /= self.currencies[base_currency]

        return round(value * self.currencies[to_currency], 4)

    def get_currencies(self):
        return self.currencies.keys()


class Units:

    def __init__(self):
        self.time_conversion = {'HR': 3600, 'MIN': 60, 'SEC': 1}
        self.distance_conversion = {
            'MM': 0.001, 'CM': 0.01, 'M': 1, 'KM': 1000, 'YD': 0.9144, 'FT': 0.3048, 'IN': 0.0254
        }
        self.mass_conversion = {'KG': 1000, 'G': 1, 'MG': 0.001, 'LB': 453.592, 'OZ': 28.3495}

    def convert(self, convert_type, unit_in, unit_out, val):
        conversion = None
        if convert_type == "TIME":
            conversion = self.time_conversion
        elif convert_type == "DISTANCE":
            conversion = self.distance_conversion

        elif convert_type == "TEMP":
            return self.convert_temp(unit_in, unit_out, val)

        elif convert_type == "MASS":
            conversion = self.mass_conversion

        return round(val * conversion[unit_in] / conversion[unit_out], 4)

    def convert_temp(self, unit_in, unit_out, val):
        converted = {}
        if unit_in == "F":
            converted["F"] = val
            converted["C"] = round((val - 32) * (5.0 / 9.0), 4)
            converted["K"] = converted["C"] + 273.15

        elif unit_in == "C":
            converted["F"] = round((val * (9.0 / 5.0)) + 32, 4)
            converted["C"] = val
            converted["K"] = converted["C"] + 273.15

        elif unit_in == "K":
            converted["F"] = round((val - 273.15) * (9.0 / 5.0) + 32)
            converted["C"] = val - 273.15
            converted["K"] = val

        return converted[unit_out]