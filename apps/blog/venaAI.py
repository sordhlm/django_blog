#coding=utf8
import aiml
import os
import re
#import pyttsx3

class venaAI(object):
    def __init__(self):
        cwd = os.getcwd()
        self.aiml_path = cwd+'/apps/blog/lib/Py3kAiml/'
        self._load_brain()
    def _load_aiml(self):
        self.vena = aiml.Kernel()
        xml_file = self.aiml_path + 'std-startup.xml'
        os.chdir(self.aiml_path)
        self.vena.learn(xml_file)
        self.vena.respond('LOAD AIML B')
        os.chdir(cwd)
    def _load_brain(self):
        self.vena = aiml.Kernel()
        xml_file = self.aiml_path + 'std-startup.xml'
        brn_file = self.aiml_path + 'brain.brn'
        #os.chdir(self.aiml_path)
        if os.path.isfile(brn_file):
            self.vena.bootstrap(brainFile = brn_file)
        else:
            self.vena.bootstrap(learnFiles = xml_file, commands = "LOAD AIML B")
            self.vena.saveBrain(brn_file)
    def aiml_talk(self,cmd):
        res = self.vena.respond(cmd)
        return res

if __name__ == "__main__":
    #api = hassAPI()
    vena = venaAI()
    while True:
        cmd = input('Enter your cmd:')
        print(vena.aiml_talk(cmd))
    #bot = Bot(console_qr=True, cache_path=True)
    #while True:
    #    my_friend = bot.friends().search('幸运的大娜')[0]
    #    @bot.register()
    #    def just_print(msg):
    #        print(msg)
    #        if 'turn on' in msg.text:
    #            print ('get turn on light cmd')
    #            api.turnOn('light.Living_Room')
    #        elif 'turn off' in msg.text:
    #            print ('get turn off light cmd')
    #            api.turnOff('light.Living_Room')
    #        elif 'shutdown' in msg.text:
    #            print('get shutdown cmd')
    #            exit(1)
    #engine = pyttsx3.init()
    #voices = engine.getProperty('name')
    #for voice in voices:
    #    print(voice.id)
    #    engine.setProperty('name', voice.id)
    #    engine.say('how are you')
    #    engine.runAndWait()
    #    time.sleep(1)

