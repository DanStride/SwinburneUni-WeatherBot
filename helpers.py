# Define a location class
class location:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


def GetItinerary():
    # Create a list of location objects
    itinerary = []
    itinerary.append(location('Lake District National Park', "54.4609", "-3.0886"))
    itinerary.append(location('Corfe Castle', "50.6395", "-2.0566"))
    itinerary.append(location('The Cotswolds', "51.8330", "-1.8433"))
    itinerary.append(location('Cambridge', "52.2053", "0.1218"))
    itinerary.append(location('Bristol', "51.4545", "-2.5879"))
    itinerary.append(location('Oxford', "51.7520", "-1.2577"))
    itinerary.append(location('Norwich', "52.6309", "1.2974"))
    itinerary.append(location('Stonehenge', "51.1789", "-1.8262"))
    itinerary.append(location('Watergate Bay', "50.4429", "-5.0553"))
    itinerary.append(location('Birmingham', "52.4862", "-1.8904"))
    return itinerary


def response_for_day_and_location(_day, _location, _responses, is_today, is_tomorrow):
    print("day and location from extracted method")
    for resp in _responses:
        new_resp = resp
        response = resp.lower()
        if _day in response and _location in response:
            if is_today:
                new_resp = "Today, " + resp
            if is_tomorrow:
                new_resp = "Tomorrow, " + resp

            return new_resp
