import requests
import json
import time


class Currency:

    def __init__(self):
        with open("back_end/curr.json", 'r+') as f:
            data = json.load(f)
            next_update = data["time_next_update_unix"]
            if int(time.time()) > next_update:
                data = requests.get("https://v6.exchangerate-api.com/v6/5e3fa81ca1fd4ed734a46127/latest/USD").json()
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
        new_dict = {}
        with open("back_end/curr_names.json", "r", encoding="utf8") as f:
            data = json.load(f)
            for key in data.keys():
                new_dict[key] = f"{key} ({data[key]['name']})"

        return new_dict


class Units:

    def __init__(self):
        self.time_conversion = {'Hr': 3600, 'Min': 60, 'Sec': 1}
        self.distance_conversion = {
            'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000, 'yd': 0.9144, 'ft': 0.3048, 'in': 0.0254
        }
        self.mass_conversion = {'kg': 1000, 'g': 1, 'mg': 0.001, 'lb': 453.592, 'oz': 28.3495}
        self.frequency_conversion = {'Hz': 1, 'MHz': 1e+6, 'GHz': 1e+9, 'KHz': 1000}

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

        elif convert_type == "FREQ":
            conversion = self.frequency_conversion

        return round(val * conversion[unit_in] / conversion[unit_out], 6)

    def convert_temp(self, unit_in, unit_out, val):
        converted = {}
        if unit_in == "F":
            converted["F"] = val
            converted["C"] = round((val - 32) * (5.0 / 9.0), 6)
            converted["K"] = converted["C"] + 273.15

        elif unit_in == "C":
            converted["F"] = round((val * (9.0 / 5.0)) + 32, 6)
            converted["C"] = val
            converted["K"] = converted["C"] + 273.15

        elif unit_in == "K":
            converted["F"] = round((val - 273.15) * (9.0 / 5.0) + 32, 6)
            converted["C"] = val - 273.15
            converted["K"] = val

        return converted[unit_out]

    def get_units(self, units):
        if units == "TIME":
            return list(self.time_conversion.keys())
        elif units == "DISTANCE":
            return list(self.distance_conversion.keys())

        elif units == "TEMP":
            return ["C", "F", "K"]

        elif units == "FREQ":
            return list(self.frequency_conversion.keys())

        elif units == "MASS":
            return list(self.mass_conversion.keys())