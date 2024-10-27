import onetouch as ot


api = ''
history = []

agent = ot.chat_glm("你可以干什么", api, stream=True, history=history)

for content in agent:
    ot.prints(content, style="color:red;", end='')
print('\n')

agent = ot.chat_glm("我刚才说了什么", api, stream=True, history=history)

for content in agent:
    ot.prints(content, style="color:red;", end='')
print('\n')
