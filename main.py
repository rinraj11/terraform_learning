import telegram.ext
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

lines = []
f = open("information.txt", "r")
for line in f:
    lines.append(line)
    
TOKEN = lines[0]
weatherAPI = lines[1]
owm = OWM(weatherAPI)
mgr = owm.weather_manager()

updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

#global variables 
nameVar = ""
locationVar = ""

def start(update, context):
    update.message.reply_text("Hi there! Welcome to WeatherBot!\nStart off by saying '\help'. You can use this command whenever!")

def help(update, context):
    update.message.reply_text("WeatherBot is created to make checking the weather much easier!\n\n\nHere are the commands you can use...\n\n\n /help \t --> \tGet a list of all of the commands you can use\n\n /name \t --> \tSet your name (use the command like this '/name John'\n\n /location \t --> \tSet where you want weather information for (use the command like this '/location Philadelphia'")

def name(update, context):
    nameVar = context.args[0]
    update.message.reply_text(f"Nice to meet you, {nameVar}!")

def location(update, context):
    global locationVar
    locationVar = context.args[0]
    update.message.reply_text(f"Got it! I'll send weather data for {locationVar}")

def weather(update, context):
    observation = mgr.weather_at_place(locationVar).weather
    tempArr = observation.temperature('fahrenheit')
    update.message.reply_text(f"It is currently showing {observation.detailed_status} at {locationVar}\n with a low of {tempArr['temp_min']}F and a high of {tempArr['temp_max']}F")




dispatcher.add_handler(telegram.ext.CommandHandler("start", start))
dispatcher.add_handler(telegram.ext.CommandHandler("help", help))
dispatcher.add_handler(telegram.ext.CommandHandler("name", name))
dispatcher.add_handler(telegram.ext.CommandHandler("location", location))
dispatcher.add_handler(telegram.ext.CommandHandler("weather", weather))

updater.start_polling()
updater.idle()
