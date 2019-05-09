#! python3
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import datetime

from maclookup import ApiClient
import logging

import pymongo
from pymongo import MongoClient

mac_client = ApiClient('APIKEY')

bot = telepot.Bot('APIKEY')

answerer = telepot.helper.Answerer(bot)

connection_params = {
    'user': '<USERNAME>',
    'password': '<PASSWORD>',
    'host': 'example.mlab.com',
    'port': 54321,
    'namespace': 'metadata',
}

connection = MongoClient(
    'mongodb://{user}:{password}@{host}:'
    '{port}/{namespace}'.format(**connection_params)
)

db = connection.metadata

userMsg = db.messages
errors = db.errors
botResponse = db.response

def handle(msg):
    try:
        person_id = msg.get('chat').get('id')
        text = msg.get('text')
        bot.sendChatAction(person_id, "typing")
        log(msg)
        userMsg.insert_one(msg)
        if text.startswith('/mac'):
            address = text.strip().split(' ')[-1].strip()
            info = mac_client.get_raw_data(address, 'json')
            bot.sendMessage(
                person_id, info)
        else:            
            result = "Please Choose one of the commands"
            bot.sendMessage(person_id, result)
            botResponse.insert_one({"person_id:": person_id, "result": result});
    except Exception as e:
        bot.sendMessage(
            person_id, "Something went wrong, please try again later")
        errors.insert_one({'error':str(e), "line": 84})
        log("Handle: Error: "+str(e))


def get_results(response):
    pass

def format_results(result):
    pass


def log(msg):
    with open('log_results.txt', 'a') as logfile:
        now = datetime.datetime.now()
        logfile.write(now.isoformat()+"\t"+str(msg)+"\n\n")


def main():
    MessageLoop(bot, {'chat': handle}).run_as_thread()

    print('Listening ...')
    log("******************************Server Started at"+datetime.datetime.now().isoformat()+"***************************")

    # Keep the program running.
    while 1:
        time.sleep(10)

if __name__ == '__main__':
    main()
