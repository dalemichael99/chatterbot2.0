from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests

OPENWEATHERMAP_API_KEY = "796f007a9f74ec0567a8f036a26e642b"

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        return f"The weather in {city} is {main_weather} ({description}) with a temperature of {temperature}°C."
    else:
        return f"Unable to retrieve weather information for {city}."

def initialize_chatbot():
    chatbot = ChatBot("WeatherBot")
    trainer = ChatterBotCorpusTrainer(chatbot)

    trainer.train("chatterbot.corpus.english")

    return chatbot

def chatbot():
    print("Hello! I'm a weather chatbot. Ask me about the weather in a city or just chat with me.")
    weather_bot = initialize_chatbot()

    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            if 'weather in' in user_input.lower():
                city = user_input.split('weather in ')[-1]
                response = get_weather(city)
            else:
                response = weather_bot.get_response(user_input)

            print(response)

        except (KeyboardInterrupt, EOFError):
            print("Goodbye!")
            break

if __name__ == "__main__":
    chatbot()