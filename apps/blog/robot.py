#coding=utf8
import time
from werobot import WeRoBot
from apps.blog.venaAI import venaAI
from apps.tensorflow_poems.gen_good_poems import PoemPool
from apps.blog.models import User, Poem

robot = WeRoBot(enable_session=False,
                token='ilovemuyao',
                APP_ID='wx1bad78267ac404dc',
                APP_SECRET='fb8162c70f72ddb2c1ceeff0d35e3567')
#client = robot.client
#client.create_menu({
#    "button":[
#        {
#            "type": "click",
#            "name": u"茶室外话",
#            "key" : "click_chat"
#        },
#        {
#            "name": '草庐弄诗',
#            "sub_button":[
#                {
#                    "type": "click",
#                    "name": "类型",
#                    "key" : "poem_ptype"
#                },
#                {
#                    "type": "click",
#                    "name": "初始",
#                    "key" : "poem_init"
#                },
#                {
#                    "type": "click",
#                    "name": "成诗",
#                    "key" : "poem_create"
#                },
#                {
#                    "type": "click",
#                    "name": "问",
#                    "key" : "poem_query"
#                },
#
#            ]
#        }]
#})
#poem = PoemPool()
#vena = venaAI()
#
#@robot.subscribe
#def subscribe(message):
#    User.objects.create(source=message.source)
#    return '欢迎关注本公众号！'
#
#@robot.key_click("poem_ptype")
#def poem_init(message):
#    user = User.objects.get(source=message.source)
#    user.mode = 2
#    user.save()
#    ret = '请回复数字选择诗的类型: 0) 五绝  1）七绝'
#    return ret
#
#@robot.key_click("poem_init")
#def poem_init(message):
#    user = User.objects.get(source=message.source)
#    user.mode = 3
#    user.save()
#    ret = '请输入你的底稿'
#    return ret
#
#@robot.key_click("poem_create")
#def poem_create(message):
#    user = User.objects.get(source=message.source)
#    poem.add(user.source, user.pinit, user.ptype, user.thrd)
#    ret = poem.gen(message.content)
#    return ret
#
#@robot.key_click("poem_query")
#def poem_query(message):
#    ret = poem.get_result(message.source)
#    if ret:
#        res = ret[0]
#    else:
#        res = "poems is on-generating"
#    return ret
#
#@robot.key_click("click_chat")
#def click_chat(message):
#    user = User.objects.get(source=message.source)
#    user.mode = 1
#    user.save()
#    return "let's chat"

@robot.text
def text_handle(message):
    cont = message.content
    source = message.source
    user = User.objects.get(source=source)
    mode = user.mode
    if cont == 'leave':
        ret = User.room_choose(user, 1)
    if mode == 0: #guest is at front door
        ret = User.room_choose(user, 1)
    elif mode == 1: # guest is choosing which room
        if cont == "0":
            ret = User.enter_char(user ,2)
        elif cont == "1":
            ret = User.enter_poem(user ,3)
        else:
            ret = r"Not supported room!\n"
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
            ret = poem.gen(message.content)
        else:
            ret = "not supported poem type!"
            ret += User.enter_poem(user ,3)
        return ret
    elif mode == 4:
        user.mode = 5
        user.pinit = cont
        user.save()
        ret = "poem init text is: %s"%cont
        poem.add(user.source, user.pinit, user.ptype, user.thrd)
        ret = poem.gen(user.content)
    elif mode == 5:
        ret = poem.get_result(user.source)
        if ret:
            ret = ret[0]
            ret += r'\n' + User.enter_poem(user ,3)
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
