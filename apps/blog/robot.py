#coding=utf8
import time
import re
from werobot import WeRoBot
from apps.blog.venaAI import venaAI
from apps.tensorflow_poems.gen_good_poems import PoemPool
from apps.blog.models import User, Poem

robot = WeRoBot(enable_session=False,
                token='',
                APP_ID='',
                APP_SECRET='')
poem = PoemPool()
vena = venaAI()

@robot.subscribe
def subscribe(message):
    User.objects.create(source=message.source)
    return '欢迎关注本公众号！'

@robot.text
def text_handle(message):
    cont = message.content.lower()
    source = message.source
    user = User.objects.get_or_create(source=source)[0]
    mode = user.mode
    print(cont+" end")
    print("mode: %d"%mode)
    print(re.match(r'leave', cont))
    if re.match(r'leave', cont):
        print("leaving the room")
        ret = User.room_choose(user, 1)
        return ret
    if mode == 0: #guest is at front door
        ret = User.room_choose(user, 1)
    elif mode == 1: # guest is choosing which room
        if cont == "1":
            ret = User.enter_chat(user ,2)
        elif cont == "0":
            ret = User.enter_poem(user ,3)
        else:
            ret = "Not supported room!\n"
            ret += User.room_choose(user, 1)
    elif mode == 2:
        print("input: %s"%cont)
        print(message.source)
        ret = vena.aiml_talk(message.content)
    elif mode == 3:
        if cont == "0":
            ret = User.cfg_poem_type(user, '5jue', 4)
        elif cont == "1":
            ret = User.cfg_poem_type(user, '7jue', 4)
        elif cont == "2":
            poem.add(user.source, user.pinit, user.ptype, user.thrd)
            ret = poem.gen(user.source)
            ret = User.start_poem(user, 5)
        else:
            ret = "not supported poem type!\n"
            ret += User.enter_poem(user ,3)
        return ret
    elif mode == 4:
        user.pinit = cont
        User.start_poem(user, 5)
        ret = "poem init text is: %s"%cont
        poem.add(user.source, user.pinit, user.ptype, user.thrd)
        ret = poem.gen(user.source)
    elif mode == 5:
        ret = poem.get_result(user.source)
        if ret:
            ret = ret[0]
            User.enter_poem(user ,3)
        else:
            ret = "poems is on-generating, please wait..."

        return ret
        #[user, cmd] = cont.split()
        #if 'poems go' in cont:
        #    poem.add(user, '月', '5jue', 12)
        #    res = poem.gen(source)
        #    print(res)
        #elif 'poems query' in cont:
        #    ret = poem.get_result(source)
        #    if ret:
        #        res = ret[0]
        #    else:
        #        res = "poems is on-generating"
        #    print(res)

    return ret
