from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# This list is used in custom WeatherLogicAdapter to provide specific answers
bot_weather_responses = []
previous_keyword = ""

# Create instance of ChatBot, select logic adapters,
# read_only attribute prevents bot from learning from chat history, set to false if training
weather_bot = ChatBot(
    name="WeatherBot",
    read_only=True,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
        },
        {
            "import_path": "weather_logic_adapter.WeatherLogicAdapter"
        }
    ],

)

# Provide very basic relevant conversational details
weather_talk = [
    "Hello",
    "Hi, ask me about the weather!",
    "What is the weather going to be like?"
    "Please provide me with a day and a location"
]

list_trainer = ListTrainer(weather_bot)


# Get user input and retrieve response
def ask_question(user_input):
    bot_response = weather_bot.get_response(user_input)
    return bot_response


# Used to return response list outside of this file
def get_response_list():
    return bot_weather_responses


# Generate location and day specific responses from weather data
def generate_bot_weather_responses(weather_data):
    for item in weather_data:
        date = item.date
        day = item.day
        loc = item.location
        min_temp = str(item.min_temp)
        max_temp = str(item.max_temp)
        summary = item.summary
        bot_weather_responses.append(
            "In " + loc + " on " + day + " " + date + ", the minimum temp will be " + min_temp + " and the max " + max_temp + "°C. " + summary)


# Train bot using provided data and corpus data. Any other training data can easily be added here
def train_bot():
    list_trainer.train(weather_talk)

    corpus_trainer = ChatterBotCorpusTrainer(weather_bot)
    corpus_trainer.train('chatterbot.corpus.english')
