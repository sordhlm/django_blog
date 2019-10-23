#coding=utf8
from werobot import WeRoBot

robot = WeRoBot(enable_session=False,
                token='yourtoken',
                APP_ID='yourappid',
                APP_SECRET='yourappsecret')

@robot.handler
def hello(message):
    return 'Hello world'
