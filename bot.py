#! python3
import sys
import time
import datetime
import json

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent



from maclookup import ApiClient

import pymongo
from pymongo import MongoClient

import analyser

mac_client = ApiClient('APIKEY')

bot = telepot.Bot('APIKEY')

connection_params = {
    'user': '<USERNAME',
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
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        person_id = msg.get('chat').get('id')
        text = msg.get('text')
        bot.sendChatAction(person_id, "typing")
        log(msg)
        userMsg.insert_one(msg)
        if text and text.startswith('/mac'):
            address = text.strip().split(' ')[-1].strip()
            info = mac_client.get_raw_data(address, 'json')
            print (type(info))
            info = format_results(info)
            bot.sendMessage(
                person_id, "`"+info+"`", parse_mode='markdown')
        elif content_type == 'document':
            file_id = msg['document']['file_id']
            file_name = msg['document']['file_name']
            bot.download_file(file_id, file_name)
            info = analyser.get_generic_file_info('./'+file_name)
            info = format_results(info)
            bot.sendMessage(
                person_id, "`"+str(info)+"`", parse_mode='markdown')
        elif content_type == 'photo':
            file_id = msg['photo'][-1]['file_id']
            file_name = msg['photo'][-1]['file_id']
            bot.download_file(file_id, file_name)
            info = analyser.get_generic_file_info('./'+file_name)
            info = format_results(info)
            bot.sendMessage(
                person_id, "`"+info+"`", parse_mode='markdown')
        else:            
            info = "Please Choose one of the commands"
            bot.sendMessage(person_id, info)
            botResponse.insert_one(
                {"person_id:": person_id, "info": str(info)})
    except Exception as e:
        bot.sendMessage(
            person_id, "Something went wrong, please try again later")
        errors.insert_one({'error': str(e), "line": 84})
        log("Handle: Error: "+str(e))
        raise e


def get_results(response):
    pass

def format_results(result):
    # Casting to JSON 
    if(type(result) == dict):
        str_json = json.dumps(result)
        decoded_json = json.loads(str_json)
    elif (type(result) == bytes ):
        decoded_json = json.loads(result.decode('utf8').replace("'", '"'))

    # Pretty Print the JSON
    ret = json.dumps(decoded_json, indent=2, sort_keys=True)
    return ret


def log(msg):
    with open('log_results.txt', 'a') as logfile:
        now = datetime.datetime.now()
        logfile.write(now.isoformat()+"\t"+str(msg)+"\n\n")


def main():
    MessageLoop(bot, {'chat': handle}).run_as_thread()

    print('Listening ...')
    log("******************************Server Started at" +
        datetime.datetime.now().isoformat()+"***************************")

    # Keep the program running.
    while 1:
        time.sleep(10)


if __name__ == '__main__':
    main()
