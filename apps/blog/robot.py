#coding=utf8
import time
from werobot import WeRoBot
from apps.blog.venaAI import venaAI
from apps.tensorflow_poems.gen_good_poems import PoemPool

robot = WeRoBot(enable_session=False,
                token='ilovemuyao',
                APP_ID='wx1bad78267ac404dc',
                APP_SECRET='R8Ed9SIyq7PB3bgATJ5a7ka36o9o2re02KNl3jNHrOx')

poem = PoemPool()

@robot.text
def text_handle(message):
    vena = venaAI()
    cont = message.content
    print("input: %s"%cont)
    print(message.source)
    #[user, cmd] = cont.split()
    user = message.source
    if 'poems go' in cont:
        res = poem.add_generator(user, '月', '5jue', 12)
        print(res)
    elif 'poems query' in cont:
        ret = poem.get_result(user)
        if ret:
            res = ret[0]
        else:
            res = "poems is on-generating"
        print(res)
    else:
        res = vena.aiml_talk(message.content)

    return res
