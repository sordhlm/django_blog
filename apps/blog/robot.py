#coding=utf8
from werobot import WeRoBot
from venaAI import venaAI

robot = WeRoBot(enable_session=False,
                token='ilovemuyao',
                APP_ID='wx1bad78267ac404dc',
                APP_SECRET='R8Ed9SIyq7PB3bgATJ5a7ka36o9o2re02KNl3jNHrOx')

@robot.text
def text_handle(message):
    vena = venaAI()
    return vena.aiml_talk(message)
