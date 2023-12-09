from chatterbot.logic import LogicAdapter
from datetime import datetime, timedelta

import bot


# Custom LogicAdapter is required to provide accurate and specific bot responses
def response_for_day_and_location(_day, _location, _responses, is_today, is_tomorrow):
    # print("day and location from extracted method")
    for resp in _responses:
        new_resp = resp
        response = resp.lower()
        if _day in response and _location in response:
            if is_today:
                new_resp = "Today, " + resp
            if is_tomorrow:
                new_resp = "Tomorrow, " + resp

            return new_resp


class WeatherLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    # This determines if the adapter can be used for a given input, and decides based on word matching
    def can_process(self, statement):

        week_days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "today",
            "tomorrow"
        ]
        locations = [
            "lake district national park",
            "corfe castle",
            "the cotswolds",
            "cambridge",
            "bristol",
            "oxford",
            "norwich",
            "stonehenge",
            "watergate bay",
            "birmingham"
        ]
        words = [
            "temp",
            "temperature",
            "heat",
            "hot",
            "cold",
            "freezing",
            "weather",
            "rain",
            "hail",
            "storm"
        ]

        user_input = str(statement).lower()

        # Check if any of the provided words are found in the user input
        for item in week_days + locations + words:
            if item.lower() in user_input or item.lower() == user_input:
                # print("WLA: Statement found matching word")
                return True

        # print("WLA: Statement found no matching word")
        return False

    # This provides the logic for how the adapter will select a response
    def process(self, statement, additional_response_selection_parameters=None):

        # Get list from outside of this class
        from bot import get_response_list, previous_keyword
        response_list = get_response_list()
        week_days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        locations = [
            "lake district national park",
            "corfe castle",
            "the cotswolds",
            "cambridge",
            "bristol",
            "oxford",
            "norwich",
            "stonehenge",
            "watergate bay",
            "birmingham"
        ]

        user_input = str(statement).lower()
        selected_day = ""
        selected_location = ""
        selected_statement = statement
        is_today = False
        is_tomorrow = False
        prev_keyword = previous_keyword
        bot.previous_keyword = ""
        # print("Before processing:")
        # print("user input: " + user_input)
        # print("is_today: " + str(is_today))
        # print("is_tomorrow: " + str(is_tomorrow))

        # Check if user input is today or tomorrow and set selected day to corresponding day
        if "today" in user_input:
            selected_day = datetime.today().strftime("%A").lower()
            is_today = True
        elif "tomorrow" in user_input:
            selected_day = (datetime.today() + timedelta(days=1)).strftime("%A").lower()
            is_tomorrow = True

        # Get specified day from user input
        for day in week_days:
            if day in user_input:
                selected_day = day
                # print(day)

        # Get specified location from user input
        for location in locations:
            if location in user_input:
                selected_location = location
                # print(location)

        # If user input contains both valid day and location, get response and set statement confidence to 1
        if selected_day and selected_location:
            selected_statement.text = response_for_day_and_location(selected_day, selected_location,
                                                                         response_list, is_today, is_tomorrow)
            selected_statement.confidence = 1

        # If only the day was supplied, prompt the user for a location
        elif selected_day:
            if prev_keyword and prev_keyword in locations:
                selected_statement.text = response_for_day_and_location(selected_day, prev_keyword,
                                                                             response_list, is_today, is_tomorrow)
                selected_statement.confidence = 1
            else:
                # print("day only, prompt user")
                selected_statement.text = "For which location do you want to know the weather on " + selected_day.title() + "?"
                selected_statement.confidence = 1
                bot.previous_keyword = selected_day

        # If only the location was supplied, prompt the user for a day
        elif selected_location:
            if prev_keyword and prev_keyword in week_days:
                selected_statement.text = response_for_day_and_location(prev_keyword, selected_location,
                                                                             response_list, is_today, is_tomorrow)
                selected_statement.confidence = 1
            else:
                # print("location only, prompt user")
                selected_statement.text = "On which day would you like to know the weather for " + selected_location.title() + "?"
                selected_statement.confidence = 1
                bot.previous_keyword = selected_location

        # If neither the day nor the location were supplied, prompt the user for a day and a location
        else:
            # print("neither day nor location")
            selected_statement.text = "Please provide me with a day and a location!"
            selected_statement.confidence = 1

        return selected_statement
