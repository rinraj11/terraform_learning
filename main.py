import telegram.ext
import requests
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import random

# reading in API information
lines = []
f = open("information.txt", "r")
for line in f:
    lines.append(line.strip())

#setting API into vars
TOKEN = lines[0]
weatherAPI = lines[1]

#Connecting to OWM Wrapper
owm = OWM(weatherAPI)
mgr = owm.weather_manager()
updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

#global variables 
nameVar = ""
locationVar = ""

cold=["It's cold today. Bring a jacket and maybe a hat too.", "It's cold, make sure you're wearing a coat or something."]

hot=["It's hot today, wear some sunscreen or something", "Wear shorts, it's blazing outside"]

windy = ["It's breezy, bring a windbreaker"]

elseCase = ["eh I got nothing, wear whatever you want. America, Freedom, etc."]

def start(update, context):
    update.message.reply_text("Hi there! Welcome to WeatherBot!\nStart off by saying '\help'. You can use this command whenever!")

def help(update, context):
    update.message.reply_text("WeatherBot is created to make checking the weather much easier!\n\n\nHere are the commands you can use...\n\n\n /help \t --> \tGet a list of all of the commands you can use\n\n /name \t --> \tSet your name (use the command like this '/name John'\n\n /location \t --> \tSet where you want weather information for (use the command like this '/location Philadelphia'\n\n /weather \t --> \tGet the current weather information for whichever location you set")

def name(update, context):
    global nameVar
    nameVar = context.args[0]
    update.message.reply_text(f"Nice to meet you, {nameVar}!")

def location(update, context):
    global locationVar
    locationVar = context.args[0]
    update.message.reply_text(f"Got it! I'll send weather data for {locationVar}")

def weather(update, context):

    response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=40.4406&lon=-79.9959&appid=23f7b63fd1c1d1a3b0dc5b97fc5c66af&units=imperial")

    response = response.json()
    
    minTemp = response["main"]["temp_min"]
    maxTemp = response["main"]["temp_max"]
    feelsLike = response["main"]["feels_like"]
    currentTemp = response["main"]["temp"]

    windSpeed = response["wind"]["speed"]
    windDeg = response["wind"]["deg"]

    description = response["weather"][0]["description"]

    extraMessage = ""

    if(minTemp < 32):
        extraMessage += random.randrange(0,len(cold))
        if(windSpeed > 7):
            extraMessage+= "Also, "
            extraMessage += windy[random.randrange(0,len(windy))]
    elif(maxTemp > 75):
        extraMessage += hot[random.randrange(0,len(hot))]
    elif(windSpeed > 7):
        extraMessage += cold[random.randrange(0,len(windy))]
    else:
        extraMessage += elseCase[random.randrange(0,len(elseCase))]
    

    update.message.reply_text(f"The weather overall is showing: {description} for good old {locationVar}. \n\nCurrently, it is {currentTemp}F with a 'Feels-Like' of {feelsLike}. Today's high is {maxTemp} and a low of {minTemp}.")

    update.message.reply_text(f"There is some wind moving towards {windDeg} deg at a speed of {windSpeed}MPH.")

    update.message.reply_text(f"Now, it's time for some bot generated responses...{extraMessage}")

#handling commands and redirecting to respective functions
dispatcher.add_handler(telegram.ext.CommandHandler("start", start))
dispatcher.add_handler(telegram.ext.CommandHandler("help", help))
dispatcher.add_handler(telegram.ext.CommandHandler("name", name))
dispatcher.add_handler(telegram.ext.CommandHandler("location", location))
dispatcher.add_handler(telegram.ext.CommandHandler("weather", weather))

updater.start_polling()
updater.idle()
