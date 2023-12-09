from flask import Flask, render_template, request
import json
from datetime import datetime, timedelta

import env
from requestHelper import GetRequests
from helpers import GetItinerary

from database import db_session, init_db, delete
from models import Weather, BotResponse, ChatHistory

from bot import ask_question, train_bot, generate_bot_weather_responses

API_KEY = env.API_KEY
URL_BASE = 'https://api.openweathermap.org/data/3.0/onecall?'

# Model used to update index.html
chat_history = ChatHistory()

# Connect to DB
init_db()

# Check first DB entry to see if it matches today's date,
# If it doesn't, the application will retrieve new data from Openweather API
if Weather.query.first():
    is_today = Weather.query.first()
else:
    is_today = False

print(datetime.today().date().strftime("%d-%m-%Y"))

# If dates match, retrieve weather data from SQL DB and use to generate specific bot responses
if is_today and datetime.today().date().strftime("%d-%m-%Y") == is_today.date:
    try:
        print("DB first entry date matches today's date")
        print("is_today.date " + is_today.date)
        weather_data = []
        rows = Weather.query.all()
        for entry in rows:
            weather_data.append(BotResponse(entry.day, entry.date, entry.location, entry.min, entry.max, entry.summary))
        train_bot()
        generate_bot_weather_responses(weather_data)
    except:
        print("There was a problem retrieving weather data from SQL database")


# If dates don't match, delete old SQL DB entries, retrieve new ones from API and store in DB
else:
    weather_data = []
    itinerary = GetItinerary()
    try:
        print("DB date doesn't match today or doesn't exist")
        db_session.execute(delete(Weather))
        db_session.commit()
    except:
        print("There was a problem removing old data from SQL database")
    try:
        get_request = GetRequests()
        for place in itinerary:
            url_string = URL_BASE + "lat=" + place.latitude + "&lon=" + place.longitude + "&exclude=current,minutely,hourly,alerts&appid=" + API_KEY
            print(url_string)
            weather_data.append(json.loads(get_request.make_request(url_string).text))
    except:
        print("There was a problem connecting to the API")
    try:
        rows = []
        for r in range(0, 10):
            for i in range(0, 7):
                today = datetime.today()
                current_day = today + timedelta(days=i)
                new_row = Weather(
                    day=current_day.date().strftime("%A"),
                    date=current_day.date().strftime("%d-%m-%Y"),
                    location=itinerary[r].name,
                    min=round(weather_data[r]['daily'][i]['temp']['min'] - 273.15, ndigits=None),
                    max=round(weather_data[r]['daily'][i]['temp']['max'] - 273.15, ndigits=None),
                    summary=weather_data[r]['daily'][i]['summary']
                )
                rows.append(new_row)
        db_session.add_all(rows)
        db_session.commit()
    except:
        print("There was a problem updating the database")
        # Use DB data to generate bot responses
    try:
        weather_data = []
        rows = Weather.query.all()
        for entry in rows:
            weather_data.append(BotResponse(entry.day, entry.date, entry.location, entry.min, entry.max, entry.summary))
        train_bot()
        generate_bot_weather_responses(weather_data)
    except:
        print("There was a problem connecting to the SQL database")

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    # Pass user input to bot, retrieve response and update chat history model
    if request.method == "POST":
        try:
            bot_response = ask_question(request.form["bot_input"])
            chat_history.update_chat(request.form["bot_input"], str(bot_response))
        except:
            print("There was a problem getting a bot response")
        finally:
            return render_template("index.html",
                                   pos_1=chat_history.pos_1,
                                   pos_2=chat_history.pos_2,
                                   pos_3=chat_history.pos_3,
                                   pos_4=chat_history.pos_4,
                                   pos_5=chat_history.pos_5,
                                   pos_6=chat_history.pos_6,
                                   pos_7=chat_history.pos_7,
                                   pos_8=chat_history.pos_8,
                                   pos_9=chat_history.pos_9
                                   )
    else:
        return render_template("index.html",
                               pos_1=chat_history.pos_1,
                               pos_2=chat_history.pos_2,
                               pos_3=chat_history.pos_3,
                               pos_4=chat_history.pos_4,
                               pos_5=chat_history.pos_5,
                               pos_6=chat_history.pos_6,
                               pos_7=chat_history.pos_7,
                               pos_8=chat_history.pos_8,
                               pos_9=chat_history.pos_9
                               )


if __name__ == "__main__":
    app.run()
