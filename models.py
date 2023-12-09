from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime, timedelta


# Class used for DB model
class Weather(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    day = Column(String(10))
    date = Column(String(50))
    location = Column(String(50))
    min = Column(Integer)
    max = Column(Integer)
    summary = Column(String(100))

    def __init__(self, day=None, date=None, location=None, min=None, max=None, summary=None):
        self.day = day
        self.date = date
        self.location = location
        self.min = min
        self.max = max
        self.summary = summary

    def __repr__(self):
        return '<User %r>' % (self.location)


# Class used for bot responses
class BotResponse:
    def __init__(self, day, date, location, min_temp, max_temp, summary):
        self.day = day
        self.date = date
        self.location = location
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.summary = summary

    def get_response(self):
        day_response = []
        if self.day == datetime.today().strftime("%A"):
            print("get_response - day is the same as today")
            day_response = "Today, " + self.day
        else:
            print("get_response - day is not the same as today")
            day_response = "On " + self.day
        return day_response + " " + self.date + " at " + self.location + ": " + self.summary + ". The minimum temperature will be " + str(
            self.min_temp) + "°C and the max will be " + str(self.max_temp) + "°C."


# Class used for chat history
class ChatHistory:
    def __init__(self, default="WB: Hello, can I interest you in some weather?"):
        self.pos_1 = default
        self.pos_2 = ""
        self.pos_3 = ""
        self.pos_4 = ""
        self.pos_5 = ""
        self.pos_6 = ""
        self.pos_7 = ""
        self.pos_8 = ""
        self.pos_9 = ""

    # Function used to move position of each user input and bot response within the model
    def update_chat(self, user_input, bot_response):
        self.pos_9 = self.pos_7
        self.pos_8 = self.pos_6
        self.pos_7 = self.pos_5
        self.pos_6 = self.pos_4
        self.pos_5 = self.pos_3
        self.pos_4 = self.pos_2
        self.pos_3 = self.pos_1
        self.pos_2 = "You: " + user_input
        self.pos_1 = "WB: " + bot_response
